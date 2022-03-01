"""Seed file to make sample data for capstone db."""

from models import db, connect_db, User, Session
from app import create_app
connect_db(create_app())

# Create all tables

db.drop_all()
db.create_all()

t = u1 = User(username="yu", email="yu@pfix.org", first_name="Yu", last_name="Te", created_time="10/31/2021 08:00:12"); db.session.add(t); db.session.commit()
t = u2 = User(username="test2", email="test2@ptest.org", first_name="Test2", last_name="Last2", created_time="10/31/2021 08:00:12"); db.session.add(t); db.session.commit()
t = u3 = User(username="test3", email="test3@ptest.org", first_name="Test3", last_name="Last3", created_time="10/31/2021 08:00:12"); db.session.add(t); db.session.commit()

t = s1 = Session(session_hash="hash1", user_id=u1.id, client_ip="192.168.0.1", host_ip="192.168.0.2", requested_url="http://hello/test", start_time="10/31/2021 08:00:12"); db.session.add(t); db.session.commit()
t = s2 = Session(session_hash="hash2", user_id=u2.id, client_ip="192.168.0.3", host_ip="192.168.0.2", requested_url="http://hello/test", start_time="10/31/2021 08:00:12"); db.session.add(t); db.session.commit()
t = s3 = Session(session_hash="hash3", user_id=u3.id, client_ip="192.168.0.4", host_ip="192.168.0.2", requested_url="http://hello/test", start_time="10/31/2021 08:00:12"); db.session.add(t); db.session.commit()
