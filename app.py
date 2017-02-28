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
def  dataImport(csvpath,dbpath,tablename):
    reader = csv.DictReader(open(csvpath,"rb"),delimiter=',',quoting=csv.QUOTE_MINIMAL)
    conn = sqlite3.connect(dbpath)
    # shz: fix error with non-ASCII input
    conn.text_factory = str
    c = conn.cursor()
    create_query = 'CREATE TABLE '+tablename +' ("cn" TEXT,"en" TEXT,"lat" DOUBLE,"lon" DOUBLE,"points" DOUBLE,"count" INTEGER,"intro" TEXT,"photo" TEXT,"url" TEXT,"content" TEXT)' 
    c.execute(create_query)
    for row in reader:
        to_db = [row['cn'], row['en'],row['lat'],row['lon'],row['points'],row['count'],row['intro'],row['photo'],row['url'],row['content']]
        c.execute('INSERT INTO '+tablename+' (cn, en, lat,lon,points,count,intro,photo,url,content) VALUES (?, ?, ?,?, ?, ?,?, ?, ?,?);', to_db)
    conn.commit()


if __name__ == "__main__":
    port = 8000
    app.run(port=port)
