import sqlite3
from services.account_service import AccountService

class TransactionService:
    """
    A class to manage transaction-related operations.

    Attributes:
        _conn (sqlite3.Connection): Connection object to the SQLite database.
        _account_service (AccountService): AccountService object for account-related operations.
    """
    def __init__(self, conn):
        """
        Initializes the TransactionService with the given database connection.

        Args:
            conn (sqlite3.Connection): Connection object to the SQLite database.
        """
        self._conn = conn
        self._account_service = AccountService(conn)


    def add_transaction(self, account_id, trans_type, amount, description):
        """
        Adds a transaction to the transaction table.

        Args:
            account_id (int): ID of the account.
            trans_type (str): Type of transaction (e.g., 'withdrawal', 'deposit', 'purchase').
            amount (float): Amount of the transaction.
            description (str): Description of the transaction.

        Returns:
            None

        Raises:
            Exception: If an error occurs while adding the transaction.
        """
        try:
            cursor = self._conn.cursor()

            # Insert new transaction to the transaction table
            cursor.execute("INSERT INTO transactions (account_id, type, amount, description) VALUES (?, ?, ?, ?)",
                            (account_id, trans_type, amount, description))
            self._conn.commit()
        except sqlite3.Error as e:
            self._conn.rollback()
            raise Exception(f"An error occurred while adding the transaction: {e}")


    def withdraw(self, account_id, amount, description):
        """
        Withdraws an amount from the account if the balance is sufficient.

        Args:
            account_id (int): ID of the account.
            amount (float): Amount to withdraw.
            description (str): Description of the withdrawal.

        Returns:
            None
        """
        balance = self._account_service.get_balance(account_id)

        # Check if balance is sufficient
        if balance >= amount:
            new_balance = balance - amount
            # Update account balance
            self._account_service.update_balance(account_id, new_balance)
            # Add withdraw transaction
            self.add_transaction(account_id, 'withdrawal', amount, description)
            print("Withdrawal successful!")
        else:
            print("Insufficient balance.")


    def deposit(self, account_id, amount, description):
        """
        Deposits an amount into the account.

        Args:
            account_id (int): ID of the account.
            amount (float): Amount to deposit.
            description (str): Description of the deposit.

        Returns:
            None
        """
        amount = round(amount, 2)
        balance = self._account_service.get_balance(account_id)
        new_balance = round(balance + amount, 2)
        # Update account balance
        self._account_service.update_balance(account_id, new_balance)
        # Add deposit transaction
        self.add_transaction(account_id, 'deposit', amount, description)
        print("Deposit successful!")


    def purchase(self, account_id, amount, description):
        """
        Makes a purchase by deducting an amount from the account if the balance is sufficient.

        Args:
            account_id (int): ID of the account.
            amount (float): Amount to be deducted for the purchase.
            description (str): Description of the purchase.

        Returns:
            None
        """
        balance = self._account_service.get_balance(account_id)
        if balance >= amount:
            new_balance = balance - amount
            # Update account balance
            self._account_service.update_balance(account_id, new_balance)
            # Add purchase transaction
            self.add_transaction(account_id, 'purchase', amount, description)
            print("Purchase successful!")
        else:
            print("Insufficient balance.")


    def transaction_history(self, account_id):
        """
        Displays the transaction history of the account.

        Args:
            account_id (int): ID of the account.

        Returns:
            None
        """
        cursor = self._conn.cursor()

        # Query to select the date, type, amount, and description
        # of transactions for the given account_id, ordered by date in descending order
        cursor.execute("SELECT date, type, amount, description FROM transactions WHERE account_id = ? ORDER BY date DESC", (account_id,))
        rows = cursor.fetchall()
        for row in rows:
            print(row)
