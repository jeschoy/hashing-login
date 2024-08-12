from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, EmailField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional

class RegistrationForm(FlaskForm):
  """User registration form"""
  username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
  password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=60)])
  email = EmailField("Email", validators=[InputRequired(), Length(max=50)])
  first_name = StringField("First name", validators=[InputRequired(), Length(max=30)])
  last_name = StringField("Last name", validators=[InputRequired(), Length(max=30)])

class LoginForm(FlaskForm):
  """User login form"""
  username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
  password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=60)])

class FeedbackForm(FlaskForm):
  """Feedback form"""
  title = StringField("Title", validators=[InputRequired(), Length(max=100)])
  content = StringField('Content', validators=[InputRequired()])