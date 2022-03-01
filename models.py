from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

print "log: models.py"
def connect_db(app):

    db.app = app
    db.init_app(app)

    print "log: models.py - connect_db()"
