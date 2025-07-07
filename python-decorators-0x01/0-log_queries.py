import sqlite3
import functools

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(query, *args, **kwargs):
        # Log the query before executing it
        print(f"Executing SQL query: {query}")
        return func(query, *args, **kwargs)
    return wrapper

# Function that fetches all users from the database and logs the query
@log_queries
def fetch_all_users(query):
    # Connect to the SQLite database (change to your actual database)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)  # Execute the query
    results = cursor.fetchall()  # Fetch all the results
    conn.close()  # Close the connection
    return results

# Example usage of the decorated function
query = "SELECT * FROM users"
users = fetch_all_users(query)  # This will log the query before executing it
