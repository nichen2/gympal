from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.validators import InputRequired


class UserForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), validators.Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired(), validators.Length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired(), validators.Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), validators.Length(max=30)])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), validators.Length(max=20)])
    password = PasswordField("Password", validators=[InputRequired()])
