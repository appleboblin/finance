import sqlite3
from services.account_service import get_balance, update_balance

def add_transaction(conn, account_id, trans_type, amount, description):
    """
    Adds a transaction to the transaction table.

    Args:
        conn (sqlite3.Connection): Connection object to the SQLite database.
        account_id (int): The ID of the account.
        trans_type (str): The type of transaction (e.g., 'withdrawal', 'deposit', 'purchase').
        amount (float): The amount of the transaction.
        description (str): A description of the transaction.

    Raises:
        Exception: If an error occurs while adding the transaction.
    """
    try:
        cursor = conn.cursor()

        # Insert new transaction to the transaction table
        cursor.execute("INSERT INTO transactions (account_id, type, amount, description) VALUES (?, ?, ?, ?)",
                        (account_id, trans_type, amount, description))
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise Exception(f"An error occurred while adding the transaction: {e}")

def withdraw(conn, account_id, amount, description):
    """
    Withdraws an amount from the account if the balance is sufficient.

    Args:
        conn (sqlite3.Connection): Connection object to the SQLite database.
        account_id (int): The ID of the account.
        amount (float): The amount to withdraw.
        description (str): A description of the withdrawal.

    Returns:
        None
    """
    balance = get_balance(conn, account_id)

    # Check if balance is sufficient
    if balance >= amount:
        new_balance = balance - amount
        # Update account balance
        update_balance(conn, account_id, new_balance)
        # Add withdraw transaction
        add_transaction(conn, account_id, 'withdrawal', amount, description)
        print("Withdrawal successful!")
    else:
        print("Insufficient balance.")

def deposit(conn, account_id, amount, description):
    """
    Deposits an amount into the account.

    Args:
        conn (sqlite3.Connection): Connection object to the SQLite database.
        account_id (int): The ID of the account.
        amount (float): The amount to deposit.
        description (str): A description of the deposit.

    Returns:
        None
    """
    amount = round(amount, 2)
    balance = get_balance(conn, account_id)
    new_balance = round(balance + amount, 2)
    # Update account balance
    update_balance(conn, account_id, new_balance)
    # Add deposit transaction
    add_transaction(conn, account_id, 'deposit', amount, description)
    print("Deposit successful!")

def purchase(conn, account_id, amount, description):
    """
    Makes a purchase by deducting an amount from the account if the balance is sufficient.

    Args:
        conn (sqlite3.Connection): Connection object to the SQLite database.
        account_id (int): The ID of the account.
        amount (float): The amount to be deducted for the purchase.
        description (str): A description of the purchase.

    Returns:
        None
    """
    balance = get_balance(conn, account_id)
    if balance >= amount:
        new_balance = balance - amount
        # Update account balance
        update_balance(conn, account_id, new_balance)
        # Add purchase transaction
        add_transaction(conn, account_id, 'purchase', amount, description)
        print("Purchase successful!")
    else:
        print("Insufficient balance.")

def transaction_history(conn, account_id):
    """
    Displays the transaction history of the account.

    Args:
        conn (sqlite3.Connection): Connection object to the SQLite database.
        account_id (int): The ID of the account.

    Returns:
        None
    """
    cursor = conn.cursor()

    # Query to select the date, type, amount, and description
    # of transactions for the given account_id, ordered by date in descending order
    cursor.execute("SELECT date, type, amount, description FROM transactions WHERE account_id = ? ORDER BY date DESC", (account_id,))
    rows = cursor.fetchall()
    for row in rows:
        print(row)
