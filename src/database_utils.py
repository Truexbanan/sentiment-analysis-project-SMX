import psycopg2
import os
from dotenv import load_dotenv

# This file serves as the conversion from JSON files to storing in the database.

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

def fetch_data_from_database(cursor):
    """
    Fetch data from the database.

    @param: A cursor object to execute database commands.
    @ret: A list of tuples.
    """
    # Fetch the query
    query = "SELECT content FROM uk_prime_minister"

    # Executing the query
    cursor.execute(query)

    return cursor.fetchall()

def insert_data_to_database(cursor, data):
    """
    Insert sentiment analyses results into the database.

    @param: A cursor object to execute database commands.
    @param :A list of tuples containing the sentiment analysis results.
    @ret: None.
    """
    pass

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