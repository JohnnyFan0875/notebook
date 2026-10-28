[Data Science](../README.md) › [Databases](README.md) › SQL 方言速查

# SQL 方言速查 (SQL Dialect Cheatsheet)

`SELECT`、`JOIN`、`GROUP BY`、window function 在各資料庫大致相同（見 [SQL 查詢基礎](sql-query-foundations.md)）；差異集中在取前幾筆、空值、日期、型別轉換、字串與匯入匯出。先查對照表，再看各平台細節。

## 對照表

| 功能 | PostgreSQL | SQL Server (T-SQL) | MySQL | Oracle | Snowflake | DuckDB |
| --- | --- | --- | --- | --- | --- | --- |
| 取前 n 筆 | `LIMIT n` | `SELECT TOP (n)` / `OFFSET ... FETCH` | `LIMIT n` | `FETCH FIRST n ROWS ONLY`（12c+） | `LIMIT n` | `LIMIT n` |
| 空值替代 | `COALESCE` | `ISNULL` / `COALESCE` | `IFNULL` / `COALESCE` | `NVL` / `COALESCE` | `NVL` / `IFNULL` / `COALESCE` | `IFNULL` / `COALESCE` |
| 現在時間 | `NOW()` | `GETDATE()` / `SYSDATETIME()` | `NOW()` | `SYSDATE` | `CURRENT_TIMESTAMP()` | `NOW()` |
| 取年份 | `EXTRACT(YEAR FROM d)` | `DATEPART(year, d)` / `YEAR(d)` | `YEAR(d)` | `EXTRACT(YEAR FROM d)` | `YEAR(d)` / `DATE_PART('year', d)` | `YEAR(d)` / `EXTRACT` |
| 日期加減 | `d + INTERVAL '1 month'` | `DATEADD(month, 1, d)` | `DATE_ADD(d, INTERVAL 1 MONTH)` | `ADD_MONTHS(d, 1)` | `DATEADD(month, 1, d)` | `d + INTERVAL 1 MONTH` |
| 日期差（天） | `d2 - d1` | `DATEDIFF(day, d1, d2)` | `DATEDIFF(d2, d1)` | `d2 - d1` | `DATEDIFF(day, d1, d2)` | `DATE_DIFF('day', d1, d2)` |
| 截斷到月 | `DATE_TRUNC('month', d)` | `DATETRUNC(month, d)`（2022+） | `DATE_FORMAT(d, '%Y-%m-01')` | `TRUNC(d, 'MM')` | `DATE_TRUNC('month', d)` | `DATE_TRUNC('month', d)` |
| 字串 → 日期 | `TO_DATE(s, 'YYYY-MM-DD')` / `s::date` | `CAST(s AS date)` / `CONVERT(date, s, 23)` | `STR_TO_DATE(s, '%Y-%m-%d')` | `TO_DATE(s, 'YYYY-MM-DD')` | `TO_DATE(s)` | `STRPTIME(s, '%Y-%m-%d')` / `s::DATE` |
| 字串串接 | `\|\|` / `CONCAT` | `+` / `CONCAT` | `CONCAT` | `\|\|` | `\|\|` / `CONCAT` | `\|\|` / `CONCAT` |
| 不分大小寫 LIKE | `ILIKE` | 依 collation（預設不分） | 依 collation（預設不分） | `UPPER(x) LIKE` | `ILIKE` | `ILIKE` |
| 字串聚合 | `STRING_AGG(x, ',')` | `STRING_AGG(x, ',')`（2017+） | `GROUP_CONCAT(x)` | `LISTAGG(x, ',')` | `LISTAGG(x, ',')` | `STRING_AGG(x, ',')` |
| 展開陣列 / JSON | `jsonb_array_elements` / `UNNEST` | `OPENJSON` | `JSON_TABLE` | `JSON_TABLE` | `LATERAL FLATTEN` | `UNNEST` |
| 整數相除 | 捨去小數 | 捨去小數 | 回傳小數 | 回傳小數 | 回傳小數 | 回傳小數（`//` 為整數除法） |
| 匯入 CSV | `COPY` / `\copy` | `BULK INSERT` / `bcp` | `LOAD DATA INFILE` | SQL*Loader | `COPY INTO` | `read_csv('f.csv')` / `COPY` |

| 跨平台陷阱 | 說明 |
| --- | --- |
| `CONCAT` 遇到 `NULL` | 多數平台把 `NULL` 當空字串；MySQL 的 `CONCAT` 只要有 `NULL` 就回傳 `NULL` |
| `\|\|` 遇到 `NULL` | 結果為 `NULL`；Oracle 例外（當空字串）；MySQL 預設 `\|\|` 是邏輯 OR |
| SQL Server `DATEDIFF` | 數的是**跨過的邊界數**：`DATEDIFF(year, '2023-12-31', '2024-01-01')` = 1；算年齡不能直接用 |
| 字串比較大小寫 | SQL Server / MySQL 預設不分大小寫，PostgreSQL / DuckDB 區分；基因名 `TP53` vs `Tp53`（人 vs 小鼠）在前者會被當成相同 |
| 識別字大小寫 | PostgreSQL 未加引號的名稱一律轉小寫，`"SampleID"` 加引號後必須永遠加引號；Snowflake / Oracle 轉大寫 |
| 空字串 | Oracle 把 `''` 當 `NULL` |

