import os


class Config:
    # Flask configuration
    APP_NAME = 'library'
    DEBUG = True
    SECRET_KEY = 'VerySecretKey'
    CSRF_ENABLED = True

    # SQLAlchemy configuration
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.getcwd()}/{APP_NAME}.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
