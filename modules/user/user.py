from flask import Flask, abort, flash, g, redirect, request, session, url_for, Blueprint, current_app as app, render_template
from data.models import db
from modules.user.user_forms import EditUser, RegisterUser
from core.auth import is_user_session_valid, is_user_authorized, do_login, do_logout
from data.models import db, connect_db, Any_Type_Group, Any_Type, Entity, User_Session, Membership, Subscription, Post, React, Message, Participant, Recipe_Search, Recipe_Task, Recipe_Ingredient, Recipe_Tool, Signup_Recipe, Signup_Ingredient, Signup_Tool
from core.data import get_json_data, dict_to_b64, row_to_dict, get_public_events, get_public_recipes, execute_sql, row_to_dict2, string_format
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_

# import ipdb; ipdb.set_trace()


bp = Blueprint('user', 
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/user'
)

@bp.route("/api/react/add")
def add_react():

    request_data = request.get_json()
    session_hash = request_data['token']
    post_id = request_data['post_id']
    react = request_data['react']

    return None

@bp.route("/api/react/delete")
def add_react():
    return None

@bp.route("/<username>", strict_slashes=False)
def show_user_home(username):
    t = is_user_session_valid(session)
    if not t:
        session.clear()
        return render_template("401_unauthorized.html")

    (user, user_session) = t
    # import ipdb; ipdb.set_trace()

    # now that we know it's a valid session, check if this is the user's home page
    if (username == user.username):
        #the page that's visited belongs to the user that's logged in
        other = user
    else:
        #check if others home page is valid
        other = Entity.query.filter(Entity.username == username).first()

    if other:
        user_dict = row_to_dict(user)
        user_dict["password"] = ""
        # import ipdb; ipdb.set_trace()
        messages_from = execute_sql(string_format(q_messages_from, user.username, other.username, 100))
        messages_to = execute_sql(string_format(q_messages_to, other.username, 100))
        reacts_from = execute_sql(string_format(q_reacts_from, user.username, other.username, 100))
        reacts_to = execute_sql(string_format(q_reacts_to, other.username, 100))
        entities = Entity.query.all()

        py_data = {}
        py_data["user"] = user_dict
        py_data["user_session"] = row_to_dict(user_session)
        py_data["other"] = row_to_dict(other)
        py_data["messages_from"] = [row_to_dict2(item) for item in messages_from]     # for row from legacy sql query
        py_data["messages_to"] = [row_to_dict2(item) for item in messages_to]     # for row from legacy sql query
        py_data["reacts_from"] = [row_to_dict2(item) for item in reacts_from]     # for row from legacy sql query
        py_data["reacts_to"] = [row_to_dict2(item) for item in reacts_to]     # for row from legacy sql query
        py_data["entities"] = [row_to_dict(item) for item in entities]
        js_data = dict_to_b64(py_data)

        return render_template("user_index.html", py_data=py_data, js_data=js_data)

    #else let the user know they visited an unknown user account and will be redirected to their own home page
    return render_template("404_redirect.html", 
                        redirect_title = "NO PAGE", 
                        redirect_message = "No content available for home page.", 
                        redirect_page = "/", 
                        redirect_seconds = 4)


@bp.route("/<username>/edit", methods=["GET", "POST"])
def update_user(username):
    t = is_user_session_valid(session)
    if t:
        (user, user_session) = t

        if user and user_session:

            if username == user.username:
                # can edit own user profile

                form = EditUser(obj=user)

                # import ipdb; ipdb.set_trace()
                if form.validate_on_submit():
                    if Entity.authenticate(user.username, form.password.data):
                        user.email = form.email.data
                        user.first_name = form.first_name.data
                        user.last_name = form.last_name.data
                        user.phone = form.phone.data
                        user.location = form.location.data
                        user.image_url = form.image_url.data
                        user.about = form.about.data
                        user.updated = datetime.utcnow()

                        db.session.commit()
                        return redirect(f"/user/{username}")

                return render_template('user_edit.html', form=form, username=username)
            else:
                # disallow edit another user's profile
                return render_template("404_redirect.html", 
                                    redirect_title = "NO ACCESS", 
                                    redirect_message = "Cannot change another user's profile.", 
                                    redirect_page = "/", 
                                    redirect_seconds = 4)

    return render_template("404_redirect.html", 
                        redirect_title = "NO ACCESS", 
                        redirect_message = "Must be logged in to change user profile.", 
                        redirect_page = "/", 
                        redirect_seconds = 4)


