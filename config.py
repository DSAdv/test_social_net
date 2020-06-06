from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask configuration from environment variables."""

    FLASK_APP = 'wsgi.py'
    FLASK_ENV = environ.get('FLASK_ENV')
    SECRET_KEY = environ.get('SECRET_KEY')
    JWT_SECRET_KEY = environ.get('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = environ.get("JWT_TOKEN_LOCATION")
    JWT_COOKIE_CSRF_PROTECT = environ.get("JWT_COOKIE_CSRF_PROTECT")
    JWT_CSRF_CHECK_FORM = environ.get("JWT_CSRF_CHECK_FORM")

    JWT_BLACKLIST_ENABLED = environ.get("JWT_BLACKLIST_ENABLED")
    JWT_BLACKLIST_TOKEN_CHECKS = environ.get("JWT_BLACKLIST_TOKEN_CHECKS")

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
