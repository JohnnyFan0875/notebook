# Databases

這個章節整理資料分析常見的關聯式資料庫筆記。對資料科學工作來說，SQL 不只是查資料，更是前置清理、聚合、抽樣與建立分析資料表的重要工具。

## 建議閱讀順序

1. 先讀 [SQL Query Foundations](sql-query-foundations.md)、[SQL Joins and Set Operations](sql-joins-and-set-operations.md)、[SQL Reporting Patterns](sql-reporting-patterns.md)，把最常用的查詢與報表邏輯補穩。
2. 再讀 [Database Design Principles](database-design-principles.md) 與 [Database Normalization](database-normalization.md)，理解資料表為什麼會長成那樣。
3. 如果工作偏分析，接著讀 [Business Analysis in SQL](business-analysis-in-sql.md)、window function、recursive SQL 與 performance notes。
4. 之後再依實際平台選 PostgreSQL、SQL Server、MySQL、Oracle、Snowflake 或 NoSQL 補專用語法與實務。

## 主題分組

### SQL 基礎與分析查詢

- [SQL Query Foundations](sql-query-foundations.md)
- [SQL Joins and Set Operations](sql-joins-and-set-operations.md)
- [SQL Reporting Patterns](sql-reporting-patterns.md)
- [Business Analysis in SQL](business-analysis-in-sql.md)
- [Recursive and Hierarchical SQL](recursive-and-hierarchical-sql.md)

### 資料模型與系統觀念

- [Database Design Principles](database-design-principles.md)
- [Database Normalization](database-normalization.md)
- [NoSQL Foundations](nosql-foundations.md)

### PostgreSQL

- [PostgreSQL](postgresql.md)
- [PostgreSQL Window Functions and Pivoting](postgresql-window-functions-and-pivoting.md)
- [PostgreSQL Query Performance](postgresql-query-performance.md)
- [PostgreSQL Transactions and Exception Handling](postgresql-transactions-and-exception-handling.md)

### SQL Server

- [SQL Server Basics](sql-server-basics.md)
- [SQL Server T-SQL Patterns](sql-server-tsql-patterns.md)
- [SQL Server Functions and Stored Procedures](sql-server-functions-and-stored-procedures.md)
- [SQL Server Transactions and Error Handling](sql-server-transactions-and-error-handling.md)
- [SQL Server Window Functions](sql-server-window-functions.md)
- [SQL Server Query Performance](sql-server-query-performance.md)
- [SQL Server Triggers](sql-server-triggers.md)

### 其他平台

- [MySQL](mysql.md)
- [Oracle SQL Patterns](oracle-sql-patterns.md)
- [Snowflake SQL Patterns](snowflake-sql-patterns.md)

## 建議使用時機

- 原始資料量太大，不適合先全部拉進 pandas。
- 需要在資料庫端先做 join、group by、window function 或條件過濾。
- 需要重新建立 `WHERE`、`GROUP BY`、`HAVING`、`COUNT()`、`LIMIT` 等基礎查詢心智模型。
- 需要把原始資料整理成報表欄位，包含 `CASE` 分類、`CAST()` 清理型別、比例欄位與分層計算。
- 需要釐清 `INNER/LEFT/RIGHT/FULL/CROSS/SELF JOIN`、`UNION` / `UNION ALL` / `INTERSECT`、以及 `EXISTS` / `NOT EXISTS` 的使用時機。
- 需要熟悉 SQL Server 裡的 `TOP`、基本 CRUD、`TRUNCATE TABLE` 與初學者 join 習慣。
- 需要在 SQL Server 中分清楚 scalar UDF、table-valued function、stored procedure、output parameter 與 return value。
- 需要在 SQL Server 中處理 `ISNULL`、`COALESCE`、日期加減、變數、CTE 或簡單流程控制。
- 需要在 SQL Server 中處理 `TRY...CATCH`、`THROW`、`@@TRANCOUNT`、`XACT_STATE()` 或 transaction rollback 模式。
- 需要在 SQL Server 中做 running total、前後列比較、分組排名與其他 window function 分析。
- 需要先建立 document、key-value、graph、JSONB 與 column-oriented storage 的基本心智模型。
- 需要在 Oracle 中處理 `DUAL`、`NVL`、`TO_CHAR`、`TO_DATE`、`TRUNC` 與 `MINUS`。
- 需要用 `EXPLAIN`、索引與 query rewrite 來診斷 PostgreSQL 效能問題。
- 需要在 PostgreSQL 中做 `LAG` / `LEAD`、ranking、running total、moving average 或 `CROSSTAB` pivot。
- 需要在 PostgreSQL 中處理 `BEGIN/COMMIT/ROLLBACK`、`SAVEPOINT`、`EXCEPTION` 或 `GET STACKED DIAGNOSTICS`。
- 需要用 `STATISTICS TIME/IO`、execution plan 與 index 來診斷 SQL Server 效能問題。
- 需要直接在 SQL 裡整理營收、留存、ARPU、成長率等商業指標。
- 需要先釐清 OLTP / OLAP、schema、view 與 access control 的設計方向。
- 需要理解資料庫層的 trigger、audit 與 schema event 管理。
- 需要展開組織樹、分類樹、BOM、路徑搜尋等遞迴查詢。
- 想把分析邏輯前移，減少本地端記憶體負擔與重複匯出流程。

## 常見閱讀路線

1. 如果你是 SQL 初學者：從 `SQL Query Foundations -> SQL Joins and Set Operations -> SQL Reporting Patterns` 開始。
2. 如果你主要做資料分析：再接 `Business Analysis in SQL -> PostgreSQL Window Functions and Pivoting -> Recursive and Hierarchical SQL`。
3. 如果你常卡在 schema 設計與重複欄位：回頭補 `Database Design Principles -> Database Normalization`。
4. 如果你已經寫得出查詢，但慢或不穩：直接進 `PostgreSQL Query Performance` 或 `SQL Server Query Performance`。
