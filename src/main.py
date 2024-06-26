import logging
from utils import load_json, save_to_json
from normalization import preprocess_data
from sentiment_analysis import sentiment_results_and_counter

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

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

    # Analyze and count sentiments
    sentiment_counts, results = sentiment_results_and_counter(processed_data)

    # Save the results and duplicates to separate JSON files
    save_to_json(results, "../data/processed_content.json")
    save_to_json({"index": duplicates}, "../data/duplicates.json") # check if correct !!!!!!!!!!!!!!!!!!!

    # Print the sentiment counts
    print("Sentiment Counts:")
    print(f"Positive: {sentiment_counts['positive']}")
    print(f"Negative: {sentiment_counts['negative']}")
    print(f"Neutral: {sentiment_counts['neutral']}")

if __name__ == '__main__':
    main()