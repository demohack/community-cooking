from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
from jinja2 import TemplateNotFound

# import ipdb; ipdb.set_trace()

from models import db, Entity

bp = Blueprint('users', __name__)

@bp.route("/users")
def show_login():
    """return page of users"""

    users = Entity.query.all()

    return render_template("users/index.html", users=users)
