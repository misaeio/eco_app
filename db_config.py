import mysql.connector #allows python to talk to mysql

import mysql.connector

def get_connection(): #defines a function called get connection
                      #will get called if they need to connect to database
    try:
        conn = mysql.connector.connect( #creates the connection to your localhost
            host="localhost",          
            user="root",              # connects to YOUR user... change if not root
            password="YOUR REAL PASSWORD", # using YOUR password... put your MySQL password here, replace "YOUR REAL PASSWORD"
            database="eco_app"        # your database name... the databse shared is eco_app
        )
        return conn

    except mysql.connector.Error as err:
        print("Database connection failed:", err)
        return None
