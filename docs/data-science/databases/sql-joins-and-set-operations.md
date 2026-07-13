# SQL Joins and Set Operations

這篇整理跨資料庫最常用的 join 與 set operation 心智模型。重點不是把所有語法背完，而是先分清楚每一種操作到底回答什麼問題，以及結果列數為什麼會變多、變少或出現 `NULL`。

## 先分兩大類

很多初學者會把 joins 和 `UNION` / `INTERSECT` 混在一起，但它們其實在做不同事情：

- join：把表橫向拼接，增加欄位
- set operation：把結果縱向堆疊或比較，增加或篩掉資料列

如果你腦中先有這條分界，很多查詢選型會清楚很多。

## `INNER JOIN`

`INNER JOIN` 只保留兩邊都有 match 的列。

```sql
SELECT
  p.country,
  p.president,
  pm.prime_minister
FROM presidents AS p
INNER JOIN prime_ministers AS pm
  ON p.country = pm.country;
```

適合情境：

- 你只關心兩邊都存在的實體
- 沒 match 的資料對這次分析沒有價值

心智模型：

- 左表先展開
- 只留下 join condition 成立的列

## `LEFT JOIN`

`LEFT JOIN` 保留左表全部資料，右表只有 match 才補進來，沒 match 就是 `NULL`。

```sql
SELECT
  l.id,
  l.value_left,
  r.value_right
FROM left_table AS l
LEFT JOIN right_table AS r
  ON l.id = r.id;
```

適合情境：

- 左表是主體
- 你想保留所有主體，即使右表缺資料
- 你想找 missing matches

很多分析工作裡，`LEFT JOIN` 比 `RIGHT JOIN` 更常見，因為閱讀方向通常更直觀。

## `RIGHT JOIN`

`RIGHT JOIN` 的邏輯和 `LEFT JOIN` 對稱，只是保留的是右表全部資料。

```sql
SELECT
  l.id,
  l.value_left,
  r.value_right
FROM left_table AS l
RIGHT JOIN right_table AS r
  ON l.id = r.id;
```

實務上常見做法是直接改寫成 `LEFT JOIN`，透過交換表順序讓主表放左邊。  
這通常會比較容易維持閱讀一致性。

## `FULL JOIN`

`FULL JOIN` 可以理解成：

- 左邊全部保留
- 右邊全部保留
- 有 match 的合併成同一列
- 沒 match 的一側用 `NULL` 補空

```sql
SELECT
  COALESCE(l.id, r.id) AS id,
  l.value_left,
  r.value_right
FROM left_table AS l
FULL JOIN right_table AS r
  ON l.id = r.id;
```

也常寫成 `FULL OUTER JOIN`。

適合情境：

- 你想同時找兩邊的 overlap 與 orphan rows
- 資料比對、對帳、雙邊覆蓋率檢查

## `CROSS JOIN`

`CROSS JOIN` 會產生兩表所有可能組合，也就是笛卡兒積。

```sql
SELECT *
FROM table1
CROSS JOIN table2;
```

如果左表有 `m` 列、右表有 `n` 列，結果通常就是 `m * n` 列。

適合情境：

- 真的需要列出所有組合
- 建日曆 × 類別矩陣
- 參數組合展開

如果你不是刻意要做所有組合，`CROSS JOIN` 通常要非常小心。

## `SELF JOIN`

`SELF JOIN` 是同一張表和自己 join。  
重點不是語法難，而是你要先明確區分同一張表的兩個角色。

```sql
SELECT
  child.employee_name,
  parent.employee_name AS manager_name
FROM employees AS child
LEFT JOIN employees AS parent
  ON child.manager_id = parent.employee_id;
```

適合情境：

- 階層資料
- 同表內部對照
- 找前任 / 後任、主管 / 部屬、來源 / 目標

## Multiple Joins

join 不一定只會接兩張表。  
實務上更常見的是一張 fact table 接多張 dimension table。

```sql
SELECT
  a.id,
  b.name,
  c.category
FROM table_a AS a
INNER JOIN table_b AS b
  ON a.b_id = b.id
INNER JOIN table_c AS c
  ON b.c_id = c.id;
```

這時最重要的是：

