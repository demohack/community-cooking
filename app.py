print("log: app.py : begin")

from flask import Flask, render_template, request, flash, redirect, session, g
app = Flask(__name__)

# from forms import UserAddForm, LoginForm, MessageForm
from models import db, connect_db #, User, Message
from config import config_app
config_app(app)
connect_db(app)


##############################################################################
# User signup/login/logout


@app.route('/')
def homepage():
    print("log: app.py - homepage() : begin")

    print("log: app.py - homepage() : end")
    return render_template('home.html')

print("log: app.py : end")
