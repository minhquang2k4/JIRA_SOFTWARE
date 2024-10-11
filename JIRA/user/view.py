from flask import Blueprint

user_blueprint = Blueprint('users', __name__, template_folder='templates', static_folder='static')

@user_blueprint.route('/')
def user():
  return 'User'