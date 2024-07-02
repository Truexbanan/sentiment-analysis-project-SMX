import boto3
import spacy
from spacy.tokens import Span
import re # Regex library
import pandas as pd
# from googletrans import Translator # Google Translate API
import logging

# translator = Translator()
# # Keep track of the current translations
# translation_cache = {}

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
    
def translate_text(text):
    """
    Translate text to English using Amazon Translate.
    
    @param text: The text to translate.
    @ret: The translated text.
    """
    # # If text has been translated already, retrieve it instead
    # if text in translation_cache:
    #     return translation_cache[text]
    
    # try:
    #     translation = translator.translate(text, dest='en').text
    # except Exception as e:
    #     translation = text # If translation fails, fall back to original text
    
    # # Store translation in transation_cache
    # translation_cache[text] = translation
    # return translation
    return text

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

    # Remove extra spaces
    text = ' '.join(text.split())

    translated_text = translate_text(text)
    doc = nlp(translated_text)
    # Create list of lemmatized tokens, excluding stop words and punctuation
    tokens = [token.lemma_ for token in doc if (not token.is_stop or token.dep_ == 'neg') and not token.is_punct]
    # Join list of tokens back into a single string
    return " ".join(tokens)

def preprocess_data(data):
    """
    Preprocess a list of data items.
    
    @param data: A list of [index, text] pairs.
    @ret: A list of unique [index, preprocessed_text] pairs.
    """
    processed_data = []
    # Ensure there are no duplicate posts
    unique_processed_texts = set()
    # List for duplicates
    duplicates = []

    # Loop over list of lists
    for index, text in data:
        processed_text = preprocess_text(text)
        if processed_text not in unique_processed_texts:
            unique_processed_texts.add(processed_text)
            processed_data.append([index, processed_text])
        else:
            duplicates.append([index, text])

    return processed_data, duplicates