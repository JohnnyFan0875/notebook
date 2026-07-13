# NoSQL Foundations

這篇整理 NoSQL 的基礎心智模型。重點不是把各家產品背熟，而是先分清楚：NoSQL 解的是什麼問題、常見資料形狀有哪些、以及它和 relational database 各自擅長的工作。

## What NoSQL Usually Means

NoSQL 通常可理解成 `not only SQL`。  
它不是單一產品，也不是「比 SQL 更新的資料庫」，而是一組偏向非關聯式、較彈性資料模型的 storage pattern。

常見特徵：

- schema 較鬆，不要求每筆資料都完全同型
- 容易處理 semi-structured data
- 常見於高吞吐、水平擴充、低延遲場景
- 不一定以複雜 join 為核心查詢模式

這不代表 relational database 過時。比較準確的理解是：

- SQL / relational database：強 schema、關聯完整性、複雜查詢
- NoSQL：彈性資料模型、特定存取模式、擴充與延遲需求

## SQL vs. NoSQL

| 面向 | Relational Database | NoSQL |
| --- | --- | --- |
| 資料形狀 | rows / columns 為主 | document、key-value、graph、wide-column |
| schema | schema-on-write 較常見 | 較鬆、欄位可變 |
| 關聯處理 | join 很強 | 常避免複雜 join，改靠資料模型設計 |
| 一致性 | 常強調 constraints 與 transaction | 常依產品設計，在一致性與擴充間取捨 |
| 常見用途 | OLTP、核心主資料、複雜分析 | 快取、事件資料、半結構化資料、關係網路 |

## Scaling and Transaction Trade-Offs

NoSQL 常被拿來處理需要水平擴充的工作負載。

- vertical scaling：把單機 CPU、RAM、storage 往上加
- horizontal scaling：增加更多節點分散資料與流量

relational database 並不是不能 scale，但許多 NoSQL 系統從一開始就把分散式擴充、低延遲讀寫、或高吞吐量放在更前面的設計順位。

另一個常見差異是 transaction 模型：

- relational database 通常把 ACID transaction 當成核心能力
- NoSQL 產品之間差異很大，有些支援交易，有些只在較小範圍保證一致性

因此比較好的選型問題不是「NoSQL 有沒有 transaction」，而是：

- 這個 workload 最需要的是什麼
- 一致性、延遲、吞吐量、擴充性之間要怎麼取捨

## Common NoSQL Families

NoSQL 不是只有一種資料庫。先分資料形狀，比背產品名稱更重要。

### Document Databases

document database 以文件為中心，每筆資料常是 JSON-like 結構。

適合情境：

- 欄位會隨業務演進
- 同一類資料不保證每筆都有完全相同欄位
- 讀取時常想一次拿到整個物件

常見特徵：

- 資料常以 key-value、array、nested object 組成
- schema 比表格式更有彈性
- 很適合 semi-structured data

### Key-Value Databases

key-value database 用最簡單的 `key -> value` 模型存資料。

可以把它想成超大規模、可持久化的 dictionary。

適合情境：

- session management
- caching
- user preferences
- 非常明確的 key-based lookup

常見特徵：

- 依 key 取值很快
- 通常不擅長複雜條件查詢
- value 可能是 string、hash、list、set、sorted set、JSON 等結構

有些 key-value 系統會逐步補上 secondary index 或額外查詢能力，但核心心智模型仍然是「先有 key，再高效取值」，而不是把它當成通用 relational query engine。

### Redis as a Key-Value Example

Redis 是很常見的 key-value database 案例。

常被拿來處理：

- cache
- session store
- rate limiting
- leaderboard
- pub/sub 或輕量即時協作場景

它的一個特色是除了簡單的 `GET` / `SET` 之外，也直接提供多種資料結構操作，因此很適合把存取模式明確、延遲要求高的資料放進記憶體型資料庫處理。

實務上也常看到：

- 以 replication 提高可用性
- 以非同步 replication 交換延遲與一致性
- 先把熱門資料放進 Redis，再把完整真實資料留在後端主資料庫

### Graph Databases

graph database 直接把資料建模成 nodes 和 edges。

- node 代表 entity
- edge 代表 relationship

這類模型來自 graph theory。它的重點不是只存「物件有哪些欄位」，而是把「物件彼此如何相連」也當成一級公民。

適合情境：

- social network
- recommendation
- fraud detection
- relationship-heavy analysis
- knowledge graph

如果問題核心是「誰和誰相連、隔幾層、路徑怎麼走」，graph model 往往比硬用多層 join 更自然。

### Traversal Thinking

graph database 很常見的操作不是 join，而是 traversal，也就是沿著 edge 從 node 走到另一個 node。

典型問題像是：

- 兩個人之間隔幾層關係
- 哪條路徑最短
- 某個商品和哪些商品常被同一群人連到

這裡的 path 可以理解成一串由 nodes 和 edges 組成的連接序列。當查詢重心是 path discovery、multi-hop relationship、或鄰近節點探索時，graph model 通常比表格模型更貼近問題本身。

### Neo4j Ecosystem at a Glance

Neo4j 是最常見的 graph database 產品之一。先記住幾個高層概念就夠：

- `Cypher` 是它最知名的 graph query language
- 常搭配 graph algorithms 或 graph data science workflow 做推薦、社群偵測、最短路徑等分析
- 生態系也常強調和 Spark、Kafka、BI 工具的整合

這些產品細節不用一開始就背熟，但它們反映了一個重要訊號：graph database 不只是 storage choice，常常也是一套圍繞 relationship analysis 的工作流。

