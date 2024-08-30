import sqlite3
import pandas as pd

DB_NAME = 'database/expenses.db'

def connect_db():
    return sqlite3.connect(DB_NAME)

def add_income(date, source, amount):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Income (date, source, amount)
    VALUES (?, ?, ?)
    ''', (date, source, amount))
    conn.commit()
    conn.close()

def add_expense(date, category, amount, description):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Expenses (date, category, amount, description)
    VALUES (?, ?, ?, ?)
    ''', (date, category, amount, description))
    conn.commit()
    conn.close()

def add_savings(date, amount):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Savings (date, amount)
    VALUES (?, ?)
    ''', (date, amount))
    conn.commit()
    conn.close()

def get_data(table_name):
    conn = connect_db()
    df = pd.read_sql_query(f'SELECT * FROM {table_name}', conn)
    conn.close()
    return df
