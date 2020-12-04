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
@app.route("/signup", methods = ["POST"])
#TODO: Check for duplicate usernames
def createuser():
    createuser_params = request.get_json()
    info = createuser_params["info"]
    username = info[0].upper()
    # passwordConf = str(createuser_params["passwordConf"])
    # if(passwordConf != password):
    #     return("passwords dont match")
    # else:
    if(db.execute("SELECT user_name FROM users WHERE user_name=:user_name",{"user_name":username}).rowcount != 0):
            return jsonify({"error":"User already exists"}),200
    signup(info)
    return jsonify({"Success":"User created"}),200

@app.route("/addUserInfo", methods = ["POST"])
def add_user_info():
    pass

# Add Friend API
@app.route("/addFriend", methods = ["POST"])
def addFriend():
        addFriend_params = request.get_json()
        username = str(addFriend_params["username"]) 
        friendkey = str(addFriend_params["friendkey"])

        add_friend(get_userkey(username), friendkey)
        return jsonify({"Success":"Added Friend"}),200

@app.route("/getFriends", methods = ["POST"])
def getFriends():
    getFriends_params = request.get_json()
    username = str(getFriends_params["user_name"])
    userkey = get_userkey(username)
    # Check if user exists:
    if(db.execute("SELECT user_key FROM users WHERE user_key=:userkey",{"userkey":userkey}).rowcount != 1):
        return jsonify({"error":"user doest exist"}),200
    friendTable = get_friends_with_name(userkey)
    friends = []
    for f in friendTable:
        temp = []
        temp.append(f[0])
        temp.append(f[1])
        friends.append(temp)
    return jsonify({"friends":friends}),200

@app.route("/getNonFriends", methods=["POST"])
def user_list():
    params = request.get_json()
    username = str(params["username"])
    data = get_nonfriends(get_userkey(username))
    cleanData = []
    for row in data:
        toInsert = []
        toInsert.append(row[0])
        toInsert.append(row[1])
        cleanData.append(toInsert)
    
    return jsonify({"users":cleanData})

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

# Update Points API
@app.route("/updatepoints", methods = ["POST"])
def updatepoints():
    params = request.get_json()
    uname = str(params["user_name"])
    if(db.execute("SELECT username FROM users WHERE user_name=:uname",{"uname":uname}).rowcount != 1):
        return jsonify({"error":"user doest exist"}),200
    points = update_points(get_userkey(uname))
    return jsonify({"points":points}),200

@app.route("/answeredquestion", methods=["POST"])
def updateUser():
    params = request.get_json()
    uname = str(params["user_name"]).upper()
    qkey = int(params["qkey"])
    result = bool(params["result"])
    ukey = get_userkey(uname)
    
    # Update points based on correctness
    points = 0
    if result == True:
        points = update_points(ukey)
    else:
        points = get_points(ukey)

    # Update user question history
    insert_question_history(ukey, qkey)

    # Update question stats
    res = search_question_history(ukey, qkey)
    if res != None and result == True:
        update_question_stats_correct_first_try(qkey)
    elif result == True:
        update_question_stats_correct(qkey)
    else:
        update_question_stats_wrong(qkey)
    
    return jsonify({"points":points}),200

    
# Get Random Question
@app.route("/randomquestion", methods = ["GET"])
def randomquestion():
    query = random_question()
    responses = get_responses(query[0])
    questionkey = query[0]
    category = query[1]
    prompt = query[2]
    authorkey= query[3]
    r1 = responses[0][1]
    r2 = responses[1][1]
    r3 = responses[2][1]
    r4 = responses[3][1]
    i = 0
    correctres = 0 
    for r in responses:
        if(r[2] == True):
            correctres = i+1
            break
        i+=1
    
    return jsonify({"questionkey":questionkey,
                    "category":category,
                    "prompt":prompt,
                    "authorkey":authorkey,
                    "r1":r1,
                    "r2":r2,
                    "r3":r3,
                    "r4":r4,
                    "correctres":correctres}),200

# Insert a question
@app.route("/addQuestion", methods=["POST"])
def add_new_question():
    params = request.get_json()
    questionInfo = params["info"]
    ukey = get_userkey(str(params["username"]))
    # print(questionInfo)
    insert_question(questionInfo, ukey)

    return jsonify({"Success":"Question Added"}),200

# Get question stats
@app.route('/questionstats', methods = ["POST"])
def questionstats():
    params = request.get_json()
    qkey = str(params["questionkey"]) 
    stats = get_question_stats(qkey)
    qkey = stats[0]
    total_amt = stats[1]
    total_correct = stats[2]
    total_first_try_correct = stats[3]
    return jsonify({"question_key":qkey,
                    "total_amt":total_amt,
                    "total_correct":total_correct,
                    "total_first_try_correct":total_first_try_correct}),200

# Get Question History
@app.route('/questionhistory', methods=["POST"])
def question_history():
    params = request.get_json()
    uname = str(params["user_name"])
    ukey = get_userkey(uname)
    data = get_question_history_with_info(ukey)
    cleanData = []
    for row in data:
        toInsert = []
        toInsert.append(row[0])
        toInsert.append(row[1])
        cleanData.append(toInsert)
    
    return jsonify({"history":cleanData})

# Get top peer 
@app.route('/gettoppeer',methods = ["POST"])
def gettoppeer():
    params = request.get_json()
    ukey = str(params["userkey"])
    if(db.execute("SELECT user_key FROM users WHERE user_key=:userkey",{"userkey":ukey}).rowcount != 1):
        return jsonify({"error":"user doest exist"}),200    
    top_peer = get_top_peer(ukey)
    user_key = top_peer[0]
    user_name = top_peer[1]
    email = top_peer[2]
    first_name = top_peer[3]
    last_name = top_peer[4]
    age = top_peer[5]
    location = top_peer[6]
    school = top_peer[7]
    return jsonify({"user_key":user_key,
                    "user_name":user_name,
                    "email":email,
                    "first_name":first_name,
                    "last_name":last_name,
                    "age":age,
                    "location":location,
                    "school":school}),200


# Get top 10 schools
@app.route('/get_top_schools')
def get_top_schools():
   res = get_top_ten_school()
   rankings = {}
   for r in res:
       rankings[r[0]] = r[1]

   return jsonify(rankings),200

# Get toughest question 
@app.route('/get_toughest_question')
def get_Toughest_question():
    res = get_toughest_question()
    qkey = res[0]
    return jsonify({"question_key":qkey}),200
        
    