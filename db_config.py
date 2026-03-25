import mysql.connector

import mysql.connector

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",              # change if not root
            password="YOUR REAL PASSWORD", # put your MySQL password here, replace "YOUR REAL PASSWORD"
            database="eco_app"        # your database name
        )
        return conn

    except mysql.connector.Error as err:
        print("Database connection failed:", err)
        return None