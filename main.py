import logging
from utils.database import (
    initialize_database_and_tables,
    fetch_prime_minister_data,
    fetch_geospatial_data_from_database,
    insert_prime_minister_content,
    insert_prime_minister_processed_content,
    insert_results_to_database,
    close_connection_to_database
)
from src.normalization import preprocess_data
from src.sentiment_analysis import count_sentiments, vader_analyze_batch
from src.data_visualization import visualize_sentiment, print_sentiment_analysis
from src.roberta_process_data import roberta_analyze_data
from src.geospatial_analysis import analyze_geospatial

import time

logging.basicConfig(level=logging.ERROR, format='[%(asctime)s] [%(levelname)s] %(message)s')

def main():
    """
    Main function to connect and fetch data from the database, preprocess it, analyze its sentiment,
    and store the results. Geospatial analysis is also performed.

    @param: None.
    @ret: None.
    """
    start_time = time.time()
    # Connect to the database and create tables
    conn, cursor = initialize_database_and_tables()
    print(f"Database initialized in {time.time() - start_time:.2f} seconds.")

    # Fetch data from the database
    fetch_start_time = time.time()
    data = fetch_prime_minister_data(cursor)
    insert_prime_minister_content(cursor, data)
    geospatial_data = fetch_geospatial_data_from_database(cursor)
    if data.size == 0:
        close_connection_to_database(conn, cursor)
        print(f"Total execution time: {time.time() - start_time:.2f} seconds.")
        return  # Exit if data is None
    print(f"Fetched data in {time.time() - fetch_start_time:.2f} seconds.")

    # Preprocess data
    preprocess_start_time = time.time()
    processed_data = preprocess_data(data)
    insert_prime_minister_processed_content(cursor, processed_data)
    print(f"Data preprocessed in {time.time() - preprocess_start_time:.2f} seconds.")

    """ SENTIMENT ANALYSIS """
    # Analyze sentiment of preprocessed data
    vader_sentiment_analysis_start_time = time.time()
    vader_results = vader_analyze_batch(processed_data)
    print(f"VADER Sentiment analysis done in {time.time() - vader_sentiment_analysis_start_time:.2f} seconds.")

    # Analyze sentiment of raw data using RoBERTa in batches
    roberta_sentiment_analysis_start_time = time.time()
    batch_size = 200  # Adjust batch size according to your memory capacity
    roberta_results = []
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        roberta_results.extend(roberta_analyze_data(batch))

    print(f"roBERTa Sentiment analysis done in {time.time() - roberta_sentiment_analysis_start_time:.2f} seconds.")

    # Count sentiments for VADER
    vader_sentiment_counts = count_sentiments(vader_results)

    # Insert the results into the database
    insert_start_time = time.time()
    insert_results_to_database(cursor, vader_results, roberta_results, geospatial_data)
    print(f"Data inserted into the database in {time.time() - insert_start_time:.2f} seconds.")

    # Print the sentiment counts for VADER
    print_sentiment_analysis(vader_sentiment_counts)

    # Visualize sentiments in a pie chart for VADER results
    visualize_sentiment(vader_results)

    """ GEOSPATIAL ANALYSIS """
    # Analyze geospatial data
    geospatial_analysis_start_time = time.time()
    analyze_geospatial(geospatial_data)
    print(f"Geospatial analysis done in {time.time() - geospatial_analysis_start_time:.2f} seconds.")

    # Commit changes and close the connection to the database
    close_connection_to_database(conn, cursor)
    print(f"Total execution time: {time.time() - start_time:.2f} seconds.")

if __name__ == '__main__':
    main()