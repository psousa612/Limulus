import os
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import scoped_session, sessionmaker
import traceback
import hashlib
import requests
import random
import json


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#Function Definitions

#JSONify Helper Function
# def makeJSON(data):
#     d = {}
#     index = 0
#     for row in data:
#         insert = {}

#         i = 0
#         for item in row:
#             insert.update({i:item})
#             i += 1
#         index += 1
#         d.update({index:insert})
    
#     return json.dumps(d)

##User Functions
def login(username, password):
    return db.execute("SELECT * FROM users WHERE user_name = :uname AND password = :pass LIMIT 1", {"uname":username, "pass":password})

def signup(info):
    passwordHash = hashlib.sha256()
    passwordHash.update(info[1].encode('utf8'))
    hashedPassword = str(passwordHash.hexdigest())

    ukey = db.execute("""INSERT INTO users(user_name, email, password)
                    VALUES(:uname, :email, :password) RETURNING user_key""", {
                            "uname": info[0].upper(),
                            "email": info[2],
                            "password": hashedPassword}).fetchone()[0]

    db.execute("""INSERT INTO user_info(user_key, first_name, last_name, age, location, school)
                    VALUES(:ukey, :f_name, :l_name, :age, :loc, :school)""", {
                            "ukey": ukey,
                            "f_name": info[3],
                            "l_name": info[4],
                            "age": info[5],
                            "loc": info[6],
                            "school": info[7]})
    db.commit()

def add_friend(userkey, friendkey):
    db.execute("INSERT INTO friends(user_key, friend_key) VALUES(:ukey, :fkey)", {"ukey":userkey, "fkey":friendkey})
    db.commit()

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
                    WHERE friend_key = :ukey;""", {"ukey":userkey}).fetchall()

def get_friends_with_name(userkey):
    return db.execute("""SELECT users.user_key, user_name FROM friends
                    JOIN users ON users.user_key = friends.friend_key
                    WHERE friends.user_key = :ukey
                    UNION
                    SELECT friends.user_key, user_name FROM friends
                    JOIN users ON users.user_key = friends.user_key
                    WHERE friend_key = :ukey;""", {"ukey":userkey}).fetchall()

def remove_friend(ukey, fkey):
    db.execute("""DELETE FROM friends WHERE (user_key = :ukey AND friend_key = :fkey) 
                    OR (user_key = :fkey AND friend_key = :ukey)""", {"ukey":ukey, "fkey":fkey})
    db.commit()

def get_nonfriends(ukey):
    return db.execute("""SELECT user_key, user_name FROM users WHERE user_key != :ukey 
                            EXCEPT (SELECT users.user_key, user_name FROM friends
                                        JOIN users ON users.user_key = friends.friend_key
                                        WHERE friends.user_key = :ukey
                                        UNION
                                        SELECT friends.user_key, user_name FROM friends
                                        JOIN users ON users.user_key = friends.user_key
                                        WHERE friend_key = :ukey)""", {"ukey":ukey}).fetchall()

def get_username(userkey):
    return db.execute("SELECT user_name FROM users WHERE user_key = :ukey", {"ukey":userkey}).fetchone()[0]
    
def get_userkey(username):
    return db.execute("SELECT user_key FROM users WHERE user_name = :uname", {"uname":username.upper()}).fetchone()[0]

def get_points(userkey):
    return db.execute("SELECT points FROM user_info WHERE user_key = :ukey", {"ukey":userkey}).fetchone()[0]
    

def update_points(ukey):
    points = db.execute("UPDATE user_info SET points = points + 1 WHERE user_key = :ukey RETURNING points", {"ukey":ukey}).fetchone()
    db.commit()
    return points[0]

##Leaderboard functions
def refresh_leaderboard():
    db.execute("DELETE FROM leaderboard")
    result = db.execute("SELECT user_key, points FROM user_info ORDER BY points")

    for row in result:
        db.execute("""INSERT INTO leaderboard(user_key, points)
                        VALUES(:user_key, :points)""", {"user_key":row[0], "points":row[1]})

    db.commit()

def fetch_top10():
    return db.execute("""SELECT ROW_NUMBER() OVER (ORDER BY leaderboard.points DESC), user_info.user_key, users.user_name, user_info.points FROM leaderboard 
                            JOIN user_info ON user_info.user_key = leaderboard.user_key 
                            JOIN users ON users.user_key = user_info.user_key
                            ORDER BY leaderboard.points DESC""").fetchall()

##Question functions
def get_categories():
    return db.execute("SELECT DISTINCT category FROM questions").fetchall()

def random_question():
    return db.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1").fetchone()

def random_question_with_category(category):
    return db.execute("SELECT * FROM questions WHERE category = :cat ORDER BY RANDOM() LIMIT 1", {"cat":category}).fetchone()

def get_responses(qkey):
    return db.execute("SELECT * FROM responses WHERE question_key = :qkey ORDER BY RANDOM()", {"qkey":qkey}).fetchall()

def get_question_stats(q_key):
    return db.execute("SELECT * FROM question_stats WHERE question_key = :q_key", {"q_key":q_key}).fetchone()

def search_question_history(ukey, qkey):
    return db.execute("SELECT COUNT(*) FROM question_history WHERE question_key = :qkey AND user_key = :ukey", {"qkey":qkey, "ukey":ukey}).fetchone()

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
                        total_first_try_correct = total_first_try_correct + 1
                    WHERE question_key = :q_key""", {"q_key":q_key})
    db.commit()


