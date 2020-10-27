from flask import Flask, request, jsonify, render_template
import os, json, threading, time, connection_db
import pandas as pd
import numpy as np

# app = Flask(__name__)
TEMPLATE_DIR = os.path.abspath('./templates')
STATIC_DIR = os.path.abspath('./static')

# app = Flask(__name__) # to make the app run without any
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
# db = connection_db.getDB()

@app.route("/dangnhap", methods=["POST"])
def checkLogin():
    # username = request.args.get('username')
    # password = request.args.get('password')
    username = request.form['username']
    password = request.form['password']
    result = connection_db.checkLogin(username, password)
    data = [{"_id": result}]
    return app.response_class(json.dumps(data),mimetype='application/json')

# @app.route("/testdangnhap", methods=["POST"])
# def testcheckLogin():
#     username = request.args.get('username')
#     password = request.args.get('password')
#     global db
#     result = connection_db.testcheckLogin(db, username, password)
#     data = [{"_id": result}]
#     return app.response_class(json.dumps(data),mimetype='application/json')

@app.route("/kiemtrataikhoan/<username>", methods=["GET"])
def checkAccount(username):
    username = username.strip()
    result = connection_db.checkAccount(username)
    data = [{"exist_account": result}]
    return app.response_class(json.dumps(data),mimetype='application/json')

@app.route("/dangky", methods=["POST"])
def signup():
    username = request.args.get('username')
    password = request.args.get('password')
    name = request.args.get('name')
    result = connection_db.signup(username, password, name)
    data = [{"result": result}]
    return app.response_class(json.dumps(data),mimetype='application/json')

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/timtu/<username>/<stringSearch>", methods=["GET"])
def searchWord(username, stringSearch):
    result = connection_db.searchWord(username, stringSearch)
    data = [{"result": result}]
    return app.response_class(json.dumps(data),mimetype='application/json')

@app.route("/test", methods=["GET"])
def test():
    return app.response_class(json.dumps([{"ok": 1}]),mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True)