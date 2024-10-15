from flask import render_template, flash, session, redirect, url_for
from functools import wraps

from JIRA import app


# def login_required(f):
#   @wraps(f)
#   def decorated_function(*args, **kwargs):
#     if not current_user.is_authenticated:
#       return redirect(url_for('login'))
#     return f(*args, **kwargs)
#   return decorated_function

@app.route('/')
def home():
  return render_template('index.html')