import logging
from utils.database import initialize_database, create_database_tables, close_connection_to_database
from src.geospatial_analysis import analyze_geospatial
from src.sentiment_pipeline import prompt_model_selection, preprocess_and_store_data, insert_to_all_tables
from src.pipeline_helpers import fetch_prime_minister_and_geospatial_data, perform_selected_sentiment_analysis
from utils.general.table_utils import get_table_name_from_user
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
        # Connect to the database
        conn, cursor = initialize_database()

        # Get and validate table name from user
        table_name = get_table_name_from_user(cursor)

        # Create database tables
        create_database_tables(cursor, table_name)

        # Fetch data from the database
        prime_minister_data, language_data, geospatial_data = fetch_prime_minister_and_geospatial_data(cursor, table_name)
        if prime_minister_data.size == 0:
            return  # Exit if data is None

        # Prompt model selection
        model = prompt_model_selection()

        if model != 'q': # Don't perform if user Quit program
            # Preprocess and store the fetched data
            processed_data = preprocess_and_store_data(cursor, prime_minister_data, language_data, table_name)

            insert_to_all_tables(cursor, prime_minister_data, language_data, geospatial_data, table_name)

            # Perform sentiment analysis
            perform_selected_sentiment_analysis(model, cursor, processed_data, prime_minister_data, table_name)

            # Perform geospatial analysis
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