"""
sentiment_pipeline.py

This module manages the sentiment analysis pipeline for the sentiment analysis project. 
It includes functions for prompting the user to select a sentiment analysis model, 
preprocessing data, and performing sentiment analysis using VADER and roBERTa models. 
The results of the analysis are then stored in the database.
"""

from src.vader_analysis import vader_analyze_batch
from src.roberta_process_data import roberta_analyze_data
from utils.database.insert_data import insert_processed_content_data, insert_vader_sentiment_data, insert_roberta_sentiment_data, insert_geospatial_data
from src.normalization import preprocess_data

def prompt_model_selection():
    """
    Prompt the user to select a sentiment analysis model.

    @param: None.
    @ret (int or str): The chosen model number (1 for VADER, 2 for roBERTa, and anything else for all models). 'q' to quit.
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

def preprocess_and_store_data(cursor, data, language, table_name):
    """
    Preprocess the data and store the processed data in the database.

    @param cursor: The database cursor.
    @param data (np.ndarray): The raw data to preprocess.
    @param language (np.ndarray): A NumPy array of [id, language] pairs used for language lookup.
    @param table_name (str): The name of the table where the data should be stored.
    @ret (np.ndarray): The processed data.
    """
    processed_data = preprocess_data(data, language)
    insert_processed_content_data(cursor, processed_data, table_name)
    return processed_data

def vader_sentiment_analysis(cursor, processed_data, table_name):
    """
    Perform VADER sentiment analysis and store the results in the database.

    @param cursor: The database cursor.
    @param processed_data (np.ndarray): The processed data to analyze.
    @param table_name (str): The name of the table where the results should be stored.
    @ret: None.
    """
    vader_results = vader_analyze_batch(processed_data)
    insert_vader_sentiment_data(cursor, vader_results, table_name)

def roberta_sentiment_analysis(cursor, data, table_name):
    """
    Perform roBERTa sentiment analysis and store the results in the database.

    @param cursor: The database cursor.
    @param data (np.ndarray): The data to analyze.
    @param table_name (str): The name of the table where the results should be stored.
    @ret: None
    """
    batch_size = 200  # Adjust batch size according to your memory capacity
    roberta_results = []
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        roberta_results.extend(roberta_analyze_data(batch))
    insert_roberta_sentiment_data(cursor, roberta_results, table_name)

def analyze_all_models(cursor, processed_data, data, table_name):
    """
    Perform sentiment analysis using both VADER and roBERTa models and store the results in the database.

    @param cursor: The database cursor.
    @param processed_data (np.ndarray): The preprocessed data for VADER analysis.
    @param data (np.ndarray): The raw data for roBERTa analysis.
    @param table_name (str): The name of the table where the results should be stored.
    @ret: None
    """
    vader_sentiment_analysis(cursor, processed_data, table_name)
    roberta_sentiment_analysis(cursor, data, table_name)