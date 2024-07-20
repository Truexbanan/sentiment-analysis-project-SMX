from .connection import connect_to_database, close_connection_to_database
from .create_tables import (
    create_prime_minister_content_table,
    create_vader_sentiment_analysis_table,
    create_roberta_sentiment_analysis_table,
    create_geospatial_analysis_table,
    create_prime_minister_processed_content_table,
    create_prime_minister_language_table
)
from .insert_data import (
    insert_prime_minister_content,
    insert_prime_minister_processed_content,
    insert_prime_minister_language,
    insert_geospatial_data_to_database,
    insert_vader_data_to_database,
    insert_roberta_data_to_database
)
from .fetch_data import fetch_prime_minister_data, fetch_prime_minister_language, fetch_geospatial_data_from_database

def initialize_database():
    """
    Connect to the database.

    @param: None.
    @ret conn (object): The connection object to the database.
    @ret cursor (object): The cursor object to execute database queries.
    """
    conn = connect_to_database()
    cursor = conn.cursor()
    return conn, cursor

def create_database_tables(cursor, table_name):
    """
    Create all necessary tables in the database.

    @param cursor (object): A cursor object to execute database commands.
    @param table_name (str): The name of the table to use for creating other tables.
    @ret: None.
    """
    create_prime_minister_content_table(cursor, table_name)
    create_prime_minister_processed_content_table(cursor, table_name)
    create_prime_minister_language_table(cursor, table_name)
    create_vader_sentiment_analysis_table(cursor, table_name)
    create_roberta_sentiment_analysis_table(cursor, table_name)
    create_geospatial_analysis_table(cursor, table_name)