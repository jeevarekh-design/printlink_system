-- SQLite compatible schema for PrintLink
-- Run: sqlite3 database.db < schema_sqlite.sql

DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS students;

CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    phone TEXT
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_name TEXT NOT NULL,
    file_name TEXT NOT NULL,
    copies INTEGER NOT NULL,
    pages INTEGER,
    print_type TEXT NOT NULL,
    status TEXT DEFAULT 'Inbox',
    seen INTEGER DEFAULT 0,
    order_time DATETIME DEFAULT CURRENT_TIMESTAMP
);
