import logging
from utils import load_json, save_to_json
from normalization import preprocess_data
from sentiment_analysis import count_sentiments, VADER_sentiment_analyzer, VADER_sentiment_label
from data_visualization import visualize_sentiment, print_sentiment_analysis

logging.basicConfig(level=logging.ERROR, format='[%(asctime)s] [%(levelname)s] %(message)s')

def main():
    """
    Main function to load data, preprocess it, and analyze its sentiment.

    @param: None.
    @ret: None.
    """
    # Load JSON data
    file_path = "../data/content.json"
    data = load_json(file_path)
    if not data:
        return  # Exit if data is None

    # Preprocess data and retrieve duplicates
    processed_data, duplicates = preprocess_data(data["index"])

    # Analyze sentiment of preprocessed data
    results = [[item[0], item[1], VADER_sentiment_label(VADER_sentiment_analyzer(item[1]))] for item in processed_data]

    # Count sentiments
    sentiment_counts = count_sentiments(results)

    # Save the results and duplicates to separate JSON files
    save_to_json({"index": results}, "../data/processed_content.json")
    save_to_json({"index": duplicates}, "../data/duplicates.json")
    
    # Print the sentiment counts
    print_sentiment_analysis(sentiment_counts)

    # Visualize sentiments in a pie chart
    visualize_sentiment(results)

if __name__ == '__main__':
    main()