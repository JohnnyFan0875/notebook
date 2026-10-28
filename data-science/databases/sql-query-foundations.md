[Data Science](../README.md) › [Databases](README.md) › SQL 查詢基礎

# SQL 查詢基礎 (SQL Query Foundations)

跨資料庫通用的查詢心智模型：子句的執行順序、過濾列與過濾群組的差別、三種 `COUNT`，以及 `NULL` 造成的意外。方言差異（`TOP` / `LIMIT`、日期函式）見 [SQL 方言速查](sql-dialect-cheatsheet.md)。

## 執行順序

SQL 寫的順序不等於邏輯處理順序。多數語法錯誤（alias 不能用、聚合不能放 `WHERE`）都來自這裡。

| 邏輯順序 | 子句 | 作用 | 這一步能用 `SELECT` alias？ |
| --- | --- | --- | --- |
| 1 | `FROM` / `JOIN` | 決定資料來源、合併表 | 否 |
| 2 | `WHERE` | 過濾**個別列** | 否 |
| 3 | `GROUP BY` | 分組 | 多數否（PostgreSQL、MySQL、DuckDB 允許） |
| 4 | `HAVING` | 過濾**群組** | 多數否 |
| 5 | `SELECT` | 計算欄位、命名 alias；window function 在這裡算 | — |
| 6 | `DISTINCT` | 去重 | — |
| 7 | `ORDER BY` | 排序 | 是 |
| 8 | `LIMIT` / `OFFSET` / `FETCH` | 截取 | — |

```sql
-- 錯：WHERE 在 SELECT 之前，alias 還不存在
SELECT budget / 1e6 AS budget_m FROM films WHERE budget_m > 100;

-- 對 1：在 WHERE 重寫運算式
SELECT budget / 1e6 AS budget_m FROM films WHERE budget / 1e6 > 100;

-- 對 2：先包成子查詢或 CTE，外層再過濾
WITH f AS (SELECT title, budget / 1e6 AS budget_m FROM films)
SELECT * FROM f WHERE budget_m > 100;
```

## 完整骨架

```sql
SELECT
  certification,
  COUNT(*)                 AS n_films,
  ROUND(AVG(duration), 1)  AS avg_duration
FROM films
WHERE release_year >= 2000                 -- 1. 先過濾列
  AND certification IN ('G', 'PG', 'PG-13')
GROUP BY certification                     -- 2. 分組
HAVING COUNT(*) > 500                      -- 3. 過濾群組（聚合條件只能放這裡）
ORDER BY n_films DESC                      -- 4. 排序（可用 alias）
LIMIT 3;                                   -- 5. 取前 3；SQL Server 用 SELECT TOP (3)
```

| 子句 | 規則 |
| --- | --- |
| `GROUP BY` | `SELECT` 裡非聚合的欄位都必須出現在 `GROUP BY`（MySQL 舊模式不檢查，會回傳任意值） |
| `HAVING` vs `WHERE` | `WHERE` 過濾列（「2000 年的電影」）；`HAVING` 過濾群組（「平均片長 > 120 分鐘的年份」） |
| `ORDER BY` | 多欄排序時第二欄是同分的 tie-breaker；每欄可各自 `ASC` / `DESC` |
| `LIMIT` | 沒有 `ORDER BY` 時回傳哪幾列沒有保證，只適合預覽；top-N 一定要排序 |
| `DISTINCT a, b` | 對**欄位組合**去重，不是各欄分別去重 |

## 過濾條件

| 運算子 | 例子 | 注意 |
| --- | --- | --- |
| 比較 | `release_year > 1960` | |
| `BETWEEN` | `release_year BETWEEN 1994 AND 2000` | **含頭含尾**；時間戳用 `>= '2024-01-01' AND < '2024-02-01'` 才不會漏掉月底當天的時間 |
| `IN` | `certification IN ('G', 'PG')` | 比多個 `OR` 清楚 |
| `LIKE` | `name LIKE 'Ade%'`、`'Ev_'` | `%` 任意長度、`_` 單一字元；開頭是 `%` 無法用一般 index |
| `IS NULL` | `budget IS NULL` | 不能寫 `= NULL` |
| `AND` / `OR` | `a = 1 AND (b = 2 OR c = 3)` | `AND` 優先於 `OR`，混用時**一定加括號** |

