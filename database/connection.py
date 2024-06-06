import os
import sqlite3

class DatabaseManager:
    """
    A class to manage the SQLite database connection and operations.

    Attributes:
        _db_name (str): Name of the database file.
        _db_path (str): Full path to the database file.
        _conn (sqlite3.Connection): Connection object to the SQLite database.
    """

    def __init__(self, db_name='bank.db'):
        """
        Initialize the DatabaseManager object.

        Args:
            db_name (str, optional): The name of the database file. Defaults to 'bank.db'.
        """
        self._db_name = db_name
        self._db_path = os.path.join(os.path.dirname(__file__), self._db_name)
        self._conn = None


    def connect(self):
        """
        Connect to the SQLite database.

        Args:
            None

        Returns:
            None

        Raises:
            Exception: If an error occurs while connecting to the database.
        """
        try:
            self._conn = sqlite3.connect(self._db_path)
        except sqlite3.Error as e:
            raise Exception(f"Error connecting to the database: {e}")


    def get_connection(self):
        """
        Get the SQLite database connection.

        Args:
            None

        Returns:
            sqlite3.Connection: Connection object to the SQLite database.
        """
        return self._conn


    def close(self):
        """
        Close the connection to the SQLite database.

        Args:
            None

        Returns:
            None

        """
        if self._conn:
            self._conn.close()


    def create_tables(self):
        """
        Create necessary tables in the SQLite database.

        Args:
            None

        Returns:
            None

        Raises:
            Exception: If an error occurs while creating tables.
        """
        try:
            cursor = self._conn.cursor()
            # Define table creation SQL queries
            account_table_query = """
                CREATE TABLE IF NOT EXISTS account (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    balance REAL NOT NULL
                )
            """
            transactions_table_query = """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY,
                    account_id INTEGER,
                    type TEXT,
                    amount REAL,
                    description TEXT,
                    date TEXT DEFAULT (datetime('now','localtime')),
                    FOREIGN KEY (account_id) REFERENCES account (id)
                )
            """
            # Execute queries, create new tables if needed
            cursor.execute(account_table_query)
            cursor.execute(transactions_table_query)
            # Commit changes
            self._conn.commit()
        except sqlite3.Error as e:
            self._conn.rollback()
            raise Exception(f"An error occurred while creating tables: {e}")
