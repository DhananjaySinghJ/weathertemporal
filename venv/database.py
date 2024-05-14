import psycopg2

def insert_into_database(email, city, db_string):
    """
    Inserts user details (email and city) into a PostgreSQL database.

    Args:
        email (str): The email address of the user.
        city (str): The city name associated with the user.
        db_string (str): The connection string for the PostgreSQL database.

    Returns:
        None
    """
    # Establish connection to the PostgreSQL database
    conn = psycopg2.connect(db_string)
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    # Execute SQL INSERT command to insert user details into the 'users' table
    cursor.execute("INSERT INTO users (email, city) VALUES (%s, %s)", (email, city))
    # Commit the transaction to make the changes persistent
    conn.commit()
    # Close the cursor and connection to release resources
    cursor.close()
    conn.close()
