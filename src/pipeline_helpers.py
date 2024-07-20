from utils.database import (
    initialize_database,
    create_database_tables,
    fetch_prime_minister_data,
    fetch_prime_minister_language,
    fetch_geospatial_data_from_database,
    insert_prime_minister_content,
)
from src.sentiment_pipeline import vader_sentiment_analysis, roberta_sentiment_analysis, analyze_all_models
from utils.database.insert_data import insert_prime_minister_language, insert_geospatial_data_to_database
from utils.general.table_utils import get_table_name_from_user
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

def initialize_and_fetch_data():
    """
    Initialize the database connection, create necessary tables, and fetch the required data.

    @param: None.
    @ret conn: The database connection object.
    @ret cursor: The database cursor object.
    @ret table_name (str): The name of the table.
    @ret prime_minister_data (np.ndarray): Fetched prime minister data.
    @ret language_data (np.ndarray): Fetched language data.
    @ret geospatial_data (np.ndarray): Fetched geospatial data.
    """
    conn, cursor = initialize_database()
    table_name = get_table_name_from_user(cursor)
    create_database_tables(cursor, table_name)
    prime_minister_data, language_data, geospatial_data = fetch_and_store_prime_minister_and_geospatial_data(cursor, table_name)
    return conn, cursor, table_name, prime_minister_data, language_data, geospatial_data

def fetch_and_store_prime_minister_and_geospatial_data(cursor, table_name):
    """
    Fetch the prime minister and geospatial data from the database, and insert
    them into their respective tables.
    
    @param cursor: The database cursor.
    @param table_name (str): The name of the table.
    @ret (tuple): A tuple containing:
        - prime_minister_data (np.ndarray): Fetched prime minister data.
        - language_data (np.ndarray): Fetched language data.
        - geospatial_data (np.ndarray): Fetched geospatial data.
    """
    try:
        data = fetch_prime_minister_data(cursor, table_name)
        language = fetch_prime_minister_language(cursor, table_name)
        insert_prime_minister_language(cursor, data, table_name)
        insert_prime_minister_content(cursor, data, table_name)
        geospatial_data = fetch_geospatial_data_from_database(cursor, table_name)
        insert_geospatial_data_to_database(cursor, geospatial_data, table_name)
    except Exception as e:
        logging.error(f"An error occurred while fetching and inserting data: {e}")
        raise  # Re-raise the exception after logging

    return data, language, geospatial_data

def perform_selected_sentiment_analysis(model, cursor, processed_data, raw_data, table_name):
    """
    Perform sentiment analysis based on the chosen model.

    @param model (int or str): The chosen model number (1 for VADER, 2 for roBERTa, and anything else for all models).
    @param cursor: The database cursor.
    @param processed_data (np.ndarray): The preprocessed data.
    @param raw_data (np.ndarray): The raw data.
    @param table_name (str): The name of the table.
    @ret: None.
    """
    if model == 'q':
        return
    elif model == 1:
        vader_sentiment_analysis(cursor, processed_data, table_name)
    elif model == 2:
        roberta_sentiment_analysis(cursor, raw_data, table_name)
    else:
        analyze_all_models(cursor, processed_data, raw_data, table_name)