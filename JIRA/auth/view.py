from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user
from functools import wraps

from JIRA.auth.forms import LoginForm, RegistrationForm
from JIRA.models import User
from JIRA import db

auth_blueprint = Blueprint('auth', __name__, template_folder='templates', static_folder='static')
def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if not current_user.is_authenticated:
      return redirect(url_for('login'))
    return f(*args, **kwargs)

  return decorated_function




@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    attempted_user = User.query.filter_by(username=form.username.data).first()
    if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
      login_user(attempted_user)  # Lưu thông tin user vào session
      return redirect(url_for('home'))

  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f'There was an error with creating a user: {err_msg}', category='danger')
  return render_template('login.html', form=form)


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User (
      name = form.name.data,
      username = form.username.data,
      email = form.email.data,
      password = form.password1.data
    )
    try:
      db.session.add(user)
      db.session.commit()
      return redirect(url_for('auth.login'))
    except Exception as e:
      print(e)
      db.session.rollback()
  
  # flash là một hàm giúp hiển thị thông báo cho người dùng 
  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f'There was an error with creating a user: {err_msg}', category='danger')
  return render_template('register.html', form=form)

@auth_blueprint.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))