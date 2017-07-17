"""
This file is part of the flask+d3 Hello World project.
"""
import json
import os
import threading
import flask
from flask import request, redirect, flash, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import csv
import sqlite3

app = flask.Flask(__name__)
UPLOAD_FOLDER = './datafile'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'])
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
    username = request.form.get('username', None)
    pswd = request.form.get('password', None)
    if request.form.get('register-submit', None) and username and pswd:
        email = request.form.get('email', None)
        if request.form.get('confirm-password') == pswd:
            u = user(username, pswd, email)
            db.session.add(u)
            db.session.commit()
        return redirect(url_for('login'))
    elif request.form.get('login-submit') and username and pswd:
        print(username, pswd)
        if check_user(username, pswd):
            dic = {
                'LinkRef': 'AL1000',
                'DataQuality': None,
                'fromDate': None,
                'toDate': None
            }
            return flask.render_template("charts.html", filter=json.dumps(dic))
        else:
            redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


# @app.route("/index.html", methods=['post', 'get'])
# def index():
#     """
#     When you request the dashboard path, you'll get the index.html template.

#     """
#     linkref = request.form.get('LinkRef', None)
#     DataQuality = request.form.get('DataQuality', None)
#     fromdate = request.form.get('fromDate', None)
#     todate = request.form.get('toDate', None)
#     dic = {
#         'LinkRef': linkref,
#         'DataQuality': DataQuality,
#         'fromDate': fromdate,
#         'toDate': todate
#     }
#     return flask.render_template("charts.html", filter=json.dumps(dic))


@app.route("/filter_chart1", methods=['post', 'get'])
def filter_chart1():
    linkref = request.form.get('LinkRef', "AL1000")
    DataQuality = request.form.get('DataQuality', None)
    fromdate = request.form.get('fromDate', None)
    todate = request.form.get('toDate', None)
    dic = {
        'LinkRef': linkref,
        'DataQuality': DataQuality,
        'fromDate': fromdate,
        'toDate': todate
    }
    return flask.render_template("charts.html", filter=json.dumps(dic))


@app.route("/filter_chart2", methods=['post', 'get'])
def filter_chart2():
    linkref = request.form.get('LinkRef', 'AL1000')
    DataQuality = request.form.get('DataQuality', None)
    fromdate = request.form.get('fromDate', None)
    todate = request.form.get('toDate', None)
    dic = {
        'LinkRef': linkref,
        'DataQuality': DataQuality,
        'fromDate': fromdate,
        'toDate': todate
    }
    return flask.render_template("charts1.html", filter=json.dumps(dic))


@app.route("/filter_chart3", methods=['post', 'get'])
def filter_chart3():
    linkref = request.form.get('LinkRef', 'AL1000')
    DataQuality = request.form.get('DataQuality', None)
    fromdate = request.form.get('fromDate', None)
    todate = request.form.get('toDate', None)
    dic = {
        'LinkRef': linkref,
        'DataQuality': DataQuality,
        'fromDate': fromdate,
        'toDate': todate
    }
    return flask.render_template("charts2.html", filter=json.dumps(dic))


@app.route("/filter_table", methods=['post', 'get'])
def filter_table():
    linkref = request.form.get('LinkRef', "AL1000")
    DataQuality = request.form.get('DataQuality', None)
    fromdate = request.form.get('fromDate', None)
    todate = request.form.get('toDate', None)
    dic = {
        'LinkRef': linkref,
        'DataQuality': DataQuality,
        'fromDate': fromdate,
        'toDate': todate
    }
    return flask.render_template("tables.html", filter=json.dumps(dic))


@app.route("/charts.html")
def chart():
    """ 
    When you request for the chart page 
    """
    dic = {
        'LinkRef': 'AL1000',
        'DataQuality': None,
        'fromDate': None,
        'toDate': None
    }
    return flask.render_template("charts.html", filter=json.dumps(dic))


@app.route("/charts1.html")
def chart1():
    """
    When you request for the chart page 
    """
    dic = {
        'LinkRef': 'AL1000',
        'DataQuality': None,
        'fromDate': None,
        'toDate': None
    }
    return flask.render_template("charts1.html", filter=json.dumps(dic))


@app.route("/charts2.html")
def chart2():
    """
    When you request for the chart page 
    """
    dic = {
        'LinkRef': 'AL1000',
        'DataQuality': None,
        'fromDate': None,
        'toDate': None
    }
    return flask.render_template("charts2.html", filter=json.dumps(dic))


@app.route("/charts3.html")
def chart3():
    """
    When you request for the chart page 
    """
    # dic ={
    #     'LinkRef':'AL1000',
    #     'DataQuality':None,
    #     'fromDate':None,
    #     'toDate':None
    # }
    return flask.render_template("charts3.html")


@app.route("/charts4.html")
def chart4():
    """
    When you request for the chart page 
    """
    return flask.render_template("charts4.html")


@app.route("/tables.html")
def table():
    """
    When you request for the tables page
    """
    dic = {
        'LinkRef': "AL1000",
        'DataQuality': None,
        'fromDate': None,
        'toDate': None
    }
    return flask.render_template("tables.html", filter=json.dumps(dic))


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
    app.run(debug=True, port=port)
