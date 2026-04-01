from flask import Flask, request, jsonify #flask creates web application, requests lets access incming requests, jsonify turns python code into JSON repsonses 
from flask_cors import CORS #CORS allows flask to respond to requests from other domains
from db_config import get_connection
import bcrypt #hashes passwords

app = Flask(__name__) #creates instance of a flask app
CORS(app) #enables CORS

# TEST ROUTE
@app.route('/') #when visiting root URL "/" displays message
def home():
    return "Backend is running!"

# SIGNUP
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json() #reads json from front end
    username = data['username'] 
    password = data['password']

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) #hashes password fro security

    conn = get_connection() #this connects to DB
    cursor = conn.cursor(dictionary=True) #cursor used to execute queries and fetch results, rows returned as python dictionaries so you get row name

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed)) #tries to insert new user
        conn.commit() #commits to it
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,)) #DB auto creates id
        user = cursor.fetchone() #this fetches it
        return jsonify({"message": "User created", "user_id": user['id']}) #return user and id
    except:
        return jsonify({"error": "Username already exists"}) #if error display "Username already exists"

# LOGIN
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')): #encrypts password
        return jsonify({"message": "Login successful", "user_id": user['id'], "username": user['username']})
    else:
        return jsonify({"error": "Invalid credentials"})

# ADD TASK
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json() #gets data from front end user
    title = data['task'] 
    user_id = data['user_id']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO tasks (title, user_id) VALUES (%s, %s)", (title, user_id))
    conn.commit()

    return jsonify({"message": "Task added"})

# GET TASKS
@app.route('/tasks/<int:user_id>', methods=['GET'])
def get_tasks(user_id): #gets task by user ID
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tasks WHERE user_id = %s", (user_id,))
    tasks = cursor.fetchall()

    return jsonify(tasks)

# DELETE TASK
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()

    return jsonify({"message": "Task deleted"})

if __name__ == '__main__': #when ran directy name -> mzin
    app.run(debug=True) #server restarts if you make changes to code, and shows error messages if fail
