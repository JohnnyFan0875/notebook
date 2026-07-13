# PostgreSQL

> Brackets like `[optional]` indicate optional parts. Examples use concrete names (e.g., `shopdb`, `orders`, `customers`) rather than placeholders.

## Quick psql tips

```bash
# Disable line-wrapping in psql output
PAGER='less -S' psql

# Enter postgres and/or a specific database
psql                 # connects with your default user, prompts for DB
psql shopdb          # connects directly to database shopdb

# Connect with host/port/user
psql -h 127.0.0.1 -p 5432 -U admin shopdb
```

### Inside psql (meta-commands)

```sql
\l                      -- list all databases
\c shopdb               -- connect to shopdb
\dt                     -- list all tables in current schema
\d orders               -- describe table structure
\q                      -- quit psql
\pset pager off         -- turn off the pager
\x                      -- toggle expanded display (great for wide rows)
\df                     -- list functions in current database
```

### Import/Export CSV (server-side safe via `\copy`)

```sql
-- Export a query to CSV with header
\copy (SELECT id, order_date, total FROM orders ORDER BY id) TO '/tmp/orders.csv' DELIMITER ',' CSV HEADER;

-- Import a CSV file into an existing table
\copy customers FROM '/tmp/customers.csv' DELIMITER ',' CSV HEADER;
```

## Create Database

```sql
CREATE DATABASE shopdb;
CREATE DATABASE analytics_db;
```

資料庫名稱通常以英文字母或底線開頭。實務上盡量使用清楚、穩定、全小寫的命名。

### Useful options

```sql
CREATE DATABASE analytics_db
  OWNER analyst
  TEMPLATE template0
  ENCODING 'UTF8';
```

- `OWNER`: 指定資料庫擁有者
- `TEMPLATE`: 從哪個 template 建立
- `ENCODING`: 指定字元編碼，通常使用 `UTF8`

## DDL: Create/Alter/Drop

### Create table

```sql
CREATE TABLE customers (
  customer_id BIGSERIAL PRIMARY KEY,
  full_name   TEXT NOT NULL,
  email       TEXT UNIQUE,
  created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE orders (
  order_id    BIGSERIAL PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES customers(customer_id),
  status      TEXT CHECK (status IN ('pending','processing','shipped','canceled')),
  total       NUMERIC(12,2) NOT NULL,
  order_date  DATE NOT NULL
);
```

### Alter table & constraints

```sql
-- Rename table
ALTER TABLE orders RENAME TO sales_orders;

-- Drop a column
ALTER TABLE sales_orders DROP COLUMN status;

-- Change a column type
ALTER TABLE sales_orders ALTER COLUMN total TYPE NUMERIC(14,2);

-- Add a composite primary key
ALTER TABLE sales_orders ADD PRIMARY KEY (order_id, order_date);

-- Add a named UNIQUE constraint
ALTER TABLE customers ADD CONSTRAINT uniq_customers_email UNIQUE (email);

-- Add a CHECK constraint
ALTER TABLE sales_orders ADD CONSTRAINT chk_total_nonneg CHECK (total >= 0);

-- Drop a constraint
ALTER TABLE customers DROP CONSTRAINT uniq_customers_email;

-- Remove NOT NULL or other column-level constraints
ALTER TABLE customers ALTER COLUMN email DROP NOT NULL;
```

### Sequences

```sql
-- Restart a sequence to a given value (example: continue from 1000)
ALTER SEQUENCE customers_customer_id_seq RESTART WITH 1000;
```

### Drop

```sql
DROP TABLE IF EXISTS sales_orders;
DROP DATABASE IF EXISTS shopdb_archive;
```

## Data Types: Selection Habits

PostgreSQL 資料型別很多，但日常建模先把幾個核心選擇養成習慣最重要。

### Text

- `TEXT`: 不限制長度，通常是 PostgreSQL 最自然的字串型別
- `VARCHAR(n)`: 需要長度上限時使用

如果沒有業務上的長度限制，常可直接用 `TEXT`。

### Numeric

- `SMALLINT`: 小範圍整數
- `INTEGER`: 一般整數預設選擇
- `BIGINT`: 大範圍整數
- `NUMERIC(p, s)`: 金額或要求精確小數時使用
- `SERIAL`, `BIGSERIAL`: 自動遞增 surrogate key 的傳統寫法

