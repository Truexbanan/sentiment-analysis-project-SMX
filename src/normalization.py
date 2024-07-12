import boto3
import spacy
import re # Regex library
import logging
import numpy as np
import concurrent.futures

def load_spacy_model(model_name):
    """
    Load a spaCy model.
    
    @param model_name: The name of the spaCy model to load.
    @ret: The loaded spaCy model.
    """
    try:
        return spacy.load(model_name)
    except IOError as e:
        logging.error(f"Error loading spaCy model: {e}")
        return None

# Load the spaCy model once
nlp = load_spacy_model("en_core_web_lg")

# Initialize the Amazon Translate client
translate_client = boto3.client('translate', region_name='us-east-1')

# Initialize translation cache
translation_cache = {}

def translate_text(text):
    """
    Translate text to English using Amazon Translate.
    
    @param text: The text to translate.
    @ret: The translated text.
    """
    # Check if the text is already in the cache
    if text in translation_cache:
        return translation_cache[text]
    
    try:
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode='auto',
            TargetLanguageCode='en'
        )
        # Store the translated text in the cache
        translation = response['TranslatedText']
        translation_cache[text] = translation
        return translation
    except Exception as e:
        return text  # If translation fails, use original text

def preprocess_text(text):
    """
    Preprocess the text by removing mentions, hashtags, URLs, and extra spaces,
    translating the text, and lemmatizing non-stop words and non-punctuation tokens.
    
    @param text: The text to preprocess.
    @ret: The preprocessed text.
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

    translated_text = translate_text(text)
    doc = nlp(translated_text)
    # Create list of lemmatized tokens, excluding stop words and punctuation
    tokens = [token.lemma_ for token in doc if (not token.is_stop or token.dep_ == 'neg') and not token.is_punct]
    # Join list of tokens back into a single string
    return " ".join(tokens)

def process_entry(entry):
    """
    Process a single entry by preprocessing the text.
    
    @param entry: A tuple containing the index and text.
    @ret: A tuple containing the index and preprocessed text.
    """
    index, text = entry
    processed_text = preprocess_text(text)
    return index, processed_text

def preprocess_data(data):
    """
    Preprocess a list of data items using parallel processing.
    
    @param data: A NumPy array of [index, text] pairs.
    @ret: A NumPy array of unique [index, preprocessed_text] pairs.
    """
    unique_processed_texts = set()
    processed_data = []

    # Convert to NumPy array if not already
    if not isinstance(data, np.ndarray):
        data = np.array(data)

    # Use ProcessPoolExecutor for parallel processing
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Submit tasks to the executor, where each task is to process an entry
        future_to_entry = {executor.submit(process_entry, entry): entry for entry in data}
        
        # Iterate over Future objects as they complete and process the result
        for future in concurrent.futures.as_completed(future_to_entry):
            # Retrieve result of the completed task
            index, processed_text = future.result()

            # Ensure each processed text is unique before adding it to the result
            if processed_text not in unique_processed_texts:
                unique_processed_texts.add(processed_text)
                processed_data.append([index, processed_text])

    return np.array(processed_data)