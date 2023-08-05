from flask import Flask, abort, flash, g, redirect, request, session, url_for, Blueprint, current_app as app, render_template
from data.models import db
from modules.user.user_forms import EditUser, RegisterUser
from core.auth import is_user_session_valid, is_user_authorized, do_login, do_logout
from data.models import db, connect_db, Any_Type_Group, Any_Type, Entity, User_Session, Membership, Subscription, Post, React, Message, Participant, Recipe_Search, Recipe_Task, Recipe_Ingredient, Recipe_Tool, Signup_Recipe, Signup_Ingredient, Signup_Tool
from core.data import get_json_data, dict_to_b64, row_to_dict, get_public_events, get_public_recipes, get_any_type_value
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_

# import ipdb; ipdb.set_trace()


bp = Blueprint('stories', 
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/stories'
)


@bp.route("/")
def show_stories():
    t = is_user_session_valid(session)
    if not t:
        session.clear()
        return render_template("401_unauthorized.html")

    (user, user_session) = t

    post_post_type = get_any_type_value("post")

    # get user favorites
    reacts = React.query.filter(React.user_id==user.id).all()
    
    # get user stories
    stories = Post.query.filter(and_(Post.creator_id==user.id, Post.post_type_id==post_post_type.id)).all()

    user_dict = row_to_dict(user)
    user_dict["password"] = ""

    py_data = {}
    py_data["user"] = user_dict
    py_data["user_session"] = row_to_dict(user_session)
    py_data["stories"] = [row_to_dict(item) for item in stories]
    py_data["reacts"] = [row_to_dict(item) for item in reacts]
    js_data = dict_to_b64(py_data)
    
    return render_template("stories_index.html", py_data=py_data, js_data=js_data)

