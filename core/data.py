from flask import current_app, url_for
from datetime import datetime
import json, requests
from base64 import b64encode
from sqlalchemy import and_
from data.models import db, Any_Type, Post

def string_format(s, *args):
    s0 = s
    loop = True
    i = 0
    while loop:
        term = '{' + str(i) + '}'
        x = s0.find(term)
        if x >= 0:
            if isinstance(args[i], str):
                s0 = s0.replace(term, args[i])
            else:
                s0 = s0.replace(term, str(args[i]))
            i += 1
        else:
            loop = False
    return s0

def execute_sql(sql):
    cn = db.get_engine().connect()
    rs = cn.execute(sql)
    return rs

def get_status_dict(title, message, status):
    
    status = {}
    status["title"] = title
    status["message"] = message
    status["status"] = status

    py_data = {}
    py_data["status"] = status
    
    return py_data


def get_error_dict(message, title, status=401):
    return get_status_dict(title=title, message=message, status=status)


def get_success_dict(message, title="Success", status=200):
    return get_status_dict(title=title, message=message, status=status)


def get_any_type_value(type_name):
    rows = Any_Type.query.filter(Any_Type.name == type_name).all()
    if rows:
        return rows[0]
    return None


def get_public_events():
    event_post_type = get_any_type_value("event")
    public_privacy_type = get_any_type_value("public")

    # print(f"get_public_events start:")
    rows = Post.query.filter(and_(Post.post_type_id == event_post_type.id, Post.privacy_type_id == public_privacy_type.id)).all()
    # import ipdb; ipdb.set_trace()
    # print(f"get_public_events end: {rows}")
    return rows


def get_public_recipes():
    recipe_post_type = get_any_type_value("recipe")
    public_privacy_type = get_any_type_value("public")

    rows = Post.query.filter(and_(Post.post_type_id == recipe_post_type.id, Post.privacy_type_id == public_privacy_type.id)).all()
    return rows


# get data from json file given a filename, assuming the file was stored on static folder
def get_json_data(filename):
    #import ipdb; ipdb.set_trace()

    try:
        url = url_for('static', filename = filename, _external = True)
        response = requests.get(url)    
    except requests.ConnectionError:
        print("connection error")

    data = None
    try:
        data = json.loads(response.text)
    except:
        print("unable to load json file")

    return data

def row_to_dict2(row):
    # import ipdb; ipdb.set_trace()
    d = dict(row)
    for key in d:
        item = d[key]

        if type(item) == datetime:
            d[key] = str(item)

    return d

# source: https://stackoverflow.com/questions/1958219/how-to-convert-sqlalchemy-row-object-to-a-python-dict
def row_to_dict(row):
    # import ipdb; ipdb.set_trace()
    # print(f"row_to_dict start: {row_to_dict}")
    d = {}
    for col in row.__table__.columns:
        # print(f"row_to_dict col: {col}")

        item = getattr(row, col.name)
        # print(f"row_to_dict item: {item}")

        if type(item) == datetime:
            # print(f"row_to_dict datetime")
            item = str(item)

        d[col.name] = item

    # import ipdb; ipdb.set_trace()
    # print(f"row_to_dict end: {row_to_dict}")
    return d


def row_to_json(row):
    return json.dumps(row_to_dict(row))


def dict_to_json(dict):
    return json.dumps(dict)


def dict_to_b64(dict):
    return b64encode(json.dumps(dict).encode('ascii'))


def row_to_b64(row):
    return b64encode(json.dumps(row_to_dict(row)).encode('ascii'))
