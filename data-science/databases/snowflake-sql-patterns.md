# Snowflake SQL Patterns

這篇整理 Snowflake 上常見的 SQL 使用模式。重點不是把所有語法背完，而是理解在 Snowflake 這種 analytical warehouse 裡，join、query history 與 semi-structured data 會怎麼影響日常分析工作。

## Join Landscape

Snowflake 支援常見的 join 類型：

- `INNER JOIN`
- `LEFT JOIN`
- `RIGHT JOIN`
- `FULL OUTER JOIN`
- `CROSS JOIN`
- `SELF JOIN`
- `NATURAL JOIN`
- `LATERAL JOIN`

如果只是一般關聯式資料表整合，最常用的仍然是 `INNER JOIN` 與 `LEFT JOIN`。

## Practical Join Guidance

### Prefer Explicit Join Conditions

一般情況下，優先使用明確的 `ON` 條件，而不是依賴隱含欄位名稱配對。

```sql
SELECT p.pizza_id, t.name
FROM pizzas AS p
JOIN pizza_type AS t
  ON t.pizza_type_id = p.pizza_type_id;
```

這樣可讀性更高，也比較不容易因 schema 變動而出錯。

### `NATURAL JOIN` Should Be Used Carefully

`NATURAL JOIN` 會自動用同名欄位當 join key，語法很短，但風險也比較高：

- 不容易一眼看出實際 join key
- schema 一改，結果可能跟著變
- 同名但語意不同的欄位可能被誤用

除非資料模型非常穩定，否則通常還是用明確 `ON` 比較安全。

### `SELF JOIN`

`SELF JOIN` 適合：

- 階層關係
- 找前後筆資料
- 同表內部比對

核心技巧是替同一張表設不同 alias，再用條件把兩份邏輯角色分開。

### `CROSS JOIN`

`CROSS JOIN` 會產生笛卡兒積，列數成長很快。  
只有在你真的需要所有組合時才應該使用，否則很容易放大掃描與計算成本。

## Lateral Join and Semi-Structured Data

Snowflake 的一個特別實用場景，是把 semi-structured data 展開後再查詢。

### Structured vs. Semi-Structured

- structured data: 欄位固定、schema 明確的 table
- semi-structured data: 常見如 JSON，欄位可能可變、巢狀結構較多

Snowflake 原生支援 JSON 類資料，常用 `VARIANT` 儲存。

### `PARSE_JSON`

當 JSON 先以字串存在時，可以用 `PARSE_JSON()` 轉成 Snowflake 可操作的 `VARIANT`。

```sql
SELECT PARSE_JSON('{"name":"alice","age":30}') AS obj;
```

### `LATERAL` + `FLATTEN`

當 JSON 裡有陣列或巢狀資料時，常用 `LATERAL` 搭配 `FLATTEN()` 把內容展開成列。

心智模型可以想成：

- 先保留原始列
- 再把某個巢狀欄位拆成多列
- 最後像查普通 table 一樣篩選與聚合

這是 Snowflake 處理 event logs、API payloads、clickstream 與彈性 schema 資料時的常見做法。

## Query Performance Habits

### Avoid `SELECT *`

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

### Read Query History

Snowflake 提供 `query_history` 類型的監控檢視，能用來看：

- `query_text`
- `start_time`
- `end_time`
- `execution_time`

這類資訊很適合拿來：

- 找慢查詢
- 回查某段 SQL 是否真的執行過
- 用 `ILIKE` 做 case-insensitive 搜尋，定位特定分析或 job

## Mental Checklist

- 一般 join 優先用明確 `ON`
- `NATURAL JOIN` 省字，但通常不夠穩
- `CROSS JOIN` 前先估列數膨脹
- semi-structured data 常搭配 `VARIANT`、`PARSE_JSON()`、`LATERAL FLATTEN()`
- 分析查詢盡量避免 `SELECT *`
- 查詢慢時，先看 history 與實際掃描需求，再決定要不要放大 compute
