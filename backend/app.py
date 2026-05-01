from flask import Flask, request, jsonify
from flask_cors import CORS
from db_config import get_connection
import bcrypt
import uuid #random string generator for password reset keys
import re #for email pattern validation
from sendgrid import SendGridAPIClient #for sending emails for forgot PW
from sendgrid.helpers.mail import Mail 


app = Flask(__name__)
CORS(app)

# TEST ROUTE
@app.route('/')
def home():
    return "Backend is running!"

# SIGNUP

#validates email format - throws error if the format is off
email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed)
        )
        conn.commit()

        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        return jsonify({
            "message": "User created",
            "user_id": user['id']
        })

    except:
        return jsonify({"error": "Username already exists"})
    
# LOGIN
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Find the user
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if user:
        # Check if password matches
        stored_password = user['password']
        if isinstance(stored_password, str):
            stored_password = stored_password.encode('utf-8')
            
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return jsonify({
                "message": "Login successful",
                "user_id": user['id'],
                "username": user['username']
            }), 200
        else:
            return jsonify({"error": "Invalid password"})
    else:
        
        return jsonify({"error": "User not found"})

# FORGOT PASSWORD ROUTE
@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json() #gets email from user
    email = data.get('username')                  

    if not email or not re.match(email_pattern, email): #ensures email is valid format
        return jsonify({"error": "Valid email is required"})


    #checks to see if email exists in db
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id FROM users WHERE username = %s", (email,))
    user = cursor.fetchone()

        #states link sent even if email doesn't exist (security measure)
    if not user:
        cursor.close()
        conn.close()
        return jsonify({"message": "If your email exists, a reset link has been sent."})

    # Delete old keys for user in db 
    cursor.execute("DELETE FROM password_resets WHERE user_id = %s", (user['id'],))

    # Create new verification key and store in DB (contains timer as well, per normal practice)
    token = str(uuid.uuid4())
    
    cursor.execute(""" #db info and timer 
        INSERT INTO password_resets (user_id, token, expires_at)
        VALUES (%s, %s, DATE_ADD(NOW(), INTERVAL 1 HOUR))
    """, (user['id'], token))

#saves changes and calls sendgrid to do its thing
    conn.commit()
    cursor.close()
    conn.close()
    send_email(email, token)
    return jsonify({"message": "If your email exists, a reset link has been sent."})

# RESET PASSWORD ROUTE
@app.route('/reset-password', methods=['POST'])
def reset_password():
    #get key and new PW from user
    data = request.get_json()
    token = data.get('token')
    new_password = data.get('newPassword')

#error handling for missing input
    if not token or not new_password:
        return jsonify({"error": "Missing token or password"})

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Check if key is valid and not expired
    cursor.execute("""
        SELECT * FROM password_resets 
        WHERE token = %s AND expires_at > NOW()
    """, (token,))
    record = cursor.fetchone()

    if record:
        #hashes new pass, updates user info, deletes key from db, and confirms success to user
        hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("UPDATE users SET password = %s WHERE id = %s", 
                       (hashed, record['user_id']))

        cursor.execute("DELETE FROM password_resets WHERE token = %s", (token,))
        conn.commit()

        cursor.close()
        conn.close()
        return jsonify({"message": "Password updated successfully!"})
    #error handling for invalid/expired key
    else:
        cursor.close()
        conn.close()
        return jsonify({"error": "Invalid or expired key"})


#RESET PASSWORD EMAIL SENDER
def send_email(to_email, token):
    #creates reset link with key attached (user clicks this)
    reset_link = f"http://127.0.0.1:5500/eco_app/FULL_APP/frontend/resetpass.html?token={token}"

#DO NOT CHANGE - handles email sending for forgot pass

    message = Mail(
        from_email="ecoappreset@gmail.com",
        to_emails=to_email,
        subject="Eco App - Password Reset",
        html_content=f"""
            <h2>Reset Your Password</h2>
            <P>Hello from Eco App! We received a request to reset your password.</p>
            <p>Click the link below to reset your password:</p>
            <a href="{reset_link}">Reset Password</a>
            <p>This link will expire in 1 hour.</p>
        """
    )
    try: #DO NOT CHANGE API KEY - WILL BREAK FORGOT PASSWORD FUNCTIONALITY
        sg = SendGridAPIClient("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")
        sg.send(message)
    except Exception as error:
        print("Something went wrong with the email!: " + str(error))

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
