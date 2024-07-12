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
    db_params = {
        'dbname': os.getenv('DBNAME'),
        'user': os.getenv('USER'),
        'password': os.getenv('PASSWORD'),
        'host': os.getenv('HOST'),
        'port': os.getenv('PORT')
    }
    return psycopg2.connect(**db_params)

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