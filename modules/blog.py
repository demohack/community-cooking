from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
from jinja2 import TemplateNotFound

# import ipdb; ipdb.set_trace()

from models import db, Post

bp = Blueprint('blog', __name__)

@bp.route("/blog")
def show_blog():
    """return page of posts"""

    posts = Post.query.all()

    return render_template("blog/index.html", posts=posts)
