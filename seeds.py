from traceback import print_list
from flask import Flask
app = Flask(__name__)

from data.models import db, connect_db, Any_Type_Group, Any_Type, Entity, User_Session, Membership, Subscription, Post, React, Message, Participant, Recipe_Search, Recipe_Task, Recipe_Ingredient, Recipe_Tool, Signup_Recipe, Signup_Ingredient, Signup_Tool

from config import config_app
config_app(app)
connect_db(app)

from random import randrange
import json
from core.data import get_any_type_value

# drop all tables so that they could be rebuilt
import sqlalchemy
from sqlalchemy import and_

file = open('data/drop_tables.sql')
escaped_sql = sqlalchemy.text(file.read())
db.engine.execute(escaped_sql)

db.create_all()

t = entity_type = Any_Type_Group(name="entity_type"); db.session.add(t); db.session.commit()
t = post_type = Any_Type_Group(name="post_type"); db.session.add(t); db.session.commit()
t = participant_type = Any_Type_Group(name="participant_type"); db.session.add(t); db.session.commit()
t = membership_type = Any_Type_Group(name="membership_type"); db.session.add(t); db.session.commit()
t = subscription_type = Any_Type_Group(name="subscription_type"); db.session.add(t); db.session.commit()
t = react_type = Any_Type_Group(name="react_type"); db.session.add(t); db.session.commit()
t = privacy_type = Any_Type_Group(name="privacy_type"); db.session.add(t); db.session.commit()

t = e_user = Any_Type(name="user", any_type_id=entity_type.id); db.session.add(t); db.session.commit()
t = e_group = Any_Type(name="group", any_type_id=entity_type.id); db.session.add(t); db.session.commit()

t = pp_personal = Any_Type(name="personal", any_type_id=privacy_type.id); db.session.add(t); db.session.commit()
t = pp_friends = Any_Type(name="friends", any_type_id=privacy_type.id); db.session.add(t); db.session.commit()
t = pp_members = Any_Type(name="members", any_type_id=privacy_type.id); db.session.add(t); db.session.commit()
t = public_privacy_type = Any_Type(name="public", any_type_id=privacy_type.id); db.session.add(t); db.session.commit()

t = p_comment = Any_Type(name="comment", any_type_id=post_type.id); db.session.add(t); db.session.commit()
t = event_post_type = Any_Type(name="event", any_type_id=post_type.id); db.session.add(t); db.session.commit()
t = ingredient_post_type = Any_Type(name="ingredient", any_type_id=post_type.id); db.session.add(t); db.session.commit()
t = p_message = Any_Type(name="message", any_type_id=post_type.id); db.session.add(t); db.session.commit()
t = post_post_type = Any_Type(name="post", any_type_id=post_type.id); db.session.add(t); db.session.commit()
t = page_post_type = Any_Type(name="page", any_type_id=post_type.id); db.session.add(t); db.session.commit()
t = p_react = Any_Type(name="react", any_type_id=post_type.id); db.session.add(t); db.session.commit()
t = recipe_post_type = Any_Type(name="recipe", any_type_id=post_type.id); db.session.add(t); db.session.commit()
t = p_replyto = Any_Type(name="replyto", any_type_id=post_type.id); db.session.add(t); db.session.commit()
t = p_repost = Any_Type(name="repost", any_type_id=post_type.id); db.session.add(t); db.session.commit()
t = search_post_type = Any_Type(name="search", any_type_id=post_type.id); db.session.add(t); db.session.commit()
t = task_post_type = Any_Type(name="task", any_type_id=post_type.id); db.session.add(t); db.session.commit()
t = tool_post_type = Any_Type(name="tool", any_type_id=post_type.id); db.session.add(t); db.session.commit()

t = participant_organizer_type = Any_Type(name="participant", any_type_id=participant_type.id); db.session.add(t); db.session.commit()
t = organizer_participant_type = Any_Type(name="organizer", any_type_id=participant_type.id); db.session.add(t); db.session.commit()
t = to_donor = Any_Type(name="donor", any_type_id=participant_type.id); db.session.add(t); db.session.commit()
t = to_volunteer = Any_Type(name="volunteer", any_type_id=participant_type.id); db.session.add(t); db.session.commit()
t = to_mentor = Any_Type(name="mentor", any_type_id=participant_type.id); db.session.add(t); db.session.commit()
t = to_judge = Any_Type(name="judge", any_type_id=participant_type.id); db.session.add(t); db.session.commit()

