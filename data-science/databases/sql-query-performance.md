# SQL Query Performance


查詢變慢時，先量測、再看執行計畫、最後才改寫或加 index。通用流程：

1. 把查詢寫清楚：只選需要的欄位、先過濾再 join、避免在 `WHERE` 欄位上套函式（會讓 index 失效）。
2. 看執行計畫：PostgreSQL 用 `EXPLAIN (ANALYZE, BUFFERS)`，SQL Server 用 `SET STATISTICS TIME/IO ON` + actual execution plan。
3. 找最貴的節點：全表掃描（`Seq Scan` / `Table Scan`）、大量排序、預估列數與實際差很多。
4. 改寫查詢或加 index，再重新量測（多跑幾次看趨勢，不要只看一次）。

| | PostgreSQL | SQL Server |
| --- | --- | --- |
| 看計畫 | `EXPLAIN`、`EXPLAIN ANALYZE` | Estimated / Actual Execution Plan |
| 量測 | `EXPLAIN (ANALYZE, BUFFERS)` | `SET STATISTICS TIME ON`、`SET STATISTICS IO ON`（看 logical reads） |
| 全表掃描 | `Seq Scan` | `Table Scan` / `Clustered Index Scan` |
| 用到 index | `Index Scan`、`Index Only Scan`、`Bitmap Heap Scan` | `Index Seek` |
| 更新統計 | `ANALYZE table` | `UPDATE STATISTICS table` |

## PostgreSQL: `EXPLAIN` 與 Index

這篇整理 PostgreSQL 查詢效能優化的常用心法。重點不是追求「所有 query 都用 index」，而是建立一套穩定的診斷流程：先理解 query 在做什麼，再用 `EXPLAIN` 看 planner 怎麼想，最後才決定要改寫查詢、補 index，或調整資料結構。

### 先有的心智模型

PostgreSQL 執行查詢時，大致會經過兩層：

- query: 你寫下的 SQL
- query plan: planner 決定實際怎麼做

所以效能問題常不是「SQL 語法對不對」，而是「planner 最後選了哪條執行路徑」。

### 一個實用的診斷順序

1. 先確認查詢真正想回答的問題
2. 刪掉不必要的欄位、排序、聚合與 join
3. 用 `EXPLAIN` 看 planner 預估的做法
4. 用 `EXPLAIN ANALYZE` 看實際執行時間與 row count
5. 再決定要不要加 index、改寫 subquery、拆 temp table 或重組 join

### `EXPLAIN` 是第一個工具

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

### `EXPLAIN` 常見節點怎麼讀

#### `Seq Scan`

代表 PostgreSQL 逐列掃描整張表。

```sql
EXPLAIN
SELECT *
FROM cheeses;
```

`Seq Scan` 不一定是壞事。對小表、低選擇性的條件，順序掃描反而可能比走 index 更划算。

#### `Sort`

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

#### `HashAggregate`

聚合查詢常會看到：

```sql
EXPLAIN ANALYZE
SELECT type, AVG(age) AS avg_age
FROM cheeses
GROUP BY type;
```

plan 可能出現 `HashAggregate`，這通常表示 PostgreSQL 先掃過資料，再用 hash 做群組聚合。

#### `Hash Join`

join 大表時很常見：

```sql
EXPLAIN ANALYZE
SELECT c.name, a.species
FROM cheeses AS c
INNER JOIN animals AS a
  ON c.species = a.species;
```

如果 planner 選 `Hash Join`，通常代表它認為先建立其中一側的 hash table，再做配對是合理的。

### `EXPLAIN VERBOSE` 與 `EXPLAIN ANALYZE`

#### `VERBOSE`

```sql
EXPLAIN VERBOSE
SELECT *
FROM cheeses;
```

適合在你想看更多 plan node 細節時使用，例如欄位來源、schema 或 alias。

#### `ANALYZE`

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

### 預估與實際不一致時代表什麼

