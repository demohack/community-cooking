from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
from jinja2 import TemplateNotFound

# import ipdb; ipdb.set_trace()

from models import db, Event

bp = Blueprint('events', __name__)

@bp.route("/events")
def show_login():
    """return page of events"""

    events = Event.query.all()

    return render_template("events/index.html", events=events)
