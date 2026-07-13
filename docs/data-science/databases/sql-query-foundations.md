# SQL Query Foundations

這篇整理跨資料庫都很常用的 SQL 基礎心智模型。它不是要取代各家資料庫語法速查，而是把最容易混淆、卻又最常出錯的查詢觀念先釐清，例如 `COUNT(*)` 與 `COUNT(col)` 的差別、`WHERE` 跟 `HAVING` 的邏輯、`LIMIT` 與 `ORDER BY` 的搭配方式，以及查詢的實際執行順序。

## 適合補強的問題

- `COUNT(*)`、`COUNT(col)`、`COUNT(DISTINCT col)` 到底差在哪裡
- `WHERE`、`GROUP BY`、`HAVING`、`ORDER BY` 分別在做什麼
- 為什麼 `SELECT` 裡的 alias 不能直接在 `WHERE` 用
- `LIKE`、`BETWEEN`、`IN`、`IS NULL` 什麼時候最適合
- 為什麼沒有 `ORDER BY` 的 `LIMIT` 常不夠穩

## Query Execution Mental Model

SQL 寫出來的順序，不等於資料庫實際處理的順序。

最常見的心智模型可以先記成：

1. `FROM`
2. `WHERE`
3. `GROUP BY`
4. `HAVING`
5. `SELECT`
6. `ORDER BY`
7. `LIMIT` / `OFFSET`

這個順序很重要，因為很多語法錯誤其實都是執行順序造成的。

### Alias 為什麼不能直接在 `WHERE` 用

```sql
SELECT
  budget AS max_budget
FROM films
WHERE max_budget IS NOT NULL;
```

這種寫法通常會失敗，因為 `WHERE` 發生在 `SELECT` 之前，alias 還沒被定義。

比較穩的做法有兩種：

```sql
SELECT
  budget AS max_budget
FROM films
WHERE budget IS NOT NULL;
```

或是先包成子查詢：

```sql
SELECT *
FROM (
  SELECT budget AS max_budget
  FROM films
) AS t
WHERE max_budget IS NOT NULL;
```

## `COUNT(*)`、`COUNT(col)`、`COUNT(DISTINCT col)`

這三者是最常被混用的統計工具。

### `COUNT(*)`

```sql
SELECT COUNT(*) AS total_rows
FROM people;
```

`COUNT(*)` 會計算資料列數，不管欄位是不是 `NULL`。

### `COUNT(col)`

```sql
SELECT COUNT(birthdate) AS known_birthdates
FROM people;
```

`COUNT(col)` 只會計算該欄位非 `NULL` 的列。

這表示：

- `COUNT(*)` 看的是總列數
- `COUNT(col)` 看的是該欄位有值的列數

如果你在做資料完整性檢查，這個差異非常重要。

### `COUNT(DISTINCT col)`

```sql
SELECT COUNT(DISTINCT birthdate) AS unique_birthdates
FROM people;
```

這會先去重，再計數。  
適合回答：

- 有多少不同使用者
- 有多少不同國家
- 有多少不同日期

心智模型上可以記成：

- `COUNT(*)`: 數列
- `COUNT(col)`: 數非空值
- `COUNT(DISTINCT col)`: 數不重複的非空值

## `DISTINCT`

如果只想列出不重複值，可以直接用：

```sql
SELECT DISTINCT language
FROM films
ORDER BY language;
```

`DISTINCT` 很適合探索類別欄位，但也要小心：

- `DISTINCT` 是對整列結果去重，不只是單欄語意問題
- 如果欄位很多，去重成本會上升

### `DISTINCT` on Multiple Columns

```sql
SELECT DISTINCT dept_id, year_hired
FROM employees;
```

這不是分別對 `dept_id` 和 `year_hired` 各自去重，  
而是只保留 `(dept_id, year_hired)` 組合不重複的列。

所以心智模型要記成：

- `DISTINCT col`: 看單欄唯一值
- `DISTINCT col1, col2`: 看欄位組合的唯一值

## `LIMIT` 要搭配 `ORDER BY`

```sql
SELECT title
FROM films
ORDER BY release_year DESC
LIMIT 10;
```

`LIMIT` 只負責裁掉結果數量，不保證回傳的是哪 10 筆。  
如果沒有 `ORDER BY`，得到的前 10 筆通常沒有穩定意義。

所以實務上：

- `LIMIT` 適合預覽資料
- `ORDER BY + LIMIT` 適合找 top N / latest N / cheapest N

如果你在 SQL Server 類語境裡，常見寫法會是：

```sql
SELECT TOP (10) title
FROM films
ORDER BY release_year DESC;
```

概念上和 `ORDER BY ... LIMIT 10` 很接近，只是語法位置不同。

## `WHERE`: 過濾原始資料列

`WHERE` 用來過濾尚未分組的個別記錄。

### Comparison operators

```sql
SELECT title
FROM films
WHERE release_year > 1960;
```

### `BETWEEN`

```sql
SELECT title
FROM films
WHERE release_year BETWEEN 1994 AND 2000;
```

`BETWEEN a AND b` 通常表示含頭含尾的區間。  
如果你很在意邊界，寫查詢時要明確記得這件事。

### `AND` / `OR`

```sql
SELECT *
FROM coats
WHERE color = 'yellow' OR length = 'short';

SELECT *
FROM coats
WHERE color = 'yellow' AND length = 'short';
```

可以先這樣記：

- `OR`: 滿足至少一個條件
- `AND`: 必須同時滿足所有條件

### `IN`

```sql
SELECT title
FROM films
WHERE certification IN ('G', 'PG', 'PG-13');
```

如果是「值在幾個固定選項中」，`IN` 往往比連續寫多個 `OR` 更清楚。

### `LIKE` / `NOT LIKE`

```sql
SELECT name
FROM people
WHERE name LIKE 'Ade%';

SELECT name
FROM people
WHERE name LIKE 'Ev_';

SELECT name
FROM people
WHERE name NOT LIKE 'A.%';
```

常見 wildcard：

- `%`: 任意長度字串
- `_`: 單一字元

## `NULL` 的基本觀念

`NULL` 代表缺失、未知或不可用，不等於空字串，也不等於 0。

### 篩選缺失值

```sql
SELECT *
FROM films
WHERE budget IS NULL;
```

### 篩選非缺失值

```sql
SELECT *
FROM films
WHERE budget IS NOT NULL;
```

不要寫成：

```sql
WHERE budget = NULL
```

這通常不會得到你想要的結果。

### `NULL` 與計數

這裡再提醒一次：

- `COUNT(col)` 不算 `NULL`
- `COUNT(*)` 會算資料列，即使該欄位是 `NULL`

## Aggregate Functions

最常用的聚合函數包括：

- `AVG()`
- `SUM()`
- `MIN()`
- `MAX()`
- `COUNT()`

例如：

```sql
SELECT
  AVG(budget) AS avg_budget,
  SUM(budget) AS total_budget,
  MIN(budget) AS min_budget,
  MAX(budget) AS max_budget
FROM films
WHERE release_year >= 2010;
```

聚合函數最適合把很多列壓縮成可解讀的摘要指標。

## `ROUND()`

聚合結果常會有很多小數位，這時可用 `ROUND()`：

```sql
SELECT ROUND(AVG(budget), 2) AS avg_budget
FROM films
WHERE release_year >= 2010;
```

如果要四捨五入到整數：

```sql
SELECT ROUND(AVG(budget), 0) AS avg_budget
FROM films
WHERE release_year >= 2010;
```

`ROUND()` 很常用在：

- 報表展示
- 單位經濟指標
- 比率與平均值輸出

## `GROUP BY`: 先分組，再聚合

如果沒有 `GROUP BY`，聚合通常是對全表做一次。  
如果想看每個類別各自的統計，就需要分組。

```sql
SELECT
  certification,
  COUNT(title) AS title_count
FROM films
GROUP BY certification;
```

這種寫法的核心是：

- 先依 `certification` 分群
- 再對每一群做 `COUNT(title)`

### 多欄分組

```sql
SELECT
  certification,
  language,
  COUNT(title) AS title_count
FROM films
GROUP BY certification, language;
```

分組欄位越多，群組通常越細。

## `ORDER BY`

### 單欄排序

```sql
SELECT title, budget
FROM films
WHERE budget IS NOT NULL
ORDER BY budget DESC;
```

### 多欄排序

```sql
SELECT title, wins, imdb_score
FROM films
ORDER BY wins DESC, imdb_score DESC;
```

第二個欄位可以當第一個欄位同分時的 tie-breaker。

### `GROUP BY` 後再排序

```sql
SELECT
  certification,
  COUNT(title) AS title_count
FROM films
GROUP BY certification
ORDER BY title_count DESC;
```

這是很常見的摘要報表模式。

## `HAVING`: 過濾已分組的結果

`WHERE` 過濾個別列，`HAVING` 過濾分組後的結果。

### 錯誤示範

```sql
SELECT
  release_year,
  COUNT(title) AS title_count
FROM films
GROUP BY release_year
WHERE COUNT(title) > 10;
```

這會報錯，因為聚合條件不應放在 `WHERE`。

### 正確寫法

```sql
SELECT
  release_year,
  COUNT(title) AS title_count
FROM films
GROUP BY release_year
HAVING COUNT(title) > 10;
```

### `HAVING` vs `WHERE`

```sql
SELECT title
FROM films
WHERE release_year = 2000;
```

這是在問「哪些影片是 2000 年上映」，所以用 `WHERE`。

```sql
SELECT release_year
FROM films
GROUP BY release_year
HAVING AVG(duration) > 120;
```

這是在問「哪些年份的平均片長超過兩小時」，所以要先分組、再用 `HAVING` 篩。

可以把差別記成：

- `WHERE`: filter rows
- `HAVING`: filter groups

## 一個完整的摘要查詢骨架

```sql
SELECT
  certification,
  COUNT(title) AS title_count
FROM films
WHERE certification IN ('G', 'PG', 'PG-13')
GROUP BY certification
HAVING COUNT(title) > 500
ORDER BY title_count DESC
LIMIT 3;
```

這個模式很值得熟記，因為很多實務查詢都只是把這個骨架換成自己的欄位與條件。

## 實務心法

- 先分清楚你是在過濾列，還是在過濾群組
- `COUNT(*)`、`COUNT(col)`、`COUNT(DISTINCT col)` 不要混用
- `LIMIT` 如果沒有 `ORDER BY`，通常只是抽樣，不是穩定排序結果
- alias 不能在 `WHERE` 用，先回想 query execution order
- 查詢一旦開始複雜，先把問題翻成：資料從哪來、先怎麼過濾、怎麼分組、最後怎麼排序
