import pymongo
from pymongo import MongoClient
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process 
import os
import threading

def getDB():
    MONGO_URL = os.environ.get('MONGO_URL')
    if not MONGO_URL:
        MONGO_URL = "mongodb+srv://hequantri:hequantri@cluster0.q0gxn.gcp.mongodb.net/watermelishDB?retryWrites=true&w=majority";
    myclient = MongoClient(MONGO_URL)
    db = myclient["watermelishDB"]
    return db
 
def checkLogin(db, username, password):
    try:
        # db = getDB()
        result = (db.watermelishCollection.find({"username": username, "password": password}, {"_id": True}))
        for x in result:
            break
        return (str(x['_id']))
    except:
        return -1
    
# def testcheckLogin(db, username, password):
#     try:
#         result = (db.watermelishCollection.find({"username": username, "password": password}, {"_id": True}))
#         for x in result:
#             break
#         return (str(x['_id']))
#     except:
#         return -1

def checkAccount(db, username):
    try:
        # db = getDB()
        result = (db.watermelishCollection.find({"username": username}, {"_id": True}))
        for x in result:
            break
        x['_id']
        return "yes"
    except:
        return "no"

def signup(db, username, password, name):
    try: 
        # db = getDB()
        if checkAccount(db, username) == "yes":
            return "thất bại"
        db.watermelishCollection.insert({"username": username, "password": password, "name": name})
        return "thành công"
    except:
        return "thất bại"

def findInWordSet(g, data, word_sets, word_set, stringSearch):
    for word in word_sets[word_set]:
        if (fuzz.token_set_ratio(word[0], stringSearch) > 80):
            # print(fuzz.token_set_ratio(word[0], stringSearch), word)
            data.append(word) 

def searchWord(db, username, stringSearch):
    try:
        # db = getDB()
        allWords = db.watermelishCollection.find({"username": username}, {"word_sets": True})
        data = []
        for x in allWords:
            break
        word_sets = x["word_sets"]
        g = []
        for word_set in word_sets:
            t = threading.Thread(target=findInWordSet, args=(g, data, word_sets, word_set, stringSearch,))
            t.start()
            g.append(t) 
        while (any([x.is_alive() for x in g])):
            pass
        # print(len(word_sets))
        return data
    except:
        return "Không tìm thấy"
    
def setTarget(db, username, target):
    try:
        db.watermelishCollection.update({"username": username}, {"$set": {"target": target}})
        return "Thành công"
    except:
        return "Thất bại"
    
def getTarget(db, username):
    try:
        result = db.watermelishCollection.find({"username": username}, {"target": True})
        for x in result:
            return x["target"]
    except:
        return "Không có"
    
def editAccount(db, username, old_password, new_password, name):
    try:
        if checkLogin(db, username, old_password) == -1:
            return "Sai mật khẩu"
        db.watermelishCollection.update({"username": username}, {"$set": {"password": new_password, "name": name}})
        return "Thành công"
    except:
        return "Thất bại"

# print(searchWord("nhom13", "interlet"))

# db = getDB()
# print(getTarget(db, "nhom13"))