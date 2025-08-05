import os
from flask import Flask
from flask_restx import Api
from flask_cors import CORS

from ..core.config import config
from ..web.routes import register_routes
from .v1 import system_api, analysis_api


def create_app(config_name=None):
    """Create and configure Flask application with both web and API interfaces"""
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')
    
    app = Flask(__name__, template_folder='../web/templates')
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Enable CORS for API endpoints
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Create API instance
    api = Api(
        app,
        version='1.0',
        title='Receipt Analysis API',
        description='AI-powered receipt analysis system using Google Gemini AI to extract costs from receipt photos',
        doc='/swagger/',
        prefix='/api/v1'
    )
    
    # Register API namespaces (test endpoint now included in system)
    api.add_namespace(system_api, path='/system')
    api.add_namespace(analysis_api, path='/analyze')
    
    # Register web routes (existing HTML interface)
    register_routes(app)
    
    return app

