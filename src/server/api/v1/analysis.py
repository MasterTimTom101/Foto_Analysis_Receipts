"""
AI Analysis API endpoints
"""

from flask import request
from flask_restx import Namespace, Resource, fields
from datetime import datetime
import os
import pandas as pd

from ..models.analysis import analysis_models
from ..models.responses import response_models
from ...core.config import DevelopmentConfig
from ...services.receipt_analyzer import ReceiptAnalyzer

# Create API namespace
api = Namespace('analyze', description='AI analysis operations')

# Define models directly with the namespace
analysis_request_model = api.model('AnalysisRequest', {
    'calendar_week': fields.String(required=True, description='Calendar week to analyze (e.g., 2025CW_30)', example='2025CW_30'),
    'force_reanalysis': fields.Boolean(default=False, description='Force re-analysis even if results exist')
})

receipt_analysis_model = api.model('ReceiptAnalysis', {
    'datum': fields.String(description='Date from receipt'),
    'uhrzeit': fields.String(description='Time from receipt'),
    'summe_food': fields.Float(description='Food costs in euros'),
    'summe_nonfood': fields.Float(description='Non-food costs in euros'),
    'foto_datei': fields.String(description='Source image filename')
})

analysis_result_model = api.model('AnalysisResult', {
    'calendar_week': fields.String(required=True, description='Calendar week analyzed'),
    'total_food': fields.Float(description='Total food costs in euros'),
    'total_nonfood': fields.Float(description='Total non-food costs in euros'),
    'total_receipts': fields.Integer(description='Number of receipts processed'),
    'receipts': fields.List(fields.Nested(receipt_analysis_model), description='Individual receipt results'),
    'analysis_date': fields.DateTime(description='When the analysis was performed'),
    'status': fields.String(enum=['pending', 'processing', 'completed', 'failed'], description='Analysis status')
})

analysis_summary_model = api.model('AnalysisSummary', {
    'calendar_week': fields.String(required=True, description='Calendar week'),
    'total_food': fields.Float(description='Total food costs in euros'),
    'total_nonfood': fields.Float(description='Total non-food costs in euros'),
    'total_receipts': fields.Integer(description='Number of receipts processed'),
    'grand_total': fields.Float(description='Total costs (food + non-food)'),
    'analysis_date': fields.DateTime(description='When the analysis was performed')
})

calendar_week_model = api.model('CalendarWeek', {
    'week': fields.String(required=True, description='Calendar week identifier'),
    'year': fields.Integer(description='Year'),
    'week_number': fields.Integer(description='Week number'),
    'file_count': fields.Integer(description='Number of receipt files'),
    'analysis_status': fields.String(enum=['not_analyzed', 'analyzed', 'failed'], description='Analysis status'),
    'last_analysis': fields.DateTime(description='Last analysis date')
})

calendar_weeks_model = api.model('CalendarWeeksList', {
    'weeks': fields.List(fields.Nested(calendar_week_model)),
    'total': fields.Integer(description='Total number of weeks available')
})

# Initialize analyzer
config = DevelopmentConfig()
analyzer = ReceiptAnalyzer(config)

@api.route('/')
class AnalysisTrigger(Resource):
    @api.doc('trigger_analysis')
    @api.expect(analysis_request_model)
    @api.marshal_with(analysis_result_model, code=202)
    def post(self):
        """Trigger AI analysis for a calendar week"""
        data = request.json
        calendar_week = data.get('calendar_week')
        
        if not calendar_week:
            api.abort(400, 'calendar_week is required')
        
        # Validate calendar week format
        if not calendar_week.startswith('2025CW_'):
            api.abort(400, 'calendar_week must be in format 2025CW_XX')
        
        try:
            # Check if photos directory exists
            photos_dir = config.PHOTOS_DIR / calendar_week
            if not photos_dir.exists():
                api.abort(404, f'No photos found for calendar week {calendar_week}')
            
            # Count available photos
            photo_files = [f for f in photos_dir.iterdir() 
                          if f.is_file() and f.suffix.lower() in config.SUPPORTED_IMAGE_EXTENSIONS]
            
            if not photo_files:
                api.abort(404, f'No supported image files found in {calendar_week}')
            
            # Perform analysis
            df_result = analyzer.analyze_calendar_week(calendar_week)
            
            if df_result is None:
                return {
                    'calendar_week': calendar_week,
                    'status': 'failed',
                    'total_food': 0.0,
                    'total_nonfood': 0.0,
                    'total_receipts': 0,
                    'receipts': [],
                    'analysis_date': datetime.utcnow().isoformat()
                }, 202
            
            # Get summary
            summary = analyzer.get_week_summary(df_result)
            
            # Convert DataFrame to list of dictionaries for API response
            receipts_data = []
            for _, row in df_result.iterrows():
                receipts_data.append({
                    'datum': str(row.get('Datum', '')),
                    'uhrzeit': str(row.get('Uhrzeit', '')),
                    'summe_food': float(row.get('Summe_Food', 0.0)),
                    'summe_nonfood': float(row.get('Summe_NonFood', 0.0)),
                    'foto_datei': str(row.get('Foto_Datei', ''))
                })
            
            return {
                'calendar_week': calendar_week,
                'status': 'completed',
                'total_food': summary['total_food'],
                'total_nonfood': summary['total_nonfood'],
                'total_receipts': summary['total_receipts'],
                'receipts': receipts_data,
                'analysis_date': datetime.utcnow().isoformat()
            }, 202
            
        except Exception as e:
            api.abort(500, f'Analysis failed: {str(e)}')

