from flask_restx import Namespace, Resource
from flask import request
from project.container import user_service
from project.setup.api.models import user
from project.tools.security import generate_tokens, approve_refresh_token

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
        user_data = request.json
        email = user_data.get("email")
        password = user_data.get("password")
        if None in [email, password]:
            return "Не введен логин или пароль", 400

        return generate_tokens(email, password)

    @api.response(404, 'Not Found')
    def put(self):
        data = request.json
        token = data.get("refresh_token")
        return approve_refresh_token(token)
