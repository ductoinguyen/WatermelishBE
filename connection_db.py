import pymongo, ast, random
from pymongo import MongoClient
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process 
import os
import threading
from datetime import datetime
import time

def getTime():
    now = datetime.now()
    return now.strftime("%d/%m/%Y")

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
        currentDay = getTime()
        db.watermelishCollection.insert({"username": username, "password": password, "name": name, "word_sets": {}, "game1": 0, "game2": 0, "game3": 0, "today": currentDay, "nowWord": 0, "totalScore": 250, "totalWord": 0})
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

def getListGroupCard(db, username):
    try:
        result = db.watermelishCollection.find({"username": username}, {"word_sets": True})
        word_sets = [x["word_sets"] for x in result][0]
        return list(word_sets.keys())
    except:
        return "Không có"
    
def getListCard(db, username, botu):
    try:
        result = db.watermelishCollection.find({"username": username}, {"word_sets": True})
        word_sets = [x["word_sets"] for x in result][0]
        word_set = word_sets[botu]
        return word_set
    except:
        return "Không có"
    
def createListCard(db, username, tenbotu, listWord):
    try:
        result = db.watermelishCollection.find({"username": username}, {"word_sets": True, "totalScore": True})
        (totalScore, word_sets) = [(x["totalScore"], x["word_sets"]) for x in result][0] 
        if totalScore < 50:
            return "Thất bại"
        if tenbotu in list(word_sets.keys()):
            return "Tên bộ từ trùng lặp"
        db.watermelishCollection.update({"username": username}, {"$set": {"word_sets." + tenbotu: list(ast.literal_eval(listWord))}})
        db.watermelishCollection.update({"username": username}, {"$inc": {"totalScore": -50}})
        return "Thành công"
    except:
        return "Thất bại"
    
def updateListCard(db, username, tenbotucu, tenbotumoi, listWord):
    try:
        result = db.watermelishCollection.find({"username": username}, {"word_sets": True})
        word_sets = [x["word_sets"] for x in result][0] 
        if tenbotucu not in list(word_sets.keys()):
            return "Bộ từ không tồn tại"
        db.watermelishCollection.update({"username": username}, {"$unset": {"word_sets." + tenbotucu: ""}})
        db.watermelishCollection.update({"username": username}, {"$set": {"word_sets." + tenbotumoi: list(ast.literal_eval(listWord))}})
        return "Thành công" 
    except:
        return "Thất bại"

def randomGame1(db, username):
    try:
        result = db.watermelishCollection.find({"username": username}, {"word_sets": True})
        word_sets = [x["word_sets"] for x in result][0]
        word_sets_name = list(word_sets.keys())
        data = []
        word_set_name = word_sets_name[random.randint(0, len(word_sets_name) - 1)]
        word_set = word_sets[word_set_name]
        word = word_set[random.randint(0, len(word_set) - 1)]
        data.append([word[0] + " (" + word[1] + ")"])
        answer = []
        answer.append([word[2], 1])
        word_set_name = word_sets_name[random.randint(0, len(word_sets_name) - 1)]
        word_set = word_sets[word_set_name]
        word = word_set[random.randint(0, len(word_set) - 1)]
        answer.append([word[2], 0])
        word_set_name = word_sets_name[random.randint(0, len(word_sets_name) - 1)]
        word_set = word_sets[word_set_name]
        word = word_set[random.randint(0, len(word_set) - 1)]
        answer.append([word[2], 0])
        random.shuffle(answer)
        data.append(answer)
        return data 
    except:
        return "Thiếu từ"
    
def randomGame2(db, username):
    try:
        result = db.watermelishCollection.find({"username": username}, {"word_sets": True})
        word_sets = [x["word_sets"] for x in result][0]
        word_sets_name = list(word_sets.keys())
        data = []
        for i in range(3):
            word_set_name = word_sets_name[random.randint(0, len(word_sets_name) - 1)]
            word_set = word_sets[word_set_name]
            word = word_set[random.randint(0, len(word_set) - 1)]
            data.append([word[0] + " (" + word[1] + ")", i])
            data.append([word[2], i])
        random.shuffle(data)
        return data 
    except:
        return "Thiếu từ"
    
