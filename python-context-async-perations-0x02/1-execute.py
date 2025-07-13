#!/usr/bin/env python3
"""
Reusable Query Context Manager
"""
import sqlite3


class ExecuteQuery:
    """
    A reusable context manager that takes a query as input and executes it,
    managing both connection and query execution.
    """
    
    def __init__(self, db_name, query, params=None):
        """
        Initialize the ExecuteQuery context manager.
        
        Args:
            db_name (str): Name of the database file
            query (str): SQL query to execute
            params (tuple, optional): Parameters for the query
        """
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None
        self.results = None
    
    def __enter__(self):
        """
        Enter the context manager - establish connection and execute query.
        
        Returns:
            list: Results of the executed query
        """
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            
            # Execute the query with parameters
            self.cursor.execute(self.query, self.params)
            self.results = self.cursor.fetchall()
            
            return self.results
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
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
        
        # Insert sample data with various ages
        sample_users = [
            ('Alice Johnson', 28, 'alice@example.com'),
            ('Bob Smith', 35, 'bob@example.com'),
            ('Charlie Brown', 42, 'charlie@example.com'),
            ('Diana Wilson', 31, 'diana@example.com'),
            ('Eve Davis', 29, 'eve@example.com'),
            ('Frank Miller', 45, 'frank@example.com'),
            ('Grace Lee', 22, 'grace@example.com'),
            ('Henry Clark', 38, 'henry@example.com'),
            ('Ivy Adams', 26, 'ivy@example.com'),
            ('Jack Turner', 33, 'jack@example.com')
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO users (name, age, email) VALUES (?, ?, ?)
        ''', sample_users)
        
        conn.commit()


def main():
    """
    Main function to demonstrate the ExecuteQuery context manager.
    """
    # Create sample database
    create_sample_database()
    
    # Use the ExecuteQuery context manager with the specified query
    query = "SELECT * FROM users WHERE age > ?"
    age_threshold = 25
    
    with ExecuteQuery('users.db', query, (age_threshold,)) as results:
        print(f"Users older than {age_threshold}:")
        print("ID | Name          | Age | Email")
        print("-" * 45)
        for row in results:
            print(f"{row[0]:<2} | {row[1]:<12} | {row[2]:<3} | {row[3]}")
    
    # Demonstrate with different parameters
    print("\n" + "="*50)
    
    query2 = "SELECT * FROM users WHERE age > ?"
    age_threshold2 = 30
    
    with ExecuteQuery('users.db', query2, (age_threshold2,)) as results:
        print(f"Users older than {age_threshold2}:")
        print("ID | Name          | Age | Email")
        print("-" * 45)
        for row in results:
            print(f"{row[0]:<2} | {row[1]:<12} | {row[2]:<3} | {row[3]}")


if __name__ == "__main__":
    main()