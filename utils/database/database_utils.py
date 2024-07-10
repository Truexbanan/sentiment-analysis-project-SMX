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

def create_sentiment_analysis_table(cursor):
    """
    Create the sentiment analysis results table if it doesn't exist.
    
    @param cursor: A cursor object to execute database commands.
    @ret: None.
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS uk_prime_minister_sentiment_analysis (
        postid INT PRIMARY KEY,
        content TEXT,
        vader_sentiment VARCHAR(10),
        roberta_sentiment VARCHAR(10),
        FOREIGN KEY (postid) REFERENCES uk_prime_minister(postid)
    );
    """
    cursor.execute(create_table_query)

def create_geospatial_analysis_table(cursor):
    """
    Create the geospatial analysis results table if it doesn't exist.
    
    @param cursor: A cursor object to execute database commands.
    @ret: None.
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS uk_prime_minister_geospatial_analysis (
        postid INT PRIMARY KEY,
        longitude DECIMAL NOT NULL,
        latitude DECIMAL NOT NULL,
        location TEXT NOT NULL,
        FOREIGN KEY (postid) REFERENCES uk_prime_minister(postid)
    );
    """
    cursor.execute(create_table_query)

def fetch_post_data_from_database(cursor):
    """
    Fetch data from the database.

    @param: A cursor object to execute database commands.
    @ret: A list of lists formatted as [[index, content], ...].
    """
    cursor.execute("SELECT postid, content FROM uk_prime_minister;")
    data = cursor.fetchall() # Initially stored as a list of tuples

    formatted_data = [[row[0], row[1]] for row in data]
    return formatted_data

def fetch_geospatial_data_from_database(cursor):
    """
    Fetch data relevant to geospatial analysis from the database.

    @param: A cursor object to execute database commands.
    @ret: A list of lists formatted as [[index, content], ...].
    """
    fetch_query = """
        SELECT postid, longitude, latitude, location
        FROM uk_prime_minister
        WHERE longitude IS NOT NULL AND latitude IS NOT NULL AND location IS NOT NULL;
    """
    cursor.execute(fetch_query)
    data = cursor.fetchall()  # This will be a list of tuples
    return [list(row) for row in data]  # Convert each tuple to a list

def insert_geospatial_data_to_database(cursor, data):
    """
    Insert geospatial analysis results into the database.

    @param cursor: A cursor object to execute database commands.
    @param data: A list of lists containing the geospatial data [postid, longitude, latitude, location].
    @ret: None.
    """
    insert_query = """
        INSERT INTO uk_prime_minister_geospatial_analysis (postid, longitude, latitude, location)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (postid) DO UPDATE SET
        longitude = EXCLUDED.longitude,
        latitude = EXCLUDED.latitude,
        location = EXCLUDED.location;
    """
    cursor.executemany(insert_query, data)

def insert_sentiment_data_to_database(cursor, data, sentiment_column):
    """
    Insert sentiment analysis results into the database.

    @param cursor: A cursor object to execute database commands.
    @param data: A list of lists containing the sentiment analysis results.
    @param sentiment_column: The name of the column to insert the sentiment data into.
    @ret: None.
    """
    insert_query = f"""
        INSERT INTO uk_prime_minister_sentiment_analysis (postid, content, {sentiment_column})
        VALUES (%s, %s, %s)
        ON CONFLICT (postid) DO UPDATE SET
        {sentiment_column} = EXCLUDED.{sentiment_column};
    """
    formatted_data = [(item[0], item[1], item[2]) for item in data]
    cursor.executemany(insert_query, formatted_data)

def insert_vader_data_to_database(cursor, data):
    """
    Insert VADER sentiment analysis results into the database.

    @param cursor: A cursor object to execute database commands.
    @param data: A list of lists containing the sentiment analysis results.
    @ret: None.
    """
    insert_sentiment_data_to_database(cursor, data, "vader_sentiment")

def insert_roberta_data_to_database(cursor, data):
    """
    Insert roBERTa sentiment analysis results into the database.

    @param cursor: A cursor object to execute database commands.
    @param data: A list of lists containing the sentiment analysis results.
    @ret: None.
    """
    insert_sentiment_data_to_database(cursor, data, "roberta_sentiment")

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