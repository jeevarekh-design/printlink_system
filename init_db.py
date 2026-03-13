import sqlite3
import os

db_path = 'database.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create students table
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    phone TEXT
)
''')

# Create orders table
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    file_name TEXT NOT NULL,
    copies INTEGER NOT NULL,
    pages INTEGER,
    print_type TEXT NOT NULL,
    status TEXT DEFAULT 'Inbox',
    seen INTEGER DEFAULT 0,
    order_time DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()

print(f"Database initialized at {os.path.abspath(db_path)}")
print("Tables created: students, orders")

