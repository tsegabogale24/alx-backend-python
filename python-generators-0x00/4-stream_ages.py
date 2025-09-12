#!/usr/bin/python3
seed = __import__('seed')


def stream_user_ages():
    """
    Generator that streams user ages one by one from the database.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:   # Loop 1
        yield row["age"]
    cursor.close()
    connection.close()


def average_age():
    """
    Compute the average age of users using the stream_user_ages generator.
    """
    total_age = 0
    count = 0
    for age in stream_user_ages():  # Loop 2
        total_age += age
        count += 1

    if count == 0:
        print("Average age of users: 0")
    else:
        avg = total_age / count
        print(f"Average age of users: {avg:.2f}")


if __name__ == "__main__":
    average_age()
