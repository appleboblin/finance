import sqlite3
from sqlite3 import Error
import os

def create_connection():
    """
    Create a connection to the SQLite database.

    Creates a connection to the 'bank.db' SQLite database located
    in the same directory as the script. If the database does not exist, it will be created.

    Returns:
        conn (sqlite3.Connection): Connection object to the SQLite database.

    Raises:
        Exception: If an error occurs during the connection to the database.
    """
    conn = None
    try:
        # Look for bank.db in the same folder
        db_path = os.path.join(os.path.dirname(__file__), 'bank.db')
        conn = sqlite3.connect(db_path)
        return conn
    except Error as e:
        raise Exception(f"Error connecting to the database: {e}")