def delete_user(user_key):
    #To completly remove a user, we need to remove them from:

    #the users table
    db.execute("DELETE FROM users WHERE user_key=:user_key",{"user_key":int(user_key)})

    #the user info table
    db.execute("DELETE FROM user_info WHERE user_key=:user_key",{"user_key":int(user_key)})

    #the friends table
    db.execute("DELETE FROM friends WHERE user_key=:user_key OR friend_key=:user_key",{"user_key":int(user_key)})
    
    #the question history table
    db.execute("DELETE FROM question_history WHERE user_key=:user_key",{"user_key":int(user_key)})
    
    #and the leaderboard table
    db.execute("DELETE FROM leaderboard WHERE user_key=:user_key",{"user_key":int(user_key)})
    db.commit()

def get_user_info(user_key):
    return db.execute("SELECT * FROM user_info WHERE user_key=:ukey", {"ukey":user_key}).fetchone()

def get_top_peer(user_key):
    return db.execute("SELECT users.user_key,user_name,email,first_name,last_name,age,location,school FROM users INNER JOIN user_info ON user_info.user_key = users.user_key WHERE school = (SELECT school FROM users WHERE user_key=:user_key) ORDER BY points DESC LIMIT 1",{"user_key":int(user_key)}).fetchone()

def get_top_ten_school():
    return db.execute("SELECT ROW_NUMBER() OVER (ORDER BY SUM(points)), school FROM users INNER JOIN user_info ON users.user_key=user_info.user_key GROUP BY school ORDER BY SUM(points) LIMIT 10").fetchall()

def get_toughest_question():
    return db.execute("SELECT question_key FROM question_stats WHERE total_amt != 0 ORDER BY total_first_try_correct ASC LIMIT 1").fetchone()

def get_question(q_key):
    return db.execute("SELECT * FROM questions WHERE question_key = :qkey", {"qkey":q_key}).fetchone()

def insert_question(questionInfo, userkey):
    # Insert the question into the main question table
    qkey = db.execute("""INSERT INTO questions(category, prompt, author_key)
                    VALUES(:cat, :prompt, :auth_key)
                    RETURNING question_key""", {
                        "cat":questionInfo[0],
                        "prompt":questionInfo[1],
                        "auth_key":userkey
                    }).fetchone()[0];

    # Insert the responses into the responses table
    db.execute("INSERT INTO responses(question_key, response, correct) VALUES(:qkey, :res, :cor)", {"qkey":qkey, "res":questionInfo[2], "cor":True})
    for i in range(3, len(questionInfo)):
        row = questionInfo[i]
        db.execute("INSERT INTO responses(question_key, response, correct) VALUES(:qkey, :res, :cor)", {"qkey":qkey, "res":row, "cor":False})
    
    # Insert a new question history entry for the new question
    db.execute("INSERT INTO question_stats(question_key) VALUES(:qkey)", {"qkey":qkey})

    db.commit()

