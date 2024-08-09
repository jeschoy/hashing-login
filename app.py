from flask import Flask, render_template, redirect, session, flash, url_for
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hashing-login'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'shhhthisisasecret'
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension()

app.app_context().push()
connect_db(app)

@app.route('/')
def root():
  return redirect(url_for('register'))

@app.route('/secret', methods=["GET"])
def secret():
  return render_template('secret.html')

@app.route('/logout')
def logout():
  session.pop('username')
  return redirect('/register')

@app.route('/register', methods=["POST", "GET"])
def register():
  """Page to show registration form for site"""
  if 'username' in session: 
    return redirect('/secret')
  form = RegistrationForm()

  if form.validate_on_submit():
    username = form.username.data
    password = form.password.data
    email = form.email.data
    first_name = form.first_name.data
    last_name = form.last_name.data
    
    user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
    db.session.add(user)
    db.session.commit()
    session['username'] = user.username
    return redirect('/secret')

  return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
  form = LoginForm()

  if form.validate_on_submit():
    username = form.username.data
    password = form.password.data
    user = User.loginUser(username, password)
    if user:
      session['username'] = user.username
      return redirect('/secret')
    else:
      form.username.errors = ["Invalid login information"]
      return render_template('/login', form=form)
  
  return render_template('login.html', form=form)