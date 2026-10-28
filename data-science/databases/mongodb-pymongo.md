# Python: MongoDB with PyMongo

MongoDB 的核心差異不只是「不用 SQL」，而是資料模型從 table / row 變成 collection / document。實作上最重要的是先建立文件模型的直覺，再把查詢、投影、排序、索引與 aggregation pipeline 串成一條工作流。

## Mental Model

- database 對應一組 collections
- collection 類似關聯式資料庫中的 table
- document 是 BSON/JSON-like 結構，類似一筆可巢狀的 row
- field 可以是純量、陣列、或子文件

MongoDB 很適合處理下列情境：

- 單筆資料天然就是巢狀結構
- 欄位不一定完全固定
- 讀取時常常以整份文件為單位

如果你的資料高度正規化、跨表關聯很多、交易一致性要求很高，關聯式資料庫通常會比較自然。

## JSON, Python, and MongoDB

PyMongo 操作 MongoDB 時，最常用的資料結構就是 Python `dict`、`list`、`str`、`int`。

```python
from pymongo import MongoClient

client = MongoClient()
db = client["nobel"]
laureates = db["laureates"]
prizes = db["prizes"]
```

常見對應關係：

- MongoDB document -> Python `dict`
- array field -> Python `list`
- embedded document -> 巢狀 `dict`

這也是 MongoDB 上手快的原因之一：查詢條件本身就是 Python dictionary。

## Insert and Basic Access

```python
documents = [
    {"category": "physics", "year": "1901"},
    {"category": "chemistry", "year": "1901"},
]

prizes.insert_many(documents)
print(prizes.count_documents({}))
print(prizes.find_one({}))
```

幾個很常用的起手式：

- `insert_one()` / `insert_many()`
- `find_one()`
- `find()`
- `count_documents({})`

`find()` 回傳的是 cursor，不是立刻展開完成的 list。

## Filtering Documents

MongoDB 查詢條件本身也是 document。

```python
db.laureates.find_one({"gender": "female"})
db.laureates.find_one({"bornCountry": "France"})
```

這種寫法最適合先從「欄位要符合什麼值」開始思考，而不是先想 SQL 語法。

### Nested Fields

巢狀欄位用 dot notation。

```python
db.laureates.find({"prizes.category": "physics"})
db.laureates.find({"prizes.share": "4"})
```

這是 MongoDB 很強的地方之一：不需要先把子結構拆表，就能直接查 nested fields。

### Existence Checks

```python
db.laureates.find({"prizes.0": {"$exists": True}})
db.laureates.find({"prizes.1": {"$exists": True}})
db.laureates.find({"prizes.2": {"$exists": True}})
```

實務上這類寫法很常用來判斷：

- 陣列是否非空
- 是否至少有第 `n` 個元素
- 某欄位是否存在

```python
db.laureates.find({"died": {"$exists": True}})
```

### Arrays Match by Contained Value

如果欄位本身是 array，直接比對值時，意思通常是「陣列中是否包含該值」。

```python
db.people.find({"nicknames": "JB"})
```

這不是要求整個陣列等於 `"JB"`，而是判斷 `"JB"` 是否是其中一個元素。

### Not Equal

```python
db.laureates.find({"gender": {"$ne": "org"}})
```

`$ne` 常用來排除特定值，但如果你需要複雜條件，通常會再搭配其他運算子一起用。

## Distinct Values

```python
db.laureates.distinct("gender")
db.laureates.distinct("prizes.category")
```

`distinct()` 可以把某欄位出現過的值去重後取回。它可以把它想成常見 aggregation 的快捷寫法。

實務上的重點：

- 拿來快速探索資料類別非常方便
- 如果欄位上有 index，通常會更有效率

## Projection

projection 的目的不是篩選列，而是縮小每筆 document 要回傳哪些欄位。

```python
docs = db.laureates.find(
    filter={},
    projection={"prizes.affiliations": 1, "_id": 0},
)
```

重點規則：

- `1` 代表包含欄位
- `0` 代表排除欄位
- `_id` 預設會被回傳

也可以用欄位名稱 list 做簡化寫法：

```python
docs = db.laureates.find({}, ["bornCountry", "firstname"])
```

projection 的實務價值很高：

- 減少網路傳輸
- 減少 client 端記憶體使用
- 讓查詢結果更聚焦

## Sorting, Skipping, and Limiting

```python
cursor = db.prizes.find(
    {"category": "physics"},
    ["year"],
    sort=[("year", 1)],
)
```

排序方向：

- `1` 代表升冪
- `-1` 代表降冪

多欄位排序：

```python
db.prizes.find(
    {},
    sort=[("year", 1), ("category", -1)],
)
```

cursor methods 通常更好讀：

```python
cursor = (
    db.prizes.find({"laureates.share": "3"})
    .sort("year", 1)
    .skip(3)
    .limit(3)
)
```

可以把它想成一條查詢管線：

1. 先找出符合條件的文件
2. 再排序
3. 跳過前幾筆
4. 最後只取一小段

## Indexes

索引的核心目標是讓常見查詢與排序不必每次都掃過整個 collection。

```python
db.prizes.create_index([("year", 1)])
db.prizes.create_index([("category", 1), ("year", 1)])
```

幾個實務重點：

