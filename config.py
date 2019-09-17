import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# TODO: fix layout.html, include logout etc


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') \
        .replace('{basedir}', basedir+'\\')
    # or \
    # 'sqlite:///' + os.path.join(basedir, 'app.db')
    # 'postgresql+psycopg2://postgres:hybrid@localhost/payroll'
    # 'firebird+fdb://sysdba:masterkey@localhost:3050/' + os.path.join(basedir, 'app.fdb')
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    ADMINS = ['jeffflask@gmail.com']
    LANGUAGES = ['en', 'es']
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')

    # flask-user settings
    USER_APP_NAME = 'Payroll Master'
    USER_ENABLE_CHANGE_USERNAME = False

    # pagination
    PAGE_SIZE = 20
    VISIBLE_PAGE_COUNT = 10
