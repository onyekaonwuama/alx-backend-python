#!/usr/bin/env python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator function that streams users in batches from the user_data table.
    Yields batches of rows, each of size `batch_size`.
    """
    connection = None
    cursor = None
    
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="ALX_prodev"
        )
        
        cursor = connection.cursor(dictionary=True)
        # Execute the query to select all rows from user_data
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        
        # Fetch all rows first
        rows = cursor.fetchall()
        
        # Initialize an empty batch
        batch = []
        # Loop 1: Process rows and yield them in batches
        for row in rows:
            batch.append(row)
            if len(batch) >= batch_size:
                yield batch
                batch = []
        
        # Yield any remaining rows in the final batch
        if batch:
            yield batch
            
    except Exception:
        pass
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    Processes users in batches, filtering and printing users older than 25.
    """
    # Loop 2: Process each batch
    for batch in stream_users_in_batches(batch_size):
        # Loop 3: Filter users over 25 in each batch
        for user in batch:
            if user['age'] > 25:
                print(user)