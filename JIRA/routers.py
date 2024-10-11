from flask import render_template, flash, session

from JIRA import app

@app.route('/')
def home():
  return render_template('index.html')
