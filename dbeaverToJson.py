import psycopg2
from psycopg2 import sql
import json
import os
from dotenv import load_dotenv
# loading variables from .env file
load_dotenv() 


db_params = {
'dbname': os.getenv('DBNAME'),
'user': os.getenv('USER'),
'password': os.getenv('PASSWORD'),
'host': os.getenv('HOST'),
'port': os.getenv('PORT') 
}


# Establishing the connection
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Query
query = "SELECT content FROM uk_prime_minister"

# Executing the query
cursor.execute(query)

# Fetching the results
results = cursor.fetchall()

# Convert the results to a list of lists
data = [[idx + 1, row[0]] for idx, row in enumerate(results)]

# Create the final JSON structure
json_data = {"index": data}

#os.path.join

# Write the data to a JSON file
with open('content.json', 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file, ensure_ascii=False, indent=4)

# Closing the connection
cursor.close()
conn.close()