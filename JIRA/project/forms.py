from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# from JIRA.models import User


class ProjectForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  description = StringField('Description')
  submit = SubmitField('Save')