- 每段 `ON` 都只服務當前那段 join
- alias 要清楚
- 不要讓 join chain 失去方向感

## `ON` vs `USING`

很多 SQL dialect 都支援兩種寫法。

### `ON`

```sql
SELECT *
FROM presidents AS p
JOIN prime_ministers AS pm
  ON p.country = pm.country;
```

優點：

- 最明確
- 不怕兩邊欄位名不同
- 可讀性通常最好

### `USING`

```sql
SELECT *
FROM presidents
JOIN prime_ministers
  USING (country);
```

適合在兩邊欄位名稱完全一致時使用。  
如果 schema 很穩定，`USING` 很精簡；但如果你想強調左右表角色，`ON` 通常比較直觀。

## Join on More Than One Field

有些資料不是只靠單一 key 對齊，而是要多欄位一起對。

```sql
SELECT *
FROM left_table AS l
INNER JOIN right_table AS r
  ON l.id = r.id
 AND l.event_date = r.event_date;
```

這通常發生在：

- entity + date
- country + year
- user_id + session_id

如果少一個條件就會誤配，就不要只 join 單欄。

## `UNION`

`UNION` 是把兩個結果上下合併，並自動去重。

```sql
SELECT country
FROM presidents
UNION
SELECT country
FROM prime_ministers;
```

前提通常是：

- 欄位數相同
- 對應欄位型別相容

心智模型：

- 先 append
- 再 deduplicate

## `UNION ALL`

`UNION ALL` 也會上下合併，但不去重。

```sql
SELECT country
FROM presidents
UNION ALL
SELECT country
FROM prime_ministers;
```

適合情境：

- 你真的要保留重複列
- 你知道來源彼此本來就可重複
- 想避免 `UNION` 的去重成本

簡單記法：

- `UNION`: 合併後去重
- `UNION ALL`: 合併後原樣保留

## `INTERSECT`

`INTERSECT` 只保留兩個結果集共同擁有的列。

```sql
SELECT country
FROM presidents
INTERSECT
SELECT country
FROM prime_ministers;
```

這比較像集合交集，而不是 join 出更多欄位。

它和 `INNER JOIN` 的差別要記清楚：

- `INTERSECT` 比的是兩個結果集中的整列值
- `INNER JOIN` 比的是 join condition，並且通常會把欄位拼接起來

## Semi Join

semi join 的核心問題是：

- 左表中，哪些列在右表有對應存在

它通常不需要把右表欄位真正 select 出來，只需要知道「有沒有 match」。

常見寫法是 `EXISTS`：

```sql
SELECT *
FROM countries AS c
WHERE EXISTS (
  SELECT 1
  FROM economies AS e
  WHERE e.country = c.country
);
```

也可以用 `IN (...)` 形成類似效果。

semi join 的特色：

- 只回傳左表列
- 右表只負責判斷存在性

## Anti Join

anti join 問的是相反的問題：

- 左表中，哪些列在右表完全找不到 match

常見寫法是 `NOT EXISTS`：

```sql
SELECT *
FROM countries AS c
WHERE NOT EXISTS (
  SELECT 1
  FROM economies AS e
  WHERE e.country = c.country
);
```

這在資料品質檢查、缺漏名單、未對齊資料找尋上非常常見。

## When to Use Join vs. Subquery

如果你需要：

- 把右表欄位真的帶進結果

通常先想 join。

如果你只需要：

- 判斷有沒有存在
- 判斷是否缺席

通常先想 `EXISTS` / `NOT EXISTS` 這種 semi / anti join 寫法。

## Practical Reminders

- `INNER JOIN` 適合只保留 match。
- `LEFT JOIN` 適合保留主表並觀察缺漏。
- `RIGHT JOIN` 常可改寫成 `LEFT JOIN`。
- `FULL JOIN` 很適合做雙邊對帳。
- `CROSS JOIN` 前先估列數膨脹。
- `SELF JOIN` 的關鍵是 alias 與角色命名。
- `UNION` 會去重，`UNION ALL` 不會。
- `INTERSECT` 是集合交集，不是欄位拼接。
- 只想檢查存在性時，先想 `EXISTS` / `NOT EXISTS`。

[Back to Databases](README.md)
