from .connection import connect_to_database, close_connection_to_database
from .create_tables import (
    create_content_table,
    create_vader_sentiment_table,
    create_roberta_sentiment_table,
    create_geospatial_analysis_table,
    create_processed_content_table,
    create_language_table
)
from .insert_data import (
    insert_content_data,
    insert_processed_content_data,
    insert_language_data,
    insert_geospatial_data,
    insert_vader_sentiment_data,
    insert_roberta_sentiment_data
)
from .fetch_data import fetch_content_data, fetch_language_data, fetch_geospatial_data

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
    create_content_table(cursor, table_name)
    create_processed_content_table(cursor, table_name)
    create_language_table(cursor, table_name)
    create_vader_sentiment_table(cursor, table_name)
    create_roberta_sentiment_table(cursor, table_name)
    create_geospatial_analysis_table(cursor, table_name)