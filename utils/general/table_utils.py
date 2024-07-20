import re
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')

def validate_table_name(cursor, table_name):
    """
    Validate the table name to prevent SQL injection.

    @param cursor: A cursor object to execute database commands.
    @param table_name: The name of the table to validate.
    @ret: None.

    """
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', table_name):
        logging.error(f"Invalid table name: {table_name}")
        raise ValueError("Invalid table name")
    elif not check_table_exists(cursor, table_name):
        logging.error(f"Table does not exist: {table_name}")
        raise ValueError("Table does not exist")
    else:
        logging.info(f"Table name '{table_name}' is valid")

def get_table_name_from_user(cursor):
    """
    Prompt the user to enter a table name and validate the input.

    @param cursor: A cursor object to execute database commands.
    @ret: Table name if valid
    """
    while True:
        table_name = input("Enter the table name: ").strip()
        try:
            validate_table_name(cursor, table_name)
            return table_name
        except ValueError as e:
            logging.error(f"Error: {e}. Please try again.")

def check_table_exists(cursor, table_name):
    """
    Check if a table exists in the database.

    @param cursor: A cursor object to execute database commands.
    @param table_name: The name of the table.
    @ret: True if the table exists, False otherwise.
    """
    query = """
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        AND table_name = %s
    );
    """
    cursor.execute(query, (table_name,))
    return cursor.fetchone()[0]