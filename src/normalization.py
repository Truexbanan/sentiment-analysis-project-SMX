import spacy
import logging
import re # Regex library

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
    doc = nlp(text)
    # Create list of lemmatized tokens, excluding stop words and punctuation
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    # Join list of tokens back into a single string
    return " ".join(tokens)

def preprocess_data(data):
    processed_data = []
    for index, item in data:
        processed_text = preprocess_text(item)
        processed_data.append([index, processed_text])
    return processed_data