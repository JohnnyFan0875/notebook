# Python Database Access with SQLAlchemy Core

這篇整理 Python 連接 relational database 的實務起點，重點放在 SQLAlchemy Core。  
它適合資料科學工作裡常見的需求：連線、讀 schema、組 query、做 aggregate，以及必要時執行基本 CRUD。

## Why Use SQLAlchemy Core

SQLAlchemy 大致可以分成兩層：

- `Core`: 比較貼近 relational model，適合直接組 SQL-style query
- `ORM`: 比較貼近 application 的 object model

如果你的工作偏分析、資料處理或腳本化查詢，通常先掌握 Core 會更直接。

## Connection Model

最基本的兩個物件是：

- `engine`: SQLAlchemy 提供的資料庫介面入口
- `connection`: 真的拿來執行 query 的連線

```python
from sqlalchemy import create_engine

engine = create_engine("sqlite:///census_nyc.sqlite")
connection = engine.connect()
```

## Connection String

connection string 的角色，是告訴 SQLAlchemy：

- database dialect 是什麼
- driver 是什麼
- database 在哪裡
- 是否需要帳號密碼或其他連線資訊

SQLite 常見長這樣：

```python
engine = create_engine("sqlite:///census_nyc.sqlite")
```

對 SQLite 來說，如果檔案不存在，建立 engine 時通常也可能順便建立資料庫檔案。  
但像 PostgreSQL、MySQL 這類資料庫，database 初始化常常要用外部工具或管理指令先完成。

## Inspecting Existing Databases

在開始 query 前，先知道資料庫裡有什麼通常比急著寫查詢更重要。

### List Tables

```python
print(engine.table_names())
```

這一步的目的不是背 API，而是先確認：

- 有哪些 tables
- table naming 是否符合預期
- 你連到的是不是正確資料庫

### Reflection

reflection 會從既有 database schema 建立 SQLAlchemy `Table` object。

```python
from sqlalchemy import MetaData, Table

metadata = MetaData()
census = Table("census", metadata, autoload=True, autoload_with=engine)
```

這很適合：

- 你不是 schema 的建立者
- 已有資料庫存在
- 想先讀現況再查詢

## Building Tables

如果是自己建立表，可以直接宣告 `Table` 與 `Column`，再用 `metadata.create_all(engine)` 寫入資料庫。

```python
from sqlalchemy import Table, Column, String, Integer, Decimal, Boolean, MetaData

metadata = MetaData()

employees = Table(
    "employees",
    metadata,
    Column("id", Integer()),
    Column("name", String(255)),
    Column("salary", Decimal()),
    Column("active", Boolean()),
)

metadata.create_all(engine)
```

常見欄位選項包括：

- `unique`
- `nullable`
- `default`

注意：`create_all()` 適合初始化，不適合拿來處理成熟專案的 schema migration。  
當 table 結構開始演進時，通常要改用 migration tool，例如 Alembic。

## Query Construction Mental Model

可以把 SQLAlchemy Core 想成：

1. 先建立 statement
2. 再逐步加上 where / group_by / order_by / functions
3. 最後用 connection 執行

```python
stmt = select([census])
results = connection.execute(stmt).fetchall()
```

常見的結果提取方式：

- `fetchall()`: 抓全部列
- `scalar()`: 抓單一值，例如 `COUNT` 或 `SUM`

## Filtering Rows

### Simple `where()`

```python
stmt = select([census])
stmt = stmt.where(census.columns.state == "California")
results = connection.execute(stmt).fetchall()
```

`where()` 本質上就是把 Boolean 條件推進 database，而不是先把整張表拉回 Python 再過濾。

常見比較包括：

- `==`
- `!=`
- `>=`
- `<=`

### Expression Helpers

當條件不只是簡單比較時，可以用 column methods：

- `in_()`
- `like()`
- `between()`
- `startswith()`

```python
stmt = select([census])
stmt = stmt.where(census.columns.state.startswith("New"))
```

### Multiple Conditions

多條件時常見的是：

- `and_()`
- `or_()`
- `not_()`

重點不是語法本身，而是把條件邏輯保留在 query layer，而不是用 Python 迴圈事後補救。

## Aggregation and Grouping

