"""
This file is part of the flask+d3 Hello World project.
"""
import json
import os
import flask
from flask import request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


@app.route("/")
def login():
    """
    When you request the root path, you'll get the index.html template.
    """
    return flask.render_template("login.html")


@app.route('/login.html', methods=['post', 'get'])
def handle_login():
    username = request.form['username']
    pswd = request.form['password']
    if request.form['register-submit']:
        email = request.form['email']
        if request.form['confirm-password'] == pswd:
            u = user(username,pswd,email)
            db.session.add(u)
            db.session.commit()
        return redirect(url_for('login'))
    elif request.form['login-submit']:
        print(username, pswd)
        if check_user(username, pswd):
            return flask.render_template("index.html")
        else:
            return redirect(url_for('login'))


@app.route("/index.html")
def index():
    """
    When you request the dashboard path, you'll get the index.html template.

    """
    return flask.render_template("index.html")


@app.route("/charts.html")
def chart():
    """
    When you request for the chart page 
    """
    return flask.render_template("charts.html")


@app.route("/tables.html")
def table():
    """
    When you request for the tables page
    """
    return flask.render_template("tables.html")


@app.route("/forms.html")
def form():
    """
    When you request for the forms page
    """
    return flask.render_template("forms.html")


'''
models
'''


class user(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    pswd = db.Column(db.String(64))
    email = db.Column(db.String(64))

    def __init__(self, username, pswd, email):
        self.username = username
        self.email = email
        self.pswd = pswd

    def __repr__(self):
        return '<User %r>' % self.username


def check_user(username, pswd):
    u = user.query.filter_by(username=username).first()
    if u:
        if u.pswd == pswd:
            return True
        else:
            return False
    else:
        return False



if __name__ == "__main__":

    port = 8000

    # Open a web browser pointing at the app.
    # os.system("open http://localhost:{0}".format(port))

    # Set up the development server on port 8000.
    # app.debug = True
    app.run(port=port)
