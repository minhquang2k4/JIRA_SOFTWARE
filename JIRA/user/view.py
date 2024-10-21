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

@user_blueprint.route('/<int:user_id>', methods=['POST', 'GET'])
def user_by_id(user_id):

  if not current_user.is_authenticated:
    return redirect(url_for('auth.login'))
  user = db.get_or_404(User, ident=user_id)

  projects = Project.query.filter(Project.manager_id == current_user.id).all()
  return render_template('user_detail.html', user=user, projects=projects)