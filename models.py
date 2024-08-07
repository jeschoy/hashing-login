from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
  """Connect database to Flask app"""

  db.app = app
  db.init_app(app)

class User(db.Model):
  """User model to store user information"""
  __tablename__ = 'users'

  username = db.Column(db.String(20), primary_key=True, unique=True, nullable=False)
  password = db.Column(db.Text, nullable=False)
  email = db.Column(db.String(50), nullable=False)
  first_name = db.Column(db.String(30), nullable=False)
  last_name = db.Column(db.String(30), nullable=False)
  
