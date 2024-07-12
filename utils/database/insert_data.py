def insert_prime_minister_content(cursor, data):
    """
    Insert fetched content into the uk_prime_minister_content table.

    @param cursor: A cursor object to execute database commands.
    @param data: A list of lists containing the content data to be inserted.
    @ret: None.
    """
    insert_query = """
        INSERT INTO uk_prime_minister_content (uk_prime_minister_id, content)
        VALUES (%s, %s)
        ON CONFLICT (uk_prime_minister_id) DO UPDATE SET
        content = EXCLUDED.content
    """
    cursor.executemany(insert_query, data)

def insert_prime_minister_processed_content(cursor, data):
    """
    Insert processed content into the uk_prime_minister_content_processed table.

    @param cursor: A cursor object to execute database commands.
    @param data: A list of lists containing the processed content data to be inserted.
    @ret: None.
    """
    insert_query = """
        INSERT INTO uk_prime_minister_content_processed (uk_prime_minister_content_id, processed_content)
        VALUES (%s, %s)
        ON CONFLICT (uk_prime_minister_content_id) DO UPDATE SET
        processed_content = EXCLUDED.processed_content
    """
    cursor.executemany(insert_query, data)

def insert_geospatial_data_to_database(cursor, data):
    """
    Insert geospatial analysis results into the database.

    @param cursor: A cursor object to execute database commands.
    @param data: A list of lists containing the geospatial data [uk_prime_minister_content_id, longitude, latitude, location].
    @ret: None.
    """
    insert_query = """
        INSERT INTO uk_prime_minister_geospatial_analysis (uk_prime_minister_content_id, longitude, latitude, location)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (uk_prime_minister_content_id) DO UPDATE SET
        longitude = EXCLUDED.longitude,
        latitude = EXCLUDED.latitude,
        location = EXCLUDED.location;
    """
    cursor.executemany(insert_query, data)

def insert_sentiment_data_to_database(cursor, data, table_name):
    """
    Insert sentiment analysis results into the database.

    @param cursor: A cursor object to execute database commands.
    @param data: A list of lists containing the sentiment analysis results.
    @param table_name: The name of the table to insert the sentiment data into.
    @ret: None.
    """
    insert_query = f"""
        INSERT INTO {table_name} (uk_prime_minister_content_id, sentiment)
        VALUES (%s, %s)
        ON CONFLICT (uk_prime_minister_content_id) DO UPDATE SET
        sentiment = EXCLUDED.sentiment;
    """
    # Convert to list of tuples for executemany
    formatted_data = [(item[0], item[2]) for item in data]
    cursor.executemany(insert_query, formatted_data)

def insert_vader_data_to_database(cursor, data):
    """
    Insert VADER sentiment analysis results into the database.

    @param cursor: A cursor object to execute database commands.
    @param data: A list of lists containing the sentiment analysis results.
    @ret: None.
    """
    insert_sentiment_data_to_database(cursor, data, "sentiment_analysis_vader")

def insert_roberta_data_to_database(cursor, data):
    """
    Insert roBERTa sentiment analysis results into the database.

    @param cursor: A cursor object to execute database commands.
    @param data: A list of lists containing the sentiment analysis results.
    @ret: None.
    """
    insert_sentiment_data_to_database(cursor, data, "sentiment_analysis_roberta")