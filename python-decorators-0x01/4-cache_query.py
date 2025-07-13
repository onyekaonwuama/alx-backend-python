import time
import sqlite3
import functools

query_cache = {}

def cache_query(func):
    """Decorator that caches query results."""
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("Using cached result.")
            return query_cache[query]
        else:
            result = func(conn, query, *args, **kwargs)
            query_cache[query] = result  # Cache the result
            return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Example usage
users = fetch_users_with_cache(query="SELECT * FROM users")
users_again = fetch_users_with_cache(query="SELECT * FROM users")
