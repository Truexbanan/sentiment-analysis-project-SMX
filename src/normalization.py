import spacy
from spacy.tokens import Span
import re # Regex library
import pandas as pd
from googletrans import Translator
import logging

translator = Translator()

def load_spacy_model(model_name):
    try:
        return spacy.load(model_name)
    except IOError as e:
        logging.error(f"Error loading spaCy model: {e}")
        return None

# Load the spaCy model once
nlp = load_spacy_model("en_core_web_sm")
    
def preprocess_text(text):
    text = text.lower()  # Convert text to lowercase for uniformity
    try:
        translated_text = translator.translate(text, dest='en').text
    except Exception as e:
        logging.error(f"Error translating text: {e}")
        translated_text = text # If translation fails, fall back to original text
    doc = nlp(translated_text)
    # Create list of lemmatized tokens, excluding stop words and punctuation
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    # Join list of tokens back into a single string
    return " ".join(tokens)

def preprocess_data(data):
    processed_data = []
    # Ensure there are no duplicate posts
    unique_processed_texts = set()
    for index, text in data:
        processed_text = preprocess_text(text)
        if processed_text not in unique_processed_texts:
            unique_processed_texts.add(processed_text)
            processed_data.append([index, processed_text])
    return processed_data