"""
Main Flask application factory
"""

import os
from flask import Flask
from flask_restx import Api
from flask_cors import CORS

from .config import config
from .web.routes import register_routes
from .api.analysis import api as analysis_api
from .api.system import api as system_api


def create_app(config_name=None):
    """Create and configure Flask application with both web and API interfaces"""
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')
    
    app = Flask(__name__, template_folder='web/templates')
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Enable CORS for API endpoints
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Create API instance (removed versioning /api/v1 -> /api)
    api = Api(
        app,
        version='1.0',
        title='Receipt Analysis API',
        description='AI-powered receipt analysis system using Google Gemini AI',
        doc='/swagger/',
        prefix='/api'
    )
    
    # Register API namespaces (simplified paths)
    api.add_namespace(analysis_api, path='/analyze')
    api.add_namespace(system_api, path='/system')
    
    # Register web routes (existing HTML interface)
    register_routes(app)
    
    return app


def create_api_only_app(config_name=None):
    """Create Flask application with only API endpoints (no web interface)"""
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')
    
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Enable CORS
    CORS(app)
    
    # Create API instance
    api = Api(
        app,
        version='1.0',
        title='Receipt Analysis API',
        description='AI-powered receipt analysis system using Google Gemini AI',
        doc='/swagger/',
        prefix='/api'
    )
    
    # Register API namespaces
    api.add_namespace(analysis_api, path='/analyze')
    api.add_namespace(system_api, path='/system')
    
    return app