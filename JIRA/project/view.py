from flask import Blueprint, render_template, redirect, url_for, session, jsonify
from flask_login import current_user


from JIRA.routers import home, login_required
from JIRA.project.forms import ProjectForm
from JIRA.task.view import get_task_list
from JIRA.models import Project, Task
from JIRA import db

project_blueprint = Blueprint('projects', __name__, template_folder='templates', static_folder='static')

@project_blueprint.route('/')
def project():

  projects = Project.query.filter(Project.manager_id == current_user.id).all()
  return render_template('project_list.html', projects=projects)

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

@project_blueprint.route('/<int:project_id>', methods=['GET'])
@login_required
def project_by_id(project_id):
  project = db.get_or_404(Project, ident=project_id)
  session['active_project_id'] = project.id
  tasks = Task.query.filter(Task.project_id == project_id).all()
  task_list = get_task_list(tasks)
  return home(project_id=project, task_list=task_list)


@project_blueprint.route('/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_project(id):
  project = db.get_or_404(Project, ident=id)
  form = ProjectForm(obj=project)
  if form.validate_on_submit():
    project.name = form.name.data
    project.description = form.description.data
    # project.sequence = form.sequence.data
    # project.manager_id = form.manager_id.data
    db.session.commit()
    return redirect(url_for('projects.project_by_id', id=id))
  projects = Project.query.filter(Project.manager_id == current_user.id).all()
  return render_template('project_edit.html', form=form, project=project, projects=projects)


@project_blueprint.route('/delete/<int:project_id>/', methods=['POST', 'GET', 'DELETE'])
@login_required
def delete_project(project_id):
  if project_id:
    project = Project.query.get(project_id)
    tasks = Task.query.filter(Task.project_id == project_id).all()
    if project:
      for task in tasks:
        db.session.delete(task)
      db.session.delete(project)
      db.session.commit()
      return home()
    else:
      return jsonify({"error": "Project not found"}, 404)
  else:
    return jsonify({"error": "Method not allowed"}, 405)
