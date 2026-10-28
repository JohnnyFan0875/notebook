# SQL Dialect Cheatsheet

不同資料庫的 SQL 大多相通（`SELECT`、`JOIN`、`GROUP BY` 見 [SQL Query Foundations](sql-query-foundations.md)），差異集中在取前幾筆、空值處理、日期函式、型別轉換與匯入匯出。本篇先給對照表，再依平台列出細節。

## 對照表

| 功能 | PostgreSQL | SQL Server (T-SQL) | MySQL | Oracle | Snowflake |
| --- | --- | --- | --- | --- | --- |
| 取前 n 筆 | `LIMIT n` | `SELECT TOP n` / `OFFSET ... FETCH` | `LIMIT n` | `FETCH FIRST n ROWS ONLY`（12c+） | `LIMIT n` |
| 空值替代 | `COALESCE` | `ISNULL` / `COALESCE` | `IFNULL` / `COALESCE` | `NVL` / `COALESCE` | `NVL` / `IFNULL` / `COALESCE` |
| 現在時間 | `NOW()` | `GETDATE()` / `SYSDATETIME()` | `NOW()` | `SYSDATE` | `CURRENT_TIMESTAMP()` |
| 取日期部分 | `EXTRACT(YEAR FROM d)` | `DATEPART(year, d)` | `YEAR(d)` / `EXTRACT` | `EXTRACT(YEAR FROM d)` | `DATE_PART('year', d)` / `EXTRACT` |
| 日期加減 | `d + INTERVAL '1 month'` | `DATEADD(month, 1, d)` | `DATE_ADD(d, INTERVAL 1 MONTH)` | `ADD_MONTHS(d, 1)` | `DATEADD(month, 1, d)` |
| 日期差 | `d2 - d1`、`AGE()` | `DATEDIFF(day, d1, d2)` | `DATEDIFF(d2, d1)` | `d2 - d1` | `DATEDIFF(day, d1, d2)` |
| 截斷到日 / 月 | `DATE_TRUNC('month', d)` | `DATETRUNC(month, d)`（2022+） | `DATE_FORMAT(d, '%Y-%m-01')` | `TRUNC(d, 'MM')` | `DATE_TRUNC('month', d)` |
| 字串 → 日期 | `TO_DATE(s, 'YYYY-MM-DD')` / `s::date` | `CAST(s AS date)` / `CONVERT` | `STR_TO_DATE(s, '%Y-%m-%d')` | `TO_DATE(s, 'YYYY-MM-DD')` | `TO_DATE(s)` |
| 字串串接 | `\|\|` / `CONCAT` | `+` / `CONCAT` | `CONCAT` | `\|\|` | `\|\|` / `CONCAT` |
| 不分大小寫 LIKE | `ILIKE` | 依 collation（預設不分） | 依 collation（預設不分） | `UPPER(x) LIKE` | `ILIKE` |
| 展開 JSON 陣列 | `jsonb_array_elements` | `OPENJSON` | `JSON_TABLE` | `JSON_TABLE` | `LATERAL FLATTEN` |
| 匯入 CSV | `COPY` / `\copy` | `BULK INSERT` / `bcp` | `LOAD DATA INFILE` | SQL*Loader | `COPY INTO` |

## NULL 處理

| 函式 | 平台 | 說明 |
| --- | --- | --- |
| `COALESCE(x, y, ...)` | 全部（標準 SQL） | 回傳第一個非 `NULL`；跨資料庫優先用這個 |
| `NVL(x, y)` | Oracle | `x` 為 `NULL` 時回傳 `y` |
| `ISNULL(x, y)` | SQL Server | 同上 |

```sql
SELECT NVL(HireDate, DATE '2004-11-19') FROM Employee;   -- Oracle
```

### `ISNULL()` and `COALESCE()`

#### `ISNULL()`

`ISNULL(expr, fallback)` 會在 `expr` 是 `NULL` 時回傳替代值。

```sql
SELECT
  GDP,
  Country,
  ISNULL(Country, 'Unknown') AS new_country
FROM EconomicIndicators;
```

也可以拿一個欄位去補另一個欄位：

```sql
SELECT
  TradeGDPPercent,
  ImportGoodPercent,
  ISNULL(TradeGDPPercent, ImportGoodPercent) AS new_percent
FROM EconomicIndicators;
```

#### `COALESCE()`

如果可能有多個候選值，`COALESCE()` 通常更彈性。

```sql
SELECT
  COALESCE(TradeGDPPercent, ImportGoodPercent, 0) AS trade_percent
FROM EconomicIndicators;
```

心智模型上：

