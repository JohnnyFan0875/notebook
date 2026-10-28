[Data Science](../README.md) › [Databases](README.md) › NoSQL 基礎

# NoSQL 基礎 (NoSQL Foundations)

NoSQL（not only SQL）不是單一產品，也不是「比 SQL 新」的資料庫，而是一組以非表格資料模型為主的系統：document、key-value、graph、wide-column。選型時先看資料形狀與存取模式，而不是流行度。

## SQL vs NoSQL

| 面向 | 關聯式資料庫 | NoSQL |
| --- | --- | --- |
| 資料形狀 | 表格（列 × 欄） | 文件、key-value、圖、wide-column |
| schema | schema-on-write，事先定義 | 彈性，欄位可變 |
| 關聯 | join 是核心能力 | 避免複雜 join，靠資料模型設計（把一起讀的資料存在一起） |
| 一致性 | ACID 交易、constraint | 依產品而異；常在一致性、延遲、可用性間取捨 |
| 擴充 | 傳統上垂直擴充（加大單機） | 多數為水平擴充（加節點、分片） |
| 適合 | 交易、主資料、複雜查詢與分析 | 快取、事件與日誌、半結構化資料、關係網路 |

> 很多 NoSQL 產品已支援交易（MongoDB 4.0+ 多文件交易），關聯式資料庫也能存 JSON 與水平擴充。比較好的問題是：這個工作負載最需要的是什麼？

## 四種資料模型

| 類型 | 資料模型 | 典型產品 | 適合 | 不適合 |
| --- | --- | --- | --- | --- |
| Document | JSON-like 文件，可巢狀 | MongoDB、Couchbase | 欄位隨演進改變、一次讀整個物件（樣本 metadata、API 回應） | 大量跨文件 join |
| Key-value | `key → value` 的超大 dict | Redis、DynamoDB | 快取、session、計數器、依 key 查詢 | 依值的條件查詢 |
| Graph | node + edge（都可帶屬性） | Neo4j、Amazon Neptune | 多跳關係：知識圖譜、交互作用網路、推薦、詐騙偵測 | 大量聚合統計 |
| Wide-column | 依 row key 分散、欄位分組（column family） | Cassandra、HBase、Bigtable | 超大量寫入、依 key 範圍讀取（時間序列、感測器） | 臨時性的分析查詢 |

### Document database

文件就是 Python 的 `dict`：

```json
{
  "sample_id": "S001",
  "tissue": "liver",
  "assays": [
    {"type": "RNA-seq", "reads": 42000000},
    {"type": "WGS", "coverage": 30}
  ]
}
```

同一 collection 的文件可以有不同欄位；巢狀欄位用 dot notation 直接查（`assays.type`）。PyMongo 實作見 [MongoDB 與 PyMongo](mongodb-pymongo.md)。

### Key-value：Redis

| 用途 | 為什麼適合 |
| --- | --- |
| 快取（cache） | 資料在記憶體，讀取延遲低；熱門資料放 Redis，完整資料留在主資料庫 |
| session、rate limiting | 依 key 讀寫、可設過期時間（TTL） |
| 排行榜 | 內建 sorted set |
| 工作佇列、pub/sub | 內建 list、stream |

value 不只是字串，還可以是 hash、list、set、sorted set 等結構。以 replication 提高可用性；非同步 replication 用一致性換延遲。

### Graph database

| 概念 | 說明 |
| --- | --- |
| node | 實體（基因、蛋白質、疾病、藥物） |
| edge | 關係（交互作用、調控、適應症），可帶權重與屬性 |
| traversal | 沿著 edge 走：「與 TP53 距離 2 跳內的所有蛋白」 |
| path | node 與 edge 交錯的序列；最短路徑、可達性 |

