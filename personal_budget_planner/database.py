import sqlite3

class BudgetDatabase:
    def __init__(self, db_name='budget.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password INT NOT NULL,
            income REAL DEFAULT 0,
            expense REAL DEFAULT 0
        )
        ''')


        self.conn.commit()

    def add_transaction(self, transaction_type, amount, category, description, date):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO transactions (type, amount, category, description, date)
        VALUES (?, ?, ?, ?, ?)
        ''', (transaction_type, amount, category, description, date))
        self.conn.commit()

    def add_user(self, name, surname, age, email,password):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO users (name, surname, age, email, password)
        VALUES (?, ?, ?, ?, ?)
        ''', (name, surname, age, email, password))
        self.conn.commit()
    
    def get_user_by_email(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = self.cursor.fetchone()
        return user
    
    def get_total_income(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT IFNULL(SUM(amount), 0) FROM transactions WHERE type='income'")
        total_income = cursor.fetchone()[0]
        return total_income if total_income is not None else 0
    
    def get_total_expense(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT IFNULL(SUM(amount), 0) FROM transactions WHERE type='expense'")
        total_expense = cursor.fetchone()[0]
        return total_expense if total_expense is not None else 0
    
    def close(self):
        self.conn.close()