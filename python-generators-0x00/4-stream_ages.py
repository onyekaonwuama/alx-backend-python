import mysql.connector

def stream_user_ages():
    """
    Generator function that yields user ages one by one from the user_data table.
    """
    connection = mysql.connector.connect(
        host="localhost",  # The MySQL server host (localhost if running on the same machine)
        user="your_mysql_user",  # Replace with your MySQL username
        password="your_mysql_password",  # Replace with your MySQL password
        database="ALX_prodev"  # Replace with your database name
    )
    
    cursor = connection.cursor(dictionary=True)  # Fetch results as dictionaries

    # Execute the query to select all ages from user_data
    cursor.execute("SELECT age FROM user_data")

    # Yield ages one by one
    for row in cursor:
        yield row['age']
    
    cursor.close()
    connection.close()

def calculate_average_age():
    """
    Calculates the average age of users using the stream_user_ages generator.
    """
    total_age = 0
    count = 0

    # Iterate over the generator to calculate total age and count
    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        return 0

    # Calculate and return the average age
    return total_age / count

# Print the average age of users
print(f"Average age of users: {calculate_average_age()}")
