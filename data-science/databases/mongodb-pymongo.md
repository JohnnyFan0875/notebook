[Data Science](../README.md) › [Databases](README.md) › MongoDB 與 PyMongo

# MongoDB 與 PyMongo

MongoDB 是 document database：資料是可巢狀的 JSON-like 文件，查詢條件本身也是 Python `dict`。適合結構會變、以整份文件讀寫的資料（樣本 metadata、API 回應、事件紀錄）；高度關聯、需要大量 join 的資料仍以關聯式資料庫較自然（見 [NoSQL 基礎](nosql-foundations.md)）。

| MongoDB | 關聯式 | Python |
| --- | --- | --- |
| database | database | `client["nobel"]` |
| collection | table | `db["laureates"]` |
| document | row（可巢狀） | `dict` |
| field | column | key |
| embedded document / array | 另一張表 + 外鍵 | 巢狀 `dict` / `list` |
| `_id` | primary key | 自動產生的 `ObjectId` |

## 連線與新增

```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")       # 帳密放環境變數：MongoClient(os.environ["MONGO_URI"])
db = client["nobel"]
prizes = db["prizes"]                                   # 也可寫 db.prizes

prizes.insert_one({"category": "physics", "year": "1901"})
prizes.insert_many([
    {"category": "chemistry", "year": "1901"},
    {"category": "medicine", "year": "1901", "laureates": [{"id": "293", "share": "1"}]},
])

prizes.count_documents({})                              # 全部文件數
prizes.find_one({})                                     # 任一份文件，看資料長什麼樣
db.list_collection_names()
client.close()
```

## 查詢

```python
lau = db.laureates

# 1. 條件就是 dict；多個 key = AND
lau.find_one({"gender": "female", "bornCountry": "France"})

# 2. 巢狀欄位用 dot notation（要加引號）
lau.find({"prizes.category": "physics"})

# 3. 陣列欄位直接比值 = 「陣列中包含此值」
db.people.find({"nicknames": "JB"})

# 4. 陣列長度：第 n 個元素是否存在（0 起算）
lau.find({"prizes.1": {"$exists": True}})               # 得過 2 次以上

# 5. 運算子
lau.find({"born": {"$gte": "1900", "$lt": "2000"}})     # 注意：此資料集年份存成字串，比較的是字典序
lau.find({"bornCountry": {"$in": ["France", "Germany"]}})
lau.find({"gender": {"$ne": "org"}})
lau.find({"$or": [{"bornCountry": "USA"}, {"diedCountry": "USA"}]})
lau.find({"firstname": {"$regex": "^Mar"}})
lau.find({"prizes": {"$elemMatch": {"category": "physics", "share": "1"}}})   # 同一個陣列元素同時滿足

lau.distinct("prizes.category")                         # 某欄出現過的值
```

| 運算子 | SQL 對應 |
| --- | --- |
| `$eq`、`$ne`、`$gt`、`$gte`、`$lt`、`$lte` | `=`、`<>`、`>`、`>=`、`<`、`<=` |
| `$in`、`$nin` | `IN`、`NOT IN` |
| `$and`、`$or`、`$not` | `AND`、`OR`、`NOT` |
| `$exists` | `IS NOT NULL`（欄位是否存在） |
| `$regex` | `LIKE` / 正規表示式 |
| `$elemMatch` | 陣列中**同一個元素**滿足多個條件 |

> `{"prizes.category": "physics", "prizes.share": "1"}` 是「某個獎是 physics、某個獎（可能是另一個）share 為 1」；要求同一個獎同時滿足兩條件時要用 `$elemMatch`。

### Projection、排序、分頁

```python
cursor = (
    lau.find({"bornCountry": "USA"}, {"firstname": 1, "surname": 1, "_id": 0})   # 1 包含、0 排除；_id 預設會回傳
       .sort([("surname", 1), ("firstname", 1)])        # 1 升冪、-1 降冪
       .skip(20)
       .limit(10)
)
docs = list(cursor)                                     # find() 回傳 cursor，迭代時才真的取資料

lau.find({}, ["bornCountry", "firstname"])              # projection 也可給欄位 list
```

## Index

```python
db.prizes.create_index([("year", 1)])
db.prizes.create_index([("category", 1), ("year", -1)])   # compound：符合常用的 filter + sort
db.prizes.index_information()

lau.find({"firstname": "Marie"}, {"bornCountry": 1, "_id": 0}).explain()   # 看是否用到 index（IXSCAN vs COLLSCAN）
```

`_id` 一定有 index。先找出最常用的 filter / sort 模式再建 index；每個 index 都會增加寫入成本與儲存空間。

## Aggregation pipeline

`aggregate()` 把資料依序送過多個 stage，類似 SQL 子句或 pandas 方法鏈。

```python
pipeline = [
    {"$match": {"category": "economics"}},              # WHERE
    {"$unwind": "$laureates"},                          # 陣列展開：每個得獎者一份文件
    {"$lookup": {                                       # LEFT JOIN 另一個 collection
        "from": "laureates",
        "localField": "laureates.id",
        "foreignField": "id",
        "as": "bio",
    }},
    {"$unwind": "$bio"},
    {"$group": {                                        # GROUP BY bornCountry
        "_id": "$bio.bornCountry",
        "n": {"$sum": 1},                               # COUNT(*)
        "first_year": {"$min": "$year"},
    }},
    {"$sort": {"n": -1}},                               # ORDER BY
    {"$limit": 5},
]
list(db.prizes.aggregate(pipeline))
```

| Stage | SQL / pandas 對應 |
| --- | --- |
| `$match` | `WHERE` / 布林篩選 |
| `$project` / `$addFields` | `SELECT` 計算欄位 / `assign` |
| `$group` | `GROUP BY` + 聚合；`_id` 是分組鍵，`None` = 全部一組 |
| `$unwind` | 展開陣列 / `explode` |
| `$lookup` | `LEFT JOIN` / `merge` |
| `$sort`、`$skip`、`$limit` | `ORDER BY`、`OFFSET`、`LIMIT` |
| `$count` | `COUNT(*)` |

```python
# $project 建立計算欄位：欄位引用要加 $，運算子是 aggregation expression
db.laureates.aggregate([
    {"$project": {
        "_id": 0,
        "n_prizes": {"$size": "$prizes"},                       # 陣列長度
        "solo_winner": {"$in": ["1", "$prizes.share"]},         # 是否有單獨得獎
        "born": {"$dateFromString": {"dateString": "$born", "onError": None}},   # 字串轉日期，失敗給 null
    }},
])
```

> `$match` 盡量放在 pipeline 最前面：可以用到 index，也讓後面的 stage 處理更少文件。若工作流嚴重依賴 `$lookup`，代表資料模型可能更適合關聯式資料庫。

## 轉進 pandas

```python
import pandas as pd

docs = list(lau.find({}, {"_id": 0, "firstname": 1, "bornCountry": 1, "prizes": 1}))
df = pd.json_normalize(docs)                                     # 巢狀 dict 攤平成 prizes.xxx 欄位
df_prizes = pd.json_normalize(docs, record_path="prizes",        # 陣列展開成多列
                              meta=["firstname", "bornCountry"])
```

| 層次 | 工具 |
| --- | --- |
| 存放巢狀、結構會變的原始資料 | MongoDB |
| 在資料庫端篩選、投影、聚合 | `find` + projection、`aggregate` |
| 攤平成表格做分析 | `pd.json_normalize` → pandas |
