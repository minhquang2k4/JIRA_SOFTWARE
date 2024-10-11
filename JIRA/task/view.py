from flask import Blueprint 

task_blueprint = Blueprint('tasks', __name__, template_folder='templates', static_folder='static')

@task_blueprint.route('/')
def task():
  return 'Task'