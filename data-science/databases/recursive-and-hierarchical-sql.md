# Recursive and Hierarchical SQL

這篇整理遞迴 CTE 與階層式 SQL 查詢的實用模式。這類查詢最適合處理「一筆資料會再指向另一筆同型資料」的問題，例如組織樹、分類樹、族譜、零件結構、路線展開與多層相依關係。

## 適合處理的問題

- 給定主管，找出所有下屬
- 計算每個節點位於第幾層
- 把祖先路徑或分類路徑串成單一欄位
- 展開多段路徑，像是轉機航線或多跳 graph traversal
- 拆解 bill of materials，計算產品由哪些零件組成

## Recursive CTE Mental Model

recursive CTE 通常由兩段查詢組成：

- anchor member: 定義起點
- recursive member: 定義如何從上一層走到下一層

常見骨架如下：

```sql
WITH RECURSIVE cte_name AS (
  SELECT ...
  FROM ...
  WHERE ... -- anchor member

  UNION ALL

  SELECT ...
  FROM some_table AS t
  JOIN cte_name AS c
    ON ...
  WHERE ... -- recursive member and termination rule
)
SELECT *
FROM cte_name;
```

如果是 SQL Server，語法不寫 `RECURSIVE`，但心智模型相同：

```sql
WITH cte_name AS (
  SELECT ...
  FROM ...
  WHERE ...

  UNION ALL

  SELECT ...
  FROM some_table AS t
  JOIN cte_name AS c
    ON ...
  WHERE ...
)
SELECT *
FROM cte_name
OPTION (MAXRECURSION 32767);
```

## 使用遞迴 CTE 時要先檢查

- anchor member 與 recursive member 的欄位數必須一致
- 對應欄位的資料型別必須相容
- 一定要有終止條件，不然容易無限遞迴
- 如果資料可能有 cycle，最好加上 path 檢查或層數上限
- SQL Server 預設遞迴層數有限，深層查詢常要加 `OPTION (MAXRECURSION n)`

實務上，最常見的終止方式有兩種：

- 結構自然走到底，例如某節點沒有子節點
- 額外設上限，例如 `level < 5` 或 `stops < 3`

## 階層資料最常見的表結構

最常見的是 adjacency list，也就是每筆資料用一個 parent 欄位指向上層：

```sql
CREATE TABLE employee (
  id int PRIMARY KEY,
  name nvarchar(100),
  supervisor_id int
);
```

這種模型容易寫入，也容易和 recursive CTE 搭配。

## Pattern 1: 展開整棵階層樹

這是最基本的 descendant expansion。從根節點出發，一路找到所有子節點。

```sql
WITH hierarchy AS (
  SELECT id, supervisor_id
  FROM employee
  WHERE supervisor_id = 0

  UNION ALL

  SELECT e.id, e.supervisor_id
  FROM employee AS e
  JOIN hierarchy AS h
    ON e.supervisor_id = h.id
)
SELECT *
FROM hierarchy;
```

這個模式常用在：

- 部門組織樹
- 分類樹
- 留言回覆樹
- 檔案夾樹狀結構

## Pattern 2: 計算層級

很多分析問題不只要知道有哪些節點，也要知道每個節點在第幾層。

```sql
WITH hierarchy AS (
  SELECT id, supervisor_id, 1 AS level
  FROM employee
  WHERE supervisor_id = 0

  UNION ALL

  SELECT e.id, e.supervisor_id, h.level + 1
  FROM employee AS e
  JOIN hierarchy AS h
    ON e.supervisor_id = h.id
)
SELECT *
FROM hierarchy
ORDER BY level, id;
```

`level` 很重要，因為後續常會拿它做：

- 階層深度分析
- 限制遞迴深度
- 排版 tree view
- 計算世代數、管理層級或零件層數

## Pattern 3: 把路徑串成單一欄位

如果想知道某節點是沿著哪條路徑走到的，可以在遞迴過程中累積 path。

```sql
WITH hierarchy AS (
  SELECT
    id,
    supervisor_id,
    CAST(id AS varchar(max)) AS path
  FROM employee
  WHERE supervisor_id = 0

  UNION ALL

  SELECT
    e.id,
    e.supervisor_id,
    CAST(h.path + ' -> ' + CAST(e.id AS varchar(max)) AS varchar(max)) AS path
  FROM employee AS e
  JOIN hierarchy AS h
    ON e.supervisor_id = h.id
)
SELECT *
FROM hierarchy;
```

這種寫法適合：

- 顯示完整祖先鏈
- 建立 breadcrumb
- 偵測 cycle
- 產生可讀的 traversal log

如果需要追蹤名稱而不是 id，也可以改成串接 `name`。

## Pattern 4: 展開多段路徑

recursive CTE 不只能查樹，也可以查 graph 上的多跳路徑。典型例子是航線、物流節點或 network traversal。

```sql
WITH flight_route AS (
  SELECT
    departure,
    arrival,
    0 AS stops,
    cost AS total_cost,
    CAST(departure + ' -> ' + arrival AS nvarchar(max)) AS route
  FROM flight_plan
  WHERE departure = 'New York'

  UNION ALL

  SELECT
    r.departure,
    f.arrival,
    r.stops + 1,
    r.total_cost + f.cost,
    CAST(r.route + ' -> ' + f.arrival AS nvarchar(max)) AS route
  FROM flight_route AS r
  JOIN flight_plan AS f
    ON r.arrival = f.departure
  WHERE r.stops < 3
)
SELECT *
FROM flight_route;
```

