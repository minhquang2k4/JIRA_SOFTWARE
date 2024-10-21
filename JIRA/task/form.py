from datetime import datetime

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, DateTimeField
from wtforms.validators import DataRequired

from JIRA.models import Project


class TaskForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  description = StringField('Description')
  priority = StringField('Priority', default='low')
  date_start = DateTimeField('Start Date', format='%d/%m/%Y', default=datetime.now())
  date_end = DateTimeField('End Date', format='%d/%m/%Y', default=datetime.now())
  status = SelectField('Status', coerce=str)
  project_id = SelectField('Project', coerce=int)
  submit = SubmitField('Submit')

  def __init__(self, *args, **kwargs):
    super(TaskForm, self).__init__(*args, **kwargs)
    self.project_id.choices = [(project.id, project.name) for project in
                                Project.query.filter_by(active=True, manager_id=current_user.id).all()]
    self.status.choices = [('todo', 'To Do'), ('in-progress', 'In Progress'), ('done', 'Done')]

  def validate(self, extra_validators=None):
    # Validate the date_start and date_end
    start_date = self.date_start._value()
    end_date = self.date_end._value()
    if start_date > end_date:
      self.date_start.errors.append('Start date must be earlier than end date')
      return False
    return super(TaskForm, self).validate(extra_validators)
