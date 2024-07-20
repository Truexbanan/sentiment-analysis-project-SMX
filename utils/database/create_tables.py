def create_prime_minister_content_table(cursor, table_name):
    """
    Create the social media post content table if it doesn't exist.
    
    @param cursor (object): A cursor object to execute database commands.
    @param table_name (str): The name of the table.
    @ret: None
    """
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name}_content (
        {table_name}_id INT PRIMARY KEY,
        content TEXT,
        FOREIGN KEY ({table_name}_id) REFERENCES {table_name}(id)
    );
    """
    cursor.execute(create_table_query)

def create_prime_minister_processed_content_table(cursor, table_name):
    """
    Create the processed social media post content table if it doesn't exist.
    
    @param cursor (object): A cursor object to execute database commands.
    @param table_name (str): The name of the table.
    @ret: None
    """
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name}_content_processed (
        {table_name}_content_id INT PRIMARY KEY,
        processed_content TEXT,
        FOREIGN KEY ({table_name}_content_id) REFERENCES {table_name}_content({table_name}_id)
    );
    """
    cursor.execute(create_table_query)

def create_prime_minister_language_table(cursor, table_name):
    """
    Create a table that stores the post's language and id.

    @param cursor (object): A cursor object to execute database commands.
    @param table_name (str): The name of the table.
    @ret: None
    """
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name}_language (
        {table_name}_id INT PRIMARY KEY,
        language TEXT,
        FOREIGN KEY ({table_name}_id) REFERENCES {table_name}(id)
    );
    """
    cursor.execute(create_table_query)

def create_vader_sentiment_analysis_table(cursor, table_name):
    """
    Create the vader sentiment analysis table if it doesn't exist.
    
    @param cursor (object): A cursor object to execute database commands.
    @param table_name (str): The name of the table.
    @ret: None
    """
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name}_sentiment_vader (
        {table_name}_content_processed_id INT PRIMARY KEY,
        sentiment TEXT,
        FOREIGN KEY ({table_name}_content_processed_id) REFERENCES {table_name}_content_processed({table_name}_content_id)
    );
    """
    cursor.execute(create_table_query)

def create_roberta_sentiment_analysis_table(cursor, table_name):
    """
    Create the roberta sentiment analysis table if it doesn't exist.
    
    @param cursor (object): A cursor object to execute database commands.
    @param table_name (str): The name of the table.
    @ret: None
    """
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name}_sentiment_roberta (
        {table_name}_content_id INT PRIMARY KEY,
        sentiment TEXT,
        FOREIGN KEY ({table_name}_content_id) REFERENCES {table_name}_content({table_name}_id)
    );
    """
    cursor.execute(create_table_query)

def create_geospatial_analysis_table(cursor, table_name):
    """
    Create the geospatial analysis results table if it doesn't exist.
    
    @param cursor (object): A cursor object to execute database commands.
    @param table_name (str): The name of the table.
    @ret: None
    """
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name}_geospatial (
        {table_name}_content_id INT PRIMARY KEY,
        longitude DECIMAL NOT NULL,
        latitude DECIMAL NOT NULL,
        location TEXT NOT NULL,
        FOREIGN KEY ({table_name}_content_id) REFERENCES {table_name}_content({table_name}_id)
    );
    """
    cursor.execute(create_table_query)