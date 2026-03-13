-- Create database
CREATE DATABASE IF NOT EXISTS printlink;

-- Use database
USE printlink;

-- Delete tables if they already exist
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS students;

-- Students table
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(15)
);

-- Orders table
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    copies INT NOT NULL,
    pages INT,
    print_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'Inbox',
    seen INT DEFAULT 0,
    order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);