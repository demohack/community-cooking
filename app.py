#
# create_app is the main entry point for this flask web app
#

#import ipdb; ipdb.set_trace()

def create_app(test_config=None):
    from flask import Flask
    app = Flask(__name__, static_url_path='/static')

    from config import config_app
    config_app(app)

    from data.models import connect_db
    connect_db(app)

    @app.after_request
    def add_header(req):
        # Turn off all caching in Flask
        # https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

        req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        req.headers["Pragma"] = "no-cache"
        req.headers["Expires"] = "0"
        req.headers['Cache-Control'] = 'public, max-age=0'
        return req

    from modules.admin import admin
    app.register_blueprint(admin.bp)

    from modules.events import events
    app.register_blueprint(events.bp)

    from modules.friends import friends
    app.register_blueprint(friends.bp)

    from modules.auth import auth
    app.register_blueprint(auth.bp)

    from modules.stories import stories
    app.register_blueprint(stories.bp)

    from modules.recipes import recipes
    app.register_blueprint(recipes.bp)

    from modules.search import search
    app.register_blueprint(search.bp)

    from modules.users import users
    app.register_blueprint(users.bp)

    from modules.user import user
    app.register_blueprint(user.bp)

    from modules.visitor import visitor
    app.register_blueprint(visitor.bp)

    from other.todos import todos
    app.register_blueprint(todos.bp)

    from other.jeopardy import jeopardy
    app.register_blueprint(jeopardy.bp)

    from other.hack_or_snooze import hack_or_snooze
    app.register_blueprint(hack_or_snooze.bp)

    from other.connect4 import connect4
    app.register_blueprint(connect4.bp)

    from other.cards import cards
    app.register_blueprint(cards.bp)

    return app
