from database.connection import DatabaseManager
from ui.menu import MainMenu

class FinanceApp:
    def __init__(self):
        self._db_manager = DatabaseManager()

    def run(self):
        """
        Run the application.

        Connects to the database, creates necessary tables,
        instantiates the main menu, and displays it.

        Args:
            None

        Returns:
            None
        """
        try:
            # Connect to the database
            self._db_manager.connect()
            # Create necessary tables
            self._db_manager.create_tables()
            # Instantiate MainMenu
            main_menu = MainMenu(self._db_manager.get_connection())
            # Display main menu
            main_menu.display()
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Close the database connection
            self._db_manager.close()

if __name__ == "__main__":
    app = FinanceApp()
    app.run()
