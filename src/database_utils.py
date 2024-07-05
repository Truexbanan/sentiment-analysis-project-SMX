import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

def connect_to_database():
    """
    Establish a connection to the database.

    @param: None.
    @ret: A connection object to interact with the PostgreSQL database.
    """
    # Database connection parameters
    db_params = {
        'dbname': os.getenv('DBNAME'),
        'user': os.getenv('USER'),
        'password': os.getenv('PASSWORD'),
        'host': os.getenv('HOST'),
        'port': os.getenv('PORT') 
    }

    # Establishing the connection to the database
    return psycopg2.connect(**db_params)

def create_table(cursor):
    """
    Create the sentiment analysis results table if it doesn't exist.
    
    @param cursor: A cursor object to execute database commands.
    @ret: None.
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS uk_prime_minister_sentiment (
        content_id SERIAL PRIMARY KEY,
        content TEXT,
        sentiment VARCHAR(10)
    );
    """
    cursor.execute(create_table_query)

def fetch_data_from_database(cursor):
    """
    Fetch data from the database.

    @param: A cursor object to execute database commands.
    @ret: A list of lists formatted as [[index, content], ...].
    """
    cursor.execute("SELECT content FROM uk_prime_minister;")
    data = cursor.fetchall() # Initially stored as a list of tuples

    cursor.execute("SELECT MAX(content_id) FROM uk_prime_minister_sentiment;")
    max_index_result = cursor.fetchone()
    start_index = max_index_result[0] + 1 if max_index_result[0] is not None else 1

    formatted_data = [[start_index + idx, row[0]] for idx, row in enumerate(data)]
    return formatted_data

def insert_data_to_database(cursor, data):
    """
    Insert sentiment analyses results into the database.

    @param cursor: A cursor object to execute database commands.
    @param data: A list of lists containing the sentiment analysis results.
    @ret: None.
    """
    insert_query = """
        INSERT INTO uk_prime_minister_sentiment (content_id, content, sentiment)
        VALUES (%s, %s, %s);
    """
    formatted_data = [(item[0], item[1], item[2]) for item in data]
    cursor.executemany(insert_query, formatted_data)

def close_connection_to_database(conn, cursor):
    """
    Commit changes and close the connection to the database.

    @param conn: A connection object to the database.
    @param cursor: A cursor object to execute database commands.
    @ret: None.
    """
    conn.commit()
    cursor.close()
    conn.close()