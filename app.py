from flask import Flask, request, jsonify, render_template
import os, json, threading, time, connection_db
import pandas as pd
import numpy as np

# app = Flask(__name__)
TEMPLATE_DIR = os.path.abspath('./templates')
STATIC_DIR = os.path.abspath('./static')

# app = Flask(__name__) # to make the app run without any
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
db = connection_db.getDB()

@app.route("/dangnhap", methods=["POST"])
def checkLogin():
    try: 
        username = request.form['username']
        password = request.form['password']
    except:
        username = request.args.get('username')
        password = request.args.get('password')
    global db
    result = connection_db.checkLogin(db, username, password)
    data = [{"_id": result}]
    return app.response_class(json.dumps(data),mimetype='application/json')

@app.route("/chinhsuathongtin", methods=["POST"])
def editAccount():
    try:
        username = request.form['username']
        old_password = request.form['oldpassword']
        new_password = request.form['newpassword']
        name = request.form['name']
    except:
        username = request.args.get('username')
        old_password = request.args.get('oldpassword')
        new_password = request.args.get('newpassword')
        name = request.args.get('name')
    global db
    result = connection_db.editAccount(db, username, old_password, new_password, name)
    data = [{"result": result}]
    return app.response_class(json.dumps(data),mimetype='application/json')

@app.route("/kiemtrataikhoan/<username>", methods=["GET"])
def checkAccount(username):
    username = username.strip()
    global db
    result = connection_db.checkAccount(db, username)
    data = [{"exist_account": result}]
    return app.response_class(json.dumps(data),mimetype='application/json')

@app.route("/dangky", methods=["POST"])
def signup():
    try:
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
    except:
        username = request.args.get('username')
        password = request.args.get('password')
        name = request.args.get('name')
    global db
    result = connection_db.signup(db, username, password, name)
    data = [{"result": result}]
    return app.response_class(json.dumps(data),mimetype='application/json')

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/timtu/<username>/<stringSearch>", methods=["GET"])
def searchWord(username, stringSearch):
    global db
    result = connection_db.searchWord(db, username, stringSearch)
    data = [{"result": result}]
    return app.response_class(json.dumps(data),mimetype='application/json')

@app.route("/datmuctieu/<username>/<int:target>", methods=["GET"])
def setTarget(username, target):
    global db
    result = connection_db.setTarget(db, username, target)
    data = [{"result": result}]
    return app.response_class(json.dumps(data),mimetype='application/json')

@app.route("/muctieuhientai/<username>", methods=["GET"])
def getTarget(username):
    global db
    result = connection_db.getTarget(db, username)
    data = [{"result": result}]
    return app.response_class(json.dumps(data),mimetype='application/json')

@app.route("/danhsachcacbotu/<username>", methods=["GET"])
def getListGroupCard(username):
    global db
    result = connection_db.getListGroupCard(db, username)
    data = [{"result": result}]
    return app.response_class(json.dumps(data),mimetype='application/json')

@app.route("/danhsachbotu/<username>/<botu>", methods=["GET"])
def getListCard(username, botu):
    global db
    result = connection_db.getListCard(db, username, botu)
    data = [{"result": result}]
    return app.response_class(json.dumps(data),mimetype='application/json')

@app.route("/thembotumoi/<username>/<tenbotu>", methods=["GET"])
def createListCard(username, tenbotu):
    global db
    try:
        listWord = request.form['listword']
    except:
        listWord = request.args.get('listword')
    result = connection_db.createListCard(db, username, tenbotu, listWord)
    data = [{"result": result}]
    return app.response_class(json.dumps(data),mimetype='application/json')

@app.route("/chinhsuabotu/<username>/<tenbotucu>/<tenbotumoi>", methods=["GET"])
def updateListCard(username, tenbotucu, tenbotumoi):
    global db
    try:
        listWord = request.form['listword']
    except:
        listWord = request.args.get('listword')
    result = connection_db.updateListCard(db, username, tenbotucu, tenbotumoi, listWord)
    data = [{"result": result}]
    return app.response_class(json.dumps(data),mimetype='application/json')

@app.route("/gameghepcap/<username>", methods=["GET"])
def randomGame2(username):
    global db
    result = connection_db.randomGame2(db, username)
    data = [{"result": result}]
    return app.response_class(json.dumps(data),mimetype='application/json')

@app.route("/gamedientu/<username>", methods=["GET"])
def randomGame3(username):
    global db
    result = connection_db.randomGame3(db, username)
    data = [{"result": result}]
    return app.response_class(json.dumps(data),mimetype='application/json')

@app.route("/test", methods=["GET"])
def test():
    return app.response_class(json.dumps([{"ok": 1}]),mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True)