from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from datetime import datetime


def connect_db(app):
    db.app = app
    db.init_app(app)


class Any_Type_Group(db.Model):
    __tablename__ = 'any_type_groups'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(s) -> str:
        return f"<{s.__tablename__} #{s.id}, {s.name}>"


class Any_Type(db.Model):
    __tablename__ = 'any_types'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    any_type_id = db.Column(db.Integer, db.ForeignKey('any_type_groups.id'))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(s) -> str:
        return f"<{s.__tablename__} #{s.id}, {s.name} {s.any_type_id}>"

    group = db.relationship("Any_Type_Group", primaryjoin=("Any_Type_Group.id == Any_Type.any_type_id"), backref="types")


class Entity(db.Model):
    __tablename__ = "entities"

    @classmethod
    def signup(cls, username, email, password, entity_type_id=None):

        # import ipdb; ipdb.set_trace()

        hash = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = Entity(
            username=username,
            password=hash,
            email=email,
            entity_type_id=entity_type_id
        )

        user.is_authenticated = True
        return user

    @classmethod
    def authenticate(cls, username, password):
        # Find user with `username` and `password`.

        # This is a class method (call it on the class, not an individual user.)
        # It searches for a user whose password hash matches this password
        # and, if it finds such a user, returns that user object.

        # If can't find matching user (or if password is wrong), returns False.

        # import ipdb; ipdb.set_trace()

        user = cls.query.filter_by(username=username).first()

        if user:
            user.is_authenticated = bcrypt.check_password_hash(user.password, password)
            if user.is_authenticated:
                return user

        return None

    is_authenticated = False

    #
    # for database record keeping
    #
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(255))
    homepage_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    entity_type_id = db.Column(db.Integer, db.ForeignKey('any_types.id'))
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    entity_name = db.Column(db.String(20))
    phone = db.Column(db.String(16))
    location = db.Column(db.String(255))
    image_url = db.Column(db.String(255))
    about = db.Column(db.String(2000))
    to_delete = db.Column(db.Boolean, default=False)
    disabled = db.Column(db.Boolean, default=False)
    updated = db.Column(db.DateTime)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(s):
        return f"<{s.__tablename__} #{s.id}, {s.username}, {s.entity_name}, {s.entity_type_id}, {s.created}>"

    homepage = db.relationship("Post", primaryjoin=("Entity.homepage_id == Post.id"))

    events = db.relationship(
        "Post",
        secondary="participants",
        primaryjoin="Entity.id==Participant.participant_id",
        secondaryjoin="Post.id==Participant.event_id",
        backref="participants"
    )

    reacts = db.relationship(
        "Post",
        secondary="reacts",
        primaryjoin="Entity.id==React.user_id",
        secondaryjoin="Post.id==React.post_id",
        backref="interactions"
    )

    messages = db.relationship(
        "Post",
        secondary="messages",
        primaryjoin="Entity.id==Message.to_id",
        secondaryjoin="Post.id==Message.post_id",
        backref="recipients"
    )

    subscriptions = db.relationship(
        "Entity",
        secondary="subscriptions",
        primaryjoin="Entity.id==Subscription.subscriber_id",
        secondaryjoin="Entity.id==Subscription.publisher_id",
        backref="subscribers"
    )

    memberships = db.relationship(
        "Entity",
        secondary="memberships",
        primaryjoin="Entity.id==Membership.member_id",
        secondaryjoin="Entity.id==Membership.group_id",
        backref="members"
    )

    def is_subscribed(self, other_user):
        found_user_list = [user for user in self.subscriptions if user == other_user]
        return len(found_user_list) == 1


