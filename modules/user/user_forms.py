from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, DateField, IntegerField, TextAreaField
from wtforms.validators import InputRequired, Length, Optional, Email, DataRequired, URL, ValidationError

class RegisterUser(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=55)])
    email = StringField("Email", validators=[InputRequired(), Email(), Length(min=0, max=50)])

class LoginUser(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=55)])


class EditUser(FlaskForm):
    username = StringField("Username")#, validators=[InputRequired(), Length(min=2, max=20)])
    password = PasswordField("Password")#, validators=[InputRequired(), Length(min=6, max=60)])
    email = StringField("Email")#, validators=[InputRequired(), Email(), Length(min=0, max=255)])
    first_name = StringField("First Name")#, validators=[InputRequired(), Length(min=0, max=45)])
    last_name = StringField("Last Name")#, validators=[InputRequired(), Length(min=0, max=45)])
    phone = TextAreaField('(Optional) Phone')#, validators=[Optional(), Length(min=0, max=16)])
    location = TextAreaField('(Optional) Address')#, validators=[Optional(), Length(min=0, max=255)])
    image_url = StringField('(Optional) Image URL')#, validators=[Optional(), Length(min=0, max=255)])
    about = TextAreaField('(Optional) Tell us about yourself')#, validators=[Optional(), Length(min=0, max=2000)])