## 聚合與 `COUNT`

```sql
SELECT
  COUNT(*)                 AS n_rows,          -- 列數，不管 NULL
  COUNT(birthdate)         AS n_known,         -- 該欄非 NULL 的列數
  COUNT(DISTINCT birthdate) AS n_unique,       -- 不重複的非 NULL 值
  AVG(budget), SUM(budget), MIN(budget), MAX(budget),
  ROUND(AVG(budget), 2)    AS avg_budget_2dp
FROM people;
```

| 函式 | 對 `NULL` 的處理 |
| --- | --- |
| `COUNT(*)` | 計入 |
| `COUNT(col)`、`SUM`、`AVG`、`MIN`、`MAX` | **忽略**；`AVG` 的分母是非 NULL 的列數 |
| 全部是 `NULL` 或沒有列 | `SUM` / `AVG` 回傳 `NULL`（不是 0）；`COUNT` 回傳 0 |

`COUNT(*) - COUNT(col)` 就是該欄缺值數，是資料完整性檢查的第一步。

## `NULL`：三值邏輯

`NULL` 表示未知，不是 0 也不是空字串。任何與 `NULL` 的比較結果都是 `UNKNOWN`，而 `WHERE` 只保留 `TRUE` 的列。

| 運算式 | 結果 |
| --- | --- |
| `NULL = NULL` | `UNKNOWN`（所以要用 `IS NULL`） |
| `NULL <> 'x'` | `UNKNOWN` |
| `TRUE AND NULL` / `FALSE AND NULL` | `UNKNOWN` / `FALSE` |
| `TRUE OR NULL` / `FALSE OR NULL` | `TRUE` / `UNKNOWN` |
| `NULL + 1`、`'a' \|\| NULL` | `NULL`（SQL Server `+` 串接也是；Oracle 例外，`\|\|` 把 NULL 當空字串） |

| 陷阱 | 例子 | 改法 |
| --- | --- | --- |
| `<>` 會排除 NULL | `WHERE status <> 'done'` 不回傳 `status IS NULL` 的列 | `WHERE status <> 'done' OR status IS NULL`；PostgreSQL / DuckDB 可用 `status IS DISTINCT FROM 'done'` |
| `NOT IN` 子查詢含 NULL | `WHERE id NOT IN (SELECT id FROM b)`，`b.id` 只要有一個 NULL，結果就是**空的** | 改用 `NOT EXISTS`（見 [anti join](sql-joins-and-set-operations.md#semi-join-與-anti-join)） |
| 平均值偏誤 | `AVG(score)` 只平均有值的列 | 先確認缺值比例與缺失機制（見 [缺失機制](../data-manipulation-and-eda/missing-data.md)） |
| 填補 | `COALESCE(x, 0)` | 只在 `NULL` 確實代表 0 時才用 |

## SQL ↔ pandas ↔ dplyr 對照

| SQL | pandas | dplyr |
| --- | --- | --- |
| `SELECT a, b` | `df[["a", "b"]]` | `select(a, b)` |
| `WHERE x > 1` | `df[df.x > 1]` / `df.query("x > 1")` | `filter(x > 1)` |
| `SELECT a * 2 AS a2` | `df.assign(a2=df.a * 2)` | `mutate(a2 = a * 2)` |
| `GROUP BY g` + 聚合 | `df.groupby("g").agg(n=("x", "size"))` | `group_by(g) \|> summarise(n = n())` |
| `HAVING COUNT(*) > 5` | 聚合後再篩選 | `filter(n > 5)`（在 `summarise` 之後） |
| `ORDER BY x DESC LIMIT 5` | `df.nlargest(5, "x")` | `slice_max(x, n = 5)` |
| `COUNT(DISTINCT x)` | `df.x.nunique()` | `n_distinct(x)` |
| `x IS NULL` | `df.x.isna()` | `is.na(x)` |

> 差別在 `NULL`：pandas 的 `groupby` 預設丟掉 key 為 NaN 的群組（`dropna=False` 保留），SQL 與 dplyr 則把 `NULL` / `NA` 當成一組。

pandas 細節見 [groupby](../python-foundations/pandas/groupby.md)；dplyr 見 [Tidyverse 工作流](../r-foundations/tidyverse-workflow.md)。
