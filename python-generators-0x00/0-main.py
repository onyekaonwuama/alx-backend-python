#!/usr/bin/python3

seed = __import__('seed')

# Step 1: Connect to the MySQL server
connection = seed.connect_db()
if connection:
    # Step 2: Create the database if it doesn't exist
    seed.create_database(connection)
    connection.close()
    print(f"Connection successful")

    # Step 3: Connect to the ALX_prodev database
    connection = seed.connect_to_prodev()

    if connection:
        # Step 4: Create the user_data table if it doesn't exist
        seed.create_table(connection)

        # Step 5: Insert data from CSV into the table
        seed.insert_data(connection, 'user_data.csv')

        # Step 6: Verify the database and table existence
        cursor = connection.cursor()
        cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print(f"Database ALX_prodev is present")

        # Step 7: Fetch and print some rows from the table
        cursor.execute(f"SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print(rows)
        cursor.close()
