from flask import Flask, render_template, redirect, session, flash, url_for
from models import db, connect_db, User, Feedback
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from forms import RegistrationForm, LoginForm, FeedbackForm

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

@app.route('/user/<username>', methods=["GET"])
def user_page(username):
  if "username" not in session or username != session['username']:
    raise Unauthorized()
  
  user = User.query.get(username)

  return render_template('user.html', user=user)


@app.route('/logout')
def logout():
  session.pop('username')
  return redirect('/register')

@app.route('/register', methods=["POST", "GET"])
def register():
  """Page to show registration form for site"""
  if 'username' in session: 
    return redirect(f'/user/{session['username']}')
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
    return redirect(f'/user/{username}')

  return render_template('register.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
  if "username" in session:
    return redirect(f"user/{session['username']}")
  form = LoginForm()

  if form.validate_on_submit():
    username = form.username.data
    password = form.password.data
    user = User.loginUser(username, password)
    if user:
      session['username'] = user.username
      return redirect(f'/user/{username}')
    else:
      flash('Invalid login information', 'danger')
      return render_template('login.html', form=form)
  
  return render_template('login.html', form=form)

@app.route('/user/<username>/delete')
def delete_user(username):
  user = User.query.get(username)
  session.pop('username')
  db.session.delete(user)
  db.session.commit()
  flash(f'{username} deleted!', 'danger')
  return redirect('/register')

@app.route('/user/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
  if 'username' in session and username != session['username']:
    raise Unauthorized()
  
  form = FeedbackForm()
  if form.validate_on_submit():
    title = form.title.data
    content = form.content.data
    feedback = Feedback(title=title, content=content, username=username)
    db.session.add(feedback)
    db.session.commit()
    return redirect(f'/user/{username}')

  return render_template('feedback.html', form=form)

@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def edit_feedback(feedback_id):
  feedback = Feedback.query.get(feedback_id)

  if 'username' in session and feedback.username != session['username']:
    raise Unauthorized()
  
  form = FeedbackForm(obj=feedback)
  if form.validate_on_submit():
    feedback.title = form.title.data
    feedback.content = form.content.data

    db.session.commit()

    return redirect(f'/user/{feedback.username}')
  
  return render_template('feedback-edit.html', form=form, feedback=feedback)

@app.route('/feedback/<feedback_id>/delete', methods=["GET", "POST"])
def delete_feedback(feedback_id):
  feedback = Feedback.query.get(feedback_id)
  db.session.delete(feedback)
  db.session.commit()
  flash('Deleted!', 'danger')
  return redirect(f'/user/{feedback.username}')