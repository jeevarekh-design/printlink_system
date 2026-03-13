CREATE DATABASE printlink;

USE printlink;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    password VARCHAR(100)
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100),
    file_name VARCHAR(200),
    copies INT,
    print_type VARCHAR(50),
    status VARCHAR(50)
);