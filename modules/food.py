from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
from jinja2 import TemplateNotFound

# import ipdb; ipdb.set_trace()

from models import db, Food

bp = Blueprint('food', __name__)

@bp.route("/food")
def show_login():
    """return page of food items"""

    list = Food.query.all()

    return render_template("food/index.html", list=list)