t = member_membership_type = Any_Type(name="member", any_type_id=membership_type.id); db.session.add(t); db.session.commit()
t = admin_membership_type = Any_Type(name="admin", any_type_id=membership_type.id); db.session.add(t); db.session.commit()
t = owner_membership_type = Any_Type(name="owner", any_type_id=membership_type.id); db.session.add(t); db.session.commit()

t = trial_subscriber_type = Any_Type(name="trial", any_type_id=subscription_type.id); db.session.add(t); db.session.commit()
t = regular_subscriber_type = Any_Type(name="regular", any_type_id=subscription_type.id); db.session.add(t); db.session.commit()
t = premium_subscriber_type = Any_Type(name="premium", any_type_id=subscription_type.id); db.session.add(t); db.session.commit()

t = like_react_type = Any_Type(name="like", any_type_id=react_type.id); db.session.add(t); db.session.commit()
t = tr_dislike= Any_Type(name="dislike", any_type_id=react_type.id); db.session.add(t); db.session.commit()
t = tr_heart = Any_Type(name="heart", any_type_id=react_type.id); db.session.add(t); db.session.commit()
t = tr_care = Any_Type(name="care", any_type_id=react_type.id); db.session.add(t); db.session.commit()
t = tr_lol = Any_Type(name="lol", any_type_id=react_type.id); db.session.add(t); db.session.commit()
t = tr_sad = Any_Type(name="sad", any_type_id=react_type.id); db.session.add(t); db.session.commit()
t = tr_angry = Any_Type(name="angry", any_type_id=react_type.id); db.session.add(t); db.session.commit()
t = tr_thoughtful = Any_Type(name="thoughtful", any_type_id=react_type.id); db.session.add(t); db.session.commit()


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# load users
#

u1 = ["yu", "yuki", "brendan", "rich", "rose", "michelle", "hugo"]
u2 = []
for name in u1:
    t = Entity.signup(username=name, email=f"{name}@pfix.org", password="123456", entity_type_id=e_user.id)
    u2.append(t)
    db.session.add(t); db.session.commit()


#
# load groups
#

g1 = ["Hollywood", "Cully"]
g2 = []
for name in g1:
    t = Entity.signup(username=name, email=f"{name}@pfix.org", password="123456", entity_type_id=e_group.id)
    g2.append(t)
    db.session.add(t); db.session.commit()


#
# load user_sessions
#

log2 = []
for user in u2:
    t = User_Session.establish(user_id=user.id, user_ip="127.0.0.1", host_ip="127.0.0.1", requested_url="http://127.0.0.1:5000/login")
    log2.append(t)
    db.session.add(t); db.session.commit()


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# load memberships
#

m2 = []
for u in u2:
    for g in g2:
        if u.id == 1:
            t = Membership(group_id=g.id, member_id=u.id, membership_type_id=owner_membership_type.id); 
        elif u.id == 2:
            t = Membership(group_id=g.id, member_id=u.id, membership_type_id=admin_membership_type.id); 
        else:
            t = Membership(group_id=g.id, member_id=u.id, membership_type_id=member_membership_type.id); 

        m2.append(t)
        db.session.add(t); db.session.commit()

#
# load subscriptions
#

s2 = []
for u in u2:
    for g in g2:
        if u.id == 1:
            t = Subscription(publisher_id=g.id, subscriber_id=u.id, subscription_type_id=premium_subscriber_type.id); 
        elif u.id == 2:
            t = Subscription(publisher_id=g.id, subscriber_id=u.id, subscription_type_id=trial_subscriber_type.id); 
        else:
            t = Subscription(publisher_id=g.id, subscriber_id=u.id, subscription_type_id=regular_subscriber_type.id); 
        s2.append(t)
        db.session.add(t); db.session.commit()


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# load user home pages
#

for u in u2:
    t = Post(creator_id=u.id, title=f"about {u.username}", post_type_id=page_post_type.id)
    db.session.add(t)
    db.session.commit()
    u.post_id = t.id
    db.session.commit()
    t.page_id = t.id
    db.session.commit()


#
# load group home pages
#