### Temporal

- `DATE`: 只有日期
- `TIMESTAMP`: 日期加時間
- `TIMESTAMPTZ`: 需要時區語意時通常更安全

### Boolean

- `BOOLEAN`

對應值常見為 `TRUE`, `FALSE`, `NULL`。

### Type choice examples

```sql
CREATE TABLE people (
  person_id   BIGSERIAL PRIMARY KEY,
  full_name   TEXT NOT NULL,
  birthday    DATE,
  account_age INTEGER,
  balance     NUMERIC(12,2),
  is_active   BOOLEAN DEFAULT TRUE
);
```

心智模型上，型別要優先服務正確性與可查詢性，不要把日期、金額、布林值都先存成文字。

## DML: Insert/Update/Delete (with conflict handling)

```sql
-- Basic insert
INSERT INTO customers (full_name, email)
VALUES ('Alice Chen', 'alice@example.com');

-- Upsert (ON CONFLICT): if email already exists, update the name
INSERT INTO customers (full_name, email)
VALUES ('A. Chen', 'alice@example.com')
ON CONFLICT (email) DO UPDATE SET full_name = EXCLUDED.full_name;

-- Update
UPDATE customers SET full_name = 'Alice C.' WHERE email = 'alice@example.com';

-- Delete
DELETE FROM customers WHERE email = 'alice@example.com';
```

## Dump/Restore

```bash
# Dump an entire database to a SQL file
pg_dump -U admin -d shopdb > /backups/shopdb_$(date +%F).psql

# Restore from SQL file (method 1: shell)
psql -U admin -d shopdb < /backups/shopdb_2025-08-20.psql

# Restore from SQL file (method 2: inside psql)
\i /backups/shopdb_2025-08-20.psql
```

## Query patterns (SELECT)

### Pagination (OFFSET/LIMIT)

```sql
SELECT order_id, total
FROM orders
ORDER BY order_id
OFFSET 20 LIMIT 10;  -- rows 21–30
```

### Boolean logic and grouping

```sql
SELECT *
FROM orders
WHERE customer_id = 42
  AND (status = 'processing' OR status = 'shipped');
```

### IN / BETWEEN

```sql
SELECT * FROM orders WHERE status IN ('processing','shipped');
SELECT * FROM orders WHERE total BETWEEN 100 AND 500;        -- works for numbers or dates
```

### Order, Distinct

```sql
SELECT * FROM customers ORDER BY created_at DESC, full_name ASC;
SELECT DISTINCT status FROM orders ORDER BY status;
```

### LIKE / ILIKE (case-insensitive)

```sql
SELECT * FROM customers WHERE full_name LIKE '%Chen%';
SELECT * FROM customers WHERE full_name LIKE '__%Chen%';  -- at least 2 chars before 'Chen'
SELECT * FROM customers WHERE full_name ILIKE '%alice%';  -- case-insensitive
```

### Aggregation & Grouping

```sql
-- Count rows matching a condition
SELECT COUNT(*) FROM orders WHERE status = 'shipped';

-- Group + count
SELECT status, COUNT(*) AS n
FROM orders
GROUP BY status
HAVING COUNT(*) > 5
ORDER BY status;

-- Min/Max/Avg with grouping
SELECT customer_id,
       MIN(total) AS min_total,
       MAX(total) AS max_total,
       ROUND(AVG(total), 2) AS avg_total
FROM orders
GROUP BY customer_id;

-- Sum by customer
SELECT customer_id, SUM(total) AS sum_total
FROM orders
GROUP BY customer_id;
```

### NULL helpers (COALESCE/NULLIF)

```sql
-- Replace NULL with a default string
SELECT COALESCE(email, 'no-email@local') AS email_or_default
FROM customers;

-- Compute a derived column, treating NULL as 0
SELECT (total - COALESCE(discount, 0)) AS net_total
FROM orders;

-- If full_name is empty string, fall back to email
SELECT COALESCE(NULLIF(full_name, ''), email) AS display_name
FROM customers;
```

## Dates & Times

