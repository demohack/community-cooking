import os
from dotenv import dotenv_values

def config_app(app):
    DATABASE_URI = ''
    SECRET_KEY = ''

    if 'ON_HEROKU' in os.environ:
        SECRET_KEY = os.environ.get('SECRET_KEY')
        DATABASE_URI = os.environ.get('DATABASE_URI')
    else:
        settings = dotenv_values("/Users/yu/sb/conf/.env")
        SECRET_KEY = settings['SECRET']

        DB_CONFIG = {
            'driver': settings['PGDRIVER'],
            'user': settings['PGUSER'],
            'pw': settings['PGPASSWORD'],
            'db': 'cooking',
            'host': settings['PGHOST'],
            'port': settings['PGPORT'],
        }

        DATABASE_URI = '{driver}://{user}:{pw}@{host}:{port}/{db}'.format_map(DB_CONFIG)

    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['TESTING'] = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
