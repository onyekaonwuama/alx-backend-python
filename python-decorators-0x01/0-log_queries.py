import sqlite3
import functools

def log_queries(func):
    """Decorator to log SQL queries before executing them"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from the function arguments
        # Assuming the query is passed as a keyword argument or first positional argument
        query = None
        if 'query' in kwargs:
            query = kwargs['query']
        elif args and isinstance(args[0], str):
            query = args[0]
        
        # Log the query if found
        if query:
            print(f"Executing query: {query}")
        
        # Execute the original function
        return func(*args, **kwargs)
    
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")