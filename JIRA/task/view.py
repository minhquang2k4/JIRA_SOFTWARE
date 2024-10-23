from flask import Blueprint, session, render_template, flash, request, jsonify
from datetime import datetime
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
  return home(task_id=task)

@task_blueprint.route('/<int:task_id>/edit', methods=['POST', 'GET', 'PUT'])
@login_required
def edit_task(task_id):
  if request.method=="PUT":
    data=request.get_json()
    task_id=data.get('taskId')
    new_status=data.get('newState')

    task= Task.query.get(task_id)
    if task:
      task.status=new_status
      db.session.commit()
      return jsonify({'message': 'Task status updated successfully!'})
    else:
      return jsonify({'message': 'Task not found!'})
  elif request.method=="POST":
    session['active_task_id'] = task_id
    session['mode'] = 'edit'
    return home()
  else:
    session.pop('mode',None)
    return home()

def is_changed(task=None,data=None):
  if task.name!=data.get('name') or task.description!=data.get('description') or task.priority!=data.get('priority') or task.status!=data.get('status') or task.project_id!=data.get('project_id') or task.date_start!=data.get('date_start') or task.date_end!=data.get('date_end'):
    return True
  return False

@task_blueprint.route('/<int:task_id>/save', methods=['POST'])
@login_required
def save_task(task_id):
  session.pop('mode', None)
  data=request.get_json()
  data.update({
    'date_start': datetime.strptime(data.get('date_start'), '%Y-%m-%d').date(),
    'date_end':datetime.strptime(data.get('date_end'), '%Y-%m-%d').date()
  })
  task=Task.query.get(task_id)
  if not task:
    return jsonify({'message':'Task not found!'})
  if is_changed(task,data):
    task.name=data.get('name')
    task.description=data.get('description')
    task.priority=data.get('priority')
    task.status=data.get('status')
    task.project_id=data.get('project_id')
    task.date_start=data.get('date_start')
    task.date_end=data.get('date_end')
    db.session.commit()
  return home()

@task_blueprint.route('/delete/<int:task_id>', methods=['POST','GET','DELETE'])
@login_required
def delete_task(task_id):
  task = Task.query.get(task_id)
  if task:
    db.session.delete(task)
    db.session.commit()
    return tasks()
  else:
    return jsonify({'message': 'Task not found!'})
