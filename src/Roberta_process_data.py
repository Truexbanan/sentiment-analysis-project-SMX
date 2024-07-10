import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification
from utils.json.json_utils import load_json
from src.normalization import preprocess_data
from src.roberta_token import tokenize_data
import os
import json


class DataFrameCreationError(Exception):
    pass

def create_dataframe(processed_data):
    try:
        df = pd.DataFrame(processed_data, columns=['id', 'text'])
        return df
    except Exception as e:
        print(f"Error creating DataFrame: {e}")
        raise DataFrameCreationError(f"Failed to create DataFrame: {e}")



#This is func to be called in main.py that takes in a json file path 
# returns a  a list of dictionaries containing the index, processed text, and sentiment 

def analyze_data(processed_data):
    # Convert to DataFrame for easier processing
    try:
        df = create_dataframe(processed_data)
    except DataFrameCreationError as e:
        print(e)
        return

    # Tokenize and create attention masks
    input_ids, attention_masks = tokenize_data(df['text'])

    # Load the model
    MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_masks)

    # Extract the predicted sentiments
    predictions = torch.argmax(outputs.logits, dim=1)

    # Map predictions to sentiment labels
    labels = ["Negative", "Neutral", "Positive"]
    results = [{"index": item[0], "text": item[1], "sentiment": labels[pred]} for item, pred in zip(processed_data, predictions)]

    return results
