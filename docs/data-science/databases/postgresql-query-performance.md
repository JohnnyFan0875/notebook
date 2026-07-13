# PostgreSQL Query Performance

這篇整理 PostgreSQL 查詢效能優化的常用心法。重點不是追求「所有 query 都用 index」，而是建立一套穩定的診斷流程：先理解 query 在做什麼，再用 `EXPLAIN` 看 planner 怎麼想，最後才決定要改寫查詢、補 index，或調整資料結構。

## 先有的心智模型

PostgreSQL 執行查詢時，大致會經過兩層：

- query: 你寫下的 SQL
- query plan: planner 決定實際怎麼做

所以效能問題常不是「SQL 語法對不對」，而是「planner 最後選了哪條執行路徑」。

## 一個實用的診斷順序

1. 先確認查詢真正想回答的問題
2. 刪掉不必要的欄位、排序、聚合與 join
3. 用 `EXPLAIN` 看 planner 預估的做法
4. 用 `EXPLAIN ANALYZE` 看實際執行時間與 row count
5. 再決定要不要加 index、改寫 subquery、拆 temp table 或重組 join

## `EXPLAIN` 是第一個工具

最基本的查法：

```sql
EXPLAIN
SELECT *
FROM cheeses
WHERE species IN ('goat', 'sheep');
```

`EXPLAIN` 不會真的執行查詢，而是顯示 planner 預估的執行計畫。

最常先看的欄位有：

- scan 類型，例如 `Seq Scan`、`Index Scan`
- estimated cost
- estimated rows
- filter / join condition

## `EXPLAIN` 常見節點怎麼讀

### `Seq Scan`

代表 PostgreSQL 逐列掃描整張表。

```sql
EXPLAIN
SELECT *
FROM cheeses;
```

`Seq Scan` 不一定是壞事。對小表、低選擇性的條件，順序掃描反而可能比走 index 更划算。

### `Sort`

如果 query 有 `ORDER BY`，常會看到 sort 節點。

```sql
EXPLAIN ANALYZE
SELECT name, age
FROM cheeses
ORDER BY age DESC;
```

實際輸出常包含：

- `Sort Key`
- `Sort Method`
- memory usage

如果排序代價高，才值得考慮：

- 是否真的需要排序
- 是否可以縮小輸入資料量後再排序
- 是否有適合支援排序的 index

### `HashAggregate`

聚合查詢常會看到：

```sql
EXPLAIN ANALYZE
SELECT type, AVG(age) AS avg_age
FROM cheeses
GROUP BY type;
```

plan 可能出現 `HashAggregate`，這通常表示 PostgreSQL 先掃過資料，再用 hash 做群組聚合。

### `Hash Join`

join 大表時很常見：

```sql
EXPLAIN ANALYZE
SELECT c.name, a.species
FROM cheeses AS c
INNER JOIN animals AS a
  ON c.species = a.species;
```

如果 planner 選 `Hash Join`，通常代表它認為先建立其中一側的 hash table，再做配對是合理的。

## `EXPLAIN VERBOSE` 與 `EXPLAIN ANALYZE`

### `VERBOSE`

```sql
EXPLAIN VERBOSE
SELECT *
FROM cheeses;
```

適合在你想看更多 plan node 細節時使用，例如欄位來源、schema 或 alias。

### `ANALYZE`

```sql
EXPLAIN ANALYZE
SELECT *
FROM cheeses;
```

這會真的執行 query，並顯示：

- actual time
- actual rows
- loops
- planning time
- execution time

這通常是最有用的版本，因為效能優化最後關心的是實際執行，而不只是 planner 的預估。

## 預估與實際不一致時代表什麼

如果 `EXPLAIN` 估的 rows 很少，但 `EXPLAIN ANALYZE` 實際 rows 很多，通常代表：

- 統計資訊不準
- filter selectivity 和 planner 預期差太多
- query 結構讓 planner 難以估算

這時候不要急著硬加 index，先確認：

- 條件是不是過寬
- join 條件是不是造成 row explosion
- 聚合前是否先做了過多展開

## Join 寫法與效能

join 本身不是慢的原因，真正影響效能的是：

- join 之前輸入的資料量
- join key 是否合理
- 是否重複展開了本來可先過濾的資料

### 先過濾，再 join

比起先把兩大表 join 完再篩條件，通常更穩的是先縮小其中一側。

```sql
WITH warm_countries AS (
  SELECT country
  FROM climate
  WHERE temp_annual > 22
)
SELECT COUNT(a.athlete_id)
FROM athletes AS a
JOIN warm_countries AS c
  ON a.country = c.country;
```

核心概念不是「CTE 一定比較快」，而是先減少 join 輸入資料量。

### Subquery vs Join

很多時候 subquery 可以改寫成 join，但不要把它當成教條。  
真正該問的是：

- 哪種寫法比較容易先過濾資料
- 哪種寫法比較容易被 planner 最佳化
- 哪種寫法比較容易檢查 row duplication

如果 subquery 寫法把過濾條件藏太深，改成明確 join 往往更容易讀 plan。

## CTE 與 Temporary Table

兩者都可以把中間結果拆出來，但適用情境不同。

### CTE

```sql
WITH celsius AS (
  SELECT country
  FROM climate
  WHERE temp_annual > 22
)
SELECT COUNT(a.athlete_id)
FROM athletes AS a
JOIN celsius AS c
  ON a.country = c.country;
```

適合：

- 單次查詢內重整邏輯
- 提高 query 可讀性
- 讓「先過濾、再 join」的結構更清楚

### Temporary table

```sql
CREATE TEMP TABLE celsius AS
SELECT country
FROM climate
WHERE temp_annual > 22;

SELECT COUNT(a.athlete_id)
FROM athletes AS a
JOIN celsius AS c
  ON a.country = c.country;
```

適合：

- 中間結果要重複使用
- 需要把大型中間結果保存成明確實體
- 想把複雜流程切成多段檢查

如果某個 expensive 子查詢會被反覆使用，temp table 往往比一直重算更實際。

## Index 策略

index 的本質，是建立一條讓 planner 更快找到資料的路。

### 查看既有 index

```sql
SELECT *
FROM pg_indexes
WHERE schemaname = 'public';
```

看 `pg_indexes` 很實用，因為它可以快速回答：

- 某張表已經有哪些 index
- index 是建在哪些欄位上
- index definition 到底長什麼樣子

### 建立 index

```sql
CREATE INDEX recipe_index
ON cookbook (recipe);
```

如果是線上系統、想降低鎖表影響，可以考慮：

```sql
CREATE INDEX CONCURRENTLY recipe_serving_index
ON cookbook (recipe, serving_size);
```

### 什麼時候比較值得用 index

- 大表
- 常出現在 `WHERE` 條件的欄位
- 常用在 join key 的欄位
- 主鍵與高選擇性的查詢欄位

### 什麼時候要保守一點

- 很小的表
- 常更新的表
- 大量 `NULL` 或低選擇性的欄位
- 寫入量遠高於讀取量的場景

原因很簡單：index 不是免費的。它會增加：

- 額外儲存空間
- insert / update / delete 的維護成本
- schema 管理複雜度

## Index 不是萬靈丹

常見誤區是看到慢 query 就先加 index。  
更穩的做法通常是先問：

- 是不是掃了太多不必要的列
- 是不是先 join 再過濾
- 是不是 `SELECT *`
- 是不是排序與聚合成本才是真正瓶頸

如果問題根源在 query shape，不改查詢只補 index，常常治標不治本。

## 分頁、排序與聚合也常是瓶頸

### `LIMIT`

`LIMIT` 可以直接減少回傳資料量，但不保證前面的掃描、排序或 join 工作量會一起下降。

```sql
SELECT name, age
FROM cheeses
ORDER BY age DESC
LIMIT 20;
```

如果 query 先做重排序，再取前 20 筆，真正的成本可能仍在排序本身。

### `GROUP BY`

聚合查詢要特別注意：

- 聚合前的輸入有多大
- 是否有不必要的 join
- 是否能先過濾再 group

先縮小資料，再做 `GROUP BY`，通常是比單純補 index 更有感的優化手段。

## Partitioning 的定位

partition 比較像資料管理與掃描範圍控制策略，不是所有效能問題的第一解。

比較適合考慮 partition 的情況：

- 超大表
- 查詢常按時間區間或固定分區鍵過濾
- 維運上需要分段管理舊資料

如果資料量還沒到那個級別，先把 query shape、索引與 plan 看懂，通常更划算。

## 一套很務實的優化流程

1. 先改掉 `SELECT *`
2. 把過濾條件提前
3. 確認 join 沒有造成 row explosion
4. 用 `EXPLAIN` 看 planner 選了 `Seq Scan`、`Hash Join`、`Sort` 還是 `HashAggregate`
5. 用 `EXPLAIN ANALYZE` 比對 estimated rows 和 actual rows
6. 再決定是否建立或調整 index
7. 若中間結果會重複使用，再考慮 temp table

## 實務心法

- 寫出來的 SQL 不等於實際執行的步驟
- `EXPLAIN ANALYZE` 幾乎是 PostgreSQL 效能調校的起點
- 先縮小資料量，再談 index，通常比較有效
- 好的 index 是為特定查詢模式服務，不是越多越好
- 能拆成可驗證的中間步驟，通常比一次寫成超大 query 更容易優化
