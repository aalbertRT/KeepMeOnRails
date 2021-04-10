from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import config

import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(testing=False):
    """Application factory

    Args: 
        testing (bool): will load TestingConfig if True, defaults to False
    Returns: 
        A Flask application object
    """
    app = Flask(
        __name__,
        instance_relative_config=False,
        template_folder="templates",
        static_folder="static")

    # Load Flask environment based on environment variable FLASK_ENV
    flask_env = os.getenv('FLASK_ENV', None)
    if testing:
        app.config.from_object(config.TestConfig)
    elif flask_env == 'production':
        app.config.from_object(config.ProdConfig)
    elif flask_env == 'development':
        app.config.from_object(config.DevConfig)
    elif flask_env == 'testing':
        app.config.from_object(config.TestConfig)
    else:
        app.config.from_object(config.DevConfig)

    # Initialize plugin 
    db.init_app(app)
    login_manager.init_app(app)
    
    with app.app_context():
        # Import blueprint modules
        from application.blueprints.home import home
        from application.blueprints.auth import auth
        # Register Blueprints
        app.register_blueprint(home.home_bp)
        app.register_blueprint(auth.auth_bp)

        # Create database
        db.create_all()

        return app
        