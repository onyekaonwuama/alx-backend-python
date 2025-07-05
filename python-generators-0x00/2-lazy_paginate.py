import mysql.connector
import sys

def paginate_users(page_size, offset):
    """
    Fetch users from the database based on page size and offset.
    """
    connection = mysql.connector.connect(
        host="localhost",  # The MySQL server host (localhost if running on the same machine)
        user="root",  # Replace with your MySQL username
        password="password",  # Replace with your MySQL password
        database="ALX_prodev"  # Replace with your database name
    )
    cursor = connection.cursor(dictionary=True)  # Fetch results as dictionaries
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_paginate(page_size):
    """
    Lazily fetch pages of users from the database, one page at a time.
    Yields a new page on each iteration.
    """
    offset = 0
    while True:
        # Fetch the next page using the paginate_users function
        page = paginate_users(page_size, offset)
        if not page:
            break  # If the page is empty, stop the loop
        
        yield page  # Yield the current page
        
        offset += page_size  # Move to the next page