- `ISNULL()`: 兩選一，偏 SQL Server 風格
- `COALESCE()`: 多選一，跨資料庫也常見

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

PostgreSQL 的對應是 `COPY` / `\copy`（見 [PostgreSQL](postgresql-psql-and-copy.md)）。

## SQL Server (T-SQL)

先分兩層理解：

- SQL Server：Microsoft 的 relational database system
- T-SQL：SQL Server 常用的 SQL dialect，也就是 Transact-SQL

很多查詢觀念仍然是通用 SQL，但在語法細節上，SQL Server 會有自己的寫法。

### `TOP` Instead of `LIMIT`

在 SQL Server 裡，取前幾筆資料很常用 `TOP`，而不是 `LIMIT`。

```sql
SELECT TOP (5) artist
FROM artists;
```

這和其他系統常見的：

```sql
SELECT artist
FROM artists
LIMIT 5;
```

概念相近，但語法位置不同。

#### `TOP ... PERCENT`

SQL Server 也支援用百分比取樣：

```sql
SELECT TOP (5) PERCENT artist
FROM artists;
```

這種寫法在跨資料庫 SQL 裡比較少見，所以如果你要寫 portable query，要先確認目標系統是否支援。

#### `TOP` Should Usually Pair with `ORDER BY`

如果你想要的是「最新 10 筆」、「最早 10 筆」、「最高分前 10 筆」，一定要搭配 `ORDER BY`。

```sql
SELECT TOP (10) product_id, year_intro
FROM products
ORDER BY year_intro DESC, product_id;
```

重點是：

- `TOP` 只負責裁列數
- `ORDER BY` 才負責定義哪幾列會被留下

如果沒有排序，`TOP` 的結果通常只適合快速 preview，不適合業務判讀。

#### Mixed Sort Directions

`ORDER BY` 可以對不同欄位指定不同方向：

```sql
SELECT TOP (10)
  appearances,
  year_intro
FROM products
ORDER BY
  year_intro DESC,
  appearances DESC;
```

這在 top-N 排序裡很常見，因為第一欄決定主排序，第二欄拿來打破 tie。

### Basic DDL: `CREATE TABLE`

SQL Server 入門最常見的 DDL 是建立表：

```sql
CREATE TABLE test_table (
  test_date DATE,
  test_name VARCHAR(20),
  test_int  INT
);
```

建立表時最先要想的通常是：

- table / column 命名
- 每個欄位存什麼型別
- 欄位長度與精度是否足夠

這些雖然不只 SQL Server 需要，但在 T-SQL 練習裡很常一起出現。

### Basic DML: `INSERT`, `UPDATE`, `DELETE`

#### `INSERT`

最穩的做法通常是明確列欄位：

```sql
INSERT INTO table_name (col1, col2, col3)
VALUES ('value1', 'value2', value3);
```

這比省略欄位名稱更安全，因為：

- 可讀性更高
- schema 變動時比較不容易 silently 出錯

#### `INSERT ... SELECT`

SQL Server 很常直接把查詢結果寫進另一張表：

```sql
INSERT INTO table_name (col1, col2, col3)
SELECT
  column1,
  column2,
  column3
FROM other_table
WHERE some_condition = 1;
```

實務上很重要的一個習慣是：

- 不要偷懶寫 `SELECT *`
- 明確列出來源與目標欄位

這能避免來源表結構調整後，匯入邏輯悄悄錯位。

#### `UPDATE`

```sql
UPDATE table_name
SET
  column1 = value1,
  column2 = value2
WHERE some_key = 123;
```

最重要的提醒不是語法，而是：

- `UPDATE` 前先確認 `WHERE`
- 沒有 `WHERE` 往往代表你要更新整張表

#### `DELETE`

```sql
DELETE
FROM table_name
WHERE some_key = 123;
```

和 `UPDATE` 一樣，真正的風險通常不是不會寫，而是忘了 `WHERE`。

### `DELETE` vs. `TRUNCATE TABLE`

如果你要清掉整張表，SQL Server 常見兩種操作：

```sql
DELETE FROM table_name;
```

或：

```sql
TRUNCATE TABLE table_name;
```

可以先這樣記：

- `DELETE`: row-level delete，通常可加 `WHERE`
- `TRUNCATE TABLE`: 一次清空整張表，不是逐列刪

所以：

- 如果你要刪部分資料，用 `DELETE ... WHERE ...`
- 如果你明確要清空整張 staging / temp-like table，`TRUNCATE TABLE` 會更直接

不過在正式資料表上動 `TRUNCATE` 前，仍要先確認資料生命週期與權限設計。

