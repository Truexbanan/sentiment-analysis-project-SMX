"""
This script connects to a database, retrieves content from a specified table,
and exports the content to a JSON file. If the file 'content.json' already exists,
the script appends the new data to the existing file and logs this action. If the
file does not exist, it creates a new file and logs the creation. The JSON file
stores data as a list of lists, where each sublist contains an index and the content.
"""

import json
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
from utils.database.connection import connect_to_database, close_connection_to_database
from utils.general.table_utils import get_table_name_from_user
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

# loading variables from .env file
load_dotenv() 

# Connect to database
conn = connect_to_database()
cursor = conn.cursor()

table_name = get_table_name_from_user(cursor)
if table_name is not None:
    # Execute query and fetch results
    cursor.execute(f"SELECT content FROM {table_name};")
    results = cursor.fetchall()

    # Path to the JSON file where data will be stored
    json_file_path = 'data/content.json'

    # Initialize the index for new data
    start_index = 1
    existing_data = {"index": []}

    # Check if the JSON file exists and read its content
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
        if existing_data["index"]:
            last_entry = existing_data["index"][-1] # Retrieve last element from list w/ "index" key
            start_index = last_entry[0] + 1
        logging.info(f"Appended data to existing file: {json_file_path}")
    else:
        logging.info(f"Created a new file: {json_file_path}")

    # Convert the results to a list of lists with updated indices
    new_data = [[start_index + idx, row[0]] for idx, row in enumerate(results)]

    # Append the new data to the existing data
    existing_data["index"].extend(new_data)

    # Write the updated data to the JSON file
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(existing_data, json_file, ensure_ascii=False, indent=4)

    # Closing the connection
    close_connection_to_database(conn, cursor)
else:
    # Closing the connection
    close_connection_to_database(conn, cursor)