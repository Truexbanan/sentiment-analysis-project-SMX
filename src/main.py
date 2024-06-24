import logging
from utils import load_json
from normalization import preprocess_data
from sentiment_analysis import sentiment_analyzer

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    # Load JSON data
    file_path = "../data/content.json"
    data = load_json(file_path)
    if not data:
        return  # Exit if data is None

    # Preprocess data
    processed_data = preprocess_data(data["index"])

    # For testing:
    for item in processed_data:
        sentiment = sentiment_analyzer(item[1])
        print(f"Index: {item[0]} || Processed Text: {item[1]}\nSentiment: {sentiment}\n")

if __name__ == '__main__':
    main()