[Data Science](../README.md) › [Databases](README.md) › PostgreSQL：psql 與 COPY

# PostgreSQL：psql 與 COPY

PostgreSQL 的日常操作速查：psql 連線與 meta-command、CSV 匯入匯出、建表與型別選擇、upsert、備份還原、權限與 schema。查詢語法見 [SQL 查詢基礎](sql-query-foundations.md)；日期函式等方言差異見 [SQL 方言速查](sql-dialect-cheatsheet.md#postgresql)。

## psql

```bash
psql -h 127.0.0.1 -p 5432 -U admin shopdb        # 主機 / 埠 / 使用者 / 資料庫
psql "postgresql://admin@127.0.0.1:5432/shopdb"  # 同上，URI 寫法
psql -d shopdb -c "SELECT count(*) FROM orders"  # 執行單一指令後離開
psql -d shopdb -f migration.sql                  # 執行 SQL 檔
PAGER='less -S' psql shopdb                      # 寬表不換行，左右捲動
```

密碼不要寫在指令或腳本裡：放 `~/.pgpass`（Windows：`%APPDATA%\postgresql\pgpass.conf`，格式 `host:port:db:user:password`）或環境變數 `PGPASSWORD`。

| meta-command | 作用 |
| --- | --- |
| `\l` | 列出資料庫 |
| `\c shopdb` | 切換資料庫 |
| `\dn` | 列出 schema |
| `\dt` / `\dt reporting.*` | 列出資料表 / 指定 schema 的資料表 |
| `\d orders` / `\d+ orders` | 欄位、型別、index、constraint / 加上大小與註解 |
| `\di`、`\dv`、`\df` | index、view、function |
| `\du` | 角色與權限 |
| `\x` | 切換直式顯示（寬列好讀） |
| `\timing` | 顯示每個查詢的執行時間 |
| `\i file.sql` | 執行 SQL 檔 |
| `\e` | 用編輯器編輯上一個查詢 |
| `\q` | 離開 |

## CSV 匯入匯出

```sql
-- \copy：psql 的 client 端指令，讀寫「你這台電腦」上的檔案，不需要 superuser
\copy customers FROM 'customers.csv' WITH (FORMAT csv, HEADER true)
\copy (SELECT id, order_date, total FROM orders ORDER BY id) TO 'orders.csv' WITH (FORMAT csv, HEADER true)

-- COPY：SQL 指令，讀寫「資料庫伺服器」上的檔案，需要 pg_read_server_files / pg_write_server_files 權限
COPY customers FROM '/srv/data/customers.csv' WITH (FORMAT csv, HEADER true, NULL 'NA');
```

| 選項 | 說明 |
| --- | --- |
| `FORMAT csv` | 處理引號與內含逗號；預設是 tab 分隔的 text 格式 |
| `HEADER true` | 第一列是欄名（匯入時略過，不比對欄名） |
| `DELIMITER E'\t'` | 改分隔符（TSV） |
| `NULL 'NA'` | 指定哪個字串代表 `NULL`（R 輸出的 `NA`） |
| `(col1, col2)` | 只匯入指定欄：`\copy t (col1, col2) FROM ...` |

`\copy` 整個指令要寫在同一行，結尾不加分號。匯入前資料表必須已存在；有一列格式錯就整批失敗（PostgreSQL 17 起可用 `ON_ERROR ignore` 跳過壞列）。從 Python 匯入見 [Python 與 SQLAlchemy](python-sqlalchemy.md#pandas-讀寫)。

## 建資料庫與資料表

```sql
CREATE DATABASE analytics_db OWNER analyst ENCODING 'UTF8' TEMPLATE template0;

CREATE TABLE customers (
  customer_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,   -- 標準寫法；舊寫法 BIGSERIAL
  full_name   TEXT NOT NULL,
  email       TEXT UNIQUE,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE orders (
  order_id    BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES customers (customer_id),
  status      TEXT CHECK (status IN ('pending', 'processing', 'shipped', 'canceled')),
  total       NUMERIC(12, 2) NOT NULL CHECK (total >= 0),
  order_date  DATE NOT NULL
);
CREATE INDEX ON orders (customer_id);                -- 外鍵欄不會自動建 index
```

```sql
ALTER TABLE orders RENAME TO sales_orders;
ALTER TABLE sales_orders ADD COLUMN note TEXT;
ALTER TABLE sales_orders DROP COLUMN status;
ALTER TABLE sales_orders ALTER COLUMN total TYPE NUMERIC(14, 2);
ALTER TABLE sales_orders ALTER COLUMN note SET DEFAULT '';
ALTER TABLE customers ALTER COLUMN email DROP NOT NULL;
ALTER TABLE customers ADD CONSTRAINT uniq_customers_email UNIQUE (email);
ALTER TABLE customers DROP CONSTRAINT uniq_customers_email;
ALTER SEQUENCE customers_customer_id_seq RESTART WITH 1000;   -- 序號從 1000 開始
DROP TABLE IF EXISTS sales_orders;
```

### 型別選擇

| 資料 | 用 | 避免 |
| --- | --- | --- |
| 文字 | `TEXT`（無長度限制，效能與 `VARCHAR` 相同） | 習慣性 `VARCHAR(255)` |
| 整數 / ID | `INTEGER`、`BIGINT`；自動編號用 `GENERATED ... AS IDENTITY` | 樣本 ID `"001"` 存成整數（前導 0 會消失） |
| 金額、需要精確的小數 | `NUMERIC(p, s)` | `REAL` / `DOUBLE PRECISION`（浮點誤差） |
| 測量值 | `DOUBLE PRECISION` | |
| 日期 / 時間 | `DATE`；時間點一律 `TIMESTAMPTZ`（以 UTC 儲存，依連線時區顯示） | 日期存成字串；`TIMESTAMP`（沒有時區，跨時區資料會混淆） |
| 布林 | `BOOLEAN` | `'Y'` / `'N'` 字串 |
| 彈性屬性 | `JSONB`（見 [NoSQL 基礎](nosql-foundations.md#postgresql-jsonb)） | 把所有欄位都塞進 JSON |
| 陣列 | `TEXT[]`、`INTEGER[]` | 逗號串成一個字串 |

## Upsert：`ON CONFLICT`

```sql
INSERT INTO customers (full_name, email)
VALUES ('A. Chen', 'alice@example.com')
ON CONFLICT (email)                                   -- 需要 email 上有 UNIQUE / PK
DO UPDATE SET full_name = EXCLUDED.full_name;         -- EXCLUDED = 這次想插入的那一列

INSERT INTO customers (full_name, email)
VALUES ('Bob', 'bob@example.com')
ON CONFLICT (email) DO NOTHING;                       -- 已存在就略過

UPDATE customers SET full_name = 'Alice C.' WHERE email = 'alice@example.com' RETURNING *;   -- RETURNING 回傳被改的列
```

## 備份與還原

```bash
# 純 SQL 格式：可讀、可用 psql 還原
pg_dump -U admin -d shopdb -f shopdb_$(date +%F).sql
psql -U admin -d shopdb_restored -f shopdb_2025-08-20.sql

# custom 格式（-Fc）：壓縮、可選擇性還原、可平行還原；建議用於正式備份
pg_dump -U admin -d shopdb -Fc -f shopdb.dump
pg_restore -U admin -d shopdb_restored --jobs 4 shopdb.dump
pg_restore -U admin -d shopdb_restored -t orders shopdb.dump     # 只還原一張表

pg_dump -U admin -d shopdb --schema-only -f schema.sql           # 只要結構
```

## 角色、權限與 schema

PostgreSQL 的使用者和群組都是 role。日常分析不要用 `postgres` superuser；先建「權限集合」role，再把使用者加進去。

```sql
-- 1. 權限集合
CREATE ROLE readonly NOLOGIN;
GRANT USAGE ON SCHEMA reporting TO readonly;                          -- 先要能「進入」schema
GRANT SELECT ON ALL TABLES IN SCHEMA reporting TO readonly;           -- 現有的表
ALTER DEFAULT PRIVILEGES IN SCHEMA reporting
  GRANT SELECT ON TABLES TO readonly;                                 -- 之後新建的表也適用

-- 2. 使用者
CREATE ROLE analyst LOGIN PASSWORD 'change-me';                       -- CREATE USER = CREATE ROLE ... LOGIN
GRANT readonly TO analyst;
ALTER ROLE analyst PASSWORD 'new-secret';

-- 3. 收回與擁有權
REVOKE UPDATE ON customers FROM analyst;
ALTER TABLE orders OWNER TO etl_owner;                                -- owner 可改表結構、刪表，權限比 GRANT 大

-- schema：資料庫內的命名空間
CREATE SCHEMA reporting;
SET search_path TO reporting, public;                                 -- 未加 schema 前綴時的查找順序
```

| 常見問題 | 原因 |
| --- | --- |
| `permission denied for schema` | 少了 `GRANT USAGE ON SCHEMA` |
| 新建的表又沒權限 | `GRANT ... ON ALL TABLES` 只影響現有的表；要加 `ALTER DEFAULT PRIVILEGES` |
| `relation does not exist` 但表明明在 | 表在別的 schema 且不在 `search_path`；或建表時名稱加了引號、有大寫 |

## Extensions

```sql
SELECT * FROM pg_available_extensions;
CREATE EXTENSION IF NOT EXISTS pg_trgm;             -- 模糊字串比對與 LIKE '%x%' 的 index
CREATE EXTENSION IF NOT EXISTS tablefunc;           -- crosstab（見 Window Functions）
SELECT gen_random_uuid();                           -- 13+ 內建，不再需要 uuid-ossp
```

| Extension | 用途 |
| --- | --- |
| `pg_stat_statements` | 統計每個查詢的累積執行時間，找出最耗資源的查詢 |
| `pg_trgm` | 相似度搜尋、子字串 index |
| `postgis` | 地理空間 |
| `pgvector` | 向量相似度搜尋（embeddings；見 [RAG](../llm/rag/README.md)） |
