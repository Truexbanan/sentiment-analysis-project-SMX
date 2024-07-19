import logging
from utils.database import initialize_database_and_tables, close_connection_to_database
from src.geospatial_analysis import analyze_geospatial
from src.sentiment_pipeline import prompt_model_selection, preprocess_and_store_data
from src.pipeline_helpers import fetch_prime_minister_and_geospatial_data, perform_selected_sentiment_analysis
import time

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

def main():
    """
    Main function to connect to the database, fetch data, preprocess it, analyze its sentiment,
    and store the results. Also performs geospatial analysis.

    @param: None.
    @ret: None.
    """
    start_time = time.time()
    try:
        # Connect to the database and create tables
        conn, cursor = initialize_database_and_tables()

        # Fetch data from the database
        prime_minister_data, language_data, geospatial_data = fetch_prime_minister_and_geospatial_data(cursor)
        if prime_minister_data.size == 0:
            return  # Exit if data is None

        # Preprocess and store the fetched data
        processed_data = preprocess_and_store_data(cursor, prime_minister_data, language_data)

        # Perform sentiment analysis
        model = prompt_model_selection()
        perform_selected_sentiment_analysis(model, cursor, processed_data, prime_minister_data)

        # Perform geospatial analysis
        if model != 'q': # Don't perform if user Quit program
            analyze_geospatial(geospatial_data)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        # Commit changes and close the connection to the database
        close_connection_to_database(conn, cursor)

    total_time = time.time() - start_time
    logging.info(f"Total execution time: {total_time // 60} minutes and {total_time % 60:.2f} seconds.")

if __name__ == '__main__':
    main()