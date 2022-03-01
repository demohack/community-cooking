from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
from jinja2 import TemplateNotFound

# import ipdb; ipdb.set_trace()

from models import db

bp = Blueprint('auth', __name__)

@bp.route("/login")
def show_login():
    """Return a list of auth."""
#    import ipdb; ipdb.set_trace()

    return render_template("auth/login.html")
