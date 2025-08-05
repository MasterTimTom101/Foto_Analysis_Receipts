import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    # AI Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = "gemini-2.5-flash"
    
    # Application Paths
    BASE_DIR = Path(__file__).parent.parent.parent.parent
    API_DIR = Path(__file__).parent.parent / 'api'
    PHOTOS_DIR = API_DIR / 'photos'
    COST_FILES_DIR = API_DIR / 'cost_files'
    
    # AI Prompt Configuration
    PROMPT_TEXT = (
        "Es ist ein Kassenbon und Eurobetraege mit Komma"
        "Mache einen CSV Datensatz no header und ohne Erlaeuterung mit Semikolon als Trenner von "
        "Datum mit Punkt, Uhrzeit mit Doppelpunkt, Summe_Food, Summe_NonFood"
    )
    
    # File Configuration
    SUPPORTED_IMAGE_EXTENSIONS = ['.jpeg', '.jpg']
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
    
    @classmethod
    def init_app(cls, app):
        """Initialize application with configuration"""
        # Create necessary directories
        cls.PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
        cls.COST_FILES_DIR.mkdir(parents=True, exist_ok=True)
        
        # Validate required configuration
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is required")

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Production-specific initialization
        if not cls.SECRET_KEY:
            raise ValueError("SECRET_KEY must be set in production")

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}