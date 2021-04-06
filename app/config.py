from os import environ, path
from dotenv import load_dotenv

# Load environment variables
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Base configuration."""

    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'template'
    # Database
    SQLALCHEMY_ECHO = False # If True: log db activity to stderr Python console
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Secrets
    SNCF_TOKEN = environ.get('SNCF_TOKEN')
    SECRET_KEY = environ.get('SECRET_KEY')

class ProdConfig(Config):
    """Production configuration."""

    FLASK_ENV = 'production'
    TESTING = False
    DEBUG = False
    # Database
    SQLALCHEMY_DATABASE_URI = environ.get('PROD_DATABASE_URI')

class DevConfig(Config):
    """Development configuration."""

    FLASK_ENV = 'development'
    TESTING = True
    DEBUG = True
    # Database
    SQLALCHEMY_DATABASE_URI = environ.get('DEV_DATABASE_URI')

class TestConfig(Config):
    """PyTest configuration."""
    
    FLASK_ENV = 'testing'
    TESTING = True
    DEBUG = True
    # Database
    SQLALCHEMY_DATABASE_URI = environ.get('TEST_DATABASE_URI')
    # Secrets
    SECRET_KEY = '?iHpf.\nsPrB,>0A"~J.K52#@'
