from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional

from JIRA.models import User

class RegistrationForm(FlaskForm):
  def validate_username(self, username_to_check):
    user = User.query.filter_by(username=username_to_check.data).first()
    if user:
      raise ValidationError('Username already exists! Please try a different username.')

  def validate_email(self, email_to_check):
    email = User.query.filter_by(email=email_to_check.data).first()
    if email:
      raise ValidationError('Email already exists! Please try a different email.')

  name = StringField('Name')
  username = StringField('Username', validators=[DataRequired()])
  password1 = PasswordField('Password', validators=[DataRequired(), EqualTo('password2')])
  password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password1')])
  email = StringField('Email', validators=[Optional(), Email()])
  submit = SubmitField('Create Account')

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Login')
