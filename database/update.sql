-- Select the database
USE printlink;

-- Add phone column to students table
ALTER TABLE students
ADD COLUMN phone VARCHAR(15);

-- Make email unique to avoid duplicate accounts
ALTER TABLE students
ADD UNIQUE (email);

-- Add pages column to orders table
ALTER TABLE orders
ADD COLUMN pages INT;

-- Add order time column to store when the order was placed
ALTER TABLE orders
ADD COLUMN order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Set default order status
ALTER TABLE orders
MODIFY status VARCHAR(50) DEFAULT 'Inbox';