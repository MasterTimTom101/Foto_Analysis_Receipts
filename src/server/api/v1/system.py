"""
System information and health check API endpoints
"""

from flask import Flask
from flask_restx import Namespace, Resource, fields
from datetime import datetime
import sys
import os

from ..models.responses import response_models
from ...core.config import DevelopmentConfig

# Create API namespace
api = Namespace('system', description='System information and health checks')

# Define models directly with the namespace
health_response_model = api.model('HealthResponse', {
    'status': fields.String(enum=['healthy', 'unhealthy'], description='Service health status'),
    'timestamp': fields.DateTime(description='Health check timestamp'),
    'version': fields.String(description='API version'),
    'uptime': fields.Float(description='Service uptime in seconds'),
    'database': fields.String(enum=['connected', 'disconnected'], description='Database connection status'),
    'ai_service': fields.String(enum=['available', 'unavailable'], description='AI service availability')
})

system_info_model = api.model('SystemInfo', {
    'api_version': fields.String(description='API version'),
    'python_version': fields.String(description='Python version'),  
    'flask_version': fields.String(description='Flask version'),
    'supported_image_formats': fields.List(fields.String, description='Supported image file formats'),
    'max_file_size': fields.Integer(description='Maximum file size in bytes'),
    'ai_model': fields.String(description='AI model being used'),
    'available_weeks': fields.List(fields.String, description='Available calendar weeks')
})

# Initialize config
config = DevelopmentConfig()

@api.route('/health')
class HealthCheck(Resource):
    @api.doc('health_check')
    @api.marshal_with(health_response_model)
    def get(self):
        """Get system health status"""
        
        # Check AI service availability
        ai_status = 'available'
        try:
            if not config.GEMINI_API_KEY:
                ai_status = 'unavailable'
        except:
            ai_status = 'unavailable'
        
        # Check database status (always connected for file-based system)
        db_status = 'connected'
        
        # Overall health
        overall_status = 'healthy' if ai_status == 'available' else 'unhealthy'
        
        return {
            'status': overall_status,
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0',
            'uptime': 0.0,  # Would need to track actual uptime
            'database': db_status,
            'ai_service': ai_status
        }

@api.route('/info')
class SystemInfo(Resource):
    @api.doc('system_info')
    @api.marshal_with(system_info_model)
    def get(self):
        """Get system information"""
        
        try:
            from ...services.receipt_analyzer import ReceiptAnalyzer
            analyzer = ReceiptAnalyzer(config)
            available_weeks = analyzer.get_available_weeks()
        except:
            available_weeks = []
        
        return {
            'api_version': '1.0.0',
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            'flask_version': Flask.__version__,
            'supported_image_formats': config.SUPPORTED_IMAGE_EXTENSIONS,
            'max_file_size': config.MAX_FILE_SIZE,
            'ai_model': config.GEMINI_MODEL,
            'available_weeks': available_weeks
        }

@api.route('/config')
class SystemConfig(Resource):
    @api.doc('system_config')
    def get(self):
        """Get system configuration (non-sensitive)"""
        
        return {
            'ai_model': config.GEMINI_MODEL,
            'supported_formats': config.SUPPORTED_IMAGE_EXTENSIONS,
            'max_file_size_mb': config.MAX_FILE_SIZE // (1024 * 1024),
            'photos_directory': str(config.PHOTOS_DIR.name),
            'results_directory': str(config.COST_FILES_DIR.name),
            'debug_mode': config.DEBUG
        }