### Date Functions in T-SQL

#### `DATEPART()`

`DATEPART()` 用來取日期的一部分，例如年、月、日、星期。

```sql
SELECT
  DATEPART(year, ModifiedDate)  AS sales_year,
  DATEPART(month, ModifiedDate) AS sales_month,
  DATEPART(day, ModifiedDate)   AS sales_day
FROM SaleGoal;
```

#### `DATENAME()`

如果你要拿到可讀的星期或月份名稱，`DATENAME()` 會比 `DATEPART()` 更直觀。

```sql
SELECT
  DATENAME(weekday, StartDate) AS day_of_week,
  DATENAME(month, StartDate)   AS month_name
FROM CapitalBikeShare;
```

這很常用在報表欄位或 EDA 摘要，但要注意它回傳的是文字，不是可自然排序的數字。

#### Sorting weekday labels logically

如果直接對 `DATENAME(weekday, ...)` 排序，通常會得到字母順序，不是星期順序。

```sql
SELECT
  DATENAME(weekday, StartDate) AS day_of_week,
  SUM(Duration) AS total_duration
FROM CapitalBikeShare
GROUP BY DATENAME(weekday, StartDate)
ORDER BY CASE
  WHEN DATENAME(weekday, StartDate) = 'Sunday' THEN 1
  WHEN DATENAME(weekday, StartDate) = 'Monday' THEN 2
  WHEN DATENAME(weekday, StartDate) = 'Tuesday' THEN 3
  WHEN DATENAME(weekday, StartDate) = 'Wednesday' THEN 4
  WHEN DATENAME(weekday, StartDate) = 'Thursday' THEN 5
  WHEN DATENAME(weekday, StartDate) = 'Friday' THEN 6
  WHEN DATENAME(weekday, StartDate) = 'Saturday' THEN 7
END;
```

這是一個很常見的報表技巧：顯示可讀標籤，但另外手動控制排序邏輯。

#### `DATEADD()`

`DATEADD(datepart, number, date)` 可以加減日期。

```sql
SELECT DATEADD(day, 30, '2020-06-21')  AS plus_30_days,
       DATEADD(day, -30, '2020-06-21') AS minus_30_days;
```

這很適合拿來做：

- 到期日計算
- 前後 N 天 / 月 / 年
- 滾動視窗邊界

#### `DATEDIFF()`

`DATEDIFF(datepart, startdate, enddate)` 用來算差距。

```sql
SELECT
  DATEDIFF(day, '2020-05-22', '2020-06-21') AS difference_1,
  DATEDIFF(day, '2020-07-21', '2020-06-21') AS difference_2;
```

很常見的用途是：

- 距今天幾天
- 兩次事件相差幾天 / 幾月
- 流程耗時

### Math Functions in T-SQL

#### `ROUND()`

```sql
SELECT
  ROUND(DurationSeconds, 0)  AS round_to_whole,
  ROUND(DurationSeconds, 1)  AS round_to_one_decimal,
  ROUND(DurationSeconds, -1) AS round_to_ten,
  ROUND(DurationSeconds, -2) AS round_to_hundred
FROM Incidents;
```

負的 precision 很實用，因為可以把數字直接四捨五入到十位、百位。

#### Truncating with `ROUND()`

`ROUND(number, length, 1)` 可以做截斷而不是一般四捨五入。

```sql
SELECT
  ROUND(DurationSeconds, 0)    AS rounding_to_whole,
  ROUND(DurationSeconds, 0, 1) AS truncating_to_whole
FROM Incidents;
```

#### Other handy math functions

```sql
SELECT
  ABS(-2.77) AS abs_decimal,
  ABS(-2)    AS abs_int,
  SQRT(9)    AS sqrt_9;
```

常見還包括：

- `ABS()`
- `SQRT()`
- `POWER()`
- `CEILING()`
- `FLOOR()`

### Temporal EDA Quick Checks

交易型資料很常先做一些時間欄位的 sanity check，快速抓出明顯不合理的 records。

```sql
SELECT *
FROM CapitalBikeShare
WHERE StartDate > GETDATE()
   OR EndDate > GETDATE()
   OR StartDate > EndDate;
```

這類查詢很適合當第一輪資料檢查，尤其在：

- 裝置時間校正可能出錯
- 分散式系統跨來源收資料
- 你還不確定欄位可信度時

### Formatting for Human-Readable Output

如果結果主要是要給人看，而不是給下游計算，`FORMAT()` 可以讓輸出更接近報表。

```sql
SELECT
  FORMAT(SUM(Duration), 'n', 'en-us') AS duration_n,
  FORMAT(SUM(Duration), '#,0.00') AS duration_custom
FROM CapitalBikeShare;
```

