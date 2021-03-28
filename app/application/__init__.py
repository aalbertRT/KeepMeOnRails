from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

import os

db = SQLAlchemy()

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
    
    with app.app_context():
        # Include app routes
        from .home import routes as home

        # Register Blueprints
        app.register_blueprint(home.home_bp)

        # Create database
        db.create_all()

        return app
        