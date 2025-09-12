#!/usr/bin/python3
from seed import connect_to_prodev

def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from user_data table in batches.
    """
    connection = connect_to_prodev()
    if not connection:
        return

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")

    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes each batch and yields users over the age of 25.
    """
    for batch in stream_users_in_batches(batch_size):   # Loop 1: batches
        for user in batch:                              # Loop 2: users in batch
            if user['age'] > 25:                        # Filter condition
                print(user)