class User_Session(db.Model):
    __tablename__ = "user_sessions"

    @classmethod
    def establish(cls, user_id, user_ip, host_ip, requested_url):

        # import ipdb; ipdb.set_trace()

        hash_input = f'{user_id} {user_ip} {host_ip} {requested_url}'
        session_hash = bcrypt.generate_password_hash(hash_input).decode('UTF-8')

        user_session = User_Session(
            session_hash=session_hash,
            user_id=user_id,
            user_ip=user_ip,
            host_ip=host_ip,
            requested_url=requested_url
        )

        return user_session

    @classmethod
    def validate(cls, session_hash):

        # import ipdb; ipdb.set_trace()

        user_session = cls.query.filter_by(session_hash=session_hash).first()

        if user_session:
            user = Entity.query.filter(Entity.id==user_session.user_id).first()
            return (user, user_session)

        return None

    @classmethod
    def lookup(cls, user_id):

        # import ipdb; ipdb.set_trace()

        user_session = cls.query.filter(User_Session.user_id==user_id).order_by(desc(User_Session.id)).first()

        return user_session

    @classmethod
    def logout(cls, session_hash):

        # import ipdb; ipdb.set_trace()

        user_session = cls.query.filter(session_hash==session_hash).first()

        if user_session:
            user_session.logout_date = datetime.utcnow()
            db.session.commit()

            rows = cls.query.filter(User_Session.user_id == user_session.user_id, User_Session.logout_date != None).all()
            for row in rows:
                row.logout_date = datetime.utcnow()
                db.session.commit()

            return user_session

        return False

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_hash = db.Column(db.String(60), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('entities.id'))
    user_ip = db.Column(db.String(45))     #https://stackoverflow.com/questions/1076714/max-length-for-client-ip-address
    host_ip = db.Column(db.String(45))
    requested_url = db.Column(db.String(255))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    updated = db.Column(db.DateTime)
    logout_date = db.Column(db.DateTime)

    def __repr__(s):
        return f"<{s.__tablename__} #{s.id}, {s.session_hash}, {s.user_id}, {s.requested_url}, {s.created}, {s.updated}>"


class Membership(db.Model):
    __tablename__ = 'memberships'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer, db.ForeignKey('entities.id'))
    member_id = db.Column(db.Integer, db.ForeignKey('entities.id'))
    membership_type_id = db.Column(db.Integer, db.ForeignKey('any_types.id'))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(s):
        return f"<{s.__tablename__} #{s.id}, {s.group_id}, {s.member_id}, {s.membership_type_id}, {s.created}>"



