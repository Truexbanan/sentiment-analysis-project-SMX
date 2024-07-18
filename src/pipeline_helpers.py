from utils.database import (
    fetch_prime_minister_data,
    fetch_geospatial_data_from_database,
    insert_prime_minister_content,
)
from src.sentiment_pipeline import vader_sentiment_analysis, roberta_sentiment_analysis, analyze_all_models

def fetch_prime_minister_and_geospatial_data(cursor):
    """
    Fetch the prime minister and geospatial data from the database.
    
    @param cursor: The database cursor.
    @ret: Tuple of prime minister data and geospatial data.
    """
    data = fetch_prime_minister_data(cursor)
    geospatial_data = fetch_geospatial_data_from_database(cursor)
    insert_prime_minister_content(cursor, data)
    return data, geospatial_data

def perform_selected_sentiment_analysis(model, cursor, processed_data, raw_data):
    """
    Perform sentiment analysis based on the chosen model.

    @param model: The chosen model number.
    @param cursor: The database cursor.
    @param processed_data: The preprocessed data.
    @param raw_data: The raw data.
    @ret: None.
    """
    if model == 1:
        vader_sentiment_analysis(cursor, processed_data)
    elif model == 2:
        roberta_sentiment_analysis(cursor, raw_data)
    else:
        analyze_all_models(cursor, processed_data, raw_data)