- MongoDB 一定會有 `_id` index
- 單欄位 index 適合簡單 filter 或 sort
- compound index 適合固定查詢模式
- projection、filter、sort 如果一起對齊某個 compound index，查詢常會更漂亮

### When to Add an Index

比較合理的順序是：

1. 先確認慢在哪裡
2. 找出最常出現的 filter / sort pattern
3. 再建立對應 index

不要為了「可能以後會用到」就先把很多索引加滿，因為索引本身也有寫入與儲存成本。

### Inspecting Query Plans

```python
db.laureates.find(
    {"firstname": "Marie"},
    {"bornCountry": 1, "_id": 0},
).explain()
```

`explain()` 可以幫你確認查詢是否真的走到你預期的 index，而不是只靠感覺優化。

## Aggregation Pipeline

如果 `find()` 是簡單查詢，那 `aggregate()` 就是把查詢拆成多個 stage 的資料處理流程。

```python
cursor = db.laureates.aggregate([
    {"$match": {"bornCountry": "USA"}},
    {"$project": {"prizes.year": 1, "_id": 0}},
    {"$limit": 3},
])
```

一個很重要的觀念是：很多 `find()` 的操作，都能改寫成 aggregation stages。

### Common Stages

- `$match`: 篩選文件
- `$project`: 選欄位或建立新欄位
- `$sort`: 排序
- `$skip`: 跳過前幾筆
- `$limit`: 限制筆數
- `$group`: 彙總
- `$unwind`: 把 array 拆成多筆文件
- `$lookup`: 跨 collection 類似 join

## `$project` as Transformation

aggregation 裡的 `$project` 不只是保留欄位，也能建立計算欄位。

```python
db.laureates.aggregate([
    {"$project": {"n_prizes": {"$size": "$prizes"}}}
])
```

這裡的 `$size` 是 aggregation expression，不是 Python 函式。

另一個常見例子：

```python
db.laureates.aggregate([
    {"$project": {"solo_winner": {"$in": ["1", "$prizes.share"]}}}
])
```

這類寫法的重點是學會區分：

- 普通欄位值
- 以 `"$field_name"` 形式引用欄位
- expression operator，例如 `$size`、`$in`

## `$group`

`$group` 用來把多筆文件收斂成較少的群組結果。

```python
db.laureates.aggregate([
    {"$group": {"_id": "$bornCountry"}}
])
```

在 `$group` 中：

- `_id` 是分組鍵
- 其他欄位通常搭配 accumulator，例如 `$sum`

```python
db.laureates.aggregate([
    {"$project": {"n_prizes": {"$size": "$prizes"}}},
    {"$group": {"_id": None, "n_prizes_total": {"$sum": "$n_prizes"}}},
])
```

把 `_id` 設成 `None`，常表示「把全部文件當成一組」。

## `$unwind`

`$unwind` 會把一個 array 欄位展開成多筆文件，這在統計 array 內元素時非常重要。

```python
db.prizes.aggregate([
    {"$unwind": "$laureates"},
    {"$project": {"year": 1, "category": 1, "laureates.id": 1}},
    {"$limit": 3},
])
```

你可以把它想成：

- 原本一筆文件內有一個陣列
- `$unwind` 後，陣列中的每個元素都變成獨立資料列

這讓後續的 `$group`、`$sort`、`$match` 都更自然。

## `$lookup`

MongoDB 雖然是文件資料庫，但還是可以在 aggregation 中做類似 join 的操作。

```python
db.prizes.aggregate([
    {"$match": {"category": "economics"}},
    {"$unwind": "$laureates"},
    {"$lookup": {
        "from": "laureates",
        "localField": "laureates.id",
        "foreignField": "id",
        "as": "laureate_bios",
    }},
])
```

`$lookup` 很有用，但如果你的工作流嚴重依賴多表 join，通常也代表你該重新思考資料模型是否真的適合放在 MongoDB。

## Date Conversion in Pipelines

如果日期是字串，可以在 pipeline 內轉型後再計算。

```python
db.laureates.aggregate([
    {
        "$project": {
            "born": {"$dateFromString": {"dateString": "$born"}},
            "died": {"$dateFromString": {"dateString": "$died"}},
        }
    }
])
```

這個技巧常用在：

- 計算年齡或期間
- 對日期做比較
- 後續再搭配數學運算

## Practical Workflow

實務上可以用下面這個順序工作：

1. 先用 `find_one()` 與 `distinct()` 了解資料形狀。
2. 再寫基本 `find()` filter。
3. 加上 projection，只取需要的欄位。
4. 如果要分頁或取樣，再加 `sort()`、`skip()`、`limit()`。
5. 觀察慢查詢，必要時補 index。
6. 當需求變成多階段整理或彙總時，改寫成 `aggregate()`.

這套流程比一開始就直接寫很長的 pipeline 更容易除錯。

## MongoDB vs pandas vs SQL

- MongoDB 擅長儲存與查詢巢狀文件
- pandas 擅長在記憶體中做分析轉換
- SQL 擅長結構明確、關聯清楚、可宣告式查詢的資料

實務上很常見的組合是：

1. 用 MongoDB 存應用資料或原始半結構化資料
2. 用 PyMongo 抽取需要的欄位
3. 再進 pandas 做分析

所以重點不是三者互相取代，而是各自負責不同層次的工作。
