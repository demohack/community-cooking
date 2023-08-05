from flask import Flask, abort, flash, g, redirect, request, session, url_for, Blueprint, current_app as app, render_template
from data.models import db
from modules.user.user_forms import EditUser, RegisterUser, LoginUser
from core.auth import is_user_session_valid, is_user_authorized, do_login, do_logout
from data.models import db, connect_db, Any_Type_Group, Any_Type, Entity, User_Session, Membership, Subscription, Post, React, Message, Participant, Recipe_Search, Recipe_Task, Recipe_Ingredient, Recipe_Tool, Signup_Recipe, Signup_Ingredient, Signup_Tool
from core.data import get_json_data, dict_to_b64, row_to_dict, get_public_events, get_public_recipes, get_any_type_value, get_status_dict, get_error_dict, get_success_dict
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_

# import ipdb; ipdb.set_trace()


bp = Blueprint('auth', 
    __name__,
    template_folder='templates',
    static_folder='static'
)


@bp.route("/api/login", methods=['POST'], strict_slashes=False)
def api_login():

    request_data = request.get_json()
    username = request_data['user']['username']
    password = request_data['user']['password']

    user = Entity.authenticate(username, password)

    # import ipdb; ipdb.set_trace()

    if user:
        user_session = do_login(user, session, request.environ)

        if user_session:
            db.session.add(user_session)
            db.session.commit()

            recipe_post_type = get_any_type_value("recipe")

            # get user favorites
            reacts = React.query.filter(React.user_id==user.id).all()
            
            # get user recipes
            recipes = Post.query.filter(and_(Post.creator_id==user.id, Post.post_type_id==recipe_post_type.id)).all()

            user_dict = row_to_dict(user)
            user_dict["password"] = ""

            py_data = {}
            py_data["user"] = user_dict
            py_data["user_session"] = row_to_dict(user_session)
            py_data["recipes"] = [row_to_dict(item) for item in recipes]
            py_data["reacts"] = [row_to_dict(item) for item in reacts]

            return py_data

    return get_error_dict(title="Unauthorized", message="Invalid username or password.")


@bp.route("/api/logout", methods=['POST'], strict_slashes=False)
def api_logout():
    do_logout(session)
    return get_success_dict(message="User logged out.")


@bp.route("/login", methods=['GET', 'POST'], strict_slashes=False)
def show_login():

    form = LoginUser()

    if form.validate_on_submit():

        user = Entity.authenticate(form.username.data,
                                    form.password.data)

        # import ipdb; ipdb.set_trace()

        if user:
            user_session = do_login(user, session, request.environ)

            if user_session:
                db.session.add(user_session)
                db.session.commit()
                return redirect(f"/user/{user.username}")
        else:
            flash("Invalid username/password.", 'danger')

    return render_template("login.html", form=form)


@bp.route("/logout", strict_slashes=False)
def show_logout():

    do_logout(session)

    return redirect("/")
