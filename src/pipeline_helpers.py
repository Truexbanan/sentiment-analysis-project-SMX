from utils.database import (
    initialize_database,
    create_database_tables,
    fetch_content_data,
    fetch_language_data,
    fetch_geospatial_data,
    insert_content_data,
)
from utils.database.insert_data import insert_language_data, insert_geospatial_data
from utils.general.table_utils import get_table_name_from_user
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

def initialize_and_fetch_data():
    """
    Initialize the database connection, create necessary tables, and fetch the required data.

    @param: None.
    @ret conn: The database connection object.
    @ret cursor: The database cursor object.
    @ret table_name (str): The name of the table.
    @ret prime_minister_data (np.ndarray): Fetched prime minister data.
    @ret language_data (np.ndarray): Fetched language data.
    @ret geospatial_data (np.ndarray): Fetched geospatial data.
    """
    conn, cursor = initialize_database()
    table_name = get_table_name_from_user(cursor)
    create_database_tables(cursor, table_name)
    prime_minister_data, language_data, geospatial_data = fetch_and_store_prime_minister_and_geospatial_data(cursor, table_name)
    return conn, cursor, table_name, prime_minister_data, language_data, geospatial_data

def fetch_and_store_prime_minister_and_geospatial_data(cursor, table_name):
    """
    Fetch the prime minister and geospatial data from the database, and insert
    them into their respective tables.
    
    @param cursor: The database cursor.
    @param table_name (str): The name of the table.
    @ret (tuple): A tuple containing:
        - prime_minister_data (np.ndarray): Fetched prime minister data.
        - language_data (np.ndarray): Fetched language data.
        - geospatial_data (np.ndarray): Fetched geospatial data.
    """
    try:
        data = fetch_content_data(cursor, table_name)
        language = fetch_language_data(cursor, table_name)
        insert_language_data(cursor, data, table_name)
        insert_content_data(cursor, data, table_name)
        geospatial_data = fetch_geospatial_data(cursor, table_name)
        insert_geospatial_data(cursor, geospatial_data, table_name)
    except Exception as e:
        logging.error(f"An error occurred while fetching and inserting data: {e}")
        raise  # Re-raise the exception after logging

    return data, language, geospatial_data