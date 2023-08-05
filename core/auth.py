from data.models import User_Session
import json
from core.data import row_to_json

SESSION_HASH_KEY = "session_hash_key"
SESSION_USER_KEY = "session_user_key"


def is_user_session_valid(session):
    # session valid lets people use the site without having to login again
    # the flask session object stores two JSON data objects for the user and session

    # import ipdb; ipdb.set_trace()

    # get the session hash
    # check database if the session hash is still valid
    # if so get the user info
    # return a tuple of the (user, user_session)

    if SESSION_HASH_KEY not in session:
        session.clear()
        return None

    session_json = session.get(SESSION_HASH_KEY, json.dumps({}))
    session_data = json.loads(session_json)

    if not session_data:
        session.clear()
        return None

    t = User_Session.validate(session_data['session_hash'])
    if not t:
        session.clear()
        return None

    (user, user_session) = t

    if not user or not user_session:
        session.clear()
        return None

    return t


def is_user_authorized(page_id, session):
    # get the page_id from record
    # determine who owns the page, and what the privacy type is for that page
    # if privacy type is personal, only the creator of the page can modify
    # else if privacy is friends or members, check the membership table
    # else if privacy public, anyone that's a site user can edit

    # import ipdb; ipdb.set_trace()

    user_json = session.get(SESSION_USER_KEY, json.dumps({}))
    user_data = json.loads(user_json)

    if not user_data:
        return None

    # NOTE that objects created from json.loads() are dictionary objects, 
    # and not SQL-Alchemy recordset object
    # Thus can't use dot notation, instead use dictionary ['key'] to get property value
    if user_data['username'] != username:
        return None

    return user_data


def do_login(user, session, environ):
    # import ipdb; ipdb.set_trace()

    # this seems odd, but the intent is to clear out the user_session table
    do_logout(session)

    user_ip = environ.get('REMOTE_ADDR', 'unknown ip')
    host_ip = environ.get('SERVER_NAME', 'unknown ip')
    requested_url = environ.get('HTTP_REFERER', 'unknown url')

    user_session = User_Session.establish(user_id=user.id, user_ip=user_ip, host_ip=host_ip, requested_url=requested_url)

    if user_session:
        session[SESSION_USER_KEY] = row_to_json(user)
        session[SESSION_HASH_KEY] = row_to_json(user_session)
        return user_session

    session.clear()
    return None


def do_logout(session):
    # import ipdb; ipdb.set_trace()

    # pop returns the value that is associated with key if present, 
    # or returns the second, default parameter. 
    # thus no need to check if key is in dictionary. 

    if SESSION_HASH_KEY in session:
        session_json = session.pop(SESSION_HASH_KEY, json.dumps({}))

        if session_json:
            session_data = json.loads(session_json)

            if session_data:
                User_Session.logout(session_data['session_hash'])

    session.clear()
