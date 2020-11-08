import os
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
import traceback
import hashlib
import requests
import random

#Function Definitions

##User Functions
def login(username, password):
    return db.execute("SELECT * FROM users WHERE user_name = :uname AND password = :pass LIMIT 1", {"uname":username, "password":password})

def signup(info):
    db.execute("""INSERT INTO users(user_name, email, password, first_name, last_name, age, location, school) 
                    VALUES(:uname, :email, :password, :f_name, :l_name, :age, :loc, :school)""", {
                            "uname": info[0],
                            "email": info[1],
                            "password": info[2],
                            "f_name": info[3],
                            "l_name": info[4],
                            "age": info[5],
                            "loc": info[6],
                            "school": info[7]})

    db.commit()

def add_friend(userkey, friendkey):
    pass

def get_friends(userkey):
    return db.execute("""SELECT friend_key FROM friends
                    WHERE user_key = :ukey
                    UNION
                    SELECT user_key FROM friends
                    WHERE friend_key = :ukey;""", {"ukey":userkey})

def get_friends_with_info(userkey):
    return db.execute("""SELECT * FROM friends
                    JOIN users ON users.user_key = friends.friend_key
                    WHERE users.user_key = :ukey
                    UNION
                    SELECT * FROM friends
                    JOIN users ON users.user_key = friends.user_key
                    WHERE friend_key = :ukey;""", {"ukey":userkey})

##Do not include this one in our total query count :3
def get_friends_with_name(userkey):
    return db.execute("""SELECT user_name FROM friends
                    JOIN users ON users.user_key = friends.friend_key
                    WHERE friends.user_key = :ukey
                    UNION
                    SELECT user_name FROM friends
                    JOIN users ON users.user_key = friends.user_key
                    WHERE friend_key = :ukey;""", {"ukey":userkey})

##Or this one
def get_username(userkey):
    res = db.execute("SELECT user_name FROM users WHERE user_key = :ukey", {"ukey":userkey})
    for row in res:
        return row[0]

def get_points(userkey):
    res = db.execute("SELECT points FROM users WHERE user_key = :ukey", {"ukey":userkey})
    for row in res:
        return row[0]

def update_points(ukey):
    db.execute("UPDATE users SET points = points + 1 WHERE user_key = :ukey", {"ukey":ukey})
    db.commit()

##Leaderboard functions
def refresh_leaderboard():
    db.execute("DELETE FROM leaderboard")
    
    result = db.execute("SELECT user_key, points FROM users ORDER BY points")

    for row in result:
        db.execute("""INSERT INTO leaderboard(user_key, points)
                        VALUES(:user_key, :points)""", {"user_key":row[0], "points":row[1]})

    db.commit()

def fetch_top10():
    return db.execute("SELECT ROW_NUMBER() OVER (ORDER BY points), * FROM leaderboard ORDER BY points")

##Question functions
def get_categories():
    return db.execute("SELECT DISTINCT category FROM questions")

def random_question():
    return db.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")

def random_question_with_category(category):
    return db.execute("SELECT * FROM questions WHERE category = :cat ORDER BY RANDOM() LIMIT 1", {"cat":category})

def get_question_stats(q_key):
    return db.execute("SELECT * FROM question_stats WHERE question_key = :q_key", {"q_key":q_key})

def random_question_with_stats():
    return db.execute("""SELECT * FROM questions 
                         LEFT JOIN question_stats ON question_stats.question_key = questions.question_key
                         ORDER BY RANDOM() LIMIT 1""")

def update_question_stats_wrong(q_key):
    db.execute("""UPDATE question_stats 
                    SET total_amt = total_amt + 1 
                    WHERE question_key = :q_key""", {"q_key":q_key})
    db.commit()

def update_question_stats_correct(q_key):
    db.execute("""UPDATE question_stats 
                    SET total_amt = total_amt + 1,
                        total_correct = total_correct + 1 
                    WHERE question_key = :q_key""", {"q_key":q_key})
    db.commit()

def update_question_stats_correct_first_try(q_key):
    db.execute("""UPDATE question_stats 
                    SET total_amt = total_amt + 1,
                        total_correct = total_correct + 1,
                        total_first_ty_correct = total_first_ty_correct + 1
                    WHERE question_key = :q_key""", {"q_key":q_key})
    db.commit()
    
def delete_user(user_key):
    db.execute("DELETE users WHERE user_key=:user_key",{"user_key":int(user_key)})
    db.commit()
    
def get_top_peer(user_key):
    return db.execute("SELECT * FROM users WHERE school = (SELECT school FROM users WHERE user_key=:user_key) ORDER BY points DESC LIMIT 1",{"user_key":int(user_key)})

def get_top_ten_school():
    return db.execute("SELECT school FROM users GROUP BY school ORDER BY SUM(points) LIMIT 10")

def get_toughest_question():
    return db.execute("SELECT question_key FROM question_stats WHERE total_amt != 0 ORDER BY total_first_try_correct ASC LIMIT 1")

def insert_question(question):
    db.execute("""INSERT INTO questions(category, prompt, correct, wrong1, wrong2, wrong3, author_key)
                    VALUES(:cat, :prompt, :correct, :wrong1, :wrong2, :wrong3, :auth_key)""", {
                        "cat":question[0],
                        "prompt":question[1],
                        "correct":question[2],
                        "wrong1":question[3],
                        "wrong2":question[4],
                        "wrong3":question[5],
                        "auth_key":question[6]
                    });
    db.commit()

