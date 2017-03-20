"""
This file is part of the flask+d3 Hello World project.
"""
import json
import os
import flask
from flask import request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
import csv,sqlite3


app = flask.Flask(__name__)
UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','csv'])
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)


@app.route("/")
def login():
    """
    When you request the root path, you'll get the index.html template.
    """
    return flask.render_template("login.html")


@app.route('/register', methods=['post', 'get'])
@app.route('/login', methods=['post', 'get'])
def handle_login():
    username = request.form.get('username',None)
    pswd = request.form.get('password',None)
    if request.form.get('register-submit',None) and username and pswd :
        email = request.form.get('email',None)
        if request.form.get('confirm-password') == pswd:
            u = user(username,pswd,email)
            db.session.add(u)
            db.session.commit()
        return redirect(url_for('login'))
    elif request.form.get('login-submit') and username and pswd:
        print(username, pswd)
        if check_user(username, pswd):
            return flask.render_template("index.html")
        else:
            redirect(url_for('login'))
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


class Data(db.model):
    __tablename__ = 'data'
    LinkRef = db.Column(primary_key=True)
    LinkDescription = db.Column(db.Text)
    Date = db.Column(db.DateTime)
    TimePeriod = db.Column(db.Integer)
    AverageJT = 
    AverageSpeed = 
    DataQuality = db.Column(db.Integer)
    LinkLength = 
    Flow = 

    def __init__(self, *param):
        self.LinkRef = param[0]
        self.LinkDescription = param[1]
        self.Date = param[2]
        self.TimePeriod = param[3]
        self.AverageJT = param[4]
        self.AverageSpeed = param[5]
        self.DataQuality = param[6]
        self.LinkLength = param[7]
        self.Flow = param[8]


def check_user(username, pswd):
    u = user.query.filter_by(username=username).first()
    if u:
        if u.pswd == pswd:
            return True
        else:
            return False
    else:
        return False

'''
functions
'''


def readcsv(csvpath):
    reader = csv.DictReader(open(csvpath, "rb"), delimiter=',', quoting=csv.QUOTE_MINIMAL)
    ret = []
    for row in reader:
        datamodel = Data(row['LinkRef'], row['LinkDescription'], row['Date'], row['TimePeriod'], row['AverageJT'], row['AverageSpeed'],row['DataQuality'],row['LinkLength'],row['Flow'])
        ret.append(datamodel)
    return ret


def dataImport(datamodels):
    for datamodel in datamodels:
        db.session.add(datamodel)
        db.session.commit()


if __name__ == "__main__":
    port = 8000
    app.run(port=port)
