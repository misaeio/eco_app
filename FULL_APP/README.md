# Eco_App

We believe that our intended app will apply to Community benefits mainly due to the call to action we provide. We plan to set up daily notifications that inspire people to better the environment. Along with this we plan to show nearby resources that encourage people to possibly beat tasks given to them by the app, providing a further drive with a reward(like a game). These tasks will likely range from easy to hard such as getting a walk in or going to a local activity during the day. By providing these resources to people we hope that this gets people out and caring for the environment.

## Description

This application aims to incentivize users to change their habits and be more thoughtful about their actions towards the environment. With the help of notifications through the app, users will be able to stay diligent in the amount of tasks they complete. The tasks will range from more simple activities, such as taking a walk or more complex, like attending a local activity once a week. This app is extremely interactive and allows users to connect with others through social media and show off their sustainable achievements. Additionally, through the app users can stay educated on current events within the environment, helpful tips such as gardening, dreadful impacts of wastefulness, and fun facts to optimize sustainable outcomes. With the application users will be able to see past and current weather/air qualities within your area, along with future weather/air conditions. In the case of a local/national disaster our app will notify you about surrounding concerns in your area. Our application is useful to individuals of all ages, backgrounds, and communities. Climate change is an extremely prevalent issue in our society so, encouraging others to better our environment is more essential than ever. With the use of our group's application there will be a significant increase in sustainable acts and habits.

## Getting Started

flask: Python web framework that handles HTTP requests (uses GET, POST, DELETE)
MySQL: Our database. Stores users, tasks, and locations.
Flask-CORS: Lets our frontend (even if hosted on another domain or port) talk to our backend without security blocks.
bcrypt: Secures user passwords by hashing them instead of storing plain text.

dbconfig.py  - connects our code to mysql anytime we call for the function get_connection(). As it sounds, requests database connection. (line by line explanation on github)

app.py - app = Flask(__name__) creates an instance of the app. 
CORS(app) allows flask server to accept cross origin requests. Front end can talk to back end (flask). Usually requests from one website to another domain BLOCKED. 

@app.route('/')
def home():
    return "Backend is running!" 
This checks if backend is alive by running http://127.0.0.1:5000/

USER SIGN UP (check git for code) 
Accepts username and password from the frontend (POST request).
(POST -> allows us to SEND data to database)
Password is HASHED for security
conn = get_connection() requests connection to database
cursor = conn.cursor() allows us to modify database from python
Try and exception handlers give us feed back in json message for frontend use to know if user sign up was successful or not

USER LOG IN 
Follows the same principle as sign up.
cursor.execute("SELECT * FROM users WHERE username = %s", (username,)) - cursor allows us to modify database or get info from it. In this case its fetching data from the table “users” where the info matches the given username.
user = cursor.fetchone() -  fetchone()  retrieves first row of table is it matches

ADD TASK 
data = request.get_json() - get jason turns JSON data into something our backend can read. Basically translating front end language to backend language
Conn.commit commits changes in data base
Jsonify is the reverse of get_json. Turns backend language to frontend so user can read it
Everything else follows the same concepts as the previous functions

GET TASKS
conn = get_connection() requests connection to database
cursor = conn.cursor() allows us to modify database from python
Dictionary = true - means that the results you get back will be in dictionary form, instead of a plain list or tuple.
fetchall() gets all info from query

DELETE TASK 
Deletes a task

## How to run

HOW TO RUN THE CODE
git clone <repo-url>
cd <repo-folder>
Or copy and paste all the code from git to your own python ide

INSTALL PYTHON AND DEPENDENCIES
RUN: 
pip install -r req_dependencies.txt 


SET UP MYSQL DATABASE (download mysql if you havent) 
Open MySQL (MySQL Workbench, terminal, or whatever you use).
Run the SQL script (eco_app.sql) or the SQL commands in your dump file to create the database and tables:
CREATE DATABASE IF NOT EXISTS eco_app;
USE eco_app;
(if you have trouble making this db let MISA know i can help)

Then create tables (users, tasks, locations) and insert default data
Make sure the credentials in db_configg.py match your MySQL username/password.

RUN BACKEND 
Once everything is prepped you can run 
python app.py in your VSCODE terminal or equivalent
Test that the backend is running by visiting 
http://127.0.0.1:5000/
You should see ‘Backend Is Running!’

### Executing program

TEST ROUTES (GET/POST/DELETE)
Run this in terminal WHILE app.py is running. Open a different terminal btw

SIGNUP
Invoke-RestMethod -Method POST http://127.0.0.1:5000/signup `
-Headers @{"Content-Type"="application/json"} `
-Body '{"username":"misael","password":"1234"}'

LOGIN 
Invoke-RestMethod -Method POST http://127.0.0.1:5000/login `
-Headers @{"Content-Type"="application/json"} `
-Body '{"username":"misael","password":"1234"}'

ADD TASK 
Invoke-RestMethod -Method POST http://127.0.0.1:5000/tasks `
-Headers @{"Content-Type"="application/json"} `
-Body '{"task":"Pick up trash","user_id":1}'

GET TASK FROM USER 
Invoke-RestMethod -Method GET http://127.0.0.1:5000/tasks/1

DELETE TASK 
Invoke-RestMethod -Method DELETE http://127.0.0.1:5000/tasks/1

## Authors

#### misaeio
#### Aaron-A-99
#### acechols
#### Lubert101
#### Ryan
#### Adrian
