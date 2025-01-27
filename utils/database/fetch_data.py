import numpy as np

def fetch_content_data(cursor, table_name):
    """
    Fetch content data from the specified table.

    @param cursor (object): A cursor object to execute database commands.
    @param table_name (str): The name of the table.
    @ret (np.ndarray): A NumPy array of shape (n, 2) formatted as [[id, content], ...].
    """
    cursor.execute(f"SELECT id, content FROM {table_name};")
    data = cursor.fetchall() # Initially stored as a list of tuples

    formatted_data = np.array([[row[0], row[1]] for row in data])
    return formatted_data

def fetch_language_data(cursor, table_name):
    """
    Fetch content language data from the specified table.

    @param cursor (object): A cursor object to execute database commands.
    @param table_name (str): The name of the table.
    @ret (np.ndarray): A NumPy array of shape (n, 2) formatted as [[id, language], ...].
    """
    cursor.execute(f"SELECT id, language FROM {table_name};")
    data = cursor.fetchall() # Initially stored as a list of tuples

    formatted_data = np.array([[row[0], row[1]] for row in data])
    return formatted_data

def fetch_geospatial_data(cursor, table_name):
    """
    Fetch data relevant to geospatial analysis from the specified table.
    Avoid fetching data that explicitly states it's from US locations.

    @param cursor (object): A cursor object to execute database commands.
    @param table_name (str): The name of the table.
    @ret (np.ndarray): A NumPy array of shape (n, 4) formatted as [[id, longitude, latitude, location], ...].
    """
    fetch_query = f"""
        SELECT id, longitude, latitude, location
        FROM {table_name}
        WHERE longitude IS NOT NULL 
          AND latitude IS NOT NULL 
          AND location IS NOT NULL 
          AND location NOT LIKE '%US%' 
          AND location NOT LIKE '%United States%';
    """
    cursor.execute(fetch_query)
    data = cursor.fetchall()  # This will be a list of tuples

    # Convert each tuple to a list and then to a NumPy array
    formatted_data = np.array([list(row) for row in data])
    return formatted_data