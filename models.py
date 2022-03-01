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

class User(db.Model):
    """User: model a user who to validate account logins."""
    __tablename__ = 'user'
    print(f"log: models.py - {__tablename__}() : begin")

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.String(32))
    email = db.Column(db.String(260))
    password_hash = db.Column(db.String(64))
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    created_time = db.Column(db.DateTime(timezone=True))

    print(f"log: models.py - {__tablename__}() : end")
    def __repr__(s) -> str:
        return f"<{s.__tablename__} {s.id} {s.name}>"

class Session(db.Model):
    """Session: model a session, who"""
    __tablename__ = 'session'
    print(f"log: models.py - {__tablename__}() : begin")

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    session_hash = db.Column(db.String(45))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    client_ip = db.Column(db.String(39))
    host_ip = db.Column(db.String(39))
    requested_url = db.Column(db.String(2048))
    start_time = db.Column(db.DateTime(timezone=True))

    print(f"log: models.py - {__tablename__}() : end")
    def __repr__(s) -> str:
        return f"<{s.__tablename__} {s.id} {s.session_hash}>"

print("log: models.py : end")
