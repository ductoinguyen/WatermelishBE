import pymongo
from pymongo import MongoClient

def getDB():
    myclient = MongoClient("mongodb+srv://hequantri:hequantri@cluster0.q0gxn.gcp.mongodb.net/watermelishDB?retryWrites=true&w=majority")
    db = myclient["watermelishDB"]
    return db
 
def checkLogin(username, password):
    try:
        db = getDB()
        result = (db.watermelishCollection.find({"username": username, "password": password}, {"_id": True}))
        for x in result:
            break
        return (str(x['_id']))
    except:
        return -1

def checkAccount(username):
    try:
        db = getDB()
        result = (db.watermelishCollection.find({"username": username}, {"_id": True}))
        for x in result:
            break
        x['_id']
        return "yes"
    except:
        return "no"

def signup(username, password, name):
    try: 
        db = getDB()
        if checkAccount(db, username) == "yes":
            return "thất bại"
        db.watermelishCollection.insert({"username": username, "password": password, "name": name})
        return "thành công"
    except:
        return "thất bại"

# db = getDB()
# print(checkLogin(db, "nhom13", "nhom13"))