### Column-Oriented / Wide-Column Thinking

有些 NoSQL 或 analytical data store 會偏 column-oriented。

這類系統的重點不是把整列資料一起讀出，而是：

- 只讀查詢真正需要的欄位
- 對大量資料做聚合或掃描
- 在分析 workload 下取得更好的壓縮與查詢效率

這和 row-oriented OLTP database 的優先順序不同：

- row-oriented：較適合單筆插入、更新、刪除
- column-oriented：較適合 bulk load、分析查詢、欄位裁切式讀取

如果是在 NoSQL 脈絡下談 wide-column 或 column family database，重點又會再不一樣一些。

### Column Family Databases

column family database 常被視為 wide-column database，經典脈絡可追到 Google Bigtable。

這類系統通常會把經常一起存取的資料放進同一個 column family，目標是：

- 讓大規模資料的讀寫更有效率
- 針對特定存取模式安排資料位置
- 在超大量資料下仍維持可擴充性

因此它和一般分析型 column store 雖然都跟「column」有關，但心智模型不完全一樣：

- analytical column store：偏重掃描少數欄位、壓縮、聚合分析
- wide-column / column family：偏重分散式擴充、依 access pattern 組織資料

## Row-Oriented vs. Column-Oriented

| 面向 | Row-Oriented | Column-Oriented |
| --- | --- | --- |
| 典型 workload | transactional | analytics |
| 寫入模式 | 單筆或小批次操作 | 大批量載入與掃描 |
| 讀取方式 | 常一次讀整列 | 常只讀部分欄位 |
| 常見優勢 | update / delete 單筆效率較自然 | compression、aggregation、selective read |

如果查詢是：

```sql
SELECT title, price
FROM books
WHERE price < 50.00;
```

在 column-oriented engine 裡，心智模型通常比較像：

1. 先掃 `price` 欄找出符合條件的 records。
2. 再回頭取那些 records 對應的 `title` 欄值。

所以它特別適合「欄位少、資料量大、以分析為主」的場景。

## Semi-Structured Data Inside SQL Systems

實務上不是只有 NoSQL database 才能處理 semi-structured data。  
很多 relational 或 analytical system 也內建了這類能力。

### Snowflake

Snowflake 常用 `VARIANT` 來放 semi-structured data，也支援 `OBJECT` 與 `ARRAY`。

可以把它先理解成：

- `OBJECT` 類似 dictionary
- `ARRAY` 類似 list
- `VARIANT` 是可容納 semi-structured value 的泛用型別

常見查法：

```sql
SELECT
    library['ISBN_13'],
    library["size"]["dimensions"]
FROM books;
```

或：

```sql
SELECT
    library:ISBN_13,
    library:size.dimensions,
    library:size.weight
FROM books;
```

重點不是語法細節，而是你可以先把 nested data 留在單一欄位裡，再逐步展開查詢。

### PostgreSQL JSON / JSONB

PostgreSQL 雖然是 relational database，但也很適合放部分 semi-structured data。

兩個常見型別：

- `JSON`：以 JSON 格式儲存
- `JSONB`：binary representation，通常更適合查詢與索引

如果欄位需要常被篩選、抽取、索引，`JSONB` 通常比 `JSON` 更實用。

例如：

```sql
CREATE TABLE students (
  student_id BIGINT,
  parent_meta JSONB
);
```

### PostgreSQL JSONB Query Pattern

`->` 取出 JSON value。  
`->>` 取出 text value。

```sql
SELECT
    parent_meta -> 'guardian' AS guardian_json,
    parent_meta ->> 'status' AS status_text
FROM students;
```

查 nested object：

```sql
SELECT
    parent_meta -> 'jobs' ->> 'P1' AS job_p1,
    parent_meta -> 'jobs' ->> 'P2' AS job_p2
FROM students;
```

查 array element：

```sql
SELECT
    parent_meta -> 'educations' ->> 0 AS education_0,
    parent_meta -> 'educations' ->> 1 AS education_1
FROM students;
```

檢查 JSON 外層型別：

```sql
SELECT
    json_typeof(parent_meta -> 'jobs') AS jobs_type
FROM students;
```

這種設計很適合：

- 先保留欄位彈性
- 只把穩定核心欄位正規化
- 把少數變動欄位留在 JSONB

但如果某些 JSON 欄位已經成為高頻 join key、主過濾條件、或報表核心欄位，通常就代表它們值得被拉回正式欄位。

## When NoSQL Is a Better Fit

- 資料型狀常變，schema 很難先完全定死
- 系統主要是 key-based lookup，而不是關聯分析
- 關係網路本身就是核心問題
- 要處理大量 semi-structured payload
- 分析系統偏向 scan 某些欄位，而不是整列交易更新

## When Relational Design Is Still Better

- 需要明確 foreign key 與資料完整性
- 複雜 join 是主要查詢模式
- 業務規則必須靠 transaction 嚴格保證
- schema 已相對穩定，而且團隊很依賴 SQL 分析

## Practical Reminders

- NoSQL 不是 relational database 的替代王者，而是另一組 trade-off。
- 選型前先問 access pattern，而不是先問流行度。
- semi-structured data 不代表完全不用 schema，只是 schema 可以延後或局部化。
- 把彈性欄位放進 JSONB 很方便，但不要把所有資料建模問題都推給單一 JSON 欄位。
- column-oriented 系統通常適合分析，不代表它自然適合高頻單筆交易。

[Back to Databases](README.md)
