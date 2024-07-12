import numpy as np

def fetch_prime_minister_content(cursor):
    """
    Fetch content data from the uk_prime_minister table.

    @param: A cursor object to execute database commands.
    @ret: A list of lists formatted as [[index, content], ...].
    """
    cursor.execute("SELECT id, content FROM uk_prime_minister;")
    data = cursor.fetchall() # Initially stored as a list of tuples

    formatted_data = np.array([[row[0], row[1]] for row in data])
    return formatted_data

def fetch_geospatial_data_from_database(cursor):
    """
    Fetch data relevant to geospatial analysis from the uk_prime_minister table.

    @param: A cursor object to execute database commands.
    @ret: A list of lists formatted as [[index, content], ...].
    """
    fetch_query = """
        SELECT id, longitude, latitude, location
        FROM uk_prime_minister
        WHERE longitude IS NOT NULL AND latitude IS NOT NULL AND location IS NOT NULL;
    """
    cursor.execute(fetch_query)
    data = cursor.fetchall()  # This will be a list of tuples

    # Convert each tuple to a list and then to a NumPy array
    formatted_data = np.array([list(row) for row in data])
    return formatted_data