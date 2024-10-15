from flask import render_template, flash, session, redirect, url_for
from flask_login import current_user
from functools import wraps

from JIRA import app


def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if not current_user.is_authenticated:
      return redirect(url_for('auth.login'))
    return f(*args, **kwargs)
  return decorated_function

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/home')
@login_required
def home():
  return render_template('home.html')