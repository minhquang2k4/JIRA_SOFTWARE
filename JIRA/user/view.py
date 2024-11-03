from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user

from JIRA.routers import login_required
from JIRA.models import User, Project
from JIRA import db

from JIRA.user.forms import UserForm, UpdateUserForm

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

@user_blueprint.route('/<int:id>/edit', methods=['POST', 'GET'])
def edit_user(id):
  if not current_user.is_authenticated:
    return redirect(url_for('auth.login'))
  user = db.get_or_404(User, ident=id)
  form = UpdateUserForm(obj=user)

  if form.validate_on_submit():
    print(form.data)
    try:
      user.name = form.name.data
      user.username = form.username.data
      user.email = form.email.data

      db.session.commit()
      return redirect(url_for('users.user'))
    except Exception as e:
      print(e)
      db.session.rollback()
  
  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f'There was an error with creating a user: {err_msg}', category='danger')
  projects = Project.query.filter(Project.manager_id == current_user.id).all()
  return render_template('user_edit.html', form=form, user=user, projects=projects)

@user_blueprint.route('/new', methods=['POST', 'GET'])
def new_user():
  if not current_user.is_authenticated:
    return redirect(url_for('auth.login'))
  form = UserForm()
  if form.validate_on_submit():
    try:
      user = User(name=form.name.data, username=form.username.data, password=form.password.data,
                 email=form.email.data, is_admin=form.is_admin.data)
      print(user)
      db.session.add(user)
      db.session.commit()
      return redirect(url_for('users.user'))
    except Exception as e:
      print(e)
      db.session.rollback()
  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f'There was an error with creating a user: {err_msg}', category='danger')
  projects = Project.query.filter(Project.manager_id == current_user.id).all()
  return render_template('user_new.html', form=form, projects=projects)