分析工作裡，很多需求其實不是「拿列」，而是「拿 summary」。

### SQL Functions

SQLAlchemy 用 `func` 來呼叫常見 SQL aggregate functions。

```python
from sqlalchemy import func

stmt = select([func.sum(census.columns.pop2008)])
total_pop = connection.execute(stmt).scalar()
```

常見用途：

- `func.count(...)`
- `func.sum(...)`
- `func.avg(...)`
- `func.min(...)`
- `func.max(...)`

這通常比把原始資料全抓回 Python 再處理更有效率。

### `group_by()`

```python
stmt = select([
    census.columns.sex,
    func.sum(census.columns.pop2008),
])
stmt = stmt.group_by(census.columns.sex)
results = connection.execute(stmt).fetchall()
```

幾個重要心智模型：

- selected columns 如果不是 aggregate，通常就要出現在 `group_by()`
- `group_by()` 可以同時放多個欄位
- 這是在 database 端做 summary，不是在 Python 端手動 regroup

## Labels, Case, and Type Casting

當 query 開始像分析問題，而不只是簡單 select 時，這幾個工具很重要：

- `label()`: 幫計算欄位命名
- `case()`: 做 conditional logic
- `cast(..., Float)`: 控制型別，避免整數除法或不預期轉型

```python
from sqlalchemy import case, cast, Float
```

這些組件很適合做：

- 比例或百分比計算
- 條件式彙總
- weighted average
- 後續更好讀的輸出欄名

## CRUD Basics

雖然分析工作以讀取為主，但有時還是需要初始化資料或修正少量資料。

### Insert One Row

```python
from sqlalchemy import insert

stmt = insert(employees).values(id=1, name="Jason", salary=1.00, active=True)
result = connection.execute(stmt)
print(result.rowcount)
```

### Insert Multiple Rows

```python
stmt = insert(employees)
values_list = [
    {"id": 2, "name": "Rebecca", "salary": 2.00, "active": True},
    {"id": 3, "name": "Bob", "salary": 0.00, "active": False},
]
result = connection.execute(stmt, values_list)
```

如果來源是 CSV，常見流程就是：

1. 讀檔
2. 轉成 list of dicts
3. 一次送進 `execute()`

### Update

```python
from sqlalchemy import update

stmt = update(employees)
stmt = stmt.where(employees.columns.id == 3)
stmt = stmt.values(active=True)
result = connection.execute(stmt)
```

### Delete

```python
from sqlalchemy import delete

stmt = delete(employees).where(employees.columns.id == 3)
result = connection.execute(stmt)
```

刪除特別需要保守，因為它通常最難回復。

## Analytical Pattern: Ask the Database First

這門課最有價值的地方，不是 CRUD 本身，而是它提醒一件事：

- 先想能不能在 database 端把問題縮小
- 再決定哪些結果真的要進 Python

例如：

- 先 `where()` 篩選州別或日期
- 先 `group_by()` 算 summary
- 先用 `case()` 與 `cast()` 算比例
- 最後只把分析所需的結果集帶回 Python

這比無差別把整張表讀進記憶體更穩，也更像真實資料工作流。

## Practical Boundaries

- SQLAlchemy Core 很適合 analysis scripts、ETL steps、資料探索與中小型工具。
- 若你需要複雜 schema migration，交給 Alembic 比手動改 `create_all()` 安全。
- 若你主要是 tabular analytics，也可以視情況搭配 pandas `read_sql()`；但先理解底層 query model 仍然很有用。
- 若資料量很大，能在 database 做完的過濾、聚合與 join，通常不要後移到 Python。

## Minimal Workflow

```python
from sqlalchemy import create_engine, MetaData, Table, select, func

engine = create_engine("sqlite:///census_nyc.sqlite")
connection = engine.connect()

metadata = MetaData()
census = Table("census", metadata, autoload=True, autoload_with=engine)

stmt = select([
    census.columns.state,
    func.sum(census.columns.pop2008).label("population"),
])
stmt = stmt.group_by(census.columns.state)

results = connection.execute(stmt).fetchall()
```

如果你能自然讀懂這段，通常就已經具備把 Python 接上 relational database 做基本分析的核心能力了。