## NULL 處理

| 函式 | 平台 | 說明 |
| --- | --- | --- |
| `COALESCE(x, y, ...)` | 全部（標準 SQL） | 第一個非 `NULL`，參數個數不限；**跨平台優先用這個** |
| `NVL(x, y)` | Oracle、Snowflake | 兩個參數 |
| `ISNULL(x, y)` | SQL Server | 兩個參數；回傳型別取第一個參數（`ISNULL(varchar(2) 欄, 'Unknown')` 會被截成 `'Un'`） |
| `IFNULL(x, y)` | MySQL、SQLite、DuckDB、Snowflake | 兩個參數 |
| `NULLIF(x, y)` | 全部 | `x = y` 時回傳 `NULL`；常用於避免除以零 |

```sql
SELECT COALESCE(TradeGDPPercent, ImportGoodPercent, 0) AS trade_percent   -- 依序取第一個有值的
FROM EconomicIndicators;
```

## SQL Server (T-SQL)

### 取前 n 筆與分頁

```sql
SELECT TOP (10) product_id, year_intro
FROM products
ORDER BY year_intro DESC, product_id;           -- 沒有 ORDER BY 的 TOP 只是預覽，不保證哪幾列

SELECT TOP (5) PERCENT artist FROM artists;     -- 依百分比；非標準語法
SELECT TOP (3) WITH TIES name, score FROM t ORDER BY score DESC;   -- 同分的一併保留

-- 分頁（標準語法，2012+）
SELECT product_id FROM products
ORDER BY product_id
OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY;
```

### DDL / DML

```sql
CREATE TABLE test_table (
  test_date DATE,
  test_name VARCHAR(20),
  test_int  INT
);

INSERT INTO table_name (col1, col2) VALUES ('v1', 2);   -- 明確列出欄位，schema 變動時才不會錯位
INSERT INTO table_name (col1, col2)                      -- 查詢結果寫入另一張表
SELECT column1, column2 FROM other_table WHERE flag = 1;

UPDATE table_name SET col1 = 'x', col2 = 3 WHERE some_key = 123;   -- 先用同一個 WHERE 跑 SELECT 確認影響列數
DELETE FROM table_name WHERE some_key = 123;

TRUNCATE TABLE staging_table;                            -- 清空整張表
```

| | `DELETE` | `TRUNCATE TABLE` |
| --- | --- | --- |
| 範圍 | 可加 `WHERE` | 整張表 |
| 方式 | 逐列刪除並記錄 log | 釋放資料頁，快很多 |
| 觸發 trigger | 是 | 否 |
| identity / 序號 | 不重設 | 重設 |
| 外鍵被參照的表 | 可（符合約束時） | 不可 |
| 交易內回滾 | 可 | SQL Server、PostgreSQL 可；MySQL、Oracle 會隱含提交，**無法回滾** |

### 日期與數學函式

```sql
SELECT
  DATEPART(year, ModifiedDate)    AS yr,            -- 數字
  DATENAME(weekday, StartDate)    AS day_name,      -- 文字（受語系設定影響）
  DATEADD(day, -30, '2020-06-21') AS minus_30,      -- 2020-05-22
  DATEDIFF(day, '2020-05-22', '2020-06-21') AS diff,  -- 30
  EOMONTH('2024-02-10')           AS month_end,     -- 2024-02-29
  ROUND(DurationSeconds, -2)      AS to_hundreds,   -- 負數精度：四捨五入到百位
  ROUND(DurationSeconds, 0, 1)    AS truncated,     -- 第三參數非 0：截斷而非四捨五入
  CEILING(x), FLOOR(x), ABS(x), SQRT(x), POWER(x, 2)
FROM Incidents;

-- 星期名稱依日曆順序排序（直接 ORDER BY DATENAME 會變字母順序）
SELECT DATENAME(weekday, StartDate) AS day_of_week, SUM(Duration) AS total_duration
FROM CapitalBikeShare
GROUP BY DATENAME(weekday, StartDate), DATEPART(weekday, StartDate)
ORDER BY DATEPART(weekday, StartDate);              -- 週日 = 1（預設 DATEFIRST 7，依語系可能不同）

-- 時間欄位 sanity check：未來時間、結束早於開始
SELECT *
FROM CapitalBikeShare
WHERE StartDate > GETDATE() OR EndDate > GETDATE() OR StartDate > EndDate;
```

`FORMAT(SUM(Duration), '#,0.00')` 產生千分位字串，只用在最後的顯示層；結果還要排序或計算時保留數值欄。

### 變數、迴圈與 CTE

```sql
DECLARE @Snack VARCHAR(10) = 'Cookies';          -- 宣告同時給值
DECLARE @Price DECIMAL(10, 2);
SET @Price = 2.5;                                 -- 單一賦值
SELECT @Price = price FROM snacks WHERE id = 1;   -- 從查詢取值（符合多列時取最後一列，不報錯）

DECLARE @ctr INT = 1;
WHILE @ctr < 10                                   -- 逐列處理很慢；能用集合運算就不要寫迴圈
BEGIN
  PRINT @ctr;
  SET @ctr += 1;
END;

-- CTE 可在名稱後列出欄名；先聚合再接回明細
WITH MaxBP (Age, MaxBloodPressure) AS (
  SELECT Age, MAX(BloodPressure) FROM Patients GROUP BY Age
)
SELECT p.PatientName, p.Age, p.BloodPressure
FROM Patients AS p
JOIN MaxBP AS m
  ON p.Age = m.Age AND p.BloodPressure = m.MaxBloodPressure;
```

交易與 `TRY...CATCH` 見 [交易與錯誤處理](sql-transactions.md#sql-servertrycatch)；執行計畫見 [查詢效能](sql-query-performance.md)。

## PostgreSQL

```sql
SELECT NOW()::DATE;                                         -- :: 是 PostgreSQL 的 CAST 簡寫
SELECT NOW() + INTERVAL '1 month', NOW() - INTERVAL '10 years';
SELECT EXTRACT(YEAR FROM NOW()), DATE_TRUNC('day', created_at), AGE(NOW(), created_at)
FROM customers;
SELECT generate_series(DATE '2024-01-01', DATE '2024-12-01', INTERVAL '1 month');   -- 產生完整月份序列，補缺月用
SELECT name FROM people WHERE name ILIKE 'ade%';            -- 不分大小寫
SELECT x IS DISTINCT FROM y;                                -- NULL 安全的不等於
```

psql、`COPY`、DDL 與權限見 [PostgreSQL：psql 與 COPY](postgresql-psql-and-copy.md)；JSONB 見 [NoSQL 基礎](nosql-foundations.md#postgresql-jsonb)。

## MySQL：匯入匯出

```sql
-- 匯入 CSV（server 與 client 都要開 local_infile；client 用 mysql --local-infile=1 連線）
SHOW GLOBAL VARIABLES LIKE 'local_infile';
SET GLOBAL local_infile = 1;

LOAD DATA LOCAL INFILE '/path/to/file.csv'
INTO TABLE users
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;                                    -- 跳過標題列

-- 匯出：路徑受 secure_file_priv 限制，檔案寫在 server 端
SHOW VARIABLES LIKE 'secure_file_priv';
SELECT name, email
FROM users
INTO OUTFILE '/var/lib/mysql-files/users.csv'
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n';
```

## Oracle：format model

| 函式 | 用途 | 範例 |
| --- | --- | --- |
| `TO_CHAR(x, fmt)` | 數字 / 日期 → 字串 | `TO_CHAR(UnitPrice, '$999.99')`、`TO_CHAR(BirthDate, 'DD-MON-YYYY')` |
| `TO_DATE(s, fmt)` | 字串 → 日期 | `TO_DATE('2016-01-31', 'YYYY-MM-DD')` |
| `TO_NUMBER(s, fmt)` | 字串 → 數字 | `TO_NUMBER('$15,000.75', '$999,999.99')` |
| `NVL(x, y)` | 空值替代 | `NVL(HireDate, DATE '2004-11-19')` |

常用 token：數字 `9`（位數）、`0`（補零）、`,`、`.`、`$`；日期 `YYYY`、`MM`、`MON`、`MONTH`、`DD`、`DY`、`DAY`、`HH24`、`MI`、`SS`。轉換失敗幾乎都是字串與 format mask 不對齊。沒有資料表的常數查詢要寫 `SELECT ... FROM DUAL`（23ai 起可省略）。

## Snowflake：半結構化資料

Snowflake 用 `VARIANT` 存 JSON（另有 `OBJECT`、`ARRAY`），以 `:` 取欄位、`LATERAL FLATTEN` 把陣列展開成列：

```sql
SELECT PARSE_JSON('{"name":"alice","tags":["a","b"]}') AS obj;     -- 字串 → VARIANT

SELECT
  e.payload:user_id::STRING   AS user_id,      -- :key 取值，::型別 轉型
  f.value::STRING             AS tag,
  f.index                     AS tag_position
FROM events AS e,
     LATERAL FLATTEN(input => e.payload:tags) AS f;   -- 每個陣列元素一列，原始列跟著複製
```

| 效能習慣 | 原因 |
| --- | --- |
| 不用 `SELECT *` | 欄式儲存，只讀需要的欄就少掃描資料 |
| 篩選條件對齊 clustering key / 日期 | 讓 micro-partition pruning 跳過不相關的區塊 |
| 查 `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY` | 找慢查詢、回查 SQL 是否執行過（`query_text ILIKE '%...%'`、`execution_time`） |

雲端資料倉儲的比較見 [雲端資料倉儲](../data-engineering/cloud-data-warehouses.md)。

## DuckDB

語法接近 PostgreSQL，另加許多便利寫法：`SELECT * EXCLUDE (col)`、`GROUP BY ALL`、`QUALIFY`、`PIVOT`、直接 `FROM 'file.parquet'`。用法見 [DuckDB 與 Parquet](duckdb-and-parquet.md)。
