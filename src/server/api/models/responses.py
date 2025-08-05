"""
Common response models for the API
"""

from flask_restx import fields

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
    'database': fields.String(enum=['connected', 'disconnected'], description='Database connection status'),
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


# Group all response models
response_models = {
    'Success': success_response_model,
    'Error': error_response_model,
    'HealthResponse': health_response_model,
    'SystemInfo': system_info_model
}