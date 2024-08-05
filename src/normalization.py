import boto3
import spacy
import re # Regex library
import logging
import numpy as np
import concurrent.futures
from utils.general.language_codes import language_mapping

def load_spacy_model(model_name):
    """
    Load a spaCy model.
    
    @param model_name (str): The name of the spaCy model to load.
    @ret (spacy.language.Language): The loaded spaCy model.
    
    @raises RuntimeError: If the model cannot be loaded.
    """
    try:
        return spacy.load(model_name)
    except IOError as e:
        logging.error(f"Error loading spaCy model: {e}")
        raise RuntimeError(f"Failed to load spaCy model '{model_name}'")

# Load the spaCy model once
nlp = load_spacy_model("en_core_web_lg")

# Initialize the Amazon Translate client
translate_client = boto3.client('translate', region_name='us-east-1')

# Initialize translation cache and preprocess cache
translation_cache = {}
preprocess_cache = {}

def translate_text(text, language):
    """
    Translate text to English using Amazon Translate.
    
    @param text (str): The text to translate.
    @param language (str): The source language code.
    @ret (str): The translated text.
    """
    # Check if the text and language pair is already in the cache
    if (text, language) in translation_cache:
        return translation_cache[(text, language)]
    
    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode=language if language is not None else 'auto',
            TargetLanguageCode='en'
        )
        # Store the translated text in the cache
        translation = response['TranslatedText']
        translation_cache[(text, language)] = translation
        return translation
    except Exception as e:
        return text  # If translation fails, use original text

def tokenize_text(text, language):
    """
    Tokenize the text by removing mentions, hashtags, URLs, and extra spaces,
    translating the text, and lemmatizing the tokens.

    @param text (str): The text to tokenize.
    @param language (str): The language code for translation.
    @ret (list of str): A list of tokens.
    """
    # Remove user tags or mentions
    text = re.sub(r'@\w+', '', text)
    # Remove hashtags
    text = re.sub(r'#\w+', '', text)
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|\S+\.\S+', '', text, flags=re.IGNORECASE)
    # Remove Emails
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text)
    # Remove extra spaces
    text = ' '.join(text.split())

    translated_text = translate_text(text, language)
    doc = nlp(translated_text)

    important_stop_words_for_vader = [
        'really', 'some', 'almost', 'quite', 'rather', 'because', 'never',
        'always', 'could', 'enough', 'might', 'without', 'have', 'also', 'can',
        'should', 'not', 'only', 'more', 'whatever', 'beside', 'although',
        'however', 'yet', 'still', 'while', 'but', 'despite', 'nowhere',
        'otherwise', 'nevertheless', 'therefore', 'moreover', 'serious', 'nothing',
        'another', 'mostly', 'except', 'hence', 'cannot', 'last', 'than', 'barely',
        'hardly', 'just', 'little', 'merely', 'nearly', 'scarcely', 'simply',
        'solely', 'very'
    ]
    # Create list of lemmatized tokens
    return [token.lemma_ for token in doc if (not token.is_stop or token.dep_ == 'neg') and (token.text.lower() not in important_stop_words_for_vader)]

def preprocess_text(text, language):
    """
    Preprocess the text by tokenizing, normalizing, and joining tokens into a single string.
    
    @param text (str): The text to preprocess.
    @param language (str): The language code for translation.
    @ret (str): The preprocessed text.
    """
    tokens = tokenize_text(text, language)
    return " ".join(tokens) # Join list of tokens back into a single string

def create_id_to_index_mapping(language_data):
    """
    Create a mapping from IDs to indices in the language_data array.
    
    @param language_data (np.ndarray): A NumPy array of [id, language] pairs.
    @ret (dict): A dictionary mapping IDs to indices.
    """
    return {id_: idx for idx, (id_, _) in enumerate(language_data)}

def process_entry(entry, id_to_index, language_data):
    """
    Process a single entry by preprocessing the text.
    
    @param entry (tuple): A tuple containing the index and text.
    @param id_to_index (dict): A dictionary mapping IDs to indices in language_data.
    @param language_data (np.ndarray): A NumPy array of [id, language] pairs.
    @ret (tuple): A tuple containing the index and preprocessed text.
    """
    id_, text = entry
    index = id_to_index.get(id_)  # Retrieve index using the ID

    # Return the original text if the ID is not found in the mapping.
    if index is None:
        return id_, text 

    language_name = language_data[int(index), 1]  # Extract the language name
    language_code = language_mapping.get(language_name)  # Get the language code
    preprocessed_text = preprocess_text(text, language_code)
    return id_, preprocessed_text

def preprocess_data(data, language_data):
    """
    Preprocess a list of data items using parallel processing.
    
    @param data (np.ndarray): A NumPy array of [id, text] pairs.
    @param language_data (np.ndarray): A NumPy array of [id, language] pairs.
    @ret (np.ndarray): A NumPy array of unique [id, preprocessed_text] pairs.
    """
    unique_preprocessed_texts = set()
    preprocessed_data = []

    # Convert to NumPy array if not already
    if not isinstance(data, np.ndarray):
        data = np.array(data)
    if not isinstance(language_data, np.ndarray):
        language_data = np.array(language_data)

    # Create mapping from IDs to indices in language_data
    id_to_index = create_id_to_index_mapping(language_data)

    # Use ProcessPoolExecutor for parallel processing
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Submit tasks to the executor, where each task is to process an entry
        future_to_entry = {executor.submit(process_entry, entry, id_to_index, language_data): entry for entry in data}
        
        # Iterate over Future objects as they complete and process the result
        for future in concurrent.futures.as_completed(future_to_entry):
            # Retrieve result of the completed task
            id_, preprocessed_text = future.result()

            # Ensure each processed text is unique before adding it to the result
            if preprocessed_text not in unique_preprocessed_texts:
                unique_preprocessed_texts.add(preprocessed_text)
                preprocess_cache[preprocessed_text] = preprocessed_text
                preprocessed_data.append([id_, preprocessed_text])
            else:
                preprocessed_data.append([id_, preprocess_cache[preprocessed_text]])

    return np.array(preprocessed_data)