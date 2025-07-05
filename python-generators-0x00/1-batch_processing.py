#!/usr/bin/python3
"""
Batch processing functions using generators for efficient memory usage
"""

import mysql.connector
from mysql.connector import Error


def stream_users_in_batches(batch_size):
    """
    Generator function that yields rows from the user_data table in batches
    Args: batch_size (int) - Number of rows to fetch in each batch
    Yields: list - List of user dictionaries for each batch
    """
    connection = None
    cursor = None
    
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host='localhost',
            user='root', 
            password='password', 
            database='ALX_prodev'
        )
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            
            # Execute query to select all users
            query = "SELECT user_id, name, email, age FROM user_data"
            cursor.execute(query)
            
            # Fetch and yield data in batches
            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch
                
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    
    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25
    Args: batch_size (int) - Number of rows to process in each batch
    """
    # Use the generator to process batches
    for batch in stream_users_in_batches(batch_size):
        # Filter users over age 25 in current batch
        for user in batch:
            if user['age'] > 25:
                print(user)