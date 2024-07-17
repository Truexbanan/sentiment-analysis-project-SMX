from .connection import connect_to_database, close_connection_to_database
from .create_tables import (
    create_prime_minister_content_table,
    create_vader_sentiment_analysis_table,
    create_roberta_sentiment_analysis_table,
    create_geospatial_analysis_table,
    create_prime_minister_processed_content_table
)
from .insert_data import (
    insert_prime_minister_content,
    insert_geospatial_data_to_database,
    insert_vader_data_to_database,
    insert_roberta_data_to_database,
    insert_prime_minister_processed_content,
    insert_results_to_database
)
from .fetch_data import fetch_prime_minister_data, fetch_geospatial_data_from_database

def initialize_database_and_tables():
    """
    Connect to the database and create necessary tables.

    @param: None.
    @ret conn: The connection object to the database.
    @ret cursor: The cursor object to execute database queries.
    """
    conn = connect_to_database()
    cursor = conn.cursor()
    create_prime_minister_content_table(cursor)
    create_prime_minister_processed_content_table(cursor)
    create_vader_sentiment_analysis_table(cursor)
    create_roberta_sentiment_analysis_table(cursor)
    create_geospatial_analysis_table(cursor)
    return conn, cursor