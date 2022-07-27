from flask import Flask, jsonify
from flask_cors import CORS

from project.exceptions import BaseServiceError
from project.setup.api import api
from project.setup.db import db


def base_service_error_handler(exception: BaseServiceError):
    return jsonify({'error': str(exception)}), exception.code


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    CORS(app=app)
    db.init_app(app)
    api.init_app(app)

    app.register_error_handler(BaseServiceError, base_service_error_handler)

    return app
