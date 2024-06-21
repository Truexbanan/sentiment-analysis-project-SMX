import spacy
import numpy as np
import pandas as pd
import matplotlib
import seaborn as sns
import json
import logging

def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def main():
    # load spaCy model
    nlp = spacy.load("en_core_web_lg")

    # load JSON data
    file_path = "content.json"
    data = load_json(file_path)

    # retrieve first content
    content = data["index"][0][1]
    print(content)

if __name__ == '__main__':
    main()