[Data Science](../README.md) › [Databases](README.md) › 遞迴與階層查詢

# 遞迴與階層查詢 (Recursive and Hierarchical SQL)

資料指向同類資料時（員工 → 主管、GO term → 上層 term、物種 → 上層分類、零件 → 子零件、機場 → 下一站），用 recursive CTE 一層層展開。範例以 PostgreSQL / DuckDB / SQLite 語法為主，SQL Server 差異見文末。

## 骨架

```sql
WITH RECURSIVE tree AS (
  -- 1. anchor：起點
  SELECT id, parent_id, 1 AS level
  FROM nodes
  WHERE parent_id IS NULL

  UNION ALL

  -- 2. recursive：從上一輪的結果走到下一層
  SELECT n.id, n.parent_id, t.level + 1
  FROM nodes AS n
  JOIN tree  AS t ON n.parent_id = t.id
  -- 3. 終止：某一輪沒有新列時停止；可再加 WHERE t.level < 10
)
SELECT * FROM tree ORDER BY level, id;
```

| 檢查 | 說明 |
| --- | --- |
| 欄位數與型別一致 | anchor 與 recursive 兩段的欄位要對齊；字串欄在 anchor 先 `CAST` 成夠長的型別 |
| 終止條件 | 樹狀結構自然走到葉節點就停；有環（cycle）時會無限遞迴 |
| `UNION ALL` vs `UNION` | `UNION` 會去掉重複列，對簡單的環有保護作用，但狀態欄（level、path）不同時仍會繼續展開 |
| 表結構 | adjacency list（每列存 `parent_id`）最常見；多個 parent（DAG，如 GO）用 `child, parent` 邊表 |

## 模式一：往下展開 + 層級 + 路徑

```sql
WITH RECURSIVE hierarchy AS (
  SELECT id, supervisor_id, 1 AS level,
         CAST(id AS VARCHAR) AS path
  FROM employee
  WHERE supervisor_id IS NULL                 -- 根節點；有些資料用 0 代表沒有上層

  UNION ALL

  SELECT e.id, e.supervisor_id, h.level + 1,
         h.path || ' -> ' || CAST(e.id AS VARCHAR)
  FROM employee AS e
  JOIN hierarchy AS h ON e.supervisor_id = h.id
)
SELECT * FROM hierarchy ORDER BY path;
-- id sup level path
-- 1  NULL 1    1
-- 2  1    2    1 -> 2
-- 3  2    3    1 -> 2 -> 3
-- 4  2    3    1 -> 2 -> 4
```

`level` 用來限制深度、縮排顯示；`path` 用來顯示祖先鏈（breadcrumb）、依路徑排序成樹狀，也用來偵測環。

## 模式二：往上找所有祖先（本體論 / 分類樹）

GO、HPO、NCBI Taxonomy 都是「子 → 父」的邊表，且 GO 的一個 term 可以有多個 parent。富集分析常需要把基因的註解往上傳播到所有祖先 term（true path rule）。

```sql
-- go_isa(child, parent)：is_a 關係
WITH RECURSIVE anc AS (
  SELECT child AS term, parent AS ancestor, 1 AS dist
  FROM go_isa
  WHERE child = 'GO:0006915'                  -- apoptotic process

  UNION ALL

  SELECT a.term, g.parent, a.dist + 1
  FROM anc AS a
  JOIN go_isa AS g ON g.child = a.ancestor
)
SELECT ancestor, MIN(dist) AS dist            -- DAG：同一祖先可經多條路徑到達
FROM anc
GROUP BY ancestor
ORDER BY dist;
```

> DAG 中同一祖先會經不同路徑出現多次，先展開、再在外層 `GROUP BY` / `DISTINCT`。資料量大時（整個 GO × 所有基因），預先算好 closure table（`term, ancestor` 全配對）存起來，比每次遞迴快。富集分析本身見 [富集分析](../../biology/genomics/workflows/rna-seq/09-annotation-and-functional-enrichment.md)。

