from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
import traceback
import hashlib
import requests
import json
import os

from database_func import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
if not os.getenv("SECRET_KEY"):
    raise RuntimeError("SECRET_KEY is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
# ROOT
@app.route("/", methods=["GET", "POST"])
def index():
    if(request.method == "GET"):
        return render_template("index.html")
    if(request.method == "POST"):
        return("uhh, what you tryin brah?")

# LOGIN API
@app.route("/login", methods=["POST"])
def login():
    login_params = request.get_json()
    username = str(login_params["username"]).upper()
    password = str(login_params["password"])
    
    passwordHash = hashlib.sha256()
    passwordHash.update(password.encode('utf8'))
    hashedPassword = str(passwordHash.hexdigest())
    
    if(db.execute("SELECT * FROM users WHERE upper(user_name) =:username AND password = :password", {"username": username, "password": hashedPassword}).rowcount == 1):
        user = db.execute("SELECT user_key FROM users WHERE upper(user_name) =:username", {
                          "username": username}).fetchone()
        return jsonify({"user_key": user.user_key}),200
    else:
        return jsonify({"error":"unsuccesful"}),200

#Create User API
@app.route("/createuser", methods = ["POST"])
#TODO: Check for duplicate usernames
def createuser():
    createuser_params = request.get_json()
    username = str(createuser_params["username"]).upper()
    password = str(createuser_params["password"])
    passwordConf = str(createuser_params["passwordConf"])
    if(passwordConf != password):
        return("passwords dont match")
    else:
        if(db.execute("SELECT user_name FROM users WHERE user_name=:user_name",{"user_name":username}).rowcount != 0):
                return jsonify({"error":"User already exists"}),200
        passwordHash = hashlib.sha256()
        passwordHash.update(password.encode('utf8'))
        hashedPassword = str(passwordHash.hexdigest())
        db.execute("INSERT INTO users (user_name,password,email) VALUES (:user_name, :password)",{"user_name":username, "password":hashedPassword})
        db.commit()
        return jsonify({"Success":"User created"}),200

# Add Friend API
@app.route("/addFriend", methods = ["POST"])
def addFriend():
        addFriend_params = request.get_json()
        userkey = str(addFriend_params["userkey"])
        friendkey = str(addFriend_params["friendkey"])
        db.execute("INSERT INTO friends(user_key, friend_key) VALUES(:ukey, :fkey)", {"ukey":userkey, "fkey":friendkey})
        db.commit()
        return jsonify({"Success":"Added Friend"}),200
        
@app.route("/getFriends", methods = ["POST"])
def getFriends():
    getFriends_params = request.get_json()
    userkey = str(getFriends_params["userkey"])
    # Check if user exists:
    if(db.execute("SELECT user_key FROM users WHERE user_key=:userkey",{"userkey":userkey}).rowcount != 1):
        return jsonify({"error":"user doest exist"}),200
    friendTable = db.execute("""SELECT friend_key FROM friends
                    WHERE user_key = :ukey
                    UNION
                    SELECT user_key FROM friends
                    WHERE friend_key = :ukey;""", {"ukey":userkey}).fetchall()
    friends = []
    for f in friendTable:
        friends.append(f[0])
    return jsonify({"friends":friends}),200

# LEADERBOARD API
@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    refresh_leaderboard()
    board = fetch_top10()
    finalData = []
    for row in board:
        data = []
        data.append(row[0])
        data.append(row[2])
        data.append(row[3])
        finalData.append(data)
    return jsonify({"leaderboard":finalData}),200
# Get categories API
@app.route("/categories", methods=["GET"])
def list_categories():
    cats = get_categories()
    data = []
    for row in cats:
        data.append(row[0])

    return jsonify({"categories":data}),200

# Get Next Question API
@app.route("/nextquestion", methods=["POST"])
def nextQuestion():
    params = request.get_json()
    requestedCat = str(params["category"])
    questionData = random_question_with_category(requestedCat)
    cleanQuestionData = []
    for item in questionData:
        cleanQuestionData.append(item)

    responsesData = get_responses(questionData[0])
    cleanResponsesData = []
    for row in responsesData:
        toInsert = []
        for item in row:
            toInsert.append(item)
        cleanResponsesData.append(toInsert)

    return jsonify({"question":{"prompt":cleanQuestionData,"responses":cleanResponsesData}}),200

# Get User Info API
@app.route("/getuserinfo", methods=["POST"])
def get_info():
    params = request.get_json()
    uname = str(params["user_name"]).upper()
    data = get_user_info(get_userkey(uname))
    cleanData = []
    for row in data:
        cleanData.append(row)
    return jsonify({"info":cleanData}),200

# Remove Friend API
@app.route("/removeFriend", methods = ["POST"])
def removefriend():
    params = request.get_json()
    ukey = str(params["userkey"])
    fkey = str(params["friendkey"])
    remove_friend(ukey,fkey)
    return jsonify({"Success":"Removed Friend"}),200

# Get username API
@app.route("/getusername",methods = ["POST"])
def getusername():
    params = request.get_json()
    ukey = str(params["userkey"])
    if(db.execute("SELECT user_key FROM users WHERE user_key=:userkey",{"userkey":ukey}).rowcount != 1):
        return jsonify({"error":"user doest exist"}),200
    username = get_username(ukey)
    return jsonify({"username":username}),200

# Get points API
@app.route("/getpoints", methods = ["POST"])
def getpoints():
    params = request.get_json()
    ukey = str(params["userkey"])
    if(db.execute("SELECT user_key FROM users WHERE user_key=:userkey",{"userkey":ukey}).rowcount != 1):
        return jsonify({"error":"user doest exist"}),200
    points = get_points(ukey)
    return jsonify({"points":points}),200

# Update points API
@app.route("/updatepoints", methods = ["POST"])
def updatepoints():
    params = request.get_json()
    ukey = str(params["userkey"])
    if(db.execute("SELECT user_key FROM users WHERE user_key=:userkey",{"userkey":ukey}).rowcount != 1):
        return jsonify({"error":"user doest exist"}),200
    update_points(ukey)
    return jsonify({"Success":"Points updated"}),200

# Get random Question
@app.route("/randomquestion", methods = ["GET"])
def randomquestion():
    query = random_question()
    questionkey = query[0]
    category = query[1]
    prompt = query[2]
    authorkey= query[3]
    return jsonify({"questionkey":questionkey,
                    "category":category,
                    "prompt":prompt,
                    "authorkey":authorkey}),200
        
    