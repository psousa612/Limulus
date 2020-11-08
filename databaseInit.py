import os
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
##DB Init Functions

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def database_init():

        db.execute("""CREATE TABLE IF NOT EXISTS users (
                        user_key SERIAL PRIMARY KEY,
                        user_name TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        first_name TEXT,
                        last_name TEXT,
                        age INTEGER,
                        location TEXT,
                        school TEXT,
                        points INTEGER NOT NULL);""")

        db.execute("""CREATE TABLE IF NOT EXISTS questions (
                        question_key SERIAL PRIMARY KEY,
                        category TEXT NOT NULL,
                        prompt TEXT NOT NULL,
                        correct TEXT NOT NULL,
                        wrong1 TEXT NOT NULL,
                        wrong2 TEXT NOT NULL,
                        wrong3 TEXT NOT NULL,
                        author_key INTEGER DEFAULT -1 NOT NULL);""")


        db.execute("""CREATE TABLE IF NOT EXISTS question_stats (
                question_key INTEGER PRIMARY KEY,
                total_amt INTEGER DEFAULT 0,
                total_correct INTEGER DEFAULT 0,
                total_first_try_correct INTEGER DEFAULT 0);""")


        db.execute("""CREATE TABLE IF NOT EXISTS leaderboard (
                user_key INTEGER NOT NULL UNIQUE,
                points INTEGER NOT NULL);""")

        db.execute("""CREATE TABLE IF NOT EXISTS friends (
                user_key INTEGER NOT NULL,
                friend_key INTEGER NOT NULL);""")

        db.execute("""CREATE TABLE IF NOT EXISTS question_history (
                user_key INTEGER PRIMARY KEY,
                question_key INTEGER NOT NULL,
                date DATE);""")

        #CS Questions: https://opentdb.com/api.php?amount=20&category=18&type=multiple
        #Math questions: https://opentdb.com/api.php?amount=20&category=19&type=multiple
        #Science: Gadget: https://opentdb.com/api.php?amount=10&category=30&type=multiple
        #Video Games:  https://opentdb.com/api.php?amount=10&category=15&type=multiple

        # populateTable("https://opentdb.com/api.php?amount=30&category=18&type=multiple")
        # populateTable("https://opentdb.com/api.php?amount=30&category=19&type=multiple")
        # populateTable("https://opentdb.com/api.php?amount=30&category=30&type=multiple")
        # populateTable("https://opentdb.com/api.php?amount=30&category=15&type=multiple")

        populateUsers()
        # populateFriends()

        db.commit()

def populateTable(url):
        #Insert questions from Open Trivia DB
        response = requests.get(url)
        results = response.json()["results"]
    
        for row in results:
                db.execute("""INSERT INTO questions(category, prompt, correct, wrong1, wrong2, wrong3) 
                        VALUES(:category, :prompt, :correct, :wrong1, :wrong2, :wrong3)""", {
                                "category":row["category"], "prompt":row["question"],
                                "correct":row["correct_answer"], "wrong1":row["incorrect_answers"][0],
                                "wrong2":row["incorrect_answers"][1], "wrong3":row["incorrect_answers"][2]})

        db.commit()

def populateUsers():
        users = [["ySharma", "yash@yash.com", "abc123", "Yash", "Sharma", 18, None, "UCMerced", 0],
                ["bbridi", "bbbbbbbbridi@protonmail.com", "securePassword99", "Busher", None, 29, None, "UCMerced", 0],
                ["psousa", "spam@gmail.com", "theseWillBeHashedEventually", None, "Sousa", 21, "San Jose", "UCMerced", 0]]
        
        for row in users:
                db.execute("""INSERT INTO users(user_name, email, password, first_name, last_name, age, location, school, points) 
                                VALUES(:uname, :email, :password, :f_name, :l_name, :age, :loc, :school, :points)""", {
                                        "uname": row[0],
                                        "email": row[1],
                                        "password": row[2],
                                        "f_name": row[3],
                                        "l_name": row[4],
                                        "age": row[5],
                                        "loc": row[6],
                                        "school": row[7],
                                        "points": row[8]})

def populateFriends():
        friends = []


def populateQuestionStats():
        print("question stats")

database_init()