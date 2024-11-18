import os
import logging

# Load environment variables from .env file
# if dotenv import cannot be resolved, try "pip install python-dotenv"

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET KEY', 'default_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    # Setting this to True will pause form submittals
    DEBUG_TB_INTERCEPT_REDIRECTS = True
    FLASK_ENV = 'development'
    USE_RELOADER = True


class ProductionConfig(Config):
    """Production Configuration"""
    DEBUG = False
    FLASK_ENV = 'production'


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    FLASK_ENV = 'testing'
    DEBUG_TB_HOSTS = 'dont-show-debug-toolbar'
    DEBUG_TB_INTERCEPT_REDIRECTS = False


# Initialize the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter and set it for the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - '
                              '%(message)s')
console_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(console_handler)
