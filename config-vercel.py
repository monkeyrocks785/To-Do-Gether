import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    # Database - Use PostgreSQL in production, SQLite in /tmp for development
    if os.environ.get('DATABASE_URL'):
        # For production (Vercel with external DB like PostgreSQL)
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    else:
        # For development (local SQLite in /tmp which is writable)
        # Vercel: Use /tmp directory (read-write)
        # Local: Use local db folder
        if os.getenv('FLASK_ENV') == 'production' or os.path.exists('/var/task'):
            # Running on Vercel - use /tmp
            SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/todos.db'
        else:
            # Local development - use db folder
            DB_PATH = os.path.join(os.path.dirname(__file__), 'db')
            try:
                os.makedirs(DB_PATH, exist_ok=True)
            except (OSError, PermissionError):
                # If we can't create db folder, use /tmp
                SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/todos.db'
            else:
                SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(DB_PATH, "todos.db")}'
    
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