for u in g2:
    t = Post(creator_id=u.id, title=f"about {u.username}", post_type_id=page_post_type.id)
    db.session.add(t)
    db.session.commit()
    u.post_id = t.id
    db.session.commit()
    t.page_id = t.id
    db.session.commit()

for u in u2:
    for i in range(randrange(4, 12)):
        t = Post(creator_id=u.id, title=f"post #{i+1} by {u.username}", post_type_id=post_post_type.id)
        db.session.add(t); db.session.commit()


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# load messages
#

p2 = []
for u in u2:
    for i in range(randrange(4, 12)):
        p = Post(creator_id=u.id, title=f"message #{i+1} by {u.username}", post_type_id=post_post_type.id)
        p2.append(p)
        db.session.add(p); db.session.commit()

        to_id = to_id=randrange(1,len(u1))

        if u.id != to_id:
            t = Message(from_id=u.id, to_id=to_id, post_id=p.id)
            db.session.add(t); db.session.commit()
        else:
            to_id = to_id=randrange(1,len(u1))

            if u.id != to_id:
                t = Message(from_id=u.id, to_id=to_id, post_id=p.id)
                db.session.add(t); db.session.commit()

#
# load reacts
#

for u in u2:
    for p in p2:
        t = React(user_id=u.id, post_id=p.id, react_type_id=(randrange(8)+like_react_type.id))
        db.session.add(t); db.session.commit()


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# load search function
#
# event_post_type = get_any_type_value("event")
# task_post_type = get_any_type_value("task")
# public_privacy_type = get_any_type_value("public")
# ingredient_post_type = get_any_type_value("ingredient")
# tool_post_type = get_any_type_value("tool")

def load_search(filename, title, user):
    with open(filename, 'r') as f:
        data = json.load(f)
    f.close()

    s = Post(creator_id=user.id, title=title, post_type_id=search_post_type.id)
    db.session.add(s); db.session.commit()

    for item in data['results']:
        r = Post(post_type_id=recipe_post_type.id, creator_id=user.id, title=item["title"], other_id=item["id"], image_url=item["image"])
        db.session.add(r); db.session.commit()

        t = Recipe_Search(search_id=s.id, recipe_id=r.id)
        db.session.add(t); db.session.commit()


def load_recipe(filename, other_id, user):
    recipe = Post.query.filter(and_(Post.other_id==other_id, Post.post_type_id==recipe_post_type.id)).first()
    if not recipe:
        return

    with open(filename, 'r') as f:
        data = json.load(f)
    f.close()

    # import ipdb; ipdb.set_trace()
    recipe.content = data["instructions"]
    recipe.privacy_type_id=public_privacy_type.id
    db.session.commit()

    # import ipdb; ipdb.set_trace()
    for item in data['analyzedInstructions'][0]['steps']:
        r = Post(post_type_id=task_post_type.id, creator_id=user.id, title=f"step {item['number']}", content=item["step"], sort=item["number"], other_id=recipe.other_id, privacy_type_id=public_privacy_type.id)

        db.session.add(r); db.session.commit()
        t = Recipe_Task(recipe_id=recipe.id, task_id=r.id)
        db.session.add(t); db.session.commit()

        # import ipdb; ipdb.set_trace()

        for ingred in item["ingredients"]:
            r1 = Post.query.filter(and_(Post.other_id==ingred["id"], Post.post_type_id==ingredient_post_type.id)).first()
            if not r1:
                r1 = Post(post_type_id=ingredient_post_type.id, creator_id=user.id, title=ingred["name"], other_id=ingred["id"])
                db.session.add(r1); db.session.commit()
            ti = Recipe_Ingredient(recipe_id=recipe.id, task_id=r.id, ingredient_id=r1.id)
            db.session.add(ti); db.session.commit()

        for equip in item["equipment"]:
            r1 = Post.query.filter(and_(Post.other_id==equip["id"], Post.post_type_id==tool_post_type.id)).first()
            if not r1:
                r1 = Post(post_type_id=tool_post_type.id, creator_id=user.id, title=equip["name"], other_id=equip["id"])
                db.session.add(r1); db.session.commit()
            ti = Recipe_Tool(recipe_id=recipe.id, task_id=r.id, tool_id=r1.id)
            db.session.add(ti); db.session.commit()

    return recipe

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# load pasta search
#

