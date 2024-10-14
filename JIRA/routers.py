from flask import render_template, flash, session, redirect, url_for

from JIRA import app

@app.route('/')
def home():
  return render_template('index.html')