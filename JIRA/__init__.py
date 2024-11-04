import os 

from flask import Flask
from flask_bcrypt import Bcrypt 
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__)) # base directory là thư mục cha của file __init__.py
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(basedir, 'database/JIRA_DB.db'))
# config db
db = SQLAlchemy(app)
# config migrate 
migrate = Migrate(app, db) 

# config bcrypt mã hóa password
bcrypt = Bcrypt(app)
# config login manager
login_manager = LoginManager(app)

# Config router
from JIRA import routers


from .auth.view import auth_blueprint
from .user.view import user_blueprint
from .task.view import task_blueprint
from .project.view import project_blueprint

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(task_blueprint, url_prefix='/tasks')
app.register_blueprint(project_blueprint, url_prefix='/projects')
