from services.account_service import create_account, select_account, get_balance
from services.transaction_service import withdraw, deposit, purchase, transaction_history

def main_menu(conn):
    """
    Main menu of the application.

    Args:
        conn: Connection object to the database.

    Returns:
        None
    """
    print("I'm just copying Toma's project")

    # Choose account
    account_id, account_name = choose_account(conn)

    # show account option if account selected or cerated
    if account_id and account_name:
        show_options(conn, account_id, account_name)

def choose_account(conn):
    """
    Login page. Present options to create a new account,
    select an existing one, or exit.

    Args:
        conn: Connection object to the database.

    Returns:
        tuple: Tuple containing the account ID and account name.
    """
    # Not sure how to have infinite loop without while True
    # I can use a variable as a condition?
    # eg. n = 0, while n<1 to loop
    # += 1 to n to stop loop
    while True:
        # Dirplay menu
        print("\n1. Create new account")
        print("2. Select existing account")
        print("3. Exit")
        choice = input("Enter choice: ")
        
        if choice == '1':
            try:
                # Create new account
                name = input("Enter account name: ")
                initial_balance = float(input("Enter initial balance: "))
                # Create new account and get id
                account_id = create_account(conn, name, initial_balance)
                if account_id is not None:
                    print(f"Account created successfully with ID: {account_id}")
                    return account_id, name
            except ValueError:
                print("Invalid input. Please enter valid data.")
            except Exception as e:
                print(f"Error: {e}. Please try again.")
        
        elif choice == '2':
            try:
                # Select existing account
                account_id = select_account(conn)
                if account_id is not None:
                    cursor = conn.cursor()
                    # Fetch account info using ID
                    cursor.execute("SELECT name FROM account WHERE id = ?", (account_id,))
                    account_name = cursor.fetchone()[0]
                    return account_id, account_name
            except ValueError:
                print("Invalid input. Please enter valid data.")
            except Exception as e:
                print(f"Error: {e}. Please try again.")
        
        elif choice == '3':
            print("Exiting.")
            exit()
        
        else:
            print("Invalid choice. Please try again.")

def show_options(conn, account_id, account_name):
    """
    Display options for the selected account.

    Args:
        conn: Connection object to the database.
        account_id (int): The ID of the selected account.
        account_name (str): The name of the selected account.

    Returns:
        None
    """
    while True:
        # account options menu
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
        
        if choice == '1':
            try:
                # Get and display account balance
                balance = get_balance(conn, account_id)
                print(f"Current balance: ${balance:.2f}")
            except Exception as e:
                print(f"Error: {e}. Please try again.")
        
        elif choice == '2':
            try:
                # Input withdraw details
                amount = float(input("Enter amount to withdraw: "))
                description = input("Enter withdrawal description: ")
                # Withdraw from account
                withdraw(conn, account_id, amount, description)
            except ValueError:
                print("Invalid input. Please enter a valid number.")
            except Exception as e:
                print(f"Error: {e}. Please try again.")
        
        elif choice == '3':
            try:
                # Input deposit details
                amount = float(input("Enter amount to deposit: "))
                description = input("Enter deposit description: ")
                # Deposit to account
                deposit(conn, account_id, amount, description)
            except ValueError:
                print("Invalid input. Please enter a valid number.")
            except Exception as e:
                print(f"Error: {e}. Please try again.")
        
        elif choice == '4':
            try:
                # Input purchase details
                amount = float(input("Enter purchase amount: "))
                description = input("Enter purchase description: ")
                # Perform purchase
                purchase(conn, account_id, amount, description)
            except ValueError:
                print("Invalid input. Please enter a valid number.")
            except Exception as e:
                print(f"Error: {e}. Please try again.")
        
        elif choice == '5':
            try:
                # Display transaction history for the account
                print("Transaction history:")
                transaction_history(conn, account_id)
            except Exception as e:
                print(f"Error: {e}. Please try again.")
        
        elif choice == '6':
            # Return to main menu
            print("Returning to main menu.")
            main_menu(conn)
            break
        
        elif choice == '7':
            # Exit application
            print("Exiting.")
            exit()
        
        else:
            print("Invalid choice. Please try again.")
