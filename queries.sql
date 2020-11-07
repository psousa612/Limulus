-- CREATE TABLES
CREATE TABLE IF NOT EXISTS users (
                        user_key INTEGER PRIMARY KEY,
                        user_name TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        first_name TEXT,
                        last_name TEXT,
                        age INTEGER,
                        location TEXT,
                        school TEXT,
                        points INTEGER NOT NULL);

CREATE TABLE IF NOT EXISTS questions (
                        question_key INTEGER PRIMARY KEY,
                        category TEXT NOT NULL,
                        prompt TEXT NOT NULL,
                        correct TEXT NOT NULL,
                        wrong1 TEXT NOT NULL,
                        wrong2 TEXT NOT NULL,
                        wrong3 TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS question_stats (
                question_key INTEGER PRIMARY KEY,
                total_amt INTEGER DEFAULT 0,
                total_correct INTEGER DEFAULT 0,
                total_first_try_correct INTEGER DEFAULT 0);

CREATE TABLE IF NOT EXISTS leaderboard (
                ranking INTEGER PRIMARY KEY,
                user_key INTEGER NOT NULL UNIQUE,
                points INTEGER NOT NULL);

CREATE TABLE IF NOT EXISTS friends (
                user_key INTEGER NOT NULL,
                friend_key INTEGER NOT NULL);

CREATE TABLE IF NOT EXISTS question_history (
                user_key INTEGER,
                question_key INTEGER NOT NULL,
                date DATE);

--LOAD SAMPLE DATA
INSERT INTO users(user_key, user_name, email, password, first_name, last_name, age, location, school, points)
    VALUES(1, "ySharma", "yash@yash.com", "abc123", "Yash", "Sharma", 18, NULL, "UCMerced", 0),
          (2, "bbridi", "bbbbbbbbridi@protonmail.com", "securePassword99", "Busher", NULL, 29, NULL, "UCMerced", 0),
          (3, "psousa", "spam@gmail.com", "theseWillBeHashedEventually", NULL, "Sousa", 21, "San Jose", "UCMerced", 0);

INSERT INTO questions(question_key, category, prompt, correct, wrong1, wrong2, wrong3) 
    VALUES(1, "Science: Computers", "How many values can a single byte represent?", "256", "1024", "1", "8"),
          (2, "Science: Computers", "The programming language Swift was created to replace what other programming language?", "Objective-C", "C++", "C#", "Ruby"),
          (3, "Entertainment: Video Games", "What was the code name for the Nintendo Gamecube?", "Dolphin", "Revolution", "Atlantis", "Nitro");

INSERT INTO question_stats(question_key, total_amt, total_correct, total_first_try_correct)
    VALUES(1, 3, 2, 2),
          (2, 5, 5, 0),
          (3, 10, 4, 2);

INSERT INTO leaderboard(ranking, user_key, points)
    VALUES(1, 1, 1000),
          (2, 3, 601),
          (3, 2, 600);

INSERT INTO friends(user_key, friend_key)
    VALUES(1, 3),
          (2, 3);

INSERT INTO question_history(user_key, question_key)
    VALUES(1, 2),
          (3, 1),
          (3, 2), 
          (3, 3);

-- LOGIN -> Given a username and password, is there a matching user profile
SELECT * FROM users WHERE user_name = "ySharma" AND password = "abc123";

-- SIGN UP
INSERT INTO users(user_key, user_name, email, password, first_name, last_name, age, location, school, points)
    VALUES(4, "ifelsejet", "jet@yahoo.com", "icey", NULL, NULL, 1, NULL, NULL, 0);

-- Getting Top 10 from leaderboard
SELECT * FROM leaderboard LIMIT 10;

-- When a user recieves points -> update user and leaderboard
UPDATE users SET points = points + 5
    WHERE user_key = 2; -- 2 is our input

UPDATE leaderboard SET points = points + 5
    WHERE user_key = 2;

-- Getting all available question categories 
SELECT DISTINCT category FROM questions;

-- Getting a random question
SELECT * FROM questions
ORDER BY random()
LIMIT 1;

-- Getting a random question from a specific category
SELECT * FROM questions
WHERE category = "Science: Computers"
ORDER BY random()
LIMIT 1;

-- Getting a specific question's stats
SELECT * FROM question_stats
WHERE question_key = 2;

--Alternativly, Get a random question with its stats
SELECT * FROM questions
NATURAL JOIN question_stats
ORDER BY random()
LIMIT 1;

    

-- Getting a list of friends
SELECT friend_key FROM friends
WHERE user_key = 1
UNION
SELECT user_key FROM friends
WHERE friend_key = 1;

--Alternativly, getting a list of friends with their info attached
SELECT * FROM friends
JOIN users ON users.user_key = friends.friend_key
WHERE friends.user_key = 3
UNION
SELECT * FROM friends
JOIN users ON users.user_key = friends.user_key
WHERE friend_key = 3;

-- See all questions your friends has done (w/t question info)


