import logging
from utils.database.database_utils import (
    initialize_database_and_tables,
    fetch_post_data_from_database,
    fetch_geospatial_data_from_database,
    insert_geospatial_data_to_database,
    insert_vader_data_to_database,
    insert_roberta_data_to_database,
    close_connection_to_database
)
from src.normalization import preprocess_data
from src.sentiment_analysis import count_sentiments, vader_sentiment_analyzer, vader_sentiment_label
from src.data_visualization import visualize_sentiment, print_sentiment_analysis
from src.roberta_process_data import roberta_analyze_data
from src.geospatial_analysis import geospatial_analyzer

logging.basicConfig(level=logging.ERROR, format='[%(asctime)s] [%(levelname)s] %(message)s')

def main():
    """
    Main function to load data from the database, preprocess it, and analyze its sentiment.

    @param: None.
    @ret: None.
    """
    # Connect to the database and create tables
    conn, cursor = initialize_database_and_tables()

    # Fetch data from the database
    data = fetch_post_data_from_database(cursor)
    geospatial_data = fetch_geospatial_data_from_database(cursor)
    if not data:
        close_connection_to_database(conn, cursor)
        return  # Exit if data is None

    # Preprocess data
    processed_data = preprocess_data(data)

    """ SENTIMENT ANALYSIS """
    # Analyze sentiment of preprocessed data
    vader_results = [[item[0], item[1], vader_sentiment_label(vader_sentiment_analyzer(item[1]))] for item in processed_data]
    roberta_results = roberta_analyze_data(processed_data)

    # Count sentiments for VADER
    vader_sentiment_counts = count_sentiments(vader_results)

    # Insert the results into the database
    insert_vader_data_to_database(cursor, vader_results)
    insert_roberta_data_to_database(cursor, roberta_results)
    insert_geospatial_data_to_database(cursor, geospatial_data)

    # Print the sentiment counts for VADER
    print_sentiment_analysis(vader_sentiment_counts)

    # Visualize sentiments in a pie chart for VADER results
    visualize_sentiment(vader_results)

    """ GEOSPATIAL ANALYSIS """
    # Analyze geospatial data
    geospatial_analyzer(geospatial_data)

    # Commit changes and close the connection to the database
    close_connection_to_database(conn, cursor)

if __name__ == '__main__':
    main()