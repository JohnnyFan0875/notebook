[Data Science](../README.md) › [Databases](README.md) › Python 與 SQLAlchemy

# Python 與 SQLAlchemy

SQLAlchemy 是 Python 連接關聯式資料庫的標準介面：同一套程式碼可以接 SQLite、PostgreSQL、MySQL、SQL Server，pandas 的 `read_sql` / `to_sql` 也建立在它上面。分析工作主要用兩種方式：直接寫 SQL 字串（`text()`）或用 Core 的 Python 運算式組查詢。本篇以 SQLAlchemy 2.x 為準。

| 層 | 用途 | 本篇 |
| --- | --- | --- |
| Engine / Connection | 連線池、執行 SQL、交易 | 是 |
| Core | 用 Python 物件組 SQL（`select`、`insert`），不同資料庫自動轉成對應方言 | 是 |
| ORM | 把資料表對應到 Python class，適合應用程式開發 | 否 |

## 連線

```python
from sqlalchemy import create_engine

engine = create_engine("sqlite:///census.sqlite")                       # 檔案不存在會自動建立
engine = create_engine("sqlite://")                                      # 記憶體資料庫，測試用
engine = create_engine("postgresql+psycopg://user:pw@localhost:5432/db") # 需要 pip install psycopg
engine = create_engine("mysql+pymysql://user:pw@host/db")
engine = create_engine("duckdb:///analysis.duckdb")                      # 需要 duckdb-engine
```

URL 格式：`dialect+driver://user:password@host:port/database`。

| 原則 | 做法 |
| --- | --- |
| 密碼不寫進程式碼與 notebook | 從環境變數讀：`os.environ["DB_URL"]`；或 `sqlalchemy.URL.create(...)` 組合 |
| 密碼含 `@`、`/` 等特殊字元 | 用 `URL.create(drivername=..., password=...)`，不必手動跳脫 |
| engine 只建立一次 | 它管理連線池，整個程式共用 |
| 連線用完就還 | 一律寫在 `with` 區塊內 |

## 查看資料庫

```python
from sqlalchemy import inspect, MetaData, Table

insp = inspect(engine)
insp.get_table_names()                  # ['census', 'employees']（舊版 engine.table_names() 已移除）
insp.get_columns("census")              # 欄位名稱、型別、nullable
insp.get_schema_names()                 # PostgreSQL 的 schema

# reflection：從既有資料表建立 Table 物件，供 Core 查詢使用
metadata = MetaData()
census = Table("census", metadata, autoload_with=engine)    # 舊版的 autoload=True 已移除
[c.name for c in census.columns]        # ['state', 'sex', 'age', 'pop2000', 'pop2008']
```

## 執行 SQL：`text()` 與參數

```python
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(
        text("SELECT state, SUM(pop2008) AS pop FROM census WHERE age > :min_age GROUP BY state"),
        {"min_age": 65},                                     # 參數化：值由 driver 安全地帶入
    )
    rows = result.all()                                      # list of Row（像 tuple，也可用 row.state）
    # result.mappings().all()  → list of dict-like
    # result.scalar()          → 第一列第一欄（COUNT、SUM）
    # for row in result: ...   → 逐列讀，不必全部載入
```

> **永遠用參數，不要用 f-string 拼 SQL。** `f"WHERE name = '{name}'"` 遇到 `O'Brien` 會語法錯誤，遇到惡意輸入就是 SQL injection。參數化查詢也讓資料庫可以重用執行計畫。表名、欄名不能當參數，只能從白名單中選。

## Core：用 Python 組查詢

```python
from sqlalchemy import select, func, case, cast, Float, and_, or_

c = census.c                                                 # census.columns 的簡寫

stmt = (
    select(c.state, func.sum(c.pop2008).label("population"))   # 2.x：select(欄位, ...)，不再傳 list
    .where(or_(c.state.startswith("New"), c.state == "California"))
    .group_by(c.state)
    .order_by(func.sum(c.pop2008).desc())
)
print(stmt)                                                  # 檢查產生的 SQL

with engine.connect() as conn:
    conn.execute(stmt).all()                                 # [('California', 250), ('New York', 95)]
    conn.execute(select(func.sum(c.pop2008))).scalar()       # 345

# 條件式聚合與比例：女性人口百分比
pct_female = select(
    (func.sum(case((c.sex == "F", c.pop2008), else_=0)) * 100.0
     / func.sum(c.pop2008)).label("pct_female")              # 乘 100.0 避免整數除法
)
```

| SQL | Core |
| --- | --- |
| `WHERE a = 1 AND b > 2` | `.where(c.a == 1, c.b > 2)` 或 `and_(...)` |
| `OR` / `NOT` | `or_(...)` / `~cond` 或 `not_(...)` |
| `IN` / `BETWEEN` / `LIKE` | `c.x.in_([...])` / `c.x.between(a, b)` / `c.x.like("A%")`、`.ilike()` |
| `IS NULL` | `c.x.is_(None)` / `c.x.is_not(None)` |
| `AS` | `.label("name")` |
| `CASE` | `case((cond, value), else_=...)` |
| `CAST` | `cast(c.x, Float)` |
| `JOIN` | `select(...).join(other, c.id == other.c.id)`、`isouter=True` 為 LEFT JOIN |
| 聚合 | `func.count()`、`func.sum()`、`func.avg()`；`func.xxx` 會直接變成 SQL 的 `xxx()` |

