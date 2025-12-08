# Flask Configuration for To-Do-Gether
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    # Create db folder if it doesn't exist
    DB_PATH = os.path.join(os.path.dirname(__file__), 'db')
    os.makedirs(DB_PATH, exist_ok=True)
    
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(DB_PATH, "todos.db")}'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    REMEMBER_COOKIE_DURATION = 604800  # 7 days in seconds

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Select config based on FLASK_ENV
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get config based on environment"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
