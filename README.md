# Limulus

Limulus is a simple trivia web app where users can create an account, add friends, and get quized on a variety of categories. Created in Python with Flask for the backend and with ReactJS for the frontend. Our PostgreSQL database is initally seeded using questions from the [Open Trivia Database](https://opentdb.com/)'s API. Created by a duo ([@psousa612](https://github.com/psousa612) && [@BusherBridi](https://github.com/BusherBridi)) of UCM students for the CSE 111 - Database Systems course.

Hosted via Heroku at: https://limulus-react.herokuapp.com/dashboard
(May take a while to load upon first entry, should be pretty quick after that)

---
### File Descriptions
[react-app/](https://github.com/psousa612/Limulus/tree/react-work/react-app) - Normal ReactJS setup. [src/components](https://github.com/psousa612/Limulus/tree/react-work/react-app/src/components) contains all of our components along with their styling (scss) files.

[application.py](https://github.com/psousa612/Limulus/blob/react-work/application.py) - The main Flask file for defining our API endpoints.

[databaseInit.py](https://github.com/psousa612/Limulus/blob/react-work/databaseInit.py) - A utility file that flushes and repopulates the database with random user details, questions, and other related info.

[database_func.py](https://github.com/psousa612/Limulus/blob/react-work/database_func.py) - Another utility file that contains functions for retrieving data from the database. application.py uses this file to get any database data.

### Diagrams
Use Case Diagram:
![Use Case Diagram](https://imgur.com/uePqJo7.png)

ER Diagram:
![ER Diagram](https://i.imgur.com/I0zGWhJ.png)
