from flask import Flask

from config.config import Config

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.article import article_bp
from routes.search import search_bp


def create_app():

    app = Flask(
        __name__,
        template_folder="webapp/templates",
        static_folder="webapp/static"
    )

    app.config.from_object(Config)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(article_bp)
    app.register_blueprint(search_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=Config.DEBUG)