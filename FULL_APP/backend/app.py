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

#CREATE POSTS
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    
    user_id = data['user_id']
    content = data.get('content', " ")
    image_url = data.get('image_url', None)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO posts (user_id, content, image_url)
        VALUES (%s, %s, %s)
    """, (user_id, content, image_url))
    conn.commit()

    return jsonify({"message": "Post Created"})

#GET POSTS
@app.route("/posts", methods=["GET"])
def get_posts():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT 
            posts.id,
            posts.content,
            posts.image_url,
            posts.user_id,
            users.username,
            users.profile_pic
        FROM posts
        JOIN users ON posts.user_id = users.id
        ORDER BY posts.id DESC
    """)

    posts = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(posts)

@app.route('/posts/<int:post_id>/likes', methods=['GET'])
def get_likes(post_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT COUNT(*) as count FROM likes WHERE post_id=%s",
        (post_id,)
    )

    return jsonify(cursor.fetchone())

@app.route('/posts/<int:post_id>/comments', methods=['POST'])
def add_comment(post_id):
    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        INSERT INTO comments (post_id, user_id, comment)
        VALUES (%s, %s, %s)
    """, (post_id, data['user_id'], data['comment']))

    conn.commit()

    return jsonify(cursor.fetchone())

@app.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT comments.comment, users.username
        FROM comments
        JOIN users ON comments.user_id = users.id
        WHERE post_id=%s
        ORDER BY comments.created_at ASC
    """, (post_id,))

    return jsonify(cursor.fetchall())

#GET PROFILE
@app.route("/profile/<int:user_id>")
def get_profile(user_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT id, username, bio, profile_pic, followers_count, following_count
        FROM users
        WHERE id=%s
    """, (user_id,))

    user = cur.fetchone()
    conn.close()

    return jsonify(user)

#MAKE USER PROFILE
app.route('/profile/<int:user_id>', methods = ['PUT'])
def user_profile(user_id):
    data = request.get_json

    username = data['username']
    bio = data['bio']
    profile_pic = data['profile_pic']

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""UPDATE users
                   SET username = %s, bio = %s, profile_pic = %s
                   WHERE id = %s""", 
                   (username, bio, profile_pic, user_id))
    
    conn.commit()

    return jsonify({"message": "Profile Updated"})

#UPDATE PROFILE
@app.route("/profile", methods=["POST"])
def update_profile():
    data = request.get_json()

    user_id = data["user_id"]
    username = data["username"]
    bio = data["bio"]
    profile_pic = data["profile_pic"]

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET username=%s,
            bio=%s,
            profile_pic=%s
        WHERE id=%s
    """, (username, bio, profile_pic, user_id))

    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Profile updated successfully"})

@app.route("/follow", methods=["POST"])
def follow():
    data = request.get_json()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO followers (follower_id, following_id)
        VALUES (%s, %s)
    """, (data["follower_id"], data["following_id"]))

    conn.commit()
    conn.close()

    return jsonify({"message": "Followed"})
    

if __name__ == '__main__':
    app.run(debug=True)
