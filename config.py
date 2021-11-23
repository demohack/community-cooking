import os
from dotenv import dotenv_values

def config_app(app):
    if 'ON_HEROKU' in os.environ:
        db_url = os.environ.get('DATABASE_URL')
    else:
        settings = dotenv_values("/Users/yu/sb/conf/.env")

        DB_CONFIG = {
            'driver': settings['PGDRIVER'],
            'user': settings['PGUSER'],
            'pw': settings['PGPASSWORD'],
            'db': 'warbler',
            'host': settings['PGHOST'],
            'port': settings['PGPORT'],
        }

        db_url = '{driver}://{user}:{pw}@{host}:{port}/{db}'.format_map(DB_CONFIG)

    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogly.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SECRET_KEY'] = 'testtest'
    app.config['TESTING'] = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

pid = str(os.getpid())
print(f'Creating PID file: {pid} => /tmp/flaskapp.pid')
fh=open("/tmp/flaskapp.pid", "w")
fh.write(pid)
fh.close()
