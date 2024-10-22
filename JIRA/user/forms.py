from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Optional, Email


class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    active = BooleanField('Active')
    phone = StringField('Phone')
    email = StringField('Email', validators=[Optional(), Email()])
    is_admin = BooleanField('Admin')
    submit = SubmitField('Create User')

class UpdateUserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    active = BooleanField('Active')
    phone = StringField('Phone')
    email = StringField('Email', validators=[Optional(), Email()])
    is_admin = BooleanField('Admin')
    submit = SubmitField('Update User')