#!/usr/bin/python3

import seed

def main():
    # 1️⃣ Connect to MySQL server
    connection = seed.connect_db()
    if connection:
        seed.create_database(connection)
        connection.close()
        print("Connection successful")

    # 2️⃣ Connect to ALX_prodev database
    connection = seed.connect_to_prodev()
    if connection:
        # 3️⃣ Create table
        seed.create_table(connection)
        # 4️⃣ Insert data from CSV
        seed.insert_data(connection, 'user_data.csv')

        # 5️⃣ Stream rows using generator
        print("\nStreaming 5 rows from user_data:")
        row_count = 0
        for row in seed.stream_rows(connection):
            print(row)
            row_count += 1
            if row_count >= 5:
                break

        connection.close()

if __name__ == "__main__":
    main()
