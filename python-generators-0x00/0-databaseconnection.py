import sqlite3

class DatabaseConnection:
    """Custom context manager for handling database connections."""
    
    def __enter__(self):
        """Open the database connection."""
        self.conn = sqlite3.connect('users.db')  # Change to your DB path
        self.cursor = self.conn.cursor()
        return self.cursor  # Return the cursor to interact with the database
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the database connection."""
        if exc_type:
            print(f"An error occurred: {exc_val}")
        self.conn.close()  # Close the connection after the block is executed

# Example usage: Fetch all users
with DatabaseConnection() as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
