import csv
import mysql.connector

def split_following(data_following):
    try:
        split_data = data_following.strip().split("'")
        account_name = split_data[0].strip()
        return account_name
    except (IndexError, ValueError):
        return None

def split_followers(data_followers):
    try:
        split_data = data_followers.strip().split("'")
        account_name = split_data[0].strip()
        return account_name
    except (IndexError, ValueError):
        return None

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Hhkn3481$",
        database="follow"
    )

def create_tables():
    connection = create_connection()
    cursor = connection.cursor()

    create_following_table = """
    CREATE TABLE IF NOT EXISTS following (
        id INT AUTO_INCREMENT PRIMARY KEY,
        following VARCHAR(255) NOT NULL
    )
    """

    create_followers_table = """
    CREATE TABLE IF NOT EXISTS followers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        followers VARCHAR(255) NOT NULL
    )
    """

    try:
        cursor.execute(create_following_table)
        cursor.execute(create_followers_table)
        connection.commit()
        print("Tables created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating tables: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def insert_data(table, data):
    connection = create_connection()
    cursor = connection.cursor()

    insert_query = f"""
        INSERT INTO {table} ({table})
        VALUES (%s)
    """

    try:
        cursor.execute(insert_query, (data,))
        connection.commit()
        print(f"Record inserted successfully into {table}")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def process_csv_file(file_name, table_name, split_function):
    with open(file_name, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, skipinitialspace=True)
        next(reader)  # Skip header row
        for row in reader:
            if "'s profile picture" not in row[0]:
                continue
            data = row[0]
            account_name = split_function(data)
            if account_name:
                insert_data(table_name, account_name)

def find_non_followers():
    connection = create_connection()
    cursor = connection.cursor()

    query = """
    SELECT following FROM following
    WHERE following NOT IN (SELECT followers FROM followers)
    """

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        print("People you follow who don't follow you back:")
        for row in results:
            print(row[0])
    except mysql.connector.Error as err:
        print(f"Error querying data: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def drop_tables():
    connection = create_connection()
    cursor = connection.cursor()

    drop_following_table = "DROP TABLE IF EXISTS following"
    drop_followers_table = "DROP TABLE IF EXISTS followers"

    try:
        cursor.execute(drop_following_table)
        cursor.execute(drop_followers_table)
        connection.commit()
        print("Tables dropped successfully")
    except mysql.connector.Error as err:
        print(f"Error dropping tables: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Main execution
create_tables()

process_csv_file("following.csv", "following", split_following)
process_csv_file("followers.csv", "followers", split_followers)

find_non_followers()

drop_tables()

print("Program execution complete")