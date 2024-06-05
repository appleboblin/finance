import sqlite3

def create_tables(conn):
    try:
        cursor = conn.cursor()  # Interaction with database

        # Create account table if needed
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS account (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                balance REAL NOT NULL
            )
        """)

        # Create transactions table if needed
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                account_id INTEGER,
                type TEXT,
                amount REAL,
                description TEXT,
                date TEXT DEFAULT (datetime('now','localtime')),
                FOREIGN KEY (account_id) REFERENCES account (id)
            )
        """)

        # Save changes
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()  # Rollback the transaction on error
        raise Exception(f"An error occurred while creating tables: {e}")
