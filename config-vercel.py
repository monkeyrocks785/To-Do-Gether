import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    # Database configuration
    if os.environ.get('DATABASE_URL'):
        # Production: Use PostgreSQL from environment variable
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    else:
        # Development/Vercel: Use SQLite in /tmp (always writable)
        SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/todos.db'
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    REMEMBER_COOKIE_DURATION = 604800  # 7 days

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