## 交易與寫入

2.x 的 `engine.connect()` 不會自動提交：寫入後沒有 `commit()`，離開 `with` 時變更會被回滾。

```python
from sqlalchemy import insert, update, delete

# 寫法 1：engine.begin()，正常結束自動 COMMIT、發生例外自動 ROLLBACK（建議）
with engine.begin() as conn:
    conn.execute(insert(employees), [                         # 傳 list of dict = 批次插入 (executemany)
        {"id": 1, "name": "Jason", "salary": 1.00},
        {"id": 2, "name": "Rebecca", "salary": 2.00},
    ])
    conn.execute(update(employees).where(employees.c.id == 2).values(active=False))
    conn.execute(delete(employees).where(employees.c.id == 3))

# 寫法 2：connect() + 手動 commit
with engine.connect() as conn:
    result = conn.execute(text("UPDATE employees SET active = true WHERE id = :id"), {"id": 2})
    result.rowcount                                          # 受影響列數
    conn.commit()
```

交易的概念見 [交易與錯誤處理](sql-transactions.md)。

### 建表

```python
from sqlalchemy import Table, Column, Integer, String, Numeric, Boolean, MetaData

metadata = MetaData()
employees = Table(
    "employees", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(255), nullable=False),
    Column("salary", Numeric(10, 2)),                        # 精確小數；SQLAlchemy 沒有 Decimal 型別
    Column("active", Boolean, default=True),
)
metadata.create_all(engine)                                   # 只建立不存在的表；不會修改既有的表
```

`create_all()` 適合初始化；表結構需要演進時用 migration 工具（Alembic）。

## pandas 讀寫

```python
import pandas as pd

# 讀：SQL 字串要用 text() 包起來才能帶參數
df = pd.read_sql(text("SELECT * FROM census WHERE age > :a"), engine, params={"a": 35})
df = pd.read_sql(stmt, engine)                                # 也可以直接給 Core 查詢
df = pd.read_sql_table("census", engine)                      # 整張表

# 大結果：分批讀，每批是一個 DataFrame
for chunk in pd.read_sql(text("SELECT * FROM big_table"), engine, chunksize=100_000):
    process(chunk)

# 寫
df.to_sql("census_copy", engine, if_exists="replace", index=False,
          chunksize=10_000, method="multi")                   # multi：一個 INSERT 帶多列，較快
```

| `if_exists` | 行為 |
| --- | --- |
| `"fail"`（預設） | 表已存在就報錯 |
| `"replace"` | 刪表重建：原有的型別、index、constraint、權限都會消失 |
| `"append"` | 附加到既有的表 |

> `to_sql` 依 DataFrame 推斷型別建表，常不理想（文字變 `TEXT`、ID 變 `BIGINT`）。正式資料表先用 SQL 建好結構，再 `if_exists="append"`。大量匯入 PostgreSQL 時，`COPY` 比 `INSERT` 快一到兩個數量級（見 [PostgreSQL：psql 與 COPY](postgresql-psql-and-copy.md#csv-匯入匯出)）。

## 先在資料庫端縮小

| 做法 | 不要 |
| --- | --- |
| `WHERE` 在 SQL 裡過濾 | `pd.read_sql("SELECT * FROM t")` 再在 pandas 篩選 |
| `GROUP BY` 在 SQL 裡聚合，只取摘要 | 拉回全部明細再 `groupby` |
| 只選需要的欄位 | `SELECT *` |
| 大結果用 `chunksize` 或串流 | 一次載入超過記憶體的結果 |

資料是本機的 CSV / Parquet 而不是資料庫時，DuckDB 可以直接用 SQL 查檔案，不必先匯入（見 [DuckDB 與 Parquet](duckdb-and-parquet.md)）。R 的對應工具是 `DBI` + `dbplyr`（見 [匯入資料（R）](../r-foundations/importing-data.md#資料庫dbi)）。

## 舊版 (1.x) → 2.x

| 1.x 寫法 | 2.x |
| --- | --- |
| `select([census])`、`select([c.a, c.b])` | `select(census)`、`select(c.a, c.b)` |
| `Table(..., autoload=True, autoload_with=engine)` | `Table(..., autoload_with=engine)` |
| `engine.table_names()` | `inspect(engine).get_table_names()` |
| `engine.execute(...)` | `with engine.connect() as conn: conn.execute(...)` |
| 寫入自動提交 (autocommit) | `engine.begin()` 或 `conn.commit()` |
| `conn.execute("SELECT ...")`（純字串） | `conn.execute(text("SELECT ..."))` |
| `result.fetchall()` | `result.all()`（`fetchall()` 仍可用） |