如果 `EXPLAIN` 估的 rows 很少，但 `EXPLAIN ANALYZE` 實際 rows 很多，通常代表：

- 統計資訊不準
- filter selectivity 和 planner 預期差太多
- query 結構讓 planner 難以估算

這時候不要急著硬加 index，先確認：

- 條件是不是過寬
- join 條件是不是造成 row explosion
- 聚合前是否先做了過多展開

### Join 寫法與效能

join 本身不是慢的原因，真正影響效能的是：

- join 之前輸入的資料量
- join key 是否合理
- 是否重複展開了本來可先過濾的資料

#### 先過濾，再 join

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

#### Subquery vs Join

很多時候 subquery 可以改寫成 join，但不要把它當成教條。  
真正該問的是：

- 哪種寫法比較容易先過濾資料
- 哪種寫法比較容易被 planner 最佳化
- 哪種寫法比較容易檢查 row duplication

如果 subquery 寫法把過濾條件藏太深，改成明確 join 往往更容易讀 plan。

### CTE 與 Temporary Table

兩者都可以把中間結果拆出來，但適用情境不同。

#### CTE

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

#### Temporary table

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

### Index 策略

index 的本質，是建立一條讓 planner 更快找到資料的路。

#### 查看既有 index

```sql
SELECT *
FROM pg_indexes
WHERE schemaname = 'public';
```

看 `pg_indexes` 很實用，因為它可以快速回答：

- 某張表已經有哪些 index
- index 是建在哪些欄位上
- index definition 到底長什麼樣子

#### 建立 index

```sql
CREATE INDEX recipe_index
ON cookbook (recipe);
```

如果是線上系統、想降低鎖表影響，可以考慮：

```sql
CREATE INDEX CONCURRENTLY recipe_serving_index
ON cookbook (recipe, serving_size);
```

#### 什麼時候比較值得用 index

- 大表
- 常出現在 `WHERE` 條件的欄位
- 常用在 join key 的欄位
- 主鍵與高選擇性的查詢欄位

#### 什麼時候要保守一點

- 很小的表
- 常更新的表
- 大量 `NULL` 或低選擇性的欄位
- 寫入量遠高於讀取量的場景

原因很簡單：index 不是免費的。它會增加：

- 額外儲存空間
- insert / update / delete 的維護成本
- schema 管理複雜度

### Index 不是萬靈丹

常見誤區是看到慢 query 就先加 index。  
更穩的做法通常是先問：

- 是不是掃了太多不必要的列
- 是不是先 join 再過濾
- 是不是 `SELECT *`
- 是不是排序與聚合成本才是真正瓶頸

如果問題根源在 query shape，不改查詢只補 index，常常治標不治本。

### 分頁、排序與聚合也常是瓶頸

#### `LIMIT`

`LIMIT` 可以直接減少回傳資料量，但不保證前面的掃描、排序或 join 工作量會一起下降。

```sql
SELECT name, age
FROM cheeses
ORDER BY age DESC
LIMIT 20;
```

如果 query 先做重排序，再取前 20 筆，真正的成本可能仍在排序本身。

#### `GROUP BY`

聚合查詢要特別注意：

- 聚合前的輸入有多大
- 是否有不必要的 join
- 是否能先過濾再 group

先縮小資料，再做 `GROUP BY`，通常是比單純補 index 更有感的優化手段。

### Partitioning 的定位

partition 比較像資料管理與掃描範圍控制策略，不是所有效能問題的第一解。

比較適合考慮 partition 的情況：

- 超大表
- 查詢常按時間區間或固定分區鍵過濾
- 維運上需要分段管理舊資料

如果資料量還沒到那個級別，先把 query shape、索引與 plan 看懂，通常更划算。

### 一套很務實的優化流程

1. 先改掉 `SELECT *`
2. 把過濾條件提前
3. 確認 join 沒有造成 row explosion
4. 用 `EXPLAIN` 看 planner 選了 `Seq Scan`、`Hash Join`、`Sort` 還是 `HashAggregate`
5. 用 `EXPLAIN ANALYZE` 比對 estimated rows 和 actual rows
6. 再決定是否建立或調整 index
7. 若中間結果會重複使用，再考慮 temp table

