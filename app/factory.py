import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from flask_jwt import JWT
from flask_security import Security
from flask_security.utils import encrypt_password
from flask import Flask, Blueprint
from app.resources import initialize_api
from app.models.database import user_datastore
from app.authentication import load_user,authenticate

from .config import config


class Factory:

    def __init__(self, environment='development'):
        self._environment = os.environ.get('APP_ENVIRONMENT', environment)
        self.flask = None

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self, env):
        self._environment = env

    def set_flask(self, **kwargs):
        self.flask = Flask(__name__, **kwargs)
        self.flask.config.from_object(config[self._environment])
        # setup logging
        file_handler = RotatingFileHandler(
            'api.log', maxBytes=10000, backupCount=1)
        file_handler.setLevel(logging.INFO)
        self.flask.logger.addHandler(file_handler)
        stdout = logging.StreamHandler(sys.stdout)
        stdout.setLevel(logging.DEBUG)
        self.flask.logger.addHandler(stdout)

        return self.flask

    def set_db(self):
        from .models.database import db
        db.init_app(self.flask)

    def set_migration(self):
        from .models.database import db, migrate
        migrate.init_app(self.flask, db)

    def set_api(self):
        # from .resources import api
        # api.init_app(self.flask, version='1.0.0', title='api')
        from flask_restful import Api
        api_bp = Blueprint('api', __name__)
        api = Api(api_bp)
        initialize_api(api)
        self.flask.register_blueprint(api_bp, url_prefix='/dev-api/v1')
    
    def set_security(self):
        #############################################
        ########## Security - Flask-Security and JWT
        #############################################
        security = Security(self.flask, user_datastore)
        jwt = JWT(self.flask, authenticate, load_user)

        #############################################
        ########## Bootstrap Several Users
        # https://github.com/graup/flask-restless-security/blob/master/server.py
        #############################################
