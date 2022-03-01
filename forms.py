"""Forms for playlist app."""

from wtforms import StringField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    """Form for adding playlists."""

    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])


class EventForm(FlaskForm):
    """Form for adding songs."""

    title = StringField('Title', validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])


