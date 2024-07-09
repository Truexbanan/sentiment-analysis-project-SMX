import logging
from database_utils import *
from normalization import preprocess_data
from sentiment_analysis import count_sentiments, vader_sentiment_analyzer, vader_sentiment_label
from data_visualization import visualize_sentiment, print_sentiment_analysis
from Roberta_process_data import analyze_data
from geospatial_analysis import geospatial_analyzer

logging.basicConfig(level=logging.ERROR, format='[%(asctime)s] [%(levelname)s] %(message)s')

def main():
    """
    Main function to load data from the database, preprocess it, and analyze its sentiment.

    @param: None.
    @ret: None.
    """
    # Connect to the database
    conn = connect_to_database()
    cursor = conn.cursor()

    # Create the sentiment and geospatial analysis tables if they don't exist
    create_sentiment_analysis_table(cursor)
    create_geospatial_analysis_table(cursor)

    # Fetch data from the database
    data = fetch_post_data_from_database(cursor)
    geospatial_data = fetch_geospatial_data_from_database(cursor)
    if not data:
        return  # Exit if data is None

    # Preprocess data
    processed_data = preprocess_data(data)

    """ SENTIMENT ANALYSIS """
    # Analyze sentiment of preprocessed data
    vader_results = [[item[0], item[1], vader_sentiment_label(vader_sentiment_analyzer(item[1]))] for item in processed_data]
    roberta_results = analyze_data(processed_data)

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