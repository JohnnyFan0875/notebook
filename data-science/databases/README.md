# Databases

這個章節整理資料分析常見的關聯式資料庫筆記。對資料科學工作來說，SQL 不只是查資料，更是前置清理、聚合、抽樣與建立分析資料表的重要工具。

## 建議閱讀順序

1. 先讀 [SQL Query Foundations](sql-query-foundations.md)、[SQL Joins and Set Operations](sql-joins-and-set-operations.md)、[SQL Reporting Patterns](sql-reporting-patterns.md)，把最常用的查詢與報表邏輯補穩。
2. 再讀 [Database Design Principles](database-design-principles.md) 與 [Database Normalization](database-normalization.md)，理解資料表為什麼會長成那樣。
3. 之後依實際平台查 [SQL Dialect Cheatsheet](sql-dialect-cheatsheet.md)，或補 NoSQL。

## 主題分組

### SQL 基礎與分析查詢

| 筆記 | 內容 |
| --- | --- |
| [SQL Query Foundations](sql-query-foundations.md) | 執行順序、`WHERE`、`COUNT`、`NULL`、aggregate、`GROUP BY` / `HAVING` |
| [SQL Joins and Set Operations](sql-joins-and-set-operations.md) | 各種 JOIN、`UNION` / `INTERSECT`、semi / anti join |
| [SQL Reporting Patterns](sql-reporting-patterns.md) | `CASE`、`CAST`、比例、`ROLLUP` / `CUBE` / `GROUPING SETS`、`EXISTS` |
| [SQL Window Functions](sql-window-functions.md) | ranking、`LAG` / `LEAD`、running total、frame、PostgreSQL `CROSSTAB` |
| [Recursive and Hierarchical SQL](recursive-and-hierarchical-sql.md) | recursive CTE、組織樹、BOM、路徑搜尋 |

### 交易、效能與方言

| 筆記 | 內容 |
| --- | --- |
| [SQL Transactions](sql-transactions.md) | `BEGIN` / `COMMIT` / `ROLLBACK`、savepoint、隔離層級；PL/pgSQL `EXCEPTION` vs T-SQL `TRY...CATCH` 對照 |
| [SQL Query Performance](sql-query-performance.md) | 診斷流程、index；PostgreSQL `EXPLAIN` 與 SQL Server `STATISTICS TIME/IO`、execution plan |
| [SQL Dialect Cheatsheet](sql-dialect-cheatsheet.md) | PostgreSQL / SQL Server / MySQL / Oracle / Snowflake 對照（`TOP` / `LIMIT`、`NVL` / `ISNULL`、日期函式、`FLATTEN`）與 T-SQL 細節 |
| [PostgreSQL: psql and COPY](postgresql-psql-and-copy.md) | psql、`\copy`、DDL、dump / restore、roles、schemas |

### 資料模型與系統觀念

| 筆記 | 內容 |
| --- | --- |
| [Database Design Principles](database-design-principles.md) | OLTP / OLAP、schema、view、access control |
| [Database Normalization](database-normalization.md) | 1NF–3NF |
| [NoSQL Foundations](nosql-foundations.md) | document、key-value、graph、column store |

### 從 Python 存取

| 筆記 | 內容 |
| --- | --- |
| [Python Database Access with SQLAlchemy](python-sqlalchemy.md) | engine、reflection、query |
| [MongoDB with PyMongo](mongodb-pymongo.md) | document CRUD、aggregation pipeline |

## 建議使用時機

- 原始資料量太大，不適合先全部拉進 pandas：在資料庫端先做 join、group by、window function 或條件過濾。
- 要把原始資料整理成報表欄位：`CASE`、`CAST()`、比例欄位、`ROLLUP` 小計。
- 寫得出查詢但慢或不穩：先看 [SQL Query Performance](sql-query-performance.md)。
- 換平台時語法不對：查 [SQL Dialect Cheatsheet](sql-dialect-cheatsheet.md)。

## 常見閱讀路線

1. 如果你是 SQL 初學者：從 `SQL Query Foundations -> SQL Joins and Set Operations -> SQL Reporting Patterns` 開始。
2. 如果你主要做資料分析：再接 `SQL Window Functions -> Recursive and Hierarchical SQL`。
3. 如果你常卡在 schema 設計與重複欄位：回頭補 `Database Design Principles -> Database Normalization`。
4. 如果你已經寫得出查詢，但慢或不穩：直接進 `SQL Query Performance` 與 `SQL Transactions`。
