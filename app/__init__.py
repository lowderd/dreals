# app/__init__.py

import datetime
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

# Initialize the app
app = Flask(__name__, instance_relative_config=True)

# instantiate the db
db = SQLAlchemy()

# set login config
login_manager = LoginManager()


def create_app(app_settings):
    """
    Create and return the Flask App
    :param app_settings: App Configuration Settings
    :return: Flask App
    """

    # set config
    app.config.from_object(app_settings)

    Bootstrap(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"
    migrate = Migrate(app, db)

    # Load the models
    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app