@api.route('/<string:calendar_week>')
@api.param('calendar_week', 'Calendar week identifier (e.g., 2025CW_30)')  
class AnalysisResult(Resource):
    @api.doc('get_analysis_result')
    @api.marshal_with(analysis_result_model)
    def get(self, calendar_week):
        """Get analysis results for a calendar week"""
        try:
            # Check if CSV file exists
            csv_file = config.COST_FILES_DIR / f"{calendar_week}_costs.csv"
            
            if not csv_file.exists():
                api.abort(404, f'No analysis results found for {calendar_week}. Run analysis first.')
            
            # Read existing results
            df_result = pd.read_csv(csv_file, sep=";")
            df_result = analyzer._process_results(df_result)
            
            # Get summary
            summary = analyzer.get_week_summary(df_result)
            
            # Convert to API format
            receipts_data = []
            for _, row in df_result.iterrows():
                receipts_data.append({
                    'datum': str(row.get('Datum', '')),
                    'uhrzeit': str(row.get('Uhrzeit', '')),
                    'summe_food': float(row.get('Summe_Food', 0.0)),
                    'summe_nonfood': float(row.get('Summe_NonFood', 0.0)),
                    'foto_datei': str(row.get('Foto_Datei', ''))
                })
            
            # Get file modification time as analysis date
            analysis_date = datetime.fromtimestamp(csv_file.stat().st_mtime).isoformat()
            
            return {
                'calendar_week': calendar_week,
                'status': 'completed',
                'total_food': summary['total_food'],
                'total_nonfood': summary['total_nonfood'],
                'total_receipts': summary['total_receipts'],
                'receipts': receipts_data,
                'analysis_date': analysis_date
            }
            
        except Exception as e:
            api.abort(500, f'Failed to retrieve analysis results: {str(e)}')

@api.route('/<string:calendar_week>/summary')
@api.param('calendar_week', 'Calendar week identifier (e.g., 2025CW_30)')
class AnalysisSummary(Resource):
    @api.doc('get_analysis_summary')
    @api.marshal_with(analysis_summary_model)
    def get(self, calendar_week):
        """Get analysis summary for a calendar week"""
        try:
            # Check if CSV file exists
            csv_file = config.COST_FILES_DIR / f"{calendar_week}_costs.csv"
            
            if not csv_file.exists():
                api.abort(404, f'No analysis results found for {calendar_week}. Run analysis first.')
            
            # Read existing results
            df_result = pd.read_csv(csv_file, sep=";")
            df_result = analyzer._process_results(df_result)
            
            # Get summary
            summary = analyzer.get_week_summary(df_result)
            
            # Get file modification time as analysis date
            analysis_date = datetime.fromtimestamp(csv_file.stat().st_mtime).isoformat()
            
            return {
                'calendar_week': calendar_week,
                'total_food': summary['total_food'],
                'total_nonfood': summary['total_nonfood'],
                'total_receipts': summary['total_receipts'],
                'grand_total': summary['total_food'] + summary['total_nonfood'],
                'analysis_date': analysis_date
            }
            
        except Exception as e:
            api.abort(500, f'Failed to get analysis summary: {str(e)}')

@api.route('/weeks')
class AnalysisWeeks(Resource):
    @api.doc('list_analysis_weeks')
    @api.marshal_with(calendar_weeks_model)
    def get(self):
        """Get list of available calendar weeks for analysis"""
        try:
            available_weeks = analyzer.get_available_weeks()
            
            weeks_data = []
            for week in available_weeks:
                # Check if analysis exists
                csv_file = config.COST_FILES_DIR / f"{week}_costs.csv"
                analysis_status = 'analyzed' if csv_file.exists() else 'not_analyzed'
                last_analysis = None
                
                if csv_file.exists():
                    last_analysis = datetime.fromtimestamp(csv_file.stat().st_mtime).isoformat()
                
                # Count files
                photos_dir = config.PHOTOS_DIR / week
                file_count = len([f for f in photos_dir.iterdir() 
                                if f.is_file() and f.suffix.lower() in config.SUPPORTED_IMAGE_EXTENSIONS])
                
                # Parse week info
                year = int(week.split('CW_')[0])
                week_number = int(week.split('CW_')[1])
                
                weeks_data.append({
                    'week': week,
                    'year': year,
                    'week_number': week_number,
                    'file_count': file_count,
                    'analysis_status': analysis_status,
                    'last_analysis': last_analysis
                })
            
            # Sort by year and week number
            weeks_data.sort(key=lambda x: (x['year'], x['week_number']))
            
            return {
                'weeks': weeks_data,
                'total': len(weeks_data)
            }
            
        except Exception as e:
            api.abort(500, f'Failed to get available weeks: {str(e)}')