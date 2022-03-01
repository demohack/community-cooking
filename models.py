"""Models for Cooking app."""

# import ipdb; ipdb.set_trace()

from datetime import datetime

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


# DO NOT MODIFY THIS FUNCTION
def connect_db(app):
    """Connect to database"""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User: model a user who to validate account logins."""
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    username = db.Column(db.String(32))
    email = db.Column(db.String(260))
    password_hash = db.Column(db.String(64))
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    created_time = db.Column(db.DateTime(timezone=True))

    def __repr__(s) -> str:
        return f"<{s.__tablename__} {s.id} {s.name}>"

class Session(db.Model):
    """Session: model a session, who"""
    __tablename__ = 'session'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    session_hash = db.Column(db.String(45))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    client_ip = db.Column(db.String(39))
    host_ip = db.Column(db.String(39))
    requested_url = db.Column(db.String(2048))
    start_time = db.Column(db.DateTime(timezone=True))

    def __repr__(s) -> str:
        return f"<{s.__tablename__} {s.id} {s.session_hash}>"

