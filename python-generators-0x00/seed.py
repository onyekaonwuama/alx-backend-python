import mysql.connector
import csv

# 1. Connect to the MySQL server
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="password",
            port = 3306  
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# 2. Create the database if it doesn't exist
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

# 3. Connect to the ALX_prodev database
def connect_to_prodev():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="ALX_prodev",
        port = 3306
    )
    return connection

# 4. Create the user_data table if it doesn't exist
def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,  -- Use CHAR(36) for UUIDs as strings
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL
    )
    """)
    connection.commit()
    cursor.close()

# 5. Insert data from CSV into the user_data table
def insert_data(connection, data):
    cursor = connection.cursor()
    with open(data, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row if CSV has one
        for row in reader:
            cursor.execute("""
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE name=VALUES(name), email=VALUES(email), age=VALUES(age)
            """, (row[0], row[1], row[2], row[3]))
    connection.commit()
    cursor.close()

# 6. Generator to stream rows from the database
def stream_rows(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row  # Yielding each row one by one
    cursor.close()
