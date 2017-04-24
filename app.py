"""
This file is part of the flask+d3 Hello World project.
"""
import json
import os
import threading
import flask
from flask import request, redirect, flash, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy 
import csv,sqlite3

app = flask.Flask(__name__)
UPLOAD_FOLDER = './datafile'
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


@app.route('/uploader', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)
    return 'succcess'

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


@app.route("/filter_chart1",methods=['post', 'get'])
def filter_chart1():
    linkref = request.form.get('LinkRef',None)
    DataQuality = request.form.get('DataQuality',None)
    fromdate = request.form.get('fromDate',None)
    todate = request.form.get('toDate',None)
    dic={
        'LinkRef':linkref,
        'DataQuality':DataQuality,
        'fromDate':fromdate,
        'toDate':todate
    }
    return flask.render_template("charts.html", filter = json.dumps(dic))


@app.route("/filter_chart2",methods=['post', 'get'])
def filter_chart2():
    linkref = request.form.get('LinkRef', None)
    DataQuality = request.form.get('DataQuality', None)
    fromdate = request.form.get('fromDate', None)
    todate = request.form.get('toDate', None)
    dic={
        'LinkRef':linkref,
        'DataQuality':DataQuality,
        'fromDate':fromdate,
        'toDate':todate
    }
    return flask.render_template("charts1.html", filter = json.dumps(dic))


@app.route("/filter_chart3",methods=['post', 'get'])
def filter_chart3():
    linkref = request.form.get('LinkRef',None)
    DataQuality = request.form.get('DataQuality',None)
    fromdate = request.form.get('fromDate',None)
    todate = request.form.get('toDate',None)
    dic={
        'LinkRef':linkref,
        'DataQuality':DataQuality,
        'fromDate':fromdate,
        'toDate':todate
    }
    return flask.render_template("charts2.html", filter = json.dumps(dic))


@app.route("/filter_table",methods=['post', 'get'])
def filter_table():
    linkref = request.form.get('LinkRef',None)
    DataQuality = request.form.get('DataQuality',None)
    fromdate = request.form.get('fromDate',None)
    todate = request.form.get('toDate',None)
    dic={
        'LinkRef':linkref,
        'DataQuality':DataQuality,
        'fromDate':fromdate,
        'toDate':todate
    }
    return flask.render_template("tables.html", filter = json.dumps(dic))


@app.route("/charts.html")
def chart():
    """ 
    When you request for the chart page 
    """
    dic ={
        'LinkRef':'AL1000',
        'DataQuality':None,
        'fromDate':None,
        'toDate':None
    }
    return flask.render_template("charts.html",filter = json.dumps(dic))


@app.route("/charts1.html")
def chart1():
    """
    When you request for the chart page 
    """
    dic ={
        'LinkRef':'AL1000',
        'DataQuality':None,
        'fromDate':None,
        'toDate':None
    }
    return flask.render_template("charts1.html",filter = json.dumps(dic))


@app.route("/charts2.html")
def chart2():
    """
    When you request for the chart page 
    """
    dic ={
        'LinkRef':'AL1000',
        'DataQuality':None,
        'fromDate':None,
        'toDate':None
    }
    return flask.render_template("charts2.html",filter = json.dumps(dic))


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


@app.route("/tables.html")
def table():
    """
    When you request for the tables page
    """
    dic ={
        'LinkRef':None,
        'DataQuality':None,
        'fromDate':None,
        'toDate':None
    }
    return flask.render_template("tables.html",filter = json.dumps(dic))


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


class Data(db.Model):
    __tablename__ = 'data'
    LinkRef = db.Column(primary_key=True)
    LinkDescription = db.Column(db.Text)
    Date = db.Column(db.String(64))
    TimePeriod = db.Column(db.Integer)
    AverageJT = db.Column(db.Float)
    AverageSpeed = db.Column(db.Float)
    DataQuality = db.Column(db.Integer)
    LinkLength = db.Column(db.Float)
    Flow = db.Column(db.Float)

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


import csv
import json
 
# # 读csv文件
# def read_csv(file):
#     csv_rows = []
#     with open(file) as csvfile:
#         reader = csv.DictReader(csvfile)
#         title = reader.fieldnames
#         for row in reader:
#             csv_rows.extend([{title[i]:row[title[i]] for i in range(len(title))}])
#     return json.dumps(csv_rows)
 
# # 写json文件
# def write_json(data, json_file, format=None):
#     with open(json_file, "w") as f:
#         if format == "good":
#             f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '),ensure_ascii=False))
#         else:
#             f.write(json.dumps(data))
   
        


        


if __name__ == "__main__":
    port = 8000
    app.run(port=port)
