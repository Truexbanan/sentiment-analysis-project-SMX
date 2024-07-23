import logging
from utils.database import close_connection_to_database
from src.geospatial_analysis import analyze_geospatial
from src.sentiment_pipeline import prompt_model_selection, preprocess_and_store_data, perform_selected_sentiment_analysis
from src.pipeline_helpers import initialize_and_fetch_data
import time

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

def main():
    """
    Main function to connect to the database, fetch data, preprocess it, analyze its sentiment,
    and store the results. Also performs geospatial plotting.

    @param: None.
    @ret: None.
    """
    start_time = time.time()
    try:
        # Initialize and fetch data
        conn, cursor, table_name, content_data, language_data, geospatial_data = initialize_and_fetch_data()

        if content_data.size == 0:
            return  # Exit if data is None

        # Prompt model selection
        model = prompt_model_selection()
        if model == 'q':
            return  # Exit if user chooses to quit
        
        # Preprocess and store the fetched data
        processed_content_data = preprocess_and_store_data(cursor, content_data, language_data, table_name)

        # Perform sentiment analysis
        results = perform_selected_sentiment_analysis(model, cursor, processed_content_data, content_data, table_name)

        for sentiment_results, model_name in results:
            # Perform geospatial plotting
            analyze_geospatial(geospatial_data, sentiment_results, model_name)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        # Commit changes and close the connection to the database
        close_connection_to_database(conn, cursor)

    total_time = time.time() - start_time
    logging.info(f"Total execution time: {total_time // 60} minutes and {total_time % 60:.2f} seconds.")

if __name__ == '__main__':
    main()