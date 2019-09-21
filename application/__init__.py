import os
import json
import logging
import functools
import google.oauth2.credentials
import googleapiclient.discovery

from flask import Flask
from application import login
from authlib.client import OAuth2Session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.register_blueprint(login.app)
    app.config.from_object('config.Config')
    db.init_app(app)
        
    with app.app_context():
        from . import routes
        db.create_all()
        return app