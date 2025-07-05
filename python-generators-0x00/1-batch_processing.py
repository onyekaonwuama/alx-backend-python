import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator function that streams users in batches from the user_data table.
    Yields batches of rows, each of size `batch_size`.
    """
    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host="localhost",
        user="root", 
        password="password",
        database="ALX_prodev"
    )
    
    cursor = connection.cursor(dictionary=True)  # Fetch results as dictionaries

    # Execute the query to select all rows from user_data
    cursor.execute("SELECT * FROM user_data")

    # Initialize an empty batch
    batch = []

    # Fetch rows and yield them in batches
    for row in cursor:
        batch.append(row)  # Add the row to the batch
        if len(batch) >= batch_size:
            yield batch  # Yield the current batch
            batch = []  # Reset the batch for the next set of rows

    # Yield any remaining rows in the final batch
    if batch:
        yield batch

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes users in batches, filtering out users older than 25.
    Yields users over 25 in each batch.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                yield user
