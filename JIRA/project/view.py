from flask import Blueprint

project_blueprint = Blueprint('projects', __name__, template_folder='templates', static_folder='static')

@project_blueprint.route('/')
def project():
  return 'Project'