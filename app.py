from flask import session

from JIRA import app
from JIRA.models import *

if __name__ == '__main__':
  app.run( debug=True, port = 5001 )