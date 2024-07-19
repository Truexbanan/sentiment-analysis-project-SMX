from utils.database import (
    fetch_prime_minister_data,
    fetch_prime_minister_language,
    fetch_geospatial_data_from_database,
    insert_prime_minister_content,
)
from src.sentiment_pipeline import vader_sentiment_analysis, roberta_sentiment_analysis, analyze_all_models
from utils.database.insert_data import insert_geospatial_data_to_database
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

def fetch_prime_minister_and_geospatial_data(cursor):
    """
    Fetch the prime minister and geospatial data from the database.
    
    @param cursor: The database cursor.
    @return: Tuple of prime minister data, language data, and geospatial data.
    """
    try:
        data = fetch_prime_minister_data(cursor)
        language = fetch_prime_minister_language(cursor)
        geospatial_data = fetch_geospatial_data_from_database(cursor)
        
        # Insert data into the database
        insert_geospatial_data_to_database(cursor, geospatial_data)
        insert_prime_minister_content(cursor, data)
        
    except Exception as e:
        logging.error(f"An error occurred while fetching and inserting data: {e}")
        raise  # Re-raise the exception after logging

    return data, language, geospatial_data

def perform_selected_sentiment_analysis(model, cursor, processed_data, raw_data):
    """
    Perform sentiment analysis based on the chosen model.

    @param model: The chosen model number.
    @param cursor: The database cursor.
    @param processed_data: The preprocessed data.
    @param raw_data: The raw data.
    @ret: None.
    """
    if model == 'q':
        return
    elif model == 1:
        vader_sentiment_analysis(cursor, processed_data)
    elif model == 2:
        roberta_sentiment_analysis(cursor, raw_data)
    else:
        analyze_all_models(cursor, processed_data, raw_data)