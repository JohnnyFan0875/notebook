[Data Science](../README.md) › Databases

# 資料庫與 SQL (Databases)

SQL 是資料分析的共同語言：資料太大不適合整批拉進 pandas / R 時，在資料庫端先過濾、join、聚合，只把結果帶回來。本章以跨資料庫通用的 SQL 為主，方言差異集中在速查表；本機分析大型 CSV / Parquet 用 DuckDB 就不必架伺服器。

## 建議順序

```
查詢基礎 → JOIN 與集合 → 報表模式 → Window functions → 遞迴查詢
                                  ↓
          資料庫設計 → 正規化            Python 存取 / DuckDB
                                  ↓
                   交易 → 效能 → 方言速查
```

## 筆記

### SQL 查詢

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [SQL 查詢基礎](sql-query-foundations.md) | 執行順序、`WHERE` / `GROUP BY` / `HAVING`、`COUNT` 三種、`NULL` 三值邏輯 | 為什麼 alias 不能放 `WHERE`？`COUNT(*)` 和 `COUNT(col)` 差在哪？ |
| [JOIN 與集合運算](sql-joins-and-set-operations.md) | 各種 JOIN、列數膨脹、`UNION` / `INTERSECT` / `EXCEPT`、semi / anti join | join 後列數為什麼變多？怎麼找沒有對到的資料？ |
| [報表查詢模式](sql-reporting-patterns.md) | `CASE`、`CAST`、比例、成長率、rolling、`ROLLUP` / `CUBE` / `GROUPING SETS` | 怎麼算佔比與小計而不出錯？ |
| [Window Functions](sql-window-functions.md) | 排名、`LAG` / `LEAD`、running total、frame、每組 top-N、PostgreSQL `crosstab` | 怎麼在保留明細的同時加上群組統計？ |
| [遞迴與階層查詢](recursive-and-hierarchical-sql.md) | recursive CTE、樹狀展開、路徑、多跳圖、BOM、cycle 保護 | 怎麼展開 parent–child 結構（如 GO / 分類樹）？ |

### 設計與系統

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [資料庫設計原則](database-design-principles.md) | OLTP vs OLAP、schema、key、外鍵、view、權限 | 資料表為什麼長這樣？ |
| [正規化](database-normalization.md) | 函數相依、1NF–3NF、異常、反正規化取捨 | 什麼時候該拆表？ |
| [NoSQL 基礎](nosql-foundations.md) | document / key-value / graph / wide-column、row vs column store、JSONB | 什麼時候不用關聯式資料庫？ |

### 交易、效能與方言

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [交易與錯誤處理](sql-transactions.md) | ACID、savepoint、隔離層級與異常；PL/pgSQL `EXCEPTION` vs T-SQL `TRY...CATCH` | 多個更新怎麼確保全部成功或全部撤銷？ |
| [查詢效能](sql-query-performance.md) | 診斷流程、`EXPLAIN ANALYZE`、index 設計與失效、SQL Server `STATISTICS IO` | 查詢為什麼慢？index 該建在哪？ |
| [SQL 方言速查](sql-dialect-cheatsheet.md) | PostgreSQL / SQL Server / MySQL / Oracle / Snowflake / DuckDB 對照；T-SQL 細節 | 換平台時這個語法怎麼寫？ |
| [PostgreSQL：psql 與 COPY](postgresql-psql-and-copy.md) | psql、`\copy`、DDL、型別、upsert、dump / restore、權限 | 怎麼建表、匯入匯出、管理使用者？ |

### 從程式存取

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [Python 與 SQLAlchemy](python-sqlalchemy.md) | SQLAlchemy 2.x engine / connection、參數化查詢、Core 查詢、`pd.read_sql` / `to_sql` | Python 怎麼安全地連資料庫？ |
| [DuckDB 與 Parquet](duckdb-and-parquet.md) | 不用伺服器直接以 SQL 查 CSV / Parquet / DataFrame、區間 join、Python 與 R | 大檔案怎麼在筆電上用 SQL 分析？ |
| [MongoDB 與 PyMongo](mongodb-pymongo.md) | document CRUD、查詢運算子、projection、index、aggregation pipeline | 巢狀文件資料怎麼查？ |

## 何時把工作交給資料庫

| 情境 | 做法 |
| --- | --- |
| 原始資料大於記憶體 | 在資料庫或 DuckDB 端先 `WHERE`、`GROUP BY`，只取結果 |
| 多張表要對齊（樣本 × 臨床資料 × 檢驗結果） | SQL join；先確認 join key 唯一，見 [JOIN 列數膨脹](sql-joins-and-set-operations.md#列數膨脹-fan-out) |
| 要給多人共用、會持續寫入 | PostgreSQL 等伺服器型資料庫，搭配交易與權限 |
| 一個人分析、檔案為主 | DuckDB（分析）或 SQLite（小型應用 / 工具內建） |

R 端用 `DBI` + `dbplyr` 存取資料庫，見 [匯入資料（R）](../r-foundations/importing-data.md#資料庫dbi)；pandas / dplyr / SQL 語法對照見 [SQL 查詢基礎](sql-query-foundations.md#sql--pandas--dplyr-對照)。資料倉儲與星狀模型見 [Data Engineering](../data-engineering/dimensional-modeling-and-star-schema.md)。
