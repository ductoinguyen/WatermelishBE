import pymongo
from pymongo import MongoClient
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process 
import os

def getDB():
    MONGO_URL = os.environ.get('MONGO_URL')
    if not MONGO_URL:
        MONGO_URL = "mongodb+srv://hequantri:hequantri@cluster0.q0gxn.gcp.mongodb.net/watermelishDB?retryWrites=true&w=majority";
    myclient = MongoClient(MONGO_URL)
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
    
# def testcheckLogin(db, username, password):
#     try:
#         result = (db.watermelishCollection.find({"username": username, "password": password}, {"_id": True}))
#         for x in result:
#             break
#         return (str(x['_id']))
#     except:
#         return -1

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

def searchWord(username, stringSearch):
    try:
        db = getDB()
        allWords = db.watermelishCollection.find({"username": username}, {"word_sets": True})
        data = []
        for x in allWords:
            break
        word_sets = x["word_sets"]
        for word_set in word_sets:
            for word in word_sets[word_set]:
                if (fuzz.token_set_ratio(word[0], stringSearch) > 80):
                    # print(fuzz.token_set_ratio(word[0], stringSearch), word)
                    data.append(word)           
        # print(len(word_sets))
        return data
    except:
        return "Không tìm thấy"

# print(searchWord("nhom13", "interlet"))