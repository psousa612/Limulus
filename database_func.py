import os
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
import traceback
import hashlib
import requests
import random


#Function Definitions

##DB Init Functions
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



def database_insert_examples():
    print("this is where i would insert values into the tables..... if i had tables")


##User Functions
def login():
    uname = input("Enter the username: ")
    password = input("Enter the password: ")

    #query here

def signup():
    uname = input("Enter the username: ")
    password = input("Enter the password: ")

    #query here

def update_points(uname):
    print("yer")

##Leaderboard functions
def refresh_leaderboard():
    # db.execute("""DELETE FROM leaderboard""")
    print('hi')
    # db.execute()

def fetch_top10():
    print("yer")


##Question functions
def get_categories():
    return db.execute("SELECT DISTINCT category FROM questions")

def random_question():
    return db.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")

def random_question_with_category(category):
    return db.execute("SELECT * FROM questions WHERE category = :cat ORDER BY RANDOM() LIMIT 1", {"cat":category})
    

def get_question_stats():
    print("yer")

def random_question_with_stats():
    print("yer")

def update_question_stats_wrong(q_key):
    print("yer")

def update_question_stats_correct_first_try(q_key):
    print("yer")

def update_question_stats_correct(q_key):
    print("yer")

def insert_question():
    print("yer")

def get_questions_from_user():
    print("yer")


def quiz_prompt(question):
    print("####################################")
    os.system('clear')

    choices = []
    question_info = [] #[0] = question_id, [1] = prompt, [2] = correct, [3] = category
    for row in question:
        question_info.append(row[0])
        question_info.append(row[2])

        question_info.append(row[3])
        choices.append(row[3])
        choices.append(row[4])
        choices.append(row[5])
        choices.append(row[6])

        question_info.append(row[1])

    random.shuffle(choices)

    print("Category: {}".format(question_info[3]))

    print("\nQuestion: ")
    print(question_info[1])
    
    print("\nChoices: ")
    for i in range(1, 5):
        print("[{}] {}".format(i, choices[i-1]))

    try:
        answer = int(input("Please put in your answer: "))
    except Exception as e:
        print("Invalid input! :(")
        return

    if answer > 4 or answer < 1:
        print("Invalid input! :(")
        return


    if choices[answer-1] == question_info[2]:
        print("Congrats, you got it!")
    else:
        print("Wrong Answer! :(")


    input("Press Enter to continue...")

def category_prompt():
    choice = ''
    while choice != 'q':
        cats = get_categories()
        categories = []
        for row in cats:
            categories.append(row[0])
        
        for i in range(1, len(categories)):
            print("[{}] {}".format(i,categories[i-1]))

        choice = input("Please enter which category you want: ")

        # if answer < 1 or answer > len(categories):
        #     print("Invalid input! :(")
        #     return

        if choice != 'q':
            return categories[int(choice)-1]
        



def question_prompt():
    choice = ''
    while choice != 'q':
        print("####################################")
        os.system('clear')

        print("[1] Print Categories")
        print("[2] Random Question")
        print("[3] Question From Specific Category")
        print("[q] Go Back")
        
        choice = input("Enter in your selection: ")
        if choice == '1':
            result = get_categories()
            for row in result:
                print(row[0])
            input("Press Enter to continue...")
        elif choice == '2':
            quiz_prompt(random_question())
        elif choice == '3':
            quiz_prompt(random_question_with_category(category_prompt()))
        

        
##Misc Functions
def print_table(table_name):
    result = db.execute("SELECT * FROM :table_name", {"table_name":table_name})
    for row in result:
        print(row)
    input("Press Enter to continue...")


def view_tables():
    choice = ''
    while choice != 'q':
        print("####################################")
        os.system('clear')
        

        print("[1] Users")
        print("[2] Friends")
        print("[3] Leaderboard")
        print("[4] Questions")
        print("[5] Indivdual Question Stats")
        print("[6] Personal Question History")
        print("[q] Go Back")
        
        choice = input("Which table to view?: ")

        os.system('clear')
        if choice == '1':
            result = db.execute("SELECT * FROM users")
        elif choice == '2':
            result = db.execute("SELECT * FROM friends")
        elif choice == '3':
            result = db.execute("SELECT * FROM leaderboard")
        elif choice == '4':
            result = db.execute("SELECT * FROM questions")
        elif choice == '5':
            result = db.execute("SELECT * FROM question_stats")
        elif choice == '6':
            result = db.execute("SELECT * FROM question_history")
        else:
            break

        for row in result:
            print(row)

        input("Press Enter to continue...")
        print("####################################")

#Main Program
os.system('clear')

print("Initializing database...")
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
if not os.getenv("SECRET_KEY"):
    raise RuntimeError("SECRET_KEY is not set")

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
database_init()

print("\Inserting example values...")
database_insert_examples()

os.system('clear')

choice = ''
user_key = -1;

while choice != 'q':
    print("##########################################")
    print("""
Welcome to.....
 ______    _      _        ___           
/_  __/___(_)  __(_)__ _  / _ \___  ___ _
 / / / __/ / |/ / / _ `/ / ___/ _ \/ _ `/
/_/ /_/ /_/|___/_/\_,_/ /_/   \___/\_, / 
                                  /___/  
""")
    print("##########################################")
    print("[1] View tables")
    print("[2] Questions")
    print("[3] Users")
    # print("[4] ")

    print("[q] quit")

    choice = input("Select an option: ")

    if choice == '1':
        view_tables()
    elif choice == '2':
        question_prompt()
    elif choice == '3':
        print("asd")
    elif choice == '9':
        db.execute("DELETE FROM questions")
        db.commit()


    print("####################################")
    os.system('clear')