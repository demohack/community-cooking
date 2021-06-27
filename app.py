import os

from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

# from forms import UserAddForm, LoginForm, MessageForm
from models import db, connect_db #, User, Message

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

from config import config_app
config_app(app)
connect_db(app)

toolbar = DebugToolbarExtension(app)


##############################################################################
# User signup/login/logout


@app.route('/')
def homepage():
    """Show homepage:

    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """

    return render_template('home.html')

