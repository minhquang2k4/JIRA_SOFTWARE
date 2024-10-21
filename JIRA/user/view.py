from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

from JIRA.routers import login_required
from JIRA.models import User, Project
from JIRA import db

user_blueprint = Blueprint('users', __name__, template_folder='templates', static_folder='static')

@user_blueprint.route('/')
@login_required
def user():
  users = User.query.all()
  projects = Project.query.filter(Project.manager_id == current_user.id).all()
  return render_template('user_list.html', users=users, projects=projects)