## 模式三：多跳路徑（圖）

把狀態（停靠數、累積成本、路徑）一起往下傳，就能回答成本上限、最便宜路線等問題。

```sql
WITH RECURSIVE route AS (
  SELECT departure, arrival,
         0                           AS stops,
         cost                        AS total_cost,
         departure || ' -> ' || arrival AS path
  FROM flights
  WHERE departure = 'New York'

  UNION ALL

  SELECT r.departure, f.arrival,
         r.stops + 1,
         r.total_cost + f.cost,
         r.path || ' -> ' || f.arrival
  FROM route   AS r
  JOIN flights AS f ON r.arrival = f.departure
  WHERE r.stops < 3                                   -- 深度上限
    AND r.path NOT LIKE '%' || f.arrival || '%'       -- 不重複造訪（防環）
)
-- 先展開所有候選路徑，再在外層篩選與彙總
SELECT arrival, MIN(total_cost) AS cheapest_cost
FROM route
WHERE total_cost <= 500
GROUP BY arrival
ORDER BY cheapest_cost;
```

| 防環方式 | 平台 | 說明 |
| --- | --- | --- |
| 深度上限 `WHERE level < n` | 全部 | 最保守，一定會停 |
| 路徑字串 `NOT LIKE` | 全部 | 簡單但會誤判子字串（`'LA'` 與 `'LAX'`）；加分隔符比對較安全 |
| 路徑陣列 `NOT f.arrival = ANY(path_arr)` | PostgreSQL、DuckDB | 精確 |
| `CYCLE id SET is_cycle USING path` | PostgreSQL 14+ | 標準語法，自動偵測 |

> 「最短路徑」「連通元件」等真正的圖分析，資料一大就該交給圖工具（networkx、igraph、圖資料庫），見 [Network Analysis](../network-analysis/README.md) 與 [NoSQL：Graph](nosql-foundations.md#graph-database)。

## 模式四：物料清單 (Bill of Materials)

數量要沿路徑相乘，再在外層加總：

```sql
WITH RECURSIVE bom AS (
  SELECT child_component, quantity,
         CAST(quantity AS BIGINT) AS total_quantity, 1 AS level
  FROM component_structure
  WHERE parent_component = 'SUV'

  UNION ALL

  SELECT c.child_component, c.quantity,
         b.total_quantity * c.quantity, b.level + 1
  FROM component_structure AS c
  JOIN bom AS b ON c.parent_component = b.child_component
)
SELECT child_component, SUM(total_quantity) AS total_quantity
FROM bom
GROUP BY child_component
ORDER BY total_quantity DESC;
-- SUV = 1 Engine + 4 Wheel；Engine = 10 Bolt、Wheel = 5 Bolt
-- → Bolt 30 (= 10 + 4×5)、Wheel 4、Engine 1
```

## SQL Server 差異

| 項目 | PostgreSQL / DuckDB / SQLite | SQL Server |
| --- | --- | --- |
| 關鍵字 | `WITH RECURSIVE` | `WITH`（不寫 `RECURSIVE`） |
| 字串串接 | `\|\|` | `+` 或 `CONCAT()` |
| 路徑欄型別 | `VARCHAR` / `TEXT` | anchor 與 recursive 都要 `CAST(... AS NVARCHAR(MAX))`，型別不一致會報錯 |
| 遞迴上限 | 無預設上限 | 預設 100 層，超過報錯；`OPTION (MAXRECURSION 1000)`，`0` 為不限 |

## 實務原則

- 先在 recursive CTE 展開候選集合，`GROUP BY`、排名、篩選放在外層：每一層都能單獨檢查，也容易除錯。
- 同一目的地出現多次不一定是錯：圖中本來就可能有多條路徑。
- 要結果穩定的樹狀順序，依 `path` 排序。
