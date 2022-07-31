from flask_restx import Namespace, Resource
from flask import request
from project.container import user_service
from project.setup.api.models import user

api = Namespace('auth')


@api.route("/register/")
class RegisterView(Resource):
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def post(self):
        data = request.json
        if data.get("email") and data.get("password"):
            return user_service.create_user(data.get("email"), data.get("password")), 201
        else:
            return "Не все поля заполнены!", 204


@api.route("/login/")
class AuthLoginView(Resource):
    @api.response(404, 'Not Found')
    def post(self):
        data = request.json
        if data.get('email') and data.get('password'):
            return user_service.check(data.get('email'), data.get('password')), 201
        else:
            return "Не все поля заполнены!", 204

    @api.response(404, 'Not Found')
    def put(self):
        data = request.json
        if data.get("access_token") and data.get("refresh_token"):
            return user_service.update_token(data.get("refresh_token")), 201
        else:
            return "Не все поля заполнены!", 204
