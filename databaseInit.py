import os
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
import random
import hashlib
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
                        email TEXT UNIQUE NOT NULL);""")

        db.execute("""CREATE TABLE IF NOT EXISTS user_info (
                        user_key INTEGER PRIMARY KEY,
                        first_name TEXT,
                        last_name TEXT,
                        age INTEGER,
                        location TEXT,
                        school TEXT,
                        points INTEGER NOT NULL DEFAULT 0);""")

        db.execute("""CREATE TABLE IF NOT EXISTS questions (
                        question_key SERIAL PRIMARY KEY,
                        category TEXT NOT NULL,
                        prompt TEXT NOT NULL,
                        author_key INTEGER DEFAULT -1 NOT NULL);""")

        db.execute("""CREATE TABLE IF NOT EXISTS responses (
                        question_key INTEGER,
                        response TEXT NOT NULL,
                        correct BOOLEAN);""")

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
                user_key INTEGER NOT NULL,
                question_key INTEGER NOT NULL,
                date DATE);""")

        #CS Questions: https://opentdb.com/api.php?amount=20&category=18&type=multiple
        #Math questions: https://opentdb.com/api.php?amount=20&category=19&type=multiple
        #Science: Gadget: https://opentdb.com/api.php?amount=10&category=30&type=multiple
        #Video Games:  https://opentdb.com/api.php?amount=10&category=15&type=multiple

        populateQuestions("https://opentdb.com/api.php?amount=30&category=18&type=multiple")
        populateQuestions("https://opentdb.com/api.php?amount=30&category=19&type=multiple")
        populateQuestions("https://opentdb.com/api.php?amount=30&category=30&type=multiple")
        populateQuestions("https://opentdb.com/api.php?amount=30&category=15&type=multiple")

        populateUsers()
        populateFriends()
        populateQuestionStats()
        populateLeaderboard()
        populateQuestionHistory()

        db.commit()

def populateQuestions(url):
        #Insert questions from Open Trivia DB
        response = requests.get(url)
        results = response.json()["results"]
    
        for row in results:
                qkey = db.execute("""INSERT INTO questions(category, prompt) 
                        VALUES(:category, :prompt) RETURNING question_key""", {
                                "category":row["category"], "prompt":row["question"],
                                "correct":row["correct_answer"], "wrong1":row["incorrect_answers"][0],
                                "wrong2":row["incorrect_answers"][1], "wrong3":row["incorrect_answers"][2]}).fetchone()

                db.execute("""INSERT INTO responses(question_key, response, correct)
                                VALUES(:qkey, :res, :cor)""", {"qkey": qkey[0], "res": row["correct_answer"], "cor": True})
                for i in range(0, 3):
                        db.execute("""INSERT INTO responses(question_key, response, correct)
                                          VALUES(:qkey, :res, :cor)""", {"qkey": qkey[0], "res": row["incorrect_answers"][i], "cor": False})

        db.commit()

def populateUsers():
        users = [["ySharma", "yash@yash.com", "abc123", "Yash", "Sharma", 18, None, "UCMerced", 600],
                ["bbridi", "bbbbbbbbridi@protonmail.com", "securePassword99", "Busher", None, 29, None, "UCMerced", 504],
                ["psousa", "spam@gmail.com", "theseWillBeHashedEventually", None, "Sousa", 21, "San Jose", "UCMerced", 339]]
        
        for row in users:
                passwordHash = hashlib.sha256()
                passwordHash.update(row[2].encode('utf8'))
                hashedPassword = str(passwordHash.hexdigest())
                ukey = db.execute("""INSERT INTO users(user_name, email, password) 
                                VALUES(:uname, :email, :password) RETURNING user_key""", {
                                        "uname": row[0],
                                        "email": row[1],
                                        "password": hashedPassword}).fetchone()

                db.execute("""INSERT INTO user_info(user_key, first_name, last_name, age, location, school, points)
                                VALUES(:ukey, :f_name, :l_name, :age, :loc, :school, :points)""", {
                                        "ukey" : ukey[0],
                                        "f_name": row[3],
                                        "l_name": row[4],
                                        "age": row[5],
                                        "loc": row[6],
                                        "school": row[7],
                                        "points" : row[8]})

def populateFriends():
        friends = [[1, 2], 
                   [3, 1],
                   [3, 2]]

        for row in friends:
                db.execute("""INSERT INTO friends(user_key, friend_key)
                                VALUES(:ukey, :fkey)""", {"ukey":row[0], "fkey":row[1]})
        db.commit()

def populateQuestionStats():
        res = db.execute("SELECT question_key FROM questions")
        qkeys = []
        for row in res:
                qkeys.append(row[0])

        for key in qkeys:
                total = random.randint(0, 50)
                correct = random.randint(0, total)
                first = random.randint(0, correct)

                db.execute("INSERT INTO question_stats VALUES(:key, :total, :correct, :first)", {
                        "key": key,
                        "total": total,
                        "correct": correct,
                        "first": first })
        
        db.commit()

def populateLeaderboard():
        db.execute("DELETE FROM leaderboard")
    
        result = db.execute("SELECT user_key, points FROM user_info ORDER BY points")

        for row in result:
                db.execute("""INSERT INTO leaderboard(user_key, points)
                                VALUES(:user_key, :points)""", {"user_key":row[0], "points":row[1]})

def populateQuestionHistory():
        keys = db.execute("SELECT user_key FROM users")
        maxQuestionKey = db.execute("SELECT MAX(question_key) FROM questions")
        
        for row in maxQuestionKey:
                maxKey = row[0]

        for ukey in keys:
                for i in range(0, random.randint(0, 10)):
                        
                        db.execute("INSERT INTO question_history(user_key, question_key) VALUES(:ukey, :qkey)", {
                                "ukey": ukey[0],
                                "qkey": random.randint(0, maxKey)
                        })
        db.commit()

def deleteDatabase():
        choice = input("You really want to delete all tables? y/n: ")

        if choice == 'n':
                input("Ok :) Press Enter to continue...")
                return
        else:
                db.execute("DROP TABLE users")
                db.execute("DROP TABLE user_info")
                db.execute("DROP TABLE friends")
                db.execute("DROP TABLE questions")
                db.execute("DROP TABLE responses")
                db.execute("DROP TABLE question_stats")
                db.execute("DROP TABLE question_history")
                db.execute("DROP TABLE leaderboard")
                db.commit()
        

database_init()
# deleteDatabase()

