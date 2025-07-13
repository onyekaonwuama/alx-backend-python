import sqlite3
import functools

def transactional(func):
    """Decorator that wraps a database operation in a transaction."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        cursor = conn.cursor()
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit the transaction if successful
            return result
        except Exception as e:
            conn.rollback()  # Rollback the transaction in case of failure
            print(f"Error: {e}")
            raise
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Example usage
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
