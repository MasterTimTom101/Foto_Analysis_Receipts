"""
System information and health check API endpoints
"""

from flask import Flask
from flask_restx import Namespace, Resource, fields
from datetime import datetime
import sys
import os

from .models import health_response_model, system_info_model, test_response_model
from ..config import DevelopmentConfig

# Create API namespace
api = Namespace('system', description='System information, health checks and tests')

# Register models with the namespace
api_health_response = api.model('HealthResponse', health_response_model)
api_system_info = api.model('SystemInfo', system_info_model)
api_test_response = api.model('TestResponse', test_response_model)

# Initialize config
config = DevelopmentConfig()

@api.route('/health')
class HealthCheck(Resource):
    @api.doc('health_check')
    @api.marshal_with(api_health_response)
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
    @api.marshal_with(api_system_info)
    def get(self):
        """Get system information"""
        
        try:
            from ..receipt_analyzer import ReceiptAnalyzer
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

@api.route('/test')
class SimpleTest(Resource):
    @api.doc('simple_test')
    @api.marshal_with(api_test_response)
    def get(self):
        """Simple test endpoint to verify API is working"""
        return {
            'message': 'Hello World from REST API!',
            'timestamp': datetime.utcnow().isoformat(),
            'status': 'success'
        }