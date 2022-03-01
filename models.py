print("log: models.py : begin")

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    print("log: models.py - connect_db() : begin")

    db.app = app
    db.init_app(app)

    print("log: models.py - connect_db() : end")

print("log: models.py : end")
