# MySQL

## Database Management

```sql
-- Show all databases
SHOW DATABASES;

-- Select a specific database
USE <database_name>;

-- List all tables in the selected database
SHOW TABLES;
```

## Table & Column Operations

```sql
-- Show structure of a table
DESCRIBE <table>;

-- Add columns to a table
ALTER TABLE <table> ADD <column_name> <data_type>;

-- Drop columns from a table
ALTER TABLE <table> DROP <column_name>, DROP <another_column>;

-- Modify a column's data type
ALTER TABLE <table> MODIFY COLUMN <column> <new_data_type>;

-- Drop a table
DROP TABLE <table>;
```