load_search('modules/recipes/data/search_pasta.json', "pasta recipe search", u2[0])
r_pasta = load_recipe('modules/recipes/data/pasta_recipe.json', 654928, u2[0])
s = evt_pasta_party = Post(creator_id=u2[0].id, title=f"pasta party at {u2[0].username}'s house", post_type_id=event_post_type.id, privacy_type_id=public_privacy_type.id); db.session.add(s); db.session.commit()

for u in u2:
    if u.id == u2[0].id:
        t = Participant(event_id=s.id, participant_id=u.id, participant_type_id=organizer_participant_type.id)
    else:
        t = Participant(event_id=s.id, participant_id=u.id, participant_type_id=participant_organizer_type.id)
    db.session.add(t); db.session.commit()


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# load pancake search
#

load_search('modules/recipes/data/search_pancake.json', "pancake recipe search", u2[0])
r_pancake = r_pasta = load_recipe('modules/recipes/data/pancake_recipe.json', 324694, u2[0])
s = evt_pancake_party = Post(creator_id=u2[0].id, title=f"pancake party at {u2[1].username}'s house", post_type_id=event_post_type.id, privacy_type_id=public_privacy_type.id); db.session.add(s); db.session.commit()

for u in u2:
    if u.id == u2[1].id:
        t = Participant(event_id=s.id, participant_id=u.id, participant_type_id=organizer_participant_type.id)
    else:
        t = Participant(event_id=s.id, participant_id=u.id, participant_type_id=participant_organizer_type.id)
    db.session.add(t); db.session.commit()


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# load burger search
#

load_search('modules/recipes/data/search_burger.json', "burger recipe search", u2[0])
r_burger = load_recipe('modules/recipes/data/burger_recipe.json', 637631, u2[0])
s = evt_burger_party = Post(creator_id=u2[0].id, title=f"burger party at {u2[0].username}'s house", post_type_id=event_post_type.id, privacy_type_id=public_privacy_type.id); db.session.add(s); db.session.commit()


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# load pho search
#

load_search('modules/recipes/data/search_pho.json', "pho recipe search", u2[0])
r_pho = load_recipe('modules/recipes/data/pho_recipe.json', 1096211, u2[0])


# --------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# load burrito search
#

load_search('modules/recipes/data/search_burrito.json', "burrito recipe search", u2[0])
r_burrito = load_recipe('modules/recipes/data/burrito_recipe.json', 637631, u2[0])
r_burrito2 = load_recipe('modules/recipes/data/burrito_recipe2.json', 1096058, u2[0])



# --------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# signup recipe
#

t = Signup_Recipe(event_id=s.id, assignedto_id=u2[randrange(1, 7)].id, recipe_id=r_pancake.id)
db.session.add(t); db.session.commit()

t = Signup_Recipe(event_id=s.id, assignedto_id=u2[randrange(1, 7)].id, recipe_id=r_pasta.id)
db.session.add(t); db.session.commit()


#
# signup pancake ingredients
#

for task in r_pancake.tasks:
    for ingred in task.ingredients:
        u = u2[randrange(1, 7)]
        t = Signup_Ingredient(event_id=s.id, assignedto_id=u.id, recipe_id=r_pancake.id, ingredient_id=ingred.id)
        db.session.add(t); db.session.commit()


#
# signup pancake tools
#

for task in r_pancake.tasks:
    for tool in task.tools:
        u = u2[randrange(1, 7)]
        t = Signup_Tool(event_id=s.id, assignedto_id=u.id, recipe_id=r_pancake.id, tool_id=tool.id)
        db.session.add(t); db.session.commit()


#
# signup pasta ingredients
#

for task in r_pasta.tasks:
    for ingred in task.ingredients:
        u = u2[randrange(1, 7)]
        t = Signup_Ingredient(event_id=s.id, assignedto_id=u.id, recipe_id=r_pasta.id, ingredient_id=r_pasta.id)
        db.session.add(t); db.session.commit()


#
# signup pasta tools
#

for task in r_pasta.tasks:
    for tool in task.tools:
        u = u2[randrange(1, 7)]
        t = Signup_Tool(event_id=s.id, assignedto_id=u.id, recipe_id=r_pasta.id, tool_id=tool.id)
        db.session.add(t); db.session.commit()

"""
print(f"{key} : " + t3[key][0].toJSON())
for key in t3.keys():
    print("############################################################")
    print(f"#### {key}")
    print("############################################################")
    for s in t3[key]:
        print(s)
"""
