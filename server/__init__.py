from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    with app.app_context():
        db.init_app(app)
        jwt.init_app(app)

        from server.resources import api_bp
        app.register_blueprint(api_bp, url_prefix="/api")

        db.create_all()
        return app
