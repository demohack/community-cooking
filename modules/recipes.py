from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
from jinja2 import TemplateNotFound

# import ipdb; ipdb.set_trace()

from models import db, Recipe, Food

bp = Blueprint('recipe', __name__)

@bp.route("/recipe")
def show_login():
    """return page of recipes"""

    list = Recipe.query.all()

    return render_template("recipe/index.html", list=list)
