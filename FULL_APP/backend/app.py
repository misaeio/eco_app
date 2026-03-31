from flask import Flask, request, jsonify
from flask_cors import CORS
from db_config import get_connection
import bcrypt

app = Flask(__name__)
CORS(app)

# TEST ROUTE
@app.route('/')
def home():
    return "Backend is running!"

# SIGNUP
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed))
        conn.commit()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        return jsonify({"message": "User created", "user_id": user['id']})
    except:
        return jsonify({"error": "Username already exists"})

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

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return jsonify({"message": "Login successful", "user_id": user['id'], "username": user['username']})
    else:
        return jsonify({"error": "Invalid credentials"})

# ADD TASK
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    title = data['task']
    user_id = data['user_id']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO tasks (title, user_id) VALUES (%s, %s)", (title, user_id))
    conn.commit()

    return jsonify({"message": "Task added"})

# GET TASKS
@app.route('/tasks/<int:user_id>', methods=['GET'])
def get_tasks(user_id):
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

if __name__ == '__main__':
    app.run(debug=True)