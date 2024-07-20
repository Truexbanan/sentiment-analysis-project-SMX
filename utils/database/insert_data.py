def insert_content_data(cursor, data, table_name):
    """
    Insert fetched content into the specified content table.

    @param cursor (object): A cursor object to execute database commands.
    @param data (list of lists): A list of lists containing the content data to be inserted. Each list should be in the format [id, content].
    @ret: None.
    """
    insert_query = f"""
        INSERT INTO {table_name}_content ({table_name}_id, content)
        VALUES (%s, %s)
        ON CONFLICT ({table_name}_id) DO UPDATE SET
        content = EXCLUDED.content
    """
    cursor.executemany(insert_query, data)

def insert_processed_content_data(cursor, data, table_name):
    """
    Insert processed content into the specified processed content table.

    @param cursor (object): A cursor object to execute database commands.
    @param data (list of lists): A list of lists containing the processed content data to be inserted. Each list should be in the format [content_id, processed_content].
    @ret: None.
    """
    insert_query = f"""
        INSERT INTO {table_name}_content_processed ({table_name}_content_id, processed_content)
        VALUES (%s, %s)
        ON CONFLICT ({table_name}_content_id) DO UPDATE SET
        processed_content = EXCLUDED.processed_content
    """
    cursor.executemany(insert_query, data)

def insert_language_data(cursor, data, table_name):
    """
    Insert language data into the specified language table.

    @param cursor (object): A cursor object to execute database commands.
    @param data (list of lists): A list of lists containing the language data to be inserted. Each list should be in the format [id, language].
    @ret: None.
    """
    insert_query = f"""
        INSERT INTO {table_name}_language ({table_name}_id, language)
        VALUES (%s, %s)
        ON CONFLICT ({table_name}_id) DO UPDATE SET
        language = EXCLUDED.language
    """
    cursor.executemany(insert_query, data)

def insert_geospatial_data(cursor, data, table_name):
    """
    Insert geospatial analysis results into the specified geospatial table.

    @param cursor (object): A cursor object to execute database commands.
    @param data (list of lists): A list of lists containing the geospatial data to be inserted. Each list should be in the format [content_id, longitude, latitude, location].
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

def insert_vader_sentiment_data(cursor, data, table_name):
    """
    Insert VADER sentiment analysis results into the specified VADER sentiment table.

    @param cursor (object): A cursor object to execute database commands.
    @param data (list of lists): A list of lists containing the VADER sentiment analysis results. Each list should be in the format [content_processed_id, _, sentiment].
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

def insert_roberta_sentiment_data(cursor, data, table_name):
    """
    Insert roBERTa sentiment analysis results into the specified roBERTa sentiment table.

    @param cursor (object): A cursor object to execute database commands.
    @param data (list of lists): A list of lists containing the roBERTa sentiment analysis results. Each list should be in the format [content_id, _, sentiment].
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