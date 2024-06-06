from services.account_service import AccountService
from services.transaction_service import TransactionService

class MainMenu:
    """
    A class representing the main menu of the application.

    Attributes:
        _conn (sqlite3.Connection): Connection object to the SQLite database.
        _account_service (AccountService): Instance of the AccountService class.
        _transaction_service (TransactionService): Instance of the TransactionService class.
    """

    def __init__(self, conn):
        """
        Initialize the MainMenu object.

        Args:
            conn (sqlite3.Connection): Connection object to the SQLite database.
        """
        self._conn = conn
        self._account_service = AccountService(self._conn)
        self._transaction_service = TransactionService(self._conn)


    def display(self):
        """
        Display menu of the application.

        Args:
            None

        Returns:
            None
        """
        print("Simple Finance Application")

        # Choose account
        account_id, account_name = self.choose_account()

        # show account option if account selected or cerated
        if account_id and account_name:
            self.show_options(account_id, account_name)

    def choose_account(self):
        """
        Login page. Present options to create a new account,
        select an existing one, or exit.

        Args:
            None

        Returns:
            tuple: Tuple containing the account ID and account name.
        """
        # Not sure how to have infinite loop without while True
        # I can use a variable as a condition?
        # eg. n = 0, while n<1 to loop
        # += 1 to n to stop loop
        while True:
            print("\n1. Create new account")
            print("2. Select existing account")
            print("3. Exit")
            choice = input("Enter choice: ")

            # Create new account
            if choice == '1':
                try:
                    name = input("Enter account name: ")
                    initial_balance = float(input("Enter initial balance: "))
                    # Create new account and get id
                    account_id = self._account_service.create_account(name, initial_balance)
                    if account_id is not None:
                        print(f"Account created successfully with ID: {account_id}")
                        return account_id, name
                except ValueError:
                    print("Invalid input. Please enter valid data.")
                except Exception as e:
                    print(f"Error: {e}. Please try again.")

            # Select existing account
            elif choice == '2':
                try:
                    account_id = self._account_service.select_account()
                    if account_id is not None:
                        # Sepch account info using account ID
                        account_name = self._account_service.get_account_id(account_id)
                        return account_name
                except ValueError:
                    print("Invalid input. Please enter valid data.")
                except Exception as e:
                    print(f"Error: {e}. Please try again.")

            # Exit
            elif choice == '3':
                print("Exiting.")
                exit()

            else:
                print("Invalid choice. Please try again.")

    def show_options(self, account_id, account_name):
        """
        Display options for the selected account.

        Args:
            account_id (int): The ID of the selected account.
            account_name (str): The name of the selected account.

        Returns:
            None
        """
        # Account options menu
        while True:
            print(f"\nAccount ID: {account_id}, Account Name: {account_name}")
            print("Choose an option:")
            print("1. Check Balance")
            print("2. Withdraw")
            print("3. Deposit")
            print("4. Make Purchase")
            print("5. Transaction History")
            print("6. Return to Main Menu")
            print("7. Exit")

            choice = input("Enter choice: ")

            # Get and display account balance
            if choice == '1':
                try:
                    balance = self._account_service.get_balance(account_id)
                    print(f"Current balance: ${balance:.2f}")
                except Exception as e:
                    print(f"Error: {e}. Please try again.")

            # Input withdraw details
            elif choice == '2':
                try:
                    amount = float(input("Enter amount to withdraw: "))
                    description = input("Enter withdrawal description: ")
                    # Withdraw from account
                    self._transaction_service.withdraw(account_id, amount, description)
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                except Exception as e:
                    print(f"Error: {e}. Please try again.")

            # Input deposit details
            elif choice == '3':
                try:
                    amount = float(input("Enter amount to deposit: "))
                    description = input("Enter deposit description: ")
                    # Deposit to account
                    self._transaction_service.deposit(account_id, amount, description)
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                except Exception as e:
                    print(f"Error: {e}. Please try again.")

            # Input purchase details
            elif choice == '4':
                try:
                    amount = float(input("Enter purchase amount: "))
                    description = input("Enter purchase description: ")
                    # Perform purchase
                    self._transaction_service.purchase(account_id, amount, description)
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                except Exception as e:
                    print(f"Error: {e}. Please try again.")

            # Display transaction history for the account
            elif choice == '5':
                try:
                    print("Transaction history:")
                    # Show transaction history
                    self._transaction_service.transaction_history(account_id)
                except Exception as e:
                    print(f"Error: {e}. Please try again.")

            # Return to main menu
            elif choice == '6':
                print("Returning to main menu.")
                self.display()
                break

            # Exit application
            elif choice == '7':
                print("Exiting.")
                exit()

            else:
                print("Invalid choice. Please try again.")