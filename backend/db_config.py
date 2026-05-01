import mysql.connector #allows python to talk to mysql

import mysql.connector

def get_connection(): #defines a function called get connection
                      #will get called if they need to connect to database
   #CONNECTED TO CLOUD DB (NON-LOCAL) 
    try:
        conn = mysql.connector.connect( #creates the connection to your localhost
            host="mysql-2f405199-ecoapp3902026.a.aivencloud.com",
            port=24568,
            user="avnadmin",
            password="DBPASSHERE",
            database="eco_app",
            ssl_disabled=False  # keep False because SSL is REQUIRED
        )
        
        return conn

    except mysql.connector.Error as err:
        print("Database connection failed:", err)
        return None