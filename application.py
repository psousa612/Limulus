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
        user = db.execute("SELECT user_name FROM users WHERE upper(user_name) =:username", {
                          "username": username}).fetchone()
        return jsonify({"user_name": user.user_name, "email":user.email}),200
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

# LEADERBOARD API
@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    refresh_leaderboard()
    board = fetch_top10()
    d = {}

    index = 0
    for row in board:
        insert = {}

        i = 0
        for item in row:
            insert.update({i:item})
            i += 1
        index += 1
        d.update({index:insert})

    return json.dumps(d)
    