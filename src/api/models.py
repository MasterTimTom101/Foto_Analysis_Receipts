"""
API models for receipt analysis
"""

from flask_restx import fields

# Analysis request model
analysis_request_model = {
    'calendar_week': fields.String(required=True, description='Calendar week to analyze (e.g., 2025CW_30)', example='2025CW_30'),
    'force_reanalysis': fields.Boolean(default=False, description='Force re-analysis even if results exist')
}

# Individual receipt analysis result
receipt_analysis_model = {
    'datum': fields.String(description='Date from receipt'),
    'uhrzeit': fields.String(description='Time from receipt'),
    'summe_food': fields.Float(description='Food costs in euros'),
    'summe_nonfood': fields.Float(description='Non-food costs in euros'),
    'foto_datei': fields.String(description='Source image filename')
}

# Analysis result model
analysis_result_model = {
    'calendar_week': fields.String(required=True, description='Calendar week analyzed'),
    'total_food': fields.Float(description='Total food costs in euros'),
    'total_nonfood': fields.Float(description='Total non-food costs in euros'),
    'total_receipts': fields.Integer(description='Number of receipts processed'),
    'receipts': fields.List(fields.Nested(receipt_analysis_model), description='Individual receipt results'),
    'analysis_date': fields.DateTime(description='When the analysis was performed'),
    'status': fields.String(enum=['pending', 'processing', 'completed', 'failed'], description='Analysis status')
}

# Analysis summary model
analysis_summary_model = {
    'calendar_week': fields.String(required=True, description='Calendar week'),
    'total_food': fields.Float(description='Total food costs in euros'),
    'total_nonfood': fields.Float(description='Total non-food costs in euros'),
    'total_receipts': fields.Integer(description='Number of receipts processed'),
    'grand_total': fields.Float(description='Total costs (food + non-food)'),
    'analysis_date': fields.DateTime(description='When the analysis was performed')
}

# Calendar week model
calendar_week_model = {
    'week': fields.String(required=True, description='Calendar week identifier'),
    'year': fields.Integer(description='Year'),
    'week_number': fields.Integer(description='Week number'),
    'file_count': fields.Integer(description='Number of receipt files'),
    'analysis_status': fields.String(enum=['not_analyzed', 'analyzed', 'failed'], description='Analysis status'),
    'last_analysis': fields.DateTime(description='Last analysis date')
}

# Calendar weeks list model
calendar_weeks_model = {
    'weeks': fields.List(fields.Nested(calendar_week_model)),
    'total': fields.Integer(description='Total number of weeks available')
}

# Success response model
success_response_model = {
    'success': fields.Boolean(default=True, description='Indicates successful operation'),
    'message': fields.String(description='Success message'),
    'data': fields.Raw(description='Response data')
}

# Error response model  
error_response_model = {
    'success': fields.Boolean(default=False, description='Indicates failed operation'),
    'message': fields.String(required=True, description='Error message'),
    'error_code': fields.String(description='Specific error code'),
    'details': fields.Raw(description='Additional error details')
}

# Health check response model
health_response_model = {
    'status': fields.String(enum=['healthy', 'unhealthy'], description='Service health status'),
    'timestamp': fields.DateTime(description='Health check timestamp'),
    'version': fields.String(description='API version'),
    'uptime': fields.Float(description='Service uptime in seconds'),
    'ai_service': fields.String(enum=['available', 'unavailable'], description='AI service availability')
}

# System info response model
system_info_model = {
    'api_version': fields.String(description='API version'),
    'python_version': fields.String(description='Python version'),  
    'flask_version': fields.String(description='Flask version'),
    'supported_image_formats': fields.List(fields.String, description='Supported image file formats'),
    'max_file_size': fields.Integer(description='Maximum file size in bytes'),
    'ai_model': fields.String(description='AI model being used'),
    'available_weeks': fields.List(fields.String, description='Available calendar weeks')
}

# Test response model
test_response_model = {
    'message': fields.String(description='Test message'),
    'timestamp': fields.DateTime(description='Test timestamp'),
    'status': fields.String(description='Test status')
}