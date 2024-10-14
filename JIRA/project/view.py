from flask import Blueprint, render_template

project_blueprint = Blueprint('projects', __name__, template_folder='templates', static_folder='static')

@project_blueprint.route('/')
def project():
  return render_template('project.html')