不過實務上要記得：

- `FORMAT()` 偏 presentation
- 如果結果還要再排序、比較或做數值運算，盡量保留原始 numeric 欄位

### Variables in T-SQL

T-SQL 很常用變數把中間值存起來，尤其在 stored procedure、批次腳本與流程控制裡。

#### Declaring variables

```sql
DECLARE @Snack VARCHAR(10);
DECLARE @Counter INT;
DECLARE @Price DECIMAL(10,2);
```

常見型別包括：

- `VARCHAR(n)`
- `INT`
- `DECIMAL(p, s)` / `NUMERIC(p, s)`

#### Assigning values

可以用 `SET`：

```sql
DECLARE @Snack VARCHAR(10);
SET @Snack = 'Cookies';
```

也可以用 `SELECT`：

```sql
DECLARE @Snack VARCHAR(10);
SELECT @Snack = 'Candy';
```

簡單記法：

- `SET` 比較明確，適合單一變數賦值
- `SELECT` 在 T-SQL 中也常見，尤其是從查詢結果取值

### `WHILE` Loops

T-SQL 支援 `WHILE` 進行流程控制，但實務上要保守使用，因為很多逐列問題其實應該先想集合化解法。

```sql
DECLARE @ctr INT;
SET @ctr = 1;

WHILE @ctr < 10
BEGIN
  PRINT @ctr;
  SET @ctr = @ctr + 1;
END;
```

#### 什麼時候要小心

- 大量資料逐筆處理通常很慢
- 能用 set-based query、window function 或 CTE 解決時，通常不要先寫 loop

### CTEs in T-SQL

CTE 很適合把複雜查詢拆成可讀的中間步驟。

#### Basic CTE syntax

```sql
WITH CTEName (Col1, Col2) AS (
  SELECT Col1, Col2
  FROM SomeTable
)
SELECT *
FROM CTEName;
```

#### Example: aggregate first, then join back

```sql
WITH MaxBloodPressureByAge (Age, MaxBloodPressure) AS (
  SELECT
    Age,
    MAX(BloodPressure) AS MaxBloodPressure
  FROM Patients
  GROUP BY Age
)
SELECT
  p.PatientName,
  p.Age,
  p.BloodPressure
FROM Patients AS p
JOIN MaxBloodPressureByAge AS m
  ON p.Age = m.Age
 AND p.BloodPressure = m.MaxBloodPressure;
```

這個模式非常實用，因為它把：

1. 先聚合
2. 再回接明細

的流程寫得很清楚。

## PostgreSQL 日期時間

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

psql、`COPY` 與管理指令見 [PostgreSQL: psql and COPY](postgresql-psql-and-copy.md)。

## Snowflake

### Lateral Join and Semi-Structured Data

Snowflake 的一個特別實用場景，是把 semi-structured data 展開後再查詢。

#### Structured vs. Semi-Structured

- structured data: 欄位固定、schema 明確的 table
- semi-structured data: 常見如 JSON，欄位可能可變、巢狀結構較多

Snowflake 原生支援 JSON 類資料，常用 `VARIANT` 儲存。

#### `PARSE_JSON`

當 JSON 先以字串存在時，可以用 `PARSE_JSON()` 轉成 Snowflake 可操作的 `VARIANT`。

```sql
SELECT PARSE_JSON('{"name":"alice","age":30}') AS obj;
```

#### `LATERAL` + `FLATTEN`

當 JSON 裡有陣列或巢狀資料時，常用 `LATERAL` 搭配 `FLATTEN()` 把內容展開成列。

心智模型可以想成：

- 先保留原始列
- 再把某個巢狀欄位拆成多列
- 最後像查普通 table 一樣篩選與聚合

這是 Snowflake 處理 event logs、API payloads、clickstream 與彈性 schema 資料時的常見做法。

### Query Performance Habits

#### Avoid `SELECT *`

在 Snowflake 這種 columnar warehouse，少讀欄位通常就少掃描資料。

```sql
SELECT o_orderdate, o_orderstatus
FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF100.ORDERS;
```

比起：

```sql
SELECT *
FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF100.ORDERS;
```

更符合分析型查詢的效能思路。

#### Read Query History

Snowflake 提供 `query_history` 類型的監控檢視，能用來看：

- `query_text`
- `start_time`
- `end_time`
- `execution_time`

這類資訊很適合拿來：

- 找慢查詢
- 回查某段 SQL 是否真的執行過
- 用 `ILIKE` 做 case-insensitive 搜尋，定位特定分析或 job
