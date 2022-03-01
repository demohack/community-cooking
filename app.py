def create_app(test_config=None):

    DATABASE_URI = ''
    SECRET_KEY = ''

    import os

    if 'ON_HEROKU' in os.environ:
        DATABASE_URI = os.environ.get('DATABASE_URL')
        SECRET_KEY = os.environ.get('SECRET_KEY')
    else:
        from dotenv import dotenv_values
        settings = dotenv_values("/Users/yu/sb/conf/.env")
        SECRET_KEY = settings['SECRET'];

        DB_CONFIG = {
            'driver': settings['PGDRIVER'],
            'user': settings['PGUSER'],
            'pw': settings['PGPASSWORD'],
            'db': 'warbler',
            'host': settings['PGHOST'],
            'port': settings['PGPORT'],
        }

        DATABASE_URI = '{driver}://{user}:{pw}@{host}:{port}/{db}'.format_map(DB_CONFIG)

    # create and configure the app
    from flask import Flask, redirect
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping (
        SECRET_KEY=SECRET_KEY,
        SQLALCHEMY_DATABASE_URI=DATABASE_URI,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
        TESTING=True,
        DEBUG_TB_INTERCEPT_REDIRECTS=False,
    )

    from models import connect_db
    connect_db(app)

#    from flask_debugtoolbar import DebugToolbarExtension
#    debug = DebugToolbarExtension(app)

#    import ipdb; ipdb.set_trace()

    @app.route('/')
    def show_index():
        """Homepage: redirect to whatever you want."""
        return redirect("/login")       # /blog, /login, /hello

    from modules.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app

"""
    from modules.blog import bp as blog_bp
    app.register_blueprint(blog_bp)

    from modules.events import bp as events_bp
    app.register_blueprint(events_bp)

    from modules.recipes import bp as recipes_bp
    app.register_blueprint(recipes_bp)

    from modules.food import bp as food_bp
    app.register_blueprint(food_bp)

    from modules.users import bp as users_bp
    app.register_blueprint(users_bp)
"""

