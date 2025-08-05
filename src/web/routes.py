from flask import render_template, request, redirect, url_for, flash, jsonify
import os
from datetime import datetime
import pandas as pd
from ..receipt_analyzer import ReceiptAnalyzer
from ..config import DevelopmentConfig

# Initialize analyzer
config = DevelopmentConfig()
try:
    analyzer = ReceiptAnalyzer(config)
except:
    analyzer = None

def register_routes(app):
    
    @app.route('/')
    def index():
        """Redirect root to receipts home"""
        return redirect(url_for('list_info'))
    
    @app.route('/receipts/home', methods=['GET'])
    def list_info():
        """Show project information and available weeks"""
        available_weeks = []
        if analyzer:
            try:
                available_weeks = analyzer.get_available_weeks()
            except:
                pass
        return render_template('index.html', available_weeks=available_weeks)

    @app.route('/receipts/about', methods=['GET'])
    def list_about_info():
        """Show about page"""
        return render_template('about.html')

    @app.route('/receipts/show', methods=['GET'])
    def list_receipts():
        """Show analysis results for all weeks"""
        results = []
        if analyzer:
            try:
                available_weeks = analyzer.get_available_weeks()
                for week in available_weeks:
                    csv_file = config.COST_FILES_DIR / f"{week}_costs.csv"
                    if csv_file.exists():
                        df = pd.read_csv(csv_file, sep=";")
                        summary = analyzer.get_week_summary(df)
                        results.append({
                            'week': week,
                            'total_food': summary['total_food'],
                            'total_nonfood': summary['total_nonfood'],
                            'total_receipts': summary['total_receipts'],
                            'grand_total': summary['total_food'] + summary['total_nonfood']
                        })
            except Exception as e:
                flash(f'Error loading results: {e}', 'error')
        
        return render_template('show.html', results=results)

    @app.route('/receipts/upload', methods=['GET', 'POST'])
    def create_receipt_data():
        """Handle file upload (placeholder for now)"""
        if request.method == 'POST':
            # This would handle actual file uploads
            flash('File upload functionality not yet implemented', 'info')
            return redirect(url_for('list_info'))
        return render_template('upload.html')

    @app.route('/receipts/analyse', methods=['GET', 'POST'])
    def create_analysis_data():
        """Handle analysis request"""
        available_weeks = []
        if analyzer:
            try:
                available_weeks = analyzer.get_available_weeks()
            except:
                pass
                
        if request.method == 'POST':
            calendar_week = request.form.get('calendar_week')
            if not calendar_week:
                flash('Please select a calendar week', 'error')
                return render_template('analyse.html', available_weeks=available_weeks)
            
            if not analyzer:
                flash('Analysis service not available', 'error')
                return render_template('analyse.html', available_weeks=available_weeks)
            
            try:
                # Perform analysis
                df_result = analyzer.analyze_calendar_week(calendar_week)
                if df_result is not None:
                    summary = analyzer.get_week_summary(df_result)
                    flash(f'Analysis completed for {calendar_week}! Total: €{summary["total_food"] + summary["total_nonfood"]:.2f}', 'success')
                    return redirect(url_for('show_results', week=calendar_week))
                else:
                    flash('Analysis failed. Check your API key and photo files.', 'error')
            except Exception as e:
                flash(f'Analysis error: {e}', 'error')
        
        return render_template('analyse.html', available_weeks=available_weeks)

    @app.route('/receipts/result_out', methods=['GET'])
    @app.route('/receipts/result_out/<week>', methods=['GET'])
    def show_results(week=None):
        """Show detailed results for a specific week"""
        if not week:
            return redirect(url_for('list_receipts'))
        
        result_data = None
        if analyzer:
            try:
                csv_file = config.COST_FILES_DIR / f"{week}_costs.csv"
                if csv_file.exists():
                    df = pd.read_csv(csv_file, sep=";")
                    df = analyzer._process_results(df)
                    summary = analyzer.get_week_summary(df)
                    
                    # Convert DataFrame to list of dictionaries
                    receipts_data = []
                    for _, row in df.iterrows():
                        receipts_data.append({
                            'datum': str(row.get('Datum', '')),
                            'uhrzeit': str(row.get('Uhrzeit', '')),
                            'summe_food': float(row.get('Summe_Food', 0.0)),
                            'summe_nonfood': float(row.get('Summe_NonFood', 0.0)),
                            'foto_datei': str(row.get('Foto_Datei', ''))
                        })
                    
                    result_data = {
                        'week': week,
                        'summary': summary,
                        'receipts': receipts_data
                    }
                else:
                    flash(f'No results found for {week}. Run analysis first.', 'error')
            except Exception as e:
                flash(f'Error loading results: {e}', 'error')
        
        return render_template('result_output.html', result=result_data)