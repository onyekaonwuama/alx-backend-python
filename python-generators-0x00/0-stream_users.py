import mysql.connector

def stream_users():
    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host="localhost",
        user="root", 
        password="password",  
        database="ALX_prodev"  
    )
    
    cursor = connection.cursor(dictionary=True)  # Fetch results as dictionaries

    # Execute the query to select all rows from user_data
    cursor.execute("SELECT * FROM user_data")

    # Yield each row one by one using a generator
    for row in cursor:
        yield row
    
    cursor.close()
    connection.close()
