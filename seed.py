"""Seed database with sample data from CSV Files."""

from flask import Flask
app = Flask(__name__)

from config import config_app
config_app(app)

from csv import DictReader

from models import db, connect_db, User, Message, Follows
connect_db(app)

db.drop_all()
db.create_all()

with open('generator/users.csv') as users:
    db.session.bulk_insert_mappings(User, DictReader(users))

with open('generator/messages.csv') as messages:
    db.session.bulk_insert_mappings(Message, DictReader(messages))

with open('generator/follows.csv') as follows:
    db.session.bulk_insert_mappings(Follows, DictReader(follows))

db.session.commit()
