from flask import redirect, url_for, render_template, flash, session

from JIRA import app

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  return render_template('login.html')

@app.route('/logout')
def logout():
  # code logout
  
  return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
  return render_template('register.html')