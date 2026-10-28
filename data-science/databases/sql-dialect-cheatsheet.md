# SQL Dialect Cheatsheet

不同資料庫的 SQL 大多相通，差異集中在空值處理、型別轉換、取前幾筆與匯入匯出。本篇收集各平台的對照（Phase 3 會再併入 SQL Server / Snowflake 的段落）。

## NULL 處理

| 函式 | 平台 | 說明 |
| --- | --- | --- |
| `COALESCE(x, y, ...)` | 全部（標準 SQL） | 回傳第一個非 `NULL`；跨資料庫優先用這個 |
| `NVL(x, y)` | Oracle | `x` 為 `NULL` 時回傳 `y` |
| `ISNULL(x, y)` | SQL Server | 同上 |

```sql
SELECT NVL(HireDate, DATE '2004-11-19') FROM Employee;   -- Oracle
```

## 型別轉換（Oracle format model）

| 函式 | 用途 | 範例 |
| --- | --- | --- |
| `TO_CHAR(x, fmt)` | number / date → 字串 | `TO_CHAR(UnitPrice, '$999.99')`、`TO_CHAR(BirthDate, 'DD-MON-YYYY')` |
| `TO_DATE(s, fmt)` | 字串 → date | `TO_DATE('2016-01-31', 'YYYY-MM-DD')` |
| `TO_NUMBER(s, fmt)` | 字串 → number | `TO_NUMBER('$15,000.75', '$999,999.99')` |

常用 token：數字 `9`（位數）、`0`（補零）、`,`、`.`、`$`；日期 `YYYY`、`MM`、`MON`、`MONTH`、`DD`、`DY`、`DAY`。轉換失敗幾乎都是字串與 format mask 不對齊。Oracle 無 `FROM` 的常數查詢要寫 `FROM DUAL`。

## 匯入匯出（MySQL）

```sql
-- 匯入 CSV（需 local_infile；client 用 mysql --local_infile=1 連線）
SHOW GLOBAL VARIABLES LIKE 'local_infile';
SET GLOBAL local_infile = true;

LOAD DATA LOCAL INFILE '/path/to/file.csv'
INTO TABLE users
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- 匯出（路徑受 secure_file_priv 限制）
SHOW VARIABLES LIKE 'secure_file_priv';
SELECT name, email
FROM users
INTO OUTFILE '/var/lib/mysql-files/users.csv'
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n';
```

PostgreSQL 的對應是 `COPY` / `\copy`（見 [PostgreSQL](postgresql.md)）。

[Back to Databases](README.md)
