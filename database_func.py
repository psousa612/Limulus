import requests

#Get questions from Open Trivia DB
response = requests.get("https://opentdb.com/api.php?amount=20&category=18&type=multiple")
results = response.json()["results"]
for row in results:
    print(row["question"])
    print("-----------------")

#Store questions here, call more links for different questions

#Math questions: https://opentdb.com/api.php?amount=20&category=19&type=multiple
#Science: Gadget: https://opentdb.com/api.php?amount=10&category=30&type=multiple
#Video Games:  https://opentdb.com/api.php?amount=10&category=15&type=multiple

