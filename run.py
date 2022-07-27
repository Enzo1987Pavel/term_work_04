from flask import render_template, Flask
from flask_restx import Api

from project.config import DevelopmentConfig
from project.server import db
from project.views import auth_ns, genres_ns, directors_ns, movies_ns, user_ns

api = Api(title="Flask Course Project 4", doc="/docs")


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    @app.route('/')
    def index():
        return render_template('index.html')

    db.init_app(app)
    api.init_app(app)

    # Регистрация эндпоинтов
    api.add_namespace(auth_ns)
    api.add_namespace(user_ns)
    api.add_namespace(genres_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(movies_ns)

    return app


app = create_app()

if __name__ == '__main__':
    app = create_app()
    app.run(
        port=25000,
        debug=True
    )

