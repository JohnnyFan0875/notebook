# MySQL

## Introduction

MySQL is an open-source relational database management system (RDBMS) that uses SQL (Structured Query Language) for managing and manipulating data.

## Connect to MySQL

```sql
mysql -u root -p
```

## User & Session Management

```sql
-- Switch user
SYSTEM mysql -u user -p;

-- View running threads
SHOW PROCESSLIST;

-- Kill a thread
KILL <id>;
```

## Database Management

```sql
-- List all databases
SHOW DATABASES;

-- Create a database
CREATE DATABASE test_db;

-- Select a database
USE test_db;

-- Show all tables in the selected database
SHOW TABLES;

-- Delete a database
DROP DATABASE test_db;
```

## Table & Column Operations

```sql
-- Show the structure of a table
DESCRIBE users;

-- Create a table
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Add a column
ALTER TABLE users ADD age INT;

-- Drop columns
ALTER TABLE users DROP age;

-- Modify column type
ALTER TABLE users MODIFY email TEXT;

-- Drop table
DROP TABLE users;
```

## Insert & Delete Rows

```sql
-- Insert data
INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com');

-- Update data
UPDATE users SET email = 'newalice@example.com' WHERE name = 'Alice';

-- Delete specific row
DELETE FROM users WHERE name = 'Alice';

-- Delete all rows
DELETE FROM users;
```

## Querying Data

```sql
-- Basic query
SELECT * FROM users;

-- Filtered query with alias
SELECT name AS username FROM users WHERE CHAR_LENGTH(name) > 3;

-- Using table alias
SELECT u.name FROM users u WHERE u.email LIKE '%@example.com%';
```

## Aggregation and Joins

```sql
-- Count grouped values
SELECT department, COUNT(*) FROM employees GROUP BY department;

-- INNER JOIN example
SELECT o.id, c.name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id;
```

## Table Creation via Query

```sql
-- Create a new table from a query result
CREATE TABLE high_salary_employees AS
SELECT * FROM employees WHERE salary > 100000;

-- Create a temporary table (session-lifetime)
CREATE TEMPORARY TABLE IF NOT EXISTS temp_sales AS
SELECT * FROM sales WHERE region = 'East';
```

## Import & Load Data

```sql
-- Check if local file import is allowed
SHOW GLOBAL VARIABLES LIKE 'local_infile';

-- Enable local_infile (if needed)
SET GLOBAL local_infile = true;

-- Reconnect with --local_infile
mysql --local_infile=1 -u root -p

-- Load CSV into table
LOAD DATA LOCAL INFILE '/path/to/file.csv'
INTO TABLE users
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
```

## Export Data to File

```sql
-- Export table to CSV
SELECT name, email
FROM users
INTO OUTFILE '/var/lib/mysql-files/users.csv'
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n';

-- Check path restriction
SHOW VARIABLES LIKE "secure_file_priv";
```

## User Privileges & Security

```sql
-- Create a new user
CREATE USER 'user1'@'localhost' IDENTIFIED BY 'password123';

-- Grant permissions
GRANT ALL PRIVILEGES ON test_db.* TO 'user1'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;

-- View privileges
SHOW GRANTS FOR 'user1'@'localhost';
```

## Indexing for Performance

```sql
-- Add index
CREATE INDEX idx_name ON users(name);

-- Show indexes
SHOW INDEX FROM users;

-- Drop index
DROP INDEX idx_name ON users;
```

## Best Practices & Tips

- Always back up before destructive operations (`DROP`, `DELETE`, etc.)
- Use `EXPLAIN` to analyze query performance
- Use `LIMIT` for large SELECT queries to avoid memory overload
- Prefer `INT` over `VARCHAR` for foreign keys when possible
- Avoid `SELECT *` in production queries – specify needed columns
