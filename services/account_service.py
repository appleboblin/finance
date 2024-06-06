import sqlite3

class AccountService:
    """
    A class to manage account-related operations.

    Attributes:
        _conn (sqlite3.Connection): Connection object to the SQLite database.
    """

    def __init__(self, conn):
        """
        Initializes the AccountService with the given database connection.

        Args:
            conn (sqlite3.Connection): Connection object to the SQLite database.
        """
        self._conn = conn


    def create_account(self, name, initial_balance):
        """
        Create a new account in the database.

        Args:
            name (str): The name of the account.
            initial_balance (float): The initial balance for the account.

        Returns:
            int: The ID of the newly created account.

        Raises:
            Exception: If an error occurs while creating the account.
        """

        try:
            initial_balance = round(initial_balance, 2)
            cursor = self._conn.cursor()  

            # Insert new account
            cursor.execute("INSERT INTO account (name, balance) VALUES (?, ?)", (name, initial_balance,))
            self._conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            self._conn.rollback()
            raise Exception(f"An error occurred while creating the account: {e}")


    def get_balance(self, account_id):
        """
        Retrieve the balance of a specific account.

        Args:
            account_id (int): ID of the account.

        Returns:
            float: Balance of the account.

        Raises:
            Exception: If the account with the given ID is not found.
        """
        cursor = self._conn.cursor()

        # Fetch balance of specified account
        cursor.execute("SELECT balance FROM account WHERE id = ?", (account_id,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            raise Exception(f"Account with ID {account_id} not found.")


    def update_balance(self, account_id, amount):
        """
        Update the balance of a specific account.

        Args:
            account_id (int): ID of the account.
            amount (float): New balance amount.

        Raises:
            Exception: If an error occurs while updating the balance.
        """
        try:
            cursor = self._conn.cursor()

            # Query to update balance of specified account
            cursor.execute("UPDATE account SET balance = ? WHERE id = ?", (amount, account_id))
            self._conn.commit()
        except sqlite3.Error as e:
            self._conn.rollback()
            raise Exception(f"An error occurred while updating the balance: {e}")


    def select_account(self):
        """
        Display a list of available accounts and allow the user to select one.

        Args:
            None

        Returns:
            int: The ID of the selected account, or None if no accounts are found.
        """
        cursor = self._conn.cursor()

        # Fetch all accounts
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


    def get_account_id(self, account_id):
        """
        Retrieves the name of the account with the given ID.

        Args:
            account_id (int): ID of the account.

        Returns:
            str: Name of the account.

        Raises:
            Exception: If an error occurs while fetching the account name.
        """
        try:
            cursor = self._conn.cursor()
            cursor.execute("SELECT name FROM account WHERE id = ?", (account_id,))
            account_name = cursor.fetchone()[0]
            return account_id, account_name
        except Exception as e:
            raise Exception(f"Invalid account ID")