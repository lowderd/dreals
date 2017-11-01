# app/__init__.py

import datetime
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

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

    # initialize the db
    db.init_app(app)

    # initialize the login manager
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"

    # migrate database
    migrate = Migrate(app, db)

    # Load the views
    from app import models, views

    return app
