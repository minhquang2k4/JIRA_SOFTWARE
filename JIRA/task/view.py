from flask import Blueprint, session, render_template, flash
from flask_login import current_user

from JIRA.routers import home, login_required
from JIRA.task.form import TaskForm
from JIRA.models import Task, Project
from JIRA import db

task_blueprint = Blueprint('tasks', __name__, template_folder='templates', static_folder='static')

def get_task_list(tasks):
  task_list = {
    'todo': [task for task in tasks if task.status == 'todo'],
    'in-progress': [task for task in tasks if task.status == 'in-progress'],
    'done': [task for task in tasks if task.status == 'done']
  }
  return task_list

@task_blueprint.route('/')
@login_required
def tasks():
  session.pop('active_task_id', None)
  session.pop('mode', None)
  session.pop('active_project_id', None)
  all_task = Task.query.filter(Task.user_id == current_user.id).all()
  task_list = get_task_list(all_task)

  return home(task_list=task_list)

@task_blueprint.route('/new', methods=['POST', 'GET'])
@login_required
def task_new():
  form = TaskForm()
  if form.validate_on_submit():
    task = Task(name=form.name.data, description=form.description.data,
                priority=form.priority.data, status=form.status.data,
                project_id=form.project_id.data, date_start=form.date_start.data,
                date_end=form.date_end.data, user_id=current_user.id)
    db.session.add(task)
    db.session.commit()
    return home(project_id=form.project_id.data)
  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f'There was an error with creating a task: {err_msg}', category='danger')


  projects = Project.query.filter(Project.manager_id == current_user.id).all()
  return render_template('task_new.html', form=form, projects=projects)

@task_blueprint.route('/<int:task_id>', methods=['GET'])
@login_required
def task_by_id(task_id):
  task = Task.query.get(task_id)

  projects = Project.query.filter(Project.manager_id == current_user.id).all()
  return render_template('task_detail.html', task=task, projects=projects)