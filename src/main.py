import json
import logging

import spacy
import numpy as np
import pandas as pd
import matplotlib
import seaborn as sns

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def load_spacy_model(model_name):
    try:
        return spacy.load(model_name)
    except IOError as e:
        logging.error(f"Error loading spaCy model: {e}")
        return None
    
def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading JSON file: {e}")
        return None

def main():
    # load spaCy model
    nlp = load_spacy_model("en_core_web_lg")
    if not nlp: return

    # load JSON data
    file_path = "data/content.json"
    data = load_json(file_path)
    if not data: return  # exit if data is None

    # retrieve first content
    content = data["index"][0][1]
    print(content)

if __name__ == '__main__':
    main()