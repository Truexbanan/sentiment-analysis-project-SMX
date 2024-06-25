import json
import logging

def load_json(file_path):
    """
    Load a JSON file from the specified path.
    
    @param file_path: The path to the JSON file.
    @ret: The loaded JSON data as a dictionary.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading JSON file: {e}")
        return None