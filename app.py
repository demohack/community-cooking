import os

from flask import Flask, render_template

# from forms import UserAddForm, LoginForm, MessageForm
from models import db, connect_db #, User, Message

CURR_USER_KEY = "curr_user"

app = Flask(__name__)


##############################################################################
# User signup/login/logout


@app.route('/')
def homepage():
    """Show homepage:

    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """

    return render_template('home.html')

