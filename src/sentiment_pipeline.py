from src.vader_analysis import vader_analyze_batch
from src.roberta_process_data import roberta_analyze_data
from utils.database.insert_data import insert_preprocessed_content_data, insert_vader_sentiment_data, insert_roberta_sentiment_data
from src.normalization import preprocess_data

def preprocess_and_store_data(cursor, data, language, table_name):
    """
    Preprocess the data and store the preprocessed data in the database.

    @param cursor (object): The database cursor.
    @param data (np.ndarray): The raw data to preprocess.
    @param language (np.ndarray): A NumPy array of [id, language] pairs used for language lookup.
    @param table_name (str): The name of the table where the data should be stored.
    @ret (np.ndarray): The preprocessed data.
    """
    preprocessed_data = preprocess_data(data, language)
    insert_preprocessed_content_data(cursor, preprocessed_data, table_name)
    return preprocessed_data

def vader_sentiment_analysis(cursor, preprocessed_data, table_name):
    """
    Perform VADER sentiment analysis and store the results in the database.

    @param cursor (object): The database cursor.
    @param preprocessed_data (np.ndarray): The preprocessed data to analyze.
    @param table_name (str): The name of the table where the results should be stored.
    @ret (np.ndarray): The VADER sentiment analysis results.
    """
    vader_results = vader_analyze_batch(preprocessed_data)
    insert_vader_sentiment_data(cursor, vader_results, table_name)
    return vader_results

def roberta_sentiment_analysis(cursor, data, table_name):
    """
    Perform RoBERTa sentiment analysis and store the results in the database.

    @param cursor (object): The database cursor.
    @param data (np.ndarray): The data to analyze.
    @param table_name (str): The name of the table where the results should be stored.
    @ret (list of lists): The RoBERTa sentiment analysis results.
    """
    batch_size = 200  # Adjust batch size according to your memory capacity
    roberta_results = []
    for i in range(0, len(data), batch_size):
        batch = data[i:i+batch_size]
        roberta_results.extend(roberta_analyze_data(batch))
    insert_roberta_sentiment_data(cursor, roberta_results, table_name)
    return roberta_results

def analyze_all_models(cursor, preprocessed_data, data, table_name):
    """
    Perform sentiment analysis using both VADER and RoBERTa models and store the results in the database.

    @param cursor (object): The database cursor.
    @param preprocessed_data (np.ndarray): The preprocessed data for VADER analysis.
    @param data (np.ndarray): The raw data for RoBERTa analysis.
    @param table_name (str): The name of the table where the results should be stored.
    @ret: A tuple containing:
        - (np.ndarray): VADER sentiment analysis results.
        - (list of lists): RoBERTa sentiment analysis results.
    """
    vader_results = vader_sentiment_analysis(cursor, preprocessed_data, table_name)
    roberta_results = roberta_sentiment_analysis(cursor, data, table_name)
    return vader_results, roberta_results

def prompt_model_selection():
    """
    Prompt the user to select a sentiment analysis model.

    @param: None.
    @ret (int or str): The chosen model number (1 for VADER, 2 for RoBERTa, and anything else for all models). 'quit' to quit.
    """
    print("""Sentiment Analysis Models:
    1. VADER
    2. Hugging Face's RoBERTa
    
    Enter any other key to run all models. To quit, enter `quit`
    """)
    user_input = input("Enter the model choice: ").strip().lower()

    if user_input == 'quit':
        return 'quit'
    elif user_input in ['1', '2']:
        return int(user_input)
    else:
        return 'all'

def perform_selected_sentiment_analysis(model, cursor, preprocessed_data, raw_data, table_name):
    """
    Perform sentiment analysis based on the chosen model.

    @param model (int or str): The chosen model number (1 for VADER, 2 for RoBERTa, and anything else for all models).
    @param cursor (object): The database cursor.
    @param preprocessed_data (np.ndarray): The preprocessed data.
    @param raw_data (np.ndarray): The raw data.
    @param table_name (str): The name of the table.
    @ret: A list of tuples, each containing:
        - (np.ndarray or list of dict): The sentiment analysis results.
        - (str): The name of the sentiment analysis model ('VADER' or 'RoBERTa').
    """
    if model == 'q':
        return []
    elif model == 1:
        vader_results = vader_sentiment_analysis(cursor, preprocessed_data, table_name)
        return [(vader_results, 'VADER')]
    elif model == 2:
        roberta_results = roberta_sentiment_analysis(cursor, raw_data, table_name)
        return [(roberta_results, 'RoBERTa')]
    else:
        vader_results, roberta_results = analyze_all_models(cursor, preprocessed_data, raw_data, table_name)
        return [(vader_results, 'VADER'), (roberta_results, 'RoBERTa')]