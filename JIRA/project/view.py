from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

from JIRA.routers import home, login_required
from JIRA.project.forms import ProjectForm
from JIRA.models import Project
from JIRA import db

project_blueprint = Blueprint('projects', __name__, template_folder='templates', static_folder='static')

@project_blueprint.route('/')
def project():
  return render_template('project_list.html')

@project_blueprint.route('/new', methods=['GET', 'POST'])
# @login_required
def project_new():
  form = ProjectForm()
  if form.validate_on_submit():
    project = Project(name=form.name.data, description=form.description.data, manager_id=current_user.id)
    db.session.add(project)
    db.session.commit()
    # tải lại trang để hiển thị project mới
    return redirect(url_for('home'))
  
  #thêm cái này để hiển thị sidebar 
  projects = Project.query.filter(Project.manager_id == current_user.id).all()
  return render_template('project_new.html', form=form, projects=projects)