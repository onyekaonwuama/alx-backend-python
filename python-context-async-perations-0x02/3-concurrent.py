#!/usr/bin/env python3
"""
Concurrent Asynchronous Database Queries
"""
import asyncio
import aiosqlite


async def async_fetch_users():
    """
    Asynchronously fetch all users from the database.
    
    Returns:
        list: All users in the database
    """
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            return results


async def async_fetch_older_users():
    """
    Asynchronously fetch users older than 40 from the database.
    
    Returns:
        list: Users older than 40
    """
    async with aiosqlite.connect('users.db') as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            return results


async def fetch_concurrently():
    """
    Execute both queries concurrently using asyncio.gather().
    """
    print("Starting concurrent database queries...")
    
    # Use asyncio.gather to run both queries concurrently
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
    # Display results
    print("All Users:")
    print("ID | Name          | Age | Email")
    print("-" * 45)
    for user in all_users:
        print(f"{user[0]:<2} | {user[1]:<12} | {user[2]:<3} | {user[3]}")
    
    print("\n" + "="*50)
    print("Users older than 40:")
    print("ID | Name          | Age | Email")
    print("-" * 45)
    for user in older_users:
        print(f"{user[0]:<2} | {user[1]:<12} | {user[2]:<3} | {user[3]}")
    
    return all_users, older_users


async def create_sample_database():
    """
    Create a sample database with users table for testing.
    """
    async with aiosqlite.connect('users.db') as db:
        # Create users table
        await db.execute('''
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
            ('Jack Turner', 33, 'jack@example.com'),
            ('Karen White', 41, 'karen@example.com'),
            ('Leo Garcia', 44, 'leo@example.com'),
            ('Maria Rodriguez', 39, 'maria@example.com'),
            ('Nathan Brown', 47, 'nathan@example.com'),
            ('Olivia Taylor', 25, 'olivia@example.com')
        ]
        
        await db.executemany('''
            INSERT OR IGNORE INTO users (name, age, email) VALUES (?, ?, ?)
        ''', sample_users)
        
        await db.commit()


async def main():
    """
    Main asynchronous function to demonstrate concurrent database queries.
    """
    # Create sample database
    await create_sample_database()
    
    # Run concurrent fetch operations
    await fetch_concurrently()


if __name__ == "__main__":
    # Use asyncio.run to run the concurrent fetch
    asyncio.run(main())