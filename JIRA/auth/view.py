from flask import Blueprint, render_template, request, flash, redirect, url_for
from JIRA.auth.forms import LoginForm, RegistrationForm

from JIRA.models import User
from JIRA import db

auth_blueprint = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  return render_template('login.html', form=form)


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(
      name = form.name.data,
      username = form.username.data,
      email = form.email.data,
      password = form.password1.data
    )
    print(form.name.data)
    print(form.username.data)
    print(form.email.data)
    print(form.password1.data)
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