def randomGame3(db, username):
    try:
        result = db.watermelishCollection.find({"username": username}, {"word_sets": True})
        word_sets = [x["word_sets"] for x in result][0]
        word_sets_name = list(word_sets.keys())
        word_set_name = word_sets_name[random.randint(0, len(word_sets_name) - 1)]
        word_set = word_sets[word_set_name]
        word = [""]
        while len(word[0]) < 4:
            word = word_set[random.randint(0, len(word_set) - 1)]
        random_index = random.randint(1, len(word[0]) - 2)
        data = [word[0][:random_index], word[0][random_index + 2:], word[0], word[1], word[2]]
        return data 
    except:
        return "Thiếu từ"
   
def maxScoreGame(db, username):
    result = db.watermelishCollection.find({"username": username}, {"game1": True, "game2": True, "game3": True})
    for x in result:
        return [x["game1"], x["game2"], x["game3"]]
 
def resultGame(db, username, game, score):
    if score > 0:
        db.watermelishCollection.update({"username": username}, {"$inc": {"totalScore": score}})
    result = db.watermelishCollection.find({"username": username}, {"game1": True, "game2": True, "game3": True})
    indexGame = {"gametracnghiem": "game1", "gameghepcap": "game2", "gamedientu": "game3"}[game]
    maxScore = [x[indexGame] for x in result][0]
    if maxScore < score:
        db.watermelishCollection.update({"username": username}, {"$set": {indexGame: score}})
        return score
    return maxScore

def learnWordSet(db, username, tenbotu):
    result = db.watermelishCollection.find({"username": username}, {"word_sets." + tenbotu: True})
    word_set = [x["word_sets"][tenbotu] for x in result][0]
    game = ["gametracnghiem", "gameghepcap", "gamedientu"][random.randint(0, 2)] 
    data = []
    if game == "gametracnghiem":
        word = word_set[random.randint(0, len(word_set) - 1)]
        data.append([word[0] + " (" + word[1] + ")"])
        answer = []
        answer.append([word[2], 1])
        word = word_set[random.randint(0, len(word_set) - 1)]
        answer.append([word[2], 0])
        word = word_set[random.randint(0, len(word_set) - 1)]
        answer.append([word[2], 0])
        random.shuffle(answer)
        data.append(answer)
    elif game == "gameghepcap":
        for i in range(3):
            word = word_set[random.randint(0, len(word_set) - 1)]
            data.append([word[0] + " (" + word[1] + ")", i])
            data.append([word[2], i])
        random.shuffle(data)
    else:
        word = [""]
        while len(word[0]) < 4:
            word = word_set[random.randint(0, len(word_set) - 1)]
        random_index = random.randint(1, len(word[0]) - 2)
        data = [word[0][:random_index], word[0][random_index + 2:], word[0], word[1], word[2]]  
    return [game, data]

def verifyLearnWord(db, username):
    result = db.watermelishCollection.find({"username": username}, {"today": True})
    nowDay = getTime()
    if nowDay != [x["today"] for x in result][0]:
        db.watermelishCollection.update({"username": username}, {"$set": {"today": nowDay, "nowWord": 1}})
    db.watermelishCollection.update({"username": username}, {"$inc": {"totalWord": 1, "nowWord": 1}})

def statistical(db, username):
    nowDay = getTime()
    result = db.watermelishCollection.find({"username": username}, {"today": True})
    if nowDay != [x["today"] for x in result][0]:
        db.watermelishCollection.update({"username": username}, {"$set": {"today": nowDay, "nowWord": 0}})
    result = db.watermelishCollection.find({"username": username}, {"today": True, "totalScore": True, "totalWord": True, "nowWord": True, "target": True})
    for x in result:
        return [x["today"], x["totalScore"], x["totalWord"], x["nowWord"], x["target"]]
    
def checkCreateWordSet(db, username):
    try:
        result = db.watermelishCollection.find({"username": username}, {"totalScore": True})
        totalScore = [x["totalScore"] for x in result][0] 
        if totalScore < 50:
            return "Không được"
        return "Có thể"
    except:
        return "Không được"

def deleteWordSet(db, username, tenbotu):
    try:
        db.watermelishCollection.update({"username": username}, {"$unset": {"word_sets." + tenbotu: ""}})
        db.watermelishCollection.update({"username": username}, {"$inc": {"totalScore": 50}})
        return "Thành công"
    except:
        return "Thất bại"
# print(searchWord("nhom13", "interlet"))

# db = getDB()
# print(getTarget(db, "nhom13"))