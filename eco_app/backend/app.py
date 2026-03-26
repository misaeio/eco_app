from flask import Flask, request, jsonify
from flask_cors import CORS
from db_config import get_connection
import bcrypt

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

#TEST ROUTE
@app.route('/')
def home():
    return "Backend is running!"

#SIGNUP
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cursor.execute(query, (username, hashed))
        conn.commit()
        return jsonify({"message": "User created"})
    except:
        return jsonify({"error": "Username already exists"})

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

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({"message": "Login successful", "user_id": user['id']})
    else:
        return jsonify({"error": "Invalid credentials"})

# ADD TASK (EDITED - AA) # was causing errors in console on webpage - adjusted accordingly 
@app.route('/tasks', methods=['POST'])
def add_task():
    try:
        data = request.get_json()

        if not data or 'task' not in data:
            return jsonify({"error": "No task provided"}), 400

        title = data['task']
        user_id = data.get('user_id', 1)

        conn = get_connection()
        cursor = conn.cursor()

        query = "INSERT INTO tasks (title, user_id) VALUES (%s, %s)"
        cursor.execute(query, (title, user_id))
        conn.commit()

        return jsonify({"message": "Task added"})

    except Exception as e:
        print("ERROR:", e)                  
        return jsonify({"error": str(e)}), 500  
    
#GET TASKS (BY USER)
@app.route('/tasks/<int:user_id>', methods=['GET'])
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
    app.run(debug=True)

