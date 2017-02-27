"""
This file is part of the flask+d3 Hello World project.
"""
import json
import os
import flask
from flask import request
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



@app.route('/login.html',methods=['post','get'])
def handle_login():
    username = request.form['username']
    pswd = request.form['password']
    print(username,pswd)
    
    return flask.render_template("index.html")



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


@app.route("/data")
@app.route("/data/<int:ndata>")
def data(ndata=100):
    """
    On request, this returns a list of ``ndata`` randomly made data points.

    :param ndata: (optional)
        The number of data points to return.

    :returns data:
        A JSON string of ``ndata`` data points.

    """
    x = 10 * np.random.rand(ndata) - 5
    y = 0.5 * x + 0.5 * np.random.randn(ndata)
    A = 10. ** np.random.rand(ndata)
    c = np.random.rand(ndata)
    return json.dumps([{"_id": i, "x": x[i], "y": y[i], "area": A[i],
                        "color": c[i]}
                       for i in range(ndata)])



if __name__ == "__main__":
    import os

    port = 8000

    # Open a web browser pointing at the app.
    # os.system("open http://localhost:{0}".format(port))

    # Set up the development server on port 8000.
    # app.debug = True
    app.run(port=port)
