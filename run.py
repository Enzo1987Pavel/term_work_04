from project.config import config
from project.server import create_app


app = create_app(config)

if __name__ == '__main__':
    app.run(
        port=25000,
        debug=True
    )