@bp.route("/<username>/disable", methods=["GET", "POST"])
def disable_user(username):
    t = is_user_session_valid(session)
    if t:
        (user, user_session) = t

        if user and user_session:

            if username == user.username:
                # can edit own user profile

                user.disabled = True
                db.session.commit()

                do_logout(session)
                # disallow edit another user's profile
                return render_template("404_redirect.html", 
                                    redirect_title = "ACCOUNT DISABLED", 
                                    redirect_message = "Profile has been disabled.", 
                                    redirect_page = "/", 
                                    redirect_seconds = 4)
            else:
                # disallow edit another user's profile
                return render_template("404_redirect.html", 
                                    redirect_title = "NO ACCESS", 
                                    redirect_message = "Cannot delete another's user profile.", 
                                    redirect_page = "/", 
                                    redirect_seconds = 4)

    return render_template("404_redirect.html", 
                        redirect_title = "NO ACCESS", 
                        redirect_message = "Must be logged in to delete a user profile.", 
                        redirect_page = "/", 
                        redirect_seconds = 4)


@bp.route("/<username>/delete", methods=["GET", "POST"])
def delete_user(username):
    t = is_user_session_valid(session)
    if t:
        (user, user_session) = t

        if user and user_session:

            if username == user.username:
                # can edit own user profile

                user.to_delete = True
                user.disabled = True
                db.session.commit()

                do_logout(session)
                # disallow edit another user's profile
                return render_template("404_redirect.html", 
                                    redirect_title = "ACCOUNT DELETION", 
                                    redirect_message = "Account has been queued to be deleted in 3 weeks.", 
                                    redirect_page = "/", 
                                    redirect_seconds = 4)
            else:
                # disallow edit another user's profile
                return render_template("404_redirect.html", 
                                    redirect_title = "NO ACCESS", 
                                    redirect_message = "Cannot delete another's user profile.", 
                                    redirect_page = "/", 
                                    redirect_seconds = 4)

    return render_template("404_redirect.html", 
                        redirect_title = "NO ACCESS", 
                        redirect_message = "Must be logged in to delete a user profile.", 
                        redirect_page = "/", 
                        redirect_seconds = 4)


# https://stackoverflow.com/questions/1490942/how-to-declare-a-variable-in-a-postgresql-query
q_messages_from = """WITH
	from_username as (values ('{0}'))
    , to_username as (values ('{1}'))
	, in_limit as (values ({2}))
select m.id as message_id
	, m.from_id as from_id
	, mfe.username as from_name
	, m.to_id as to_id
	, mte.username as to_name
	, p.id as post_id
	, p.created as post_created
	, p.title as post_title
	, p.content as post_content
from (messages m
inner join posts p
on m.post_id = p.id)	   
inner join entities mte
on m.to_id = mte.id
inner join entities mfe
on m.from_id = mfe.id
where mfe.username = (table from_username)
and mte.username = (table to_username)
order by m.id
limit (table in_limit);
"""

q_messages_to = """WITH
	to_username as (values ('{0}'))
	, in_limit as (values ({1}))
select m.id as message_id
	, m.from_id as from_id
	, mfe.username as from_name
	, m.to_id as to_id
	, mte.username as to_name
	, p.id as post_id
	, p.created as post_created
	, p.title as post_title
	, p.content as post_content
from (messages m
inner join posts p
on m.post_id = p.id)	   
inner join entities mte
on m.to_id = mte.id
inner join entities mfe
on m.from_id = mfe.id
where mte.username = (table to_username)
order by m.id
limit (table in_limit);
"""

q_reacts_from = """WITH
	from_username as (values ('{0}'))
    , to_username as (values ('{1}'))
	, in_limit as (values ({2}))
select r.id as react_id
, r.user_id as rf_user_id
, rfe.username as rf_username
, r.post_id as post_id
, r.react_type_id as react_type_id
, t.name as react_type
from (((reacts as r
inner join messages as m
on r.post_id = m.post_id)
inner join entities as mte
on m.to_id = mte.id)
inner join any_types t
on t.id = r.react_type_id)
inner join entities as rfe
on r.user_id = rfe.id
where rfe.username = (table from_username)
and mte.username = (table to_username)
order by r.post_id, r.id
limit (table in_limit);
"""

q_reacts_to = """WITH
	to_username as (values ('{0}'))
	, in_limit as (values ({1}))
select r.id as react_id
, r.user_id as rf_user_id
, rfe.username as rf_username
, r.post_id as post_id
, r.react_type_id as react_type_id
, t.name as react_type
from (((reacts as r
inner join messages as m
on r.post_id = m.post_id)
inner join entities as mte
on m.to_id = mte.id)
inner join any_types t
on t.id = r.react_type_id)
inner join entities as rfe
on r.user_id = rfe.id
where mte.username = (table to_username)
order by r.post_id, r.id
limit (table in_limit);
"""