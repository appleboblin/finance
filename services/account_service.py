import sqlite3

def create_account(conn, name, initial_balance):
    """
    Create a new account in the database.

    Args:
        conn (sqlite3.Connection): Connection object to the SQLite database.
        name (str): The name of the account account.
        initial_balance (float): The initial balance for the account.

    Returns:
        int: The ID of the newly created account.

    Raises:
        Exception: If an error occurs while creating the account.
    """

    try:
        initial_balance = round(initial_balance, 2)
        cursor = conn.cursor()  # Interaction with database

        # Insert new account
        cursor.execute("INSERT INTO account (name, balance) VALUES (?, ?)", (name, initial_balance,))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        conn.rollback()
        raise Exception(f"An error occurred while creating the account: {e}")


def get_balance(conn, account_id):
    """
    Retrieve the balance of a specific account.

    Args:
        conn (sqlite3.Connection): Connection object to the SQLite database.
        account_id (int): The ID of the account.

    Returns:
        float: The balance of the account.

    Raises:
        Exception: If the account with the given ID is not found.
    """
    cursor = conn.cursor()

    # Fetch balance of specified account
    cursor.execute("SELECT balance FROM account WHERE id = ?", (account_id,))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        raise Exception(f"Account with ID {account_id} not found.")

def update_balance(conn, account_id, amount):
    """
    Update the balance of a specific account.

    Args:
        conn (sqlite3.Connection): Connection object to the SQLite database.
        account_id (int): The ID of the account.
        amount (float): The new balance amount.

    Raises:
        Exception: If an error occurs while updating the balance.
    """
    try:
        cursor = conn.cursor()

        # Query to update balance of specified account
        cursor.execute("UPDATE account SET balance = ? WHERE id = ?", (amount, account_id))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise Exception(f"An error occurred while updating the balance: {e}")

def select_account(conn):
    """
    Display a list of available accounts and allow the user to select one.

    Args:
        conn (sqlite3.Connection): Connection object to the SQLite database.

    Returns:
        int: The ID of the selected account, or None if no accounts are found.
    """
    cursor = conn.cursor()

    # Fetch all account
    cursor.execute("SELECT id, name FROM account")
    accounts = cursor.fetchall()
    if not accounts:
        print("No accounts found.")
        return None
    print("Available accounts:")
    for acc in accounts:
        print(f"ID: {acc[0]}, Name: {acc[1]}")
    account_id = int(input("Enter account ID to select: "))
    return account_id