問題的核心是「誰和誰相連、隔幾層、怎麼走」時，圖模型比多層 SQL join（或 [recursive CTE](recursive-and-hierarchical-sql.md#模式三多跳路徑圖)）自然得多。Neo4j 用 Cypher 查詢語言，並提供社群偵測、中心性、最短路徑等圖演算法。生醫知識圖譜（藥物再利用、疾病基因預測）常用這類系統；單純分析一個網路則用 networkx / igraph 即可（見 [Network Analysis](../network-analysis/README.md)）。

### Wide-column 與 column store

兩者名稱都有 column，但目的不同：

| | Wide-column / column family（Cassandra、HBase） | 欄式分析儲存（Parquet、DuckDB、Snowflake） |
| --- | --- | --- |
| 目的 | 分散式擴充、超大寫入量 | 掃描少數欄並聚合 |
| 存取 | 依 row key 讀寫 | 讀整欄、壓縮、跳過不相關區塊 |
| 類別 | NoSQL | 多為 SQL 系統 |

## Row-oriented vs column-oriented

| 面向 | Row-oriented | Column-oriented |
| --- | --- | --- |
| 儲存 | 一列的所有欄位放在一起 | 一欄的所有值放在一起 |
| 擅長 | 單筆插入、更新、讀整列（OLTP） | 大量列、少數欄的聚合（OLAP） |
| 壓縮 | 一般 | 好（同欄型別相同、值相近） |
| 例子 | PostgreSQL、MySQL、SQLite | DuckDB、Snowflake、BigQuery、Parquet 檔 |

```sql
SELECT title, price FROM books WHERE price < 50;
-- column store：只讀 price 欄找出符合的列，再取對應的 title；其他欄完全不碰
```

表現量矩陣、變異位點表這類「很多列、分析時只用幾欄」的資料，欄式格式（Parquet）的優勢最明顯，見 [DuckDB 與 Parquet](duckdb-and-parquet.md)。

## 關聯式資料庫裡的半結構化資料

不必為了少數彈性欄位就換成 NoSQL：PostgreSQL、Snowflake、DuckDB 都能在欄位裡存 JSON。

### PostgreSQL JSONB

| 型別 | 儲存 | 用途 |
| --- | --- | --- |
| `JSON` | 原始文字，保留空白與 key 順序 | 只存不查 |
| `JSONB` | 解析後的二進位格式 | 查詢、建 index（GIN）；**通常選這個** |

```sql
CREATE TABLE samples (
  sample_id TEXT PRIMARY KEY,
  meta      JSONB
);

SELECT
  meta -> 'library'                   AS library_json,   -- -> 回傳 JSON
  meta ->> 'tissue'                   AS tissue,         -- ->> 回傳文字
  meta -> 'library' ->> 'kit'         AS kit,            -- 巢狀
  meta -> 'lanes' ->> 0               AS first_lane,     -- 陣列（0 起算）
  (meta ->> 'rin')::NUMERIC           AS rin,            -- 取出後轉型
  jsonb_typeof(meta -> 'lanes')       AS lanes_type      -- 'array'
FROM samples
WHERE meta @> '{"tissue": "liver"}';                     -- 包含運算子，可用 GIN index

CREATE INDEX ON samples USING GIN (meta);
SELECT sample_id, jsonb_array_elements_text(meta -> 'lanes') AS lane FROM samples;   -- 陣列展開成列
```

### Snowflake VARIANT

```sql
SELECT
  library:ISBN_13::STRING,            -- : 取值，:: 轉型
  library:size.dimensions,            -- 巢狀用 .
  library['size']['weight']           -- 也可用中括號
FROM books;
```

陣列展開用 `LATERAL FLATTEN`，見 [SQL 方言速查](sql-dialect-cheatsheet.md#snowflake半結構化資料)。

> 穩定、常用來過濾或 join 的欄位拉成正式欄位；只把少數變動的屬性留在 JSON。某個 JSON 欄位成為主要過濾條件或報表核心時，就該升級成一般欄位。

## 選型

| 情境 | 選擇 |
| --- | --- |
| 需要外鍵、constraint、交易保證 | 關聯式 |
| 主要查詢是多表 join 與聚合 | 關聯式（或分析型 column store） |
| 結構常變、以整份文件讀寫 | Document |
| 只依 key 存取、要求極低延遲 | Key-value |
| 核心問題是多跳關係 | Graph |
| 超大寫入量、依 key 範圍讀取 | Wide-column |
| 主體是關聯式，只有部分欄位彈性 | 關聯式 + JSONB |