def get_question_history(ukey):
    return db.execute("SELECT * FROM question_history WHERE user_key = :ukey", {"ukey":ukey})

def get_question_history_with_info(ukey):
    return db.execute("""SELECT question_history.question_key, prompt FROM question_history 
                            JOIN questions ON questions.question_key = question_history.question_key
                            WHERE question_history.user_key = :ukey""", {"ukey":ukey})

def insert_question_history(ukey, qkey):
    db.execute("""INSERT INTO question_history(user_key, question_key)
                    VALUES(:ukey, :qkey)""", {"ukey":ukey, "qkey":qkey})
    db.commit()

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
            ukey = userkey_prompt()
            uname = get_username(ukey)
            delete_user(ukey)
            print("{} has successfully been deleted!".format(uname))
            input("Press Enter to continue...")
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
            print("First userkey:")
            ukey = userkey_prompt()
            print("Second userkey: ")
            fkey = userkey_prompt()

            add_friend(ukey, fkey)
            print("Success! {} and {} are now friends!".format(get_username(ukey), get_username(fkey)))
            input("Press Enter to continue...")
        elif choice == '3':
            print("Select user to delete a friend from")
            ukey = userkey_prompt()
            res = get_friends_with_name(ukey)
            friends = []
            for row in res:
                friends.append(row[0])

            for i in range(0, len(friends)):
                print("[{}] {}".format(i+1, friends[i-1]))

            choice = int(input("Select which friend to remove: "))

            if choice <= 0 or choice > len(friends):
                input("Invalid selection. Press Enter to continue...")
            else:
                remove_friend(ukey, get_userkey(friends[choice-1]))
                print("{} and {} are no longer friends.".format(get_username(ukey), get_userkey(friends[choice-1])))
                input("Press Enter to continue...")

def leaderboard_prompt():
    choice = ''
    while choice != 'q':
        print("####################################")
        os.system('clear')

        print("[1] View Leaderboard")
        print("[2] View Top 10 Players")
        print("[3] Get Top Peer")
        print("[4] Get Top 10 Schools")
        print("[5] Get Toughest Question")

        print("[q] Go Back")

        choice = input("Enter in your selection: ")
        if choice == '1':
            refresh_leaderboard()
            os.system('clear')
            print("{:>8s} | {:<10s}".format("Ranking", "Name"))
            for row in fetch_top10():
                print("{:>8} | {:<10s}".format(row[0], get_username(row[1])))
            
            input("Press Enter to continue...")
        elif choice == '2':
            ukey = userkey_prompt()
            os.system('clear')

            print("The toughest question is: ")
            print("{:>8s} | {:<10s}".format("Ranking", "Name"))
            for row in get_top_peer(ukey):
                print("{:>8} | {:<10s}".format(row[0], row[2]))

            input("Press Enter to continue...")
        elif choice == '3':
            ukey = userkey_prompt()
            res = get_top_peer(ukey)
            os.system('clear')

            print("{}'s top peer is {}.".format(get_username(ukey), res[1]))
            input("\nPress Enter to continue...")
        elif choice == '4':
            os.system('clear')

            print("{:>8s} | {:<8s}".format("Ranking", "School"))
            for row in get_top_ten_school():
                print("{:>8} | {:<8s}".format(row[0], row[1]))

            input("Press Enter to continue...")
        elif choice == '5':
            os.system('clear')

            res = get_toughest_question()
            for row in res:
                qkey = row
            question = get_question(qkey)
            stats = get_question_stats(qkey)

            print("{} | {}  \nTotal Answers: {} \nTotal Wrong: {}".format(question[1], question[2], stats[1], stats[1]-stats[2]))
            input("Press Enter to continue...")

