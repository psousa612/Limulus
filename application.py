import os

from flask import Flask, session, render_template, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
import traceback
import hashlib
import requests


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
if not os.getenv("SECRET_KEY"):
    raise RuntimeError("SECRET_KEY is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
# ROOT
@app.route("/", METHOD=["GET", "POST"])
def index():
    if(request.method == "GET"):
        return render_template("index.html")
    if(request.method == "POST"):
        return("uhh, what you tryin brah?")

# LOGIN API
@app.route("/login", METHODS=["POST"])
def login():
    username = str(request.form.get("username").upper())
    password = str(request.form.get("password"))
    passwordHash = hashlib.sha256()
    passwordHash.update(password.encode('utf8'))
    hashedPassword = str(passwordHash.hexdigest())
    if(db.execute("SELECT * FROM users WHERE upper(username) =:username AND password = :password", {"username": username, "password": hashedPassword}).rowcount == 1):
        user = db.execute("SELECT username FROM users WHERE upper(username) =:username", {
                          "username": username}).fetchone()
        return("Logged in")
    else:
        return("Wrong Username or Password")

# SIGNOUT API
@app.route("/signout", METHODS = ["POST"])
def signout():
    return("Signed out")

#Create User API
@app.route("/createuser", METHODS = ["POST"])
#TODO: Check for duplicate usernames
def createuser():
    username = str(request.form.get("username").upper())
    password = str(request.form.get("password"))
    passwordConf = str(request.form.get("passwordConf"))
    if(passwordConf != password):
        return("passwords dont match")
    else:
        passwordHash = hashlib.sha256()
        passwordHash.update(password.encode('utf8'))
        hashedPassword = str(passwordHash.hexdigest())
        db.execute("INSERT INTO users VALUES (:username, :hashedPassword)",{"username":username, "hashedPassword":hashedPassword})
        db.commit()
        return("User Created")
    