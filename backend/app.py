from flask import Flask, request, jsonify
from flask_cors import CORS
from db_config import get_connection
import bcrypt
import uuid #random string generator for password reset keys
import re #for email pattern validation
from sendgrid import SendGridAPIClient #for sending emails for forgot PW
from sendgrid.helpers.mail import Mail
import requests #for openstreetmapapi

app = Flask(__name__)
CORS(app)

# ================= HOME =================
@app.route('/')
def home():
    return "Backend is running!"

email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'

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
        sg = SendGridAPIClient("API KEY HERE") #*************API KEY GOES HERE*****************
        sg.send(message)
    except Exception as error:
        print("Something went wrong with the email!: " + str(error))
# ================= SIGNUP =================
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
    
#login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT * FROM users WHERE username=%s", (data['username'],))
    user = cur.fetchone()

    if not user:
        return jsonify({"error": "User not found"})

    stored = user['password']
    if isinstance(stored, str):
        stored = stored.encode()

    if bcrypt.checkpw(data['password'].encode(), stored):
        return jsonify({
            "user_id": user['id'],
            "username": user['username']
        })

    return jsonify({"error": "Wrong password"})


# posts
@app.route('/posts', methods=['GET'])
def get_posts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT posts.id, posts.user_id, posts.content, posts.image_url,
               users.username, users.profile_pic
        FROM posts
        JOIN users ON posts.user_id = users.id
        ORDER BY posts.id DESC
    """)

    rows = cur.fetchall()

    return jsonify([
        {
            "id": r[0],
            "user_id": r[1],
            "content": r[2],
            "image_url": r[3],
            "username": r[4],
            "profile_pic": r[5]
        }
        for r in rows
    ])


@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO posts (user_id, content, image_url)
        VALUES (%s, %s, %s)
    """, (
        data['user_id'],
        data.get('content', ''),
        data.get('image_url', '')
    ))

    conn.commit()
    return jsonify({"message": "Post created"})


# likes
@app.route('/posts/<int:post_id>/likes', methods=['GET'])
def get_likes(post_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("SELECT COUNT(*) AS count FROM likes WHERE post_id=%s", (post_id,))
    return jsonify(cur.fetchone())


@app.route('/posts/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    data = request.get_json()
    user_id = data['user_id']

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 1 FROM likes
        WHERE post_id=%s AND user_id=%s
    """, (post_id, user_id))

    if cur.fetchone():
        conn.close()
        return jsonify({"message": "already liked"})

    cur.execute("""
        INSERT INTO likes (post_id, user_id)
        VALUES (%s, %s)
    """, (post_id, user_id))

    conn.commit()
    conn.close()

    return jsonify({"message": "liked"})


# comments
@app.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT comments.comment, users.username
        FROM comments
        JOIN users ON comments.user_id = users.id
        WHERE post_id=%s
        ORDER BY comments.created_at ASC
    """, (post_id,))

    return jsonify(cur.fetchall())

#post Comments
@app.route('/posts/<int:post_id>/comments', methods=['POST'])
def add_comment(post_id):
    data = request.get_json()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO comments (post_id, user_id, comment)
        VALUES (%s, %s, %s)
    """, (post_id, data['user_id'], data['comment']))

    conn.commit()
    return jsonify({"message": "comment added"})


# profile
@app.route('/user/<int:user_id>')
def get_user(user_id):
    current_user_id = request.args.get("current_user_id")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT username, bio, profile_pic
        FROM users
        WHERE id=%s
    """, (user_id,))
    user = cur.fetchone()

    cur.execute("SELECT COUNT(*) FROM follows WHERE following_id=%s", (user_id,))
    followers = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM follows WHERE follower_id=%s", (user_id,))
    following = cur.fetchone()[0]

    cur.execute("""
        SELECT 1 FROM follows
        WHERE follower_id=%s AND following_id=%s
    """, (current_user_id, user_id))

    is_following = cur.fetchone() is not None

    return jsonify({
        "username": user[0],
        "bio": user[1],
        "profile_pic": user[2],
        "followers": followers,
        "following": following,
        "is_following": is_following
    })


# follow
@app.route("/follow", methods=["POST"])
def follow():
    data = request.get_json()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO follows (follower_id, following_id)
        VALUES (%s, %s)
    """, (data["follower_id"], data["following_id"]))

    conn.commit()
    conn.close()

    return jsonify({"message": "followed"})


@app.route("/unfollow", methods=["POST"])
def unfollow():
    data = request.get_json()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        DELETE FROM follows
        WHERE follower_id=%s AND following_id=%s
    """, (data["follower_id"], data["following_id"]))

    conn.commit()
    conn.close()

    return jsonify({"message": "unfollowed"})


@app.route('/profile', methods=['POST'])
def update_profile():
    data = request.get_json()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET username=%s, bio=%s, profile_pic=%s
        WHERE id=%s
    """, (data['username'], data['bio'], data['profile_pic'], data['user_id']))

    conn.commit()
    conn.close()

    return jsonify({"message": "updated"})
@app.route('/recycling-centers', methods=['POST'])
def get_recycling_centers():
    # finds 3 recycling centers within 20 miles of zip code
    data = request.get_json()
    zip_code = data.get('zip_code')

    if not zip_code:
        return jsonify({"error": "Zip code is required"}), 400

    url = f"https://nominatim.openstreetmap.org/search?q={zip_code},USA&format=json&limit=1"
    headers = {
        "User-Agent": "EcoApp/1.0",
        "From": "aygonzalez@mail.bradley.edu" #IMPORTANT tag for request from API that gives identifying information
    }

    try:
        response = requests.get(url, headers=headers)
        geo_data = response.json()

        if not geo_data:
            return jsonify({"error": "ZIP code not found. Please review, enter valid ZIP code and try again."}), 404

        lat = float(geo_data[0]["lat"])
        lon = float(geo_data[0]["lon"])

        query = f'[out:json];node["amenity"="recycling"](around:32187,{lat},{lon});out body;' # searches within 20 mile  , 32187 meters is 20 miles
        overpass_response = requests.post(
            "https://overpass.kumi.systems/api/interpreter",
            data=query,
            headers={"Content-Type": "text/plain"}
        )

        centers = []
        for element in overpass_response.json().get("elements", []):
            tags = element.get("tags", {})
            center_lat = element.get("lat")
            center_lon = element.get("lon")

            if center_lat and center_lon:
                name = tags.get("name") or "Recycling Center"
                street = tags.get("addr:street", "")
                city = tags.get("addr:city", "")


                if street and city:
                    address = f"{street}, {city}"
                elif street:
                    address = street
                elif city:
                    address = city
                else:
                    address = "View on Google Maps" # checks whats available to display and displays full address if it can
                maps_url = f"https://www.google.com/maps?q={center_lat},{center_lon}"

                centers.append({
                    "name": name,
                    "address": address,
                    "maps_url": maps_url,
                    "latitude": center_lat,
                    "longitude": center_lon
                })

                if len(centers) >= 3:
                    break

        if not centers:
            return jsonify({"error": "No recycling centers found within 20 miles"}), 404

        return jsonify({
            "centers": centers,
            "zip_code": zip_code
        })

    except Exception as e:
        print(f"Error in recycling centers: {e}")
        return jsonify({"error": "Unable to find recycling centers"}), 500

if __name__ == '__main__':
    app.run(debug=True)
