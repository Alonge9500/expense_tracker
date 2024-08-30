import sqlite3
DB_NAME = 'database/expenses.db'

def create_database(db_name= DB_NAME):
    # Connect to SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Create the Income table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Income (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        source TEXT NOT NULL,
        amount REAL NOT NULL
    )
    ''')

    # Create the Expenses table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT
    )
    ''')

    # Create the Savings table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Savings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        amount REAL NOT NULL
    )
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print(f"Database '{db_name}' created successfully with tables Income, Expenses, and Savings.")

if __name__ == "__main__":
    create_database()
