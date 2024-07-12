def create_prime_minister_content_table(cursor):
    """
    Create the social media post content table if it doesn't exist.
    
    @param cursor: A cursor object to execute database commands.
    @ret: None.
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS uk_prime_minister_content (
        uk_prime_minister_id INT PRIMARY KEY,
        content TEXT,
        FOREIGN KEY (uk_prime_minister_id) REFERENCES uk_prime_minister(id)
    );
    """
    cursor.execute(create_table_query)

def create_prime_minister_processed_content_table(cursor):
    """
    Create the processed social media post content table if it doesn't exist.
    
    @param cursor: A cursor object to execute database commands.
    @ret: None.
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS uk_prime_minister_content_processed (
        uk_prime_minister_content_id INT PRIMARY KEY,
        processed_content TEXT,
        FOREIGN KEY (uk_prime_minister_content_id) REFERENCES uk_prime_minister_content(uk_prime_minister_id)
    );
    """
    cursor.execute(create_table_query)

def create_vader_sentiment_analysis_table(cursor):
    """
    Create the vader_sentiment_analysis table if it doesn't exist.
    
    @param cursor: A cursor object to execute database commands.
    @ret: None.
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS sentiment_analysis_vader (
        uk_prime_minister_content_id INT PRIMARY KEY,
        sentiment TEXT,
        FOREIGN KEY (uk_prime_minister_content_id) REFERENCES uk_prime_minister_content(uk_prime_minister_id)
    );
    """
    cursor.execute(create_table_query)

def create_roberta_sentiment_analysis_table(cursor):
    """
    Create the roberta_sentiment_analysis table if it doesn't exist.
    
    @param cursor: A cursor object to execute database commands.
    @ret: None.
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS sentiment_analysis_roberta (
        uk_prime_minister_content_id INT PRIMARY KEY,
        sentiment TEXT,
        FOREIGN KEY (uk_prime_minister_content_id) REFERENCES uk_prime_minister_content(uk_prime_minister_id)
    );
    """
    cursor.execute(create_table_query)

def create_geospatial_analysis_table(cursor):
    """
    Create the geospatial analysis results table if it doesn't exist.
    
    @param cursor: A cursor object to execute database commands.
    @ret: None.
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS uk_prime_minister_geospatial_analysis (
        uk_prime_minister_content_id INT PRIMARY KEY,
        longitude DECIMAL NOT NULL,
        latitude DECIMAL NOT NULL,
        location TEXT NOT NULL,
        FOREIGN KEY (uk_prime_minister_content_id) REFERENCES uk_prime_minister_content(uk_prime_minister_id)
    );
    """
    cursor.execute(create_table_query)