def get_questions_from_user():
    print("####################################")
    os.system('clear')

    ques_info = []
    ques_info.append(input("Category: "))
    ques_info.append(input("Question: "))
    ques_info.append(input("The correct answer: "))
    ques_info.append(input("Wrong answer 1: "))
    ques_info.append(input("Wrong answer 2: "))
    ques_info.append(input("Wrong answer 3: "))
    ques_info.append(input("author key: (-1 for default / system): "))
    
    os.system('clear')
    print(ques_info)

    choice = input("Is this correct? y/n: ")

    if choice == 'y':
        insert_question(ques_info)
    else:
        print("Cancelling...")
        input("Press Enter to continue...")

def get_question_history(ukey):
    return db.execute("SELECT * FROM question_history WHERE user_key = :ukey", {"ukey":ukey})

def get_question_history_with_info(ukey):
    return db.execute("""SELECT question_history.question_key, prompt FROM question_history 
                            JOIN questions ON questions.question_key = question_history.question_key
                            JOIN users ON users.user_key = question_history.user_key
                            WHERE users.user_key = :ukey""", {"ukey":ukey})


##Prompts
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
        
        for i in range(1, len(categories)+1):
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
        print("[4] Submit A New Question")
        print("[5] View A User's Question History")
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
        elif choice == '4':
            get_questions_from_user()
        elif choice == '5':
            ukey = userkey_prompt()
            res = get_question_history_with_info(ukey)
            os.system('clear')
            print("{}'s Question History".format(get_username(ukey)))
            for row in res:
                print("{}: {}".format(row[0], row[1]))

            input("Press Enter to continue...")



def checkForNone(value):
    if value == '':
        return None
    else:
        return value

def login_prompt():
    print("####################################")
    os.system('clear')

    uname = input("Enter in your username: ")
    password = input("Enter in your password:")

    result = login(uname, password)

    if result.rowcount() == 1:
        print("Successively logged in.")
    else:
        print("Error logging in.")

    input("Press Enter to continue...")

def signup_prompt():
    print("####################################")
    os.system('clear')

    info = []
    info.append(input("Enter in your username: "))
    info.append(input("Enter in your email: "))
    info.append(input("Enter in your password: "))

    print("\n####################################")
    print("The following questions are optional.")

    info.append(checkForNone(input("First Name: ")))
    info.append(checkForNone(input("Last Name: ")))
    info.append(checkForNone(input("Age: ")))
    info.append(checkForNone(input("Location: ")))
    info.append(checkForNone(input("School: ")))

    signup(info)

    input("Thanks for signing up! Press Enter to continue...")

def delete_user_prompt():
    users = db.execute("SELECT * FROM users")
    pass

def user_prompt():
    choice = ''
    while choice != 'q':
        print("####################################")
        os.system('clear')

        print("[1] Log In")
        print("[2] Sign Up")
        print("[3] Delete User")
        print("[4] Add Points To User")
        print("[q] Go Back")

        choice = input("Enter in your selection: ")
        if choice == '1':
            login_prompt()
        elif choice == '2':
            signup_prompt()
        elif choice == '3':
            delete_user_prompt()
        elif choice == '4':
            ukey = userkey_prompt()
            update_points(ukey)
            print("{} now has {} points.".format(get_username(ukey), get_points(ukey)))
            input("Press Enter to continue...")

def userkey_prompt():
    users = db.execute("""SELECT user_key, user_name FROM users ORDER BY user_key ASC""")

    print("----------------------")
    print("User List:")
    for row in users:
        print("[{}] {}".format(row[0], row[1]))


    return(int(input("\nEnter in which user: ")))

def friend_prompt():
    choice = ''
    while choice != 'q':
        print("####################################")
        os.system('clear')

        print("[1] View Friends")
        print("[2] Add Friend")
        print("[3] Remove Friend")
        

        print("[q] Go Back")

        choice = input("Enter in your selection: ")
        
        os.system('clear')
        if choice == '1':
            userkey = userkey_prompt()
            username = get_username(userkey)
            res = get_friends_with_name(userkey)
            for row in res:
                print("{} is friends with {}".format(username, row[0]))

            input("Press Enter to continue...")

        elif choice == '2':
            pass

        elif choice == '3':
            pass

def leaderboard_prompt():
    choice = ''
    while choice != 'q':
        print("####################################")
        os.system('clear')

        print("[1] View Top 10 Players")
        print("[2] ")

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
            result = db.execute("SELECT ROW_NUMBER() OVER (ORDER BY points), * FROM leaderboard")
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
    print("[4] Friends")
    print("[5] Leaderboard")

    print("[q] quit")

    choice = input("Select an option: ")

    if choice == '1':
        view_tables()
    elif choice == '2':
        question_prompt()
    elif choice == '3':
        user_prompt()
    elif choice == '4':
        friend_prompt()
    elif choice == '5':
        leaderboard_prompt()
    elif choice == '.':
        os.system('clear')
        try:
            query = input()
            db.execute(query)
            db.commit()
        except Exception as e:
            print("Error! {}".format(e))

        input("Press enter to continue...")

    print("####################################")
    os.system('clear')