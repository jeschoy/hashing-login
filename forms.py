from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField, EmailField, PasswordField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional