from database.connection import create_connection
from database.models import create_tables
from ui.menu import main_menu

def main():
    # Connection to database
    conn = create_connection()

    # Create necessary tables if not already exist
    create_tables(conn)

    # Display main menu
    main_menu(conn)

    # Close database connection
    conn.close()

if __name__ == '__main__':
    main()