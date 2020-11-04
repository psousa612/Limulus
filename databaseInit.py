import os
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
##DB Init Functions

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

def database_init():
    db.execute("""CREATE TABLE IF NOT EXISTS users (
                    user_key SERIAL PRIMARY KEY,
                    user_name TEXT UNIQUE NOT NULL,
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
                    wrong3 TEXT NOT NULL);""")


    db.execute("""CREATE TABLE IF NOT EXISTS question_stats (
            question_key INTEGER PRIMARY KEY,
            total_amt INTEGER DEFAULT 0,
            total_correct INTEGER DEFAULT 0,
            total_first_try_correct INTEGER DEFAULT 0);""")


    db.execute("""CREATE TABLE IF NOT EXISTS leaderboard (
            ranking INTEGER PRIMARY KEY,
            user_key INTEGER NOT NULL UNIQUE,
            points INTEGER NOT NULL);""")

    db.execute("""CREATE TABLE IF NOT EXISTS friends (
            user_key INTEGER NOT NULL,
            friend_key INTEGER NOT NULL);""")

    db.execute("""CREATE TABLE IF NOT EXISTS question_history (
            user_key INTEGER PRIMARY KEY,
            question_key INTEGER NOT NULL,
            date DATE);""")

    #Insert questions from Open Trivia DB
    response = requests.get("https://opentdb.com/api.php?amount=20&category=18&type=multiple")
    results = response.json()["results"]
    
    for row in results:
        db.execute("""INSERT INTO questions(category, prompt, correct, wrong1, wrong2, wrong3) 
                        VALUES(:category, :prompt, :correct, :wrong1, :wrong2, :wrong3)""", {
                                "category":row["category"], "prompt":row["question"],
                                "correct":row["correct_answer"], "wrong1":row["incorrect_answers"][0],
                                "wrong2":row["incorrect_answers"][1], "wrong3":row["incorrect_answers"][2]})
    
    db.commit()

database_init()