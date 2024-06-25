import logging
import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification
from src.utils import load_json
from src.normalization import preprocess_data
from RobertaToken import tokenize_data
import os
import json

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def process_and_analyze_data(json_file_path):
    # Load JSON data
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    if not data:
        return  # Exit if data is None

    # Preprocess data
    processed_data = preprocess_data(data["index"])

    # Debug: Print the structure and a few entries of processed_data
    print(f"Processed data length: {len(processed_data)}")
    print(f"Sample processed data: {processed_data[:5]}")

    # Convert to DataFrame for easier processing
    try:
        df = pd.DataFrame(processed_data, columns=['id', 'text'])
    except Exception as e:
        print(f"Error creating DataFrame: {e}")
        return

    # Tokenize and create attention masks
    input_ids, attention_masks = tokenize_data(df['text'])

    # Load the model
    MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)

    # Perform model inference
    with torch.no_grad():
        outputs = model(input_ids, attention_mask=attention_masks)

    # Extract the predicted sentiments
    predictions = torch.argmax(outputs.logits, dim=1)

    # Map predictions to sentiment labels
    labels = ["Negative", "Neutral", "Positive"]
    results = [{"index": item[0], "text": item[1], "sentiment": labels[pred]} for item, pred in zip(processed_data, predictions)]

    return results
