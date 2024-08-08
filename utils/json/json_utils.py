import json
import logging
import os

def load_json(file_path):
    """
    Load a JSON file from the specified path.
    
    @param file_path (str): The path to the JSON file.
    @ret (dict or None): The loaded JSON data as a dictionary.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading JSON file: {e}")
        return None
    
def save_to_json(new_data, file_path):
    """
    Save the processed data to a JSON file, appending to it if it already exists.

    @param new_data (dict): The new data to save.
    @param file_path (str): The path to the JSON file. If the file does not exist, it will be created with this name.
    @ret: None.
    """
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        else:
            existing_data = {"index": []}

        # Initialize the index for new data
        start_index = 1
        if existing_data["index"]:
            last_entry = existing_data["index"][-1]
            start_index = last_entry[0] + 1

        # Adjust new data indices to continue from the highest index
        for idx, item in enumerate(new_data["index"], start=start_index):
            item[0] = idx

        # Append new data to existing data
        existing_data["index"].extend(new_data["index"])

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"Error saving to JSON file: {e}")