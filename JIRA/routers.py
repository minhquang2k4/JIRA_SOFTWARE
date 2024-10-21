from flask import render_template, flash, session, redirect, url_for
from flask_login import current_user
from functools import wraps

from JIRA import app
from JIRA.models import *


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
def home(project_id=None, task_list=None, task_id=None):
  projects = Project.query.filter(Project.manager_id == current_user.id).all()

  return render_template('home.html', projects=projects)