```sql
SELECT NOW()::TIMESTAMP, NOW()::DATE; -- current timestamp and date

-- Arithmetic with intervals
SELECT NOW() + INTERVAL '1 month' AS next_month,
       NOW() - INTERVAL '10 years' AS ten_years_ago;

-- Extract parts
SELECT EXTRACT(YEAR FROM NOW())   AS yr,
       EXTRACT(MONTH FROM NOW())  AS mon;

-- Age since a stored timestamp
SELECT DATE_TRUNC('day', created_at) AS created_day,
       AGE(NOW(), created_at)        AS account_age
FROM customers;
```

## Joins & Relationships

```sql
-- One car belongs to one person (example relationship)
CREATE TABLE person (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  car_id BIGINT UNIQUE  -- unique means a car can only be tied to one person
);

CREATE TABLE car (
  id BIGSERIAL PRIMARY KEY,
  model TEXT NOT NULL
);

-- attach a car to a person
UPDATE person SET car_id = 2 WHERE id = 1;

-- INNER JOIN
SELECT p.id, p.name, c.model
FROM person AS p
JOIN car AS c ON p.car_id = c.id;

-- LEFT JOIN (include people without cars)
SELECT p.id, p.name, c.model
FROM person AS p
LEFT JOIN car AS c ON p.car_id = c.id;

-- Find people with no car
SELECT p.*
FROM person AS p
LEFT JOIN car AS c ON p.car_id = c.id
WHERE c.* IS NULL;

-- USING (when join keys share the same name)
-- Example: orders(customer_id) and customers(customer_id)
SELECT *
FROM orders
JOIN customers USING (customer_id);
```

> Not equal operator: `<>`

## Extensions (UUID example)

```sql
SELECT * FROM pg_available_extensions;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
SELECT uuid_generate_v4();
```

## Roles, Users, and Access Control

PostgreSQL 用 role 模型處理權限。`postgres` 是預設 superuser，但日常工作不應長期直接拿 superuser 帳號操作業務資料。

### Create and modify users

```sql
CREATE USER analyst;
CREATE USER analyst WITH PASSWORD 'change-me';
ALTER USER analyst WITH PASSWORD 'new-secret';
```

### Grant object privileges

```sql
GRANT SELECT ON orders TO analyst;
GRANT INSERT, UPDATE ON customers TO analyst;
```

### Revoke privileges

```sql
REVOKE UPDATE ON customers FROM analyst;
REVOKE ALL PRIVILEGES ON orders FROM analyst;
```

### Change ownership

```sql
ALTER TABLE orders OWNER TO analyst;
```

ownership 與 privilege 不完全相同。擁有者可做的事情通常更多，因此變更 owner 前要先想清楚責任邊界。

## Schemas

schema 是資料庫內的 namespace，可用來隔離不同模組、不同人或不同用途的物件。

```sql
CREATE SCHEMA accounting;
CREATE SCHEMA reporting;
```

如果要讓使用者能存取某個 schema，通常至少要先給 `USAGE`：

```sql
GRANT USAGE ON SCHEMA accounting TO analyst;
GRANT SELECT, INSERT, UPDATE, DELETE
ON ALL TABLES IN SCHEMA accounting
TO analyst;
```

這個模式比把所有東西都塞進 `public` 更容易管理。

## Handy snippets from the basics

```sql
-- Create a database and a simple table
CREATE DATABASE mydb;
CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT, age INT);

-- Insert/query/update/delete
INSERT INTO users (name, age) VALUES ('Alice', 30), ('Bob', 25);
SELECT * FROM users; -- list all users
UPDATE users SET age = 31 WHERE name = 'Alice';
DELETE FROM users WHERE name = 'Bob';

-- Drop examples
DROP DATABASE mydb;
DROP TABLE users;
```

### Notes

- Prefer `\copy` inside `psql` for CSV IO when you don’t want server-side file permissions.
- `ON CONFLICT` requires a unique index or primary key on the target column(s).
- Use `EXPLAIN (ANALYZE, BUFFERS)` when queries get slow (beyond this quick sheet).
- `TEXT` 在 PostgreSQL 裡通常是很合理的預設字串型別，不必凡事先寫成 `VARCHAR(255)`.
- 若不是管理任務，盡量不要長期使用 `postgres` superuser 帳號處理一般資料操作。
