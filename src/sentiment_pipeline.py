"""
sentiment_pipeline.py

This module manages the sentiment analysis pipeline for the sentiment analysis project. 
It includes functions for prompting the user to select a sentiment analysis model, 
preprocessing data, and performing sentiment analysis using VADER and roBERTa models. 
The results of the analysis are then stored in the database.
"""

from src.vader_analysis import vader_analyze_batch
from src.roberta_process_data import roberta_analyze_data
from utils.database.insert_data import insert_prime_minister_processed_content, insert_vader_data_to_database, insert_roberta_data_to_database
from src.normalization import preprocess_data

def prompt_model_selection():
    """
    Prompt the user to select a sentiment analysis model.

    @ret: The chosen model number (1 for VADER, 2 for roBERTa, and anything else for all models).
    """
    print("""Sentiment Analysis Models:
    1. VADER
    2. Hugging Face's roBERTa
    
    Enter any other key to run all models. To quit, enter `q`
    """)
    user_input = input("Enter the model choice: ").strip().lower()

    if user_input == 'q':
        return 'q'
    elif user_input in ['1', '2']:
        return int(user_input)
    else:
        return 'all'

def preprocess_and_store_data(cursor, data):
    """
    Preprocess the data and store the processed data in the database.

    @param cursor: The database cursor.
    @param data: The raw data to preprocess.
    @ret: The processed data.
    """
    processed_data = preprocess_data(data)
    insert_prime_minister_processed_content(cursor, processed_data)
    return processed_data

def vader_sentiment_analysis(cursor, processed_data):
    """
    Perform VADER sentiment analysis and store the results in the database.

    @param cursor: The database cursor.
    @param data: The processed data to analyze.
    @ret: The VADER sentiment analysis results.
    """
    vader_results = vader_analyze_batch(processed_data)
    insert_vader_data_to_database(cursor, vader_results)
    return vader_results

def roberta_sentiment_analysis(cursor, data):
    """
    Perform roBERTa sentiment analysis and store the results in the database.

    @param cursor: The database cursor.
    @param data: The data to analyze.
    @ret: None.
    """
    batch_size = 200  # Adjust batch size according to your memory capacity
    roberta_results = []
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        roberta_results.extend(roberta_analyze_data(batch))
    insert_roberta_data_to_database(cursor, roberta_results)

def analyze_all_models(cursor, processed_data, data):
    """
    Perform sentiment analysis using both VADER and roBERTa models and store the results in the database.

    @param cursor: The database cursor.
    @param processed_data: The preprocessed data for VADER analysis.
    @param data: The raw data for roBERTa analysis.
    @ret: None.
    """
    vader_sentiment_analysis(cursor, processed_data)
    roberta_sentiment_analysis(cursor, data)