def question_stats_prompt():
    choice = ''
    while choice != 'q':
        print("####################################")
        os.system('clear')

        print("[1] View A Questions Stats")
        print("[2] Increment A Question's Stats Entry")

        print("[q] Go Back")

        choice = input("Please enter in a selection: ")

        if choice == '1':
            qkey = input("Please enter the question key: ")
            os.system('clear')
            try:
                print("{:13} | {:20} | {:20} | {:20}".format("Question Key", "Amount of Responses", "Total Correct", "Total First Tries"))
                res = get_question_stats(qkey)
                print("{:<13} | {:<20} | {:<20} | {:<20}".format(res[0], res[1], res[2], res[3]))
                input("Press Enter to continue...")
            except Exception as e:
                input("Invalid input! Press Enter to continue...")
        elif choice == '2':
            qkey = input("Please enter the question key: ")
            os.system('clear')
            try:
                print("Current Question Stats:")
                res = get_question_stats(qkey)
                print("{:13} | {:20} | {:20} | {:20}".format("Question Key", "Amount of Responses", "Total Correct", "Total First Tries"))
                print("{:<13} | {:<20} | {:<20} | {:<20}".format(res[0], res[1], res[2], res[3]))
                print("------------------------")

                print("[1] Correct Answer")
                print("[2] Correct Answer, First Try")
                print("[3] Wrong Answer")

                opt = input("Please enter a selection: ")

                if opt == '1':
                    update_question_stats_correct(qkey)
                elif opt == '2':
                    update_question_stats_correct_first_try(qkey)
                elif opt == '3':
                    update_question_stats_wrong(qkey)

                print("------------------------")
                res = get_question_stats(qkey)
                print("{:13} | {:20} | {:20} | {:20}".format("Question Key", "Amount of Responses", "Total Correct", "Total First Tries"))
                print("{:<13} | {:<20} | {:<20} | {:<20}".format(res[0], res[1], res[2], res[3]))

            except Exception as e:
                print("Something went wrong! :(")
            input("Press Enter to continue...")
            
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


# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")
# if not os.getenv("SECRET_KEY"):
#     raise RuntimeError("SECRET_KEY is not set")

# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))

#Main Program
# if __name__ == "__main__":
#     os.system('clear')

#     print("Initializing database...")
#     if not os.getenv("DATABASE_URL"):
#         raise RuntimeError("DATABASE_URL is not set")
#     if not os.getenv("SECRET_KEY"):
#         raise RuntimeError("SECRET_KEY is not set")

#     engine = create_engine(os.getenv("DATABASE_URL"))
#     db = scoped_session(sessionmaker(bind=engine))

#     os.system('clear')

#     choice = ''
#     while choice != 'q':
#         print("##########################################")
#         print("""
#         Welcome to.....
#         ______    _      _        ___           
#         /_  __/___(_)  __(_)__ _  / _ \___  ___ _
#         / / / __/ / |/ / / _ `/ / ___/ _ \/ _ `/
#         /_/ /_/ /_/|___/_/\_,_/ /_/   \___/\_, / 
#                                         /___/  
#         """)
#         print("##########################################")
#         print("[1] View tables")
#         print("[2] Questions")
#         print("[3] Users")
#         print("[4] Friends")
#         print("[5] Leaderboard")
#         print("[6] Question Stats")

#         print("[q] Quit")

#         choice = input("Select an option: ")

#         if choice == '1':
#             view_tables()
#         elif choice == '2':
#             question_prompt()
#         elif choice == '3':
#             user_prompt()
#         elif choice == '4':
#             friend_prompt()
#         elif choice == '5':
#             leaderboard_prompt()
#         elif choice == '6':
#             question_stats_prompt()
#         elif choice == '.':
#             os.system('clear')
#             try:
#                 query = input()
#                 db.execute(query)
#                 db.commit()
#             except Exception as e:
#                 print("Error! {}".format(e))

#             input("Press enter to continue...")

#         print("####################################")
#         os.system('clear')