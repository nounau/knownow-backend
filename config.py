import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGO_DB_URL = os.environ.get('MONGO_DB_URL')
    MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME')
    print("DB URL ",MONGO_DB_URL)
    print("DB URL ",MONGO_DB_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False