### 實務心法

- 寫出來的 SQL 不等於實際執行的步驟
- `EXPLAIN ANALYZE` 幾乎是 PostgreSQL 效能調校的起點
- 先縮小資料量，再談 index，通常比較有效
- 好的 index 是為特定查詢模式服務，不是越多越好
- 能拆成可驗證的中間步驟，通常比一次寫成超大 query 更容易優化

## SQL Server: `STATISTICS TIME/IO` 與 Execution Plan

這篇整理 SQL Server 查詢效能調校時最常用的觀察點。重點不是一開始就改 schema 或狂加 index，而是先用 SQL Server 自帶的統計與 execution plan 看出瓶頸在哪裡。

### 一個實用的診斷順序

1. 先把 query 改到容易閱讀
2. 確認過濾條件與 join 條件是否能提早縮小資料量
3. 開啟 `STATISTICS TIME` 與 `STATISTICS IO`
4. 看 estimated execution plan
5. 再決定要不要補 index、改寫查詢，或調整資料存放方式

### 先把查詢寫清楚

效能調校前，先把 SQL 寫成自己看得懂的版本。  
很多慢 query 的問題，不是 optimizer 太神秘，而是查詢本身把條件、子查詢與計算欄位塞得太亂。

例如：

- 避免不必要的 `SELECT *`
- 讓 join 條件與 filter 條件分開排版
- 先確認 `WHERE` 是否在最有效的地方縮小資料集

### `WHERE` 的處理順序很重要

SQL Server 的 `WHERE` 先於 `SELECT` 別名處理，所以這種寫法會出錯：

```sql
SELECT
  PlayerName,
  Team,
  DRebound + ORebound AS TotalRebounds
FROM PlayerStats
WHERE TotalRebounds >= 1000
ORDER BY TotalRebounds DESC;
```

如果過濾條件依賴計算欄位，應改成：

- 直接在 `WHERE` 重寫運算式
- 或先包成子查詢 / CTE，再在外層過濾

這不只是語法問題，也會影響 query shape 與 optimizer 的選擇空間。

### `SET STATISTICS TIME ON`

第一個常用工具是時間統計：

```sql
SET STATISTICS TIME ON;

SELECT ...
FROM ...
WHERE ...;

SET STATISTICS TIME OFF;
```

常見輸出會包含：

- `CPU time`
- `elapsed time`

#### 怎麼看 `CPU time` 與 `elapsed time`

- `CPU time`: server processor 真正花在處理 query 的時間
- `elapsed time`: 整體經過時間

實務上可以這樣理解：

- `elapsed time` 比較接近使用者感受到的慢不慢
- `CPU time` 比較適合看查詢本身處理成本

但兩者都不是看一次就下結論。  
同一支 query 可能因為快取、並行、伺服器當下負載不同而波動，所以至少要跑多次看趨勢。

#### 不要只看單次測量

一筆 `elapsed time = 2032 ms` 不代表真實水準。  
比較穩的做法是：

- 連跑幾次
- 看平均值
- 比較調整前後的整體趨勢

### `SET STATISTICS IO ON`

第二個核心工具是頁面讀取統計：

```sql
SET STATISTICS IO ON;

SELECT ...
FROM ...
WHERE ...;

SET STATISTICS IO OFF;
```

這會顯示每張表的讀取情況，例如：

- `Scan count`
- `logical reads`
- `physical reads`
- `read-ahead reads`

#### `logical reads` 特別重要

SQL Server 以 page 為基本讀取單位，每頁通常是 8 KB。  
`logical reads` 可以理解成 query 為了完成工作，總共讀了多少資料頁。

心智模型上：

- `logical reads` 越高，通常表示 query 接觸的資料範圍越大
- 如果改寫 query 後 `logical reads` 明顯下降，通常是很有價值的改善

很多時候，`logical reads` 比單次 elapsed time 更穩定，因為它比較不受當下機器忙碌程度影響。

### 什麼是 index

index 本質上是幫資料建立更快的尋找路徑，避免每次都掃整張表。

適合改善的場景通常是：

- 常用在 `WHERE` 條件的欄位
- 常用在 join key 的欄位
- 需要快速定位少量資料列的查詢

但 index 不是免費的，它會增加：

- 額外儲存空間
- insert / update / delete 的維護成本

### Clustered 與 Nonclustered Index

#### Clustered index

可以把 clustered index 想成字典：

- 資料頁本身依照 index key 排序
- 一張表只能有一個 clustered index
- 很適合支援範圍查詢與有序存取

#### Nonclustered index

可以把 nonclustered index 想成教科書後面的索引：

- index 自己有排序結構
- 指向實際資料頁
- 一張表可以有多個 nonclustered index

這兩種 index 的差別，核心不在名詞，而在資料頁是不是依照 key 本身排列。

### B-tree 心智模型

SQL Server index 常以 B-tree 結構組織，可以粗略理解成：

- root node
- branch nodes
- leaf / page nodes

這種設計讓 SQL Server 不必從第一列一路掃到最後一列，而是可以快速縮小搜尋範圍。

### Table Scan、Index Seek、Index Scan

看 execution plan 時，先學會區分幾種最常見的存取方式：

- `Table Scan`: 整張表掃描
- `Index Scan`: 掃描整個 index 或大範圍 index
- `Index Seek`: 直接定位到較小範圍資料

`Index Seek` 通常比 `Table Scan` 更令人安心，但也不要把它當成唯一目標。  
如果表很小，或條件本來就要讀大部分資料，scan 也可能是合理選擇。

### Execution Plan 要看什麼

execution plan 可以回答很多關鍵問題：

- 有沒有用到 index
- 用了哪種 join
- 是否有 sort
- 哪些 operator 代價最高

在 SSMS 中，estimated execution plan 很適合先看 optimizer 預估會怎麼跑。  
如果還要驗證實際執行狀況，再搭配真正執行與統計輸出一起判讀。

### 常見 operator

#### Join operators

執行計畫常見的 join operator 包括：

- `Nested Loops`
- `Hash Match`
- `Merge Join`

通常可以這樣粗略理解：

- `Nested Loops`: 一側較小、另一側可快速查找時常見
- `Hash Match`: 大量資料配對時常見
- `Merge Join`: 雙方已排序或容易排序時可能出現

#### `Sort`

如果 query 有 `ORDER BY`、`DISTINCT` 或某些聚合操作，常會看到 `Sort`。  
sort 本身可能就是成本來源，所以要先問：

- 是否真的需要排序
- 是否可以先過濾再排序
- 是否有適合的 index 能減少排序成本

### Query rewrite 常比硬加 index 更有效

很多查詢其實可以先從重寫開始：

- 先過濾，再 join
- 把重複子查詢改寫成較清楚的 `EXISTS`、join 或 CTE
- 降低中間結果大小
- 移除不必要欄位與排序

如果改寫後 `logical reads` 從 54 降到 18，通常代表你真的讓 SQL Server 少做了工作，而不只是碰巧快了一次。

### 比較查詢時要看趨勢，不要只看一次

實務上比較兩種寫法時，至少同時看：

- 平均 elapsed time
- CPU time
- logical reads
- execution plan 裡是否出現不同 operator 或不同資料存取方式

這樣比較能分辨：

- 是真的查得更少
- 還是只是剛好吃到 cache
- 或只是當下伺服器比較空閒

### 實務心法

- 效能調校前，先把 query 寫清楚
- `SET STATISTICS TIME ON` 用來看時間
- `SET STATISTICS IO ON` 用來看資料頁讀取成本
- execution plan 用來理解 SQL Server 到底怎麼跑
- index 是針對查詢模式設計，不是越多越好
- 能先減少資料量，通常比事後補救更有效