class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subscriber_id = db.Column(db.Integer, db.ForeignKey('entities.id'))
    publisher_id = db.Column(db.Integer, db.ForeignKey('entities.id'))
    subscription_type_id = db.Column(db.Integer, db.ForeignKey('any_types.id'))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(s):
        return f"<{s.__tablename__} #{s.id}, {s.subscriber_id}, {s.publisher_id}, {s.created}>"


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(2000))
    post_type_id = db.Column(db.Integer, db.ForeignKey('any_types.id'))
    privacy_type_id = db.Column(db.Integer, db.ForeignKey('any_types.id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('entities.id'), nullable=False)
    editor_id = db.Column(db.Integer, db.ForeignKey('entities.id'))
    edited = db.Column(db.DateTime)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    link_url = db.Column(db.String(255))

    #search
    search_term = db.Column(db.String(255))
    source = db.Column(db.String(255))

    #event
    event_date = db.Column(db.DateTime)
    location = db.Column(db.String(255))
    contact = db.Column(db.String(255))

    #recipe
    other_id = db.Column(db.Integer)
    sort = db.Column(db.Integer)
    image_url = db.Column(db.String(255))

    def __repr__(s):
        return f"<{s.__tablename__} #{s.id}, {s.creator_id}, {s.title}, {s.post_type_id}, {s.created}>"

    recipes = db.relationship(
        "Post",
        secondary="recipe_searches",
        primaryjoin="Post.id==Recipe_Search.search_id",
        secondaryjoin="Post.id==Recipe_Search.recipe_id",
        backref="search"
    )

    tasks = db.relationship(
        "Post",
        secondary="recipe_tasks",
        primaryjoin="Post.id==Recipe_Task.recipe_id",
        secondaryjoin="Post.id==Recipe_Task.task_id",
    )

    ingredients = db.relationship(
        "Post",
        secondary="recipe_ingredients",
        primaryjoin="Post.id==Recipe_Ingredient.task_id",
        secondaryjoin="Post.id==Recipe_Ingredient.ingredient_id",
    )

    tools = db.relationship(
        "Post",
        secondary="recipe_tools",
        primaryjoin="Post.id==Recipe_Tool.task_id",
        secondaryjoin="Post.id==Recipe_Tool.tool_id",
    )


class React(db.Model):
    __tablename__ = 'reacts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('entities.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    react_type_id = db.Column(db.Integer, db.ForeignKey('any_types.id'))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(s):
        return f"<{s.__tablename__} #{s.id}, {s.user_id}, {s.post_id}, {s.react_type_id}, {s.created}>"


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    
    from_id = db.Column(db.Integer, db.ForeignKey('entities.id'), nullable=False)
    to_id = db.Column(db.Integer, db.ForeignKey('entities.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    replyto_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    repost_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    sent_date = db.Column(db.DateTime)
    read_date = db.Column(db.DateTime)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(s):
        return f"<{s.__tablename__} #{s.id}, {s.from_id}, {s.to_id}, {s.post_id}, {s.created}>"


class Recipe_Search(db.Model):
    __tablename__ = "recipe_searches"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    search_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(s):
        return f"<{s.__tablename__} #{s.id}, {s.recipe_id}, {s.search_id}, {s.created}>"


class Recipe_Task(db.Model):
    __tablename__ = "recipe_tasks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(s):
        return f"<{s.__tablename__} #{s.id}, {s.recipe_id}, {s.task_id}, {s.created}>"


class Recipe_Ingredient(db.Model):
    __tablename__ = "recipe_ingredients"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(s):
        return f"<{s.__tablename__} #{s.id}, {s.task_id}, {s.ingredient_id}, {s.created}>"


class Recipe_Tool(db.Model):
    __tablename__ = "recipe_tools"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    tool_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(s):
        return f"<{s.__tablename__} #{s.id}, {s.task_id}, {s.tool_id}, {s.created}>"


class Participant(db.Model):
    __tablename__ = "participants"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    event_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey('entities.id'), nullable=False)
    participant_type_id = db.Column(db.Integer, db.ForeignKey('any_types.id'))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(s):
        return f"<{s.__tablename__} #{s.id}, {s.event_id}, {s.participant_id}, {s.created}>"


class Signup_Recipe(db.Model):
    __tablename__ = "signup_recipes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    assignedto_id = db.Column(db.Integer, db.ForeignKey('entities.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    due_date = db.Column(db.DateTime)
    done_date = db.Column(db.DateTime)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(s):
        return f"<{s.__tablename__} #{s.id}, {s.event_id}, {s.assignedto_id}, {s.recipe_id}, {s.created}>"


class Signup_Ingredient(db.Model):
    __tablename__ = "signup_ingredients"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    assignedto_id = db.Column(db.Integer, db.ForeignKey('entities.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    due_date = db.Column(db.DateTime)
    done_date = db.Column(db.DateTime)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(s):
        return f"<{s.__tablename__} #{s.id}, {s.event_id}, {s.assignedto_id}, {s.ingredient_id}, {s.created}>"


class Signup_Tool(db.Model):
    __tablename__ = "signup_tools"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    assignedto_id = db.Column(db.Integer, db.ForeignKey('entities.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    tool_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    due_date = db.Column(db.DateTime)
    done_date = db.Column(db.DateTime)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(s):
        return f"<{s.__tablename__} #{s.id}, {s.event_id}, {s.assignedto_id}, {s.tool_id}, {s.created}>"