這個模式的重點是把「狀態」一起往下傳：

- 目前停靠數 `stops`
- 累積成本 `total_cost`
- 已走過的路徑 `route`

一旦把狀態放進 recursive member，就能回答更進一步的問題。

### Example: 找成本上限內的路線

```sql
WITH flight_route AS (
  SELECT
    departure,
    arrival,
    0 AS stops,
    cost AS total_cost,
    CAST(departure + ' -> ' + arrival AS nvarchar(max)) AS route
  FROM flight_plan
  WHERE departure = 'New York'

  UNION ALL

  SELECT
    r.departure,
    f.arrival,
    r.stops + 1,
    r.total_cost + f.cost,
    CAST(r.route + ' -> ' + f.arrival AS nvarchar(max)) AS route
  FROM flight_route AS r
  JOIN flight_plan AS f
    ON r.arrival = f.departure
  WHERE r.stops < 3
)
SELECT departure, arrival, total_cost, route
FROM flight_route
WHERE total_cost <= 500
ORDER BY total_cost;
```

### Example: 找每個目的地最便宜的路線

先展開所有可能路徑，再做彙總，通常比試圖在 recursive member 裡直接求最小值更穩。

```sql
WITH flight_route AS (
  SELECT
    departure,
    arrival,
    0 AS stops,
    cost AS total_cost,
    CAST(departure + ' -> ' + arrival AS nvarchar(max)) AS route
  FROM flight_plan
  WHERE departure = 'New York'

  UNION ALL

  SELECT
    r.departure,
    f.arrival,
    r.stops + 1,
    r.total_cost + f.cost,
    CAST(r.route + ' -> ' + f.arrival AS nvarchar(max)) AS route
  FROM flight_route AS r
  JOIN flight_plan AS f
    ON r.arrival = f.departure
  WHERE r.stops < 3
)
SELECT arrival, MIN(total_cost) AS cheapest_cost
FROM flight_route
GROUP BY arrival
ORDER BY cheapest_cost;
```

## Pattern 5: Bill of Materials

零件結構是另一個很典型的階層模型。每個 component 會再由多個子零件組成。

```sql
CREATE TABLE component_structure (
  parent_component nvarchar(100),
  child_component nvarchar(100),
  quantity int
);
```

如果要問「一台 SUV 有哪些層級的零件」，就可以把根產品當 anchor，逐層往下展開。

```sql
WITH bom AS (
  SELECT
    parent_component,
    child_component,
    quantity,
    1 AS level
  FROM component_structure
  WHERE parent_component = 'SUV'

  UNION ALL

  SELECT
    c.parent_component,
    c.child_component,
    c.quantity,
    b.level + 1
  FROM component_structure AS c
  JOIN bom AS b
    ON c.parent_component = b.child_component
)
SELECT child_component, level, quantity
FROM bom
ORDER BY level, child_component;
```

如果每層 quantity 需要相乘，則要把累積數量一起往下傳：

```sql
WITH bom AS (
  SELECT
    parent_component,
    child_component,
    quantity,
    CAST(quantity AS bigint) AS total_quantity
  FROM component_structure
  WHERE parent_component = 'SUV'

  UNION ALL

  SELECT
    c.parent_component,
    c.child_component,
    c.quantity,
    b.total_quantity * c.quantity
  FROM component_structure AS c
  JOIN bom AS b
    ON c.parent_component = b.child_component
)
SELECT
  child_component,
  SUM(total_quantity) AS total_quantity
FROM bom
GROUP BY child_component
ORDER BY total_quantity DESC, child_component;
```

這種寫法很適合回答：

- 做一個成品總共需要多少零件
- 哪些零件在多條子路徑上重複出現
- 哪些零件是最上層、最底層或中間組件

## 常見陷阱

### Cycle

如果 `A -> B -> C -> A` 形成環，遞迴就可能無限展開。最保守的做法是：

- 限制最大層數
- 在 path 中檢查新節點是否已出現

### Duplicate Paths

在 graph 型資料中，同一目的地可能由多條不同路徑抵達。  
所以 `arrival` 重複不一定是錯誤，而是代表路徑空間本來就不只一種。

### 把太多邏輯塞進 Recursive Member

通常比較穩的做法是：

1. 先用 recursive CTE 展開候選集合
2. 再在外層查詢做 `GROUP BY`、排名、篩選或報表整理

這樣比較容易 debug，也比較容易驗證每一層輸出是否合理。

## 實務心法

- 遞迴查詢的本質是「定義起點」與「定義下一步」
- 如果問題聽起來像「從某節點一路往下或往上找」，通常可以先試 recursive CTE
- `level`、`path`、累積數量、累積成本，都是很常見的狀態欄位
- 對樹狀資料，`parent_id` 模型通常已經夠用
- 對多跳圖狀資料，務必先想好去重、成本、終止條件與 cycle 保護
