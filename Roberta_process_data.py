import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification
from src.utils import load_json
from src.normalization import preprocess_data
from RobertaToken import tokenize_data
import os
import json

#This is func to be called in main.py that takes in a json file path 
# returns a  a list of dictionaries containing the index, processed text, and sentiment 

def process_and_analyze_data(json_file_path):
    # Load JSON data
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    if not data:
        return  # Exit if data is None

    # Preprocess data
    processed_data = preprocess_data(data["index"])

    # Convert to DataFrame
    df = pd.DataFrame(processed_data, columns=['id', 'text'])

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
