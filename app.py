from flask import Flask, request, jsonify #flask -> web frame work to handle http reuqests, GET/POST 
from flask_cors import CORS #will allow front end to communicate with backend
from db_config import get_connection #gives you database connection
import bcrypt #allows password hashing

app = Flask(__name__) #creates backend server
CORS(app)

#TEST ROUTE
@app.route('/')
def home():
    return "Backend is running!"

#(for any app.route -> connects a URL to the function followed)
#to tell flask what type of request is allowed we use GET POST and DELETE

#SIGNUP
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json() #converts our data to json data so frontend can read
    username = data['username']
    password = data['password']

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) #uses bcrypt to HASH the password (keep secure)

    conn = get_connection()
    cursor = conn.cursor() #this is how we actually modify on mysql

    try:
        query = "INSERT INTO users (username, password) VALUES (%s, %s)" #tries this function 
        cursor.execute(query, (username, hashed))
        conn.commit()
        return jsonify({"message": "User created"})
    except: #if username alr exists jumps here
        return jsonify({"error": "Username already exists"})

#the rest of these functions follow the same principal as the one above

#LOGIN
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return jsonify({"message": "Login successful", "user_id": user['id']})
    else:
        return jsonify({"error": "Invalid credentials"})

#ADD TASK
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    task = data['task']
    user_id = data['user_id']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (task, user_id) VALUES (%s, %s)",
        (task, user_id)
    )
    conn.commit()

    return jsonify({"message": "Task added"})

#GET TASKS (BY USER)
@app.route('/tasks/<int:user_id>', methods=['GET']) #whithout getting task by suer, all data would be combined NOT speccific by user
def get_tasks(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
    tasks = cursor.fetchall()

    return jsonify(tasks)

#DELETE TASK
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()

    return jsonify({"message": "Task deleted"})

if __name__ == '__main__':
    app.run(debug=True) #if this is ran on straight from the code (on terminal) flask names is __main__ if we try to run this outside the code
    #this file will be reffered as "app". its a way to differentiate whether this is ran straight from the code or not.
