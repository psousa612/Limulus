import os
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
import traceback
import hashlib
import requests

#Function Definitions

##DB Init Functions
def database_init():
    if not os.getenv("DATABASE_URL"):
        raise RuntimeError("DATABASE_URL is not set")
    if not os.getenv("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY is not set")

    engine = create_engine(os.getenv("DATABASE_URL"))
    db = scoped_session(sessionmaker(bind=engine))


    #Get questions from Open Trivia DB
    response = requests.get("https://opentdb.com/api.php?amount=20&category=18&type=multiple")
    results = response.json()["results"]
    # for row in results:
    #     print(row["question"])
    #     print("-----------------")

#Store questions here, call more links for different questions

#Math questions: https://opentdb.com/api.php?amount=20&category=19&type=multiple
#Science: Gadget: https://opentdb.com/api.php?amount=10&category=30&type=multiple
#Video Games:  https://opentdb.com/api.php?amount=10&category=15&type=multiple

def database_insert_examples():
    print("insdoans")

    


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
    print("yer")

def fetch_top10():
    print("yer")


##Question functions
def get_categories():
    print("yer")


def random_question():
    print("yer")

def random_question_with_category():
    #print category selection menu here
    category = input("Which category do you want?: ")

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






##Misc Functions
def view_tables():
    choice = ''
    while(choice != 'q'):
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
            print("1")
        elif choice == '2':
            print("2")
        elif choice == '3':
            print("3")
        elif choice == '4':
            print("4")
        elif choice == '5':
            print("5")
        elif choice == '6':
            print("6")

        print("####################################")





#Main Program
print("Welcome <3")

print("Initializing database...")
database_init()

print("\Inserting example values...")
database_insert_examples()


choice = ''
user_key = -1;

while choice != 'q':
    print("####################################")
    os.system('clear')

    print("[1] View tables")
    print("[2] ")
    print("[3] ")

    print("[q] quit")

    choice = input("Select an option: ")

    if choice == '1':
        view_tables()
    elif choice == '2':
        print("asd")
    elif choice == '3':
        print("asd")