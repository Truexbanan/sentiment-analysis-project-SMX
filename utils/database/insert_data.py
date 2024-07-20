def insert_prime_minister_content(cursor, data, table_name):
    """
    Insert fetched content into the uk_prime_minister_content table.

    @param cursor: A cursor object to execute database commands.
    @param data: A list of lists containing the content data to be inserted.
    @ret: None.
    """
    insert_query = f"""
        INSERT INTO {table_name}_content ({table_name}_id, content)
        VALUES (%s, %s)
        ON CONFLICT ({table_name}_id) DO UPDATE SET
        content = EXCLUDED.content
    """
    cursor.executemany(insert_query, data)

def insert_prime_minister_processed_content(cursor, data, table_name):
    """
    Insert processed content into the uk_prime_minister_content_processed table.

    @param cursor: A cursor object to execute database commands.
    @param data: A list of lists containing the processed content data to be inserted.
    @ret: None.
    """
    insert_query = f"""
        INSERT INTO {table_name}_content_processed ({table_name}_content_id, processed_content)
        VALUES (%s, %s)
        ON CONFLICT ({table_name}_content_id) DO UPDATE SET
        processed_content = EXCLUDED.processed_content
    """
    cursor.executemany(insert_query, data)

def insert_prime_minister_language(cursor, data, table_name):
    """
    Insert language into the uk_prime_minister_language table.

    @param cursor: A cursor object to execute database commands.
    @param data: 
    @ret: None.
    """
    insert_query = f"""
        INSERT INTO {table_name}_language ({table_name}_id, language)
        VALUES (%s, %s)
        ON CONFLICT ({table_name}_id) DO UPDATE SET
        language = EXCLUDED.language
    """
    cursor.executemany(insert_query, data)

def insert_geospatial_data_to_database(cursor, data, table_name):
    """
    Insert geospatial analysis results into the database.

    @param cursor: A cursor object to execute database commands.
    @param data: A list of lists containing the geospatial data [uk_prime_minister_content_id, longitude, latitude, location].
    @ret: None.
    """
    insert_query = f"""
        INSERT INTO {table_name}_geospatial ({table_name}_content_id, longitude, latitude, location)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT ({table_name}_content_id) DO UPDATE SET
        longitude = EXCLUDED.longitude,
        latitude = EXCLUDED.latitude,
        location = EXCLUDED.location;
    """
    cursor.executemany(insert_query, data)

def insert_vader_data_to_database(cursor, data, table_name):
    """
    Insert sentiment analysis results into the database.

    @param cursor: A cursor object to execute database commands.
    @param data: A list of lists containing the sentiment analysis results using VADER.
    @ret: None.
    """
    insert_query = f"""
        INSERT INTO {table_name}_sentiment_vader ({table_name}_content_processed_id, sentiment)
        VALUES (%s, %s)
        ON CONFLICT ({table_name}_content_processed_id) DO UPDATE SET
        sentiment = EXCLUDED.sentiment;
    """ 
    # Convert to list of tuples for executemany
    formatted_data = [(item[0], item[2]) for item in data]
    cursor.executemany(insert_query, formatted_data)

def insert_roberta_data_to_database(cursor, data, table_name):
    """
    Insert sentiment analysis results into the database.

    @param cursor: A cursor object to execute database commands.
    @param data: A list of lists containing the sentiment analysis results using roBERTa.
    @ret: None.
    """
    insert_query = f"""
        INSERT INTO {table_name}_sentiment_roberta ({table_name}_content_id, sentiment)
        VALUES (%s, %s)
        ON CONFLICT ({table_name}_content_id) DO UPDATE SET
        sentiment = EXCLUDED.sentiment;
    """ 
    # Convert to list of tuples for executemany
    formatted_data = [(item[0], item[2]) for item in data]
    cursor.executemany(insert_query, formatted_data)