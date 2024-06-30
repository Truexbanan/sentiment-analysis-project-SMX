import psycopg2
from psycopg2 import sql
import json
import os
from dotenv import load_dotenv

# loading variables from .env file
load_dotenv() 

# Database connection parameters
db_params = {
'dbname': os.getenv('DBNAME'),
'user': os.getenv('USER'),
'password': os.getenv('PASSWORD'),
'host': os.getenv('HOST'),
'port': os.getenv('PORT') 
}

# Establishing the connection to the database
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Query
query = "SELECT content FROM uk_prime_minister"

# Executing the query
cursor.execute(query)

# Fetching the results
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

# Convert the results to a list of lists with updated indices
new_data = [[start_index + idx, row[0]] for idx, row in enumerate(results)]

# Append the new data to the existing data
existing_data["index"].extend(new_data)

# Write the updated data to the JSON file
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(existing_data, json_file, ensure_ascii=False, indent=4)

# Closing the connection
cursor.close()
conn.close()