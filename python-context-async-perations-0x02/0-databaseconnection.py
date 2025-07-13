#!/usr/bin/env python3
"""
Custom class-based context manager for Database connection
"""
import sqlite3


class DatabaseConnection:
    """
    A class-based context manager for handling database connections.
    Automatically opens and closes database connections.
    """
    
    def __init__(self, db_name):
        """
        Initialize the DatabaseConnection with a database name.
        
        Args:
            db_name (str): Name of the database file
        """
        self.db_name = db_name
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        """
        Enter the context manager - establish database connection.
        
        Returns:
            sqlite3.Cursor: Database cursor for executing queries
        """
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            return self.cursor
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager - close database connection.
        
        Args:
            exc_type: Exception type if an exception occurred
            exc_val: Exception value if an exception occurred
            exc_tb: Exception traceback if an exception occurred
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            if exc_type is None:
                # Commit changes if no exception occurred
                self.connection.commit()
            else:
                # Rollback changes if an exception occurred
                self.connection.rollback()
            self.connection.close()
        
        # Return False to propagate any exception
        return False


def create_sample_database():
    """
    Create a sample database with users table for testing.
    """
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                email TEXT UNIQUE NOT NULL
            )
        ''')
        
        # Insert sample data
        sample_users = [
            ('Alice Johnson', 28, 'alice@example.com'),
            ('Bob Smith', 35, 'bob@example.com'),
            ('Charlie Brown', 42, 'charlie@example.com'),
            ('Diana Wilson', 31, 'diana@example.com'),
            ('Eve Davis', 29, 'eve@example.com')
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO users (name, age, email) VALUES (?, ?, ?)
        ''', sample_users)
        
        conn.commit()


def main():
    """
    Main function to demonstrate the DatabaseConnection context manager.
    """
    # Create sample database
    create_sample_database()
    
    # Use the context manager to query the database
    with DatabaseConnection('users.db') as cursor:
        # Execute the query
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        
        # Print the results
        print("Query Results:")
        print("ID | Name          | Age | Email")
        print("-" * 40)
        for row in results:
            print(f"{row[0]:<2} | {row[1]:<12} | {row[2]:<3} | {row[3]}")


if __name__ == "__main__":
    main()