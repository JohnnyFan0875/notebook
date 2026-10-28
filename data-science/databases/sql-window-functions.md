# SQL Window Functions

Window function 在**保留明細列**的同時算出排名、前後列比較、running total、moving average。語法在 PostgreSQL、SQL Server、Snowflake、BigQuery 大致相同；範例以 PostgreSQL 為主，PostgreSQL 專屬的 `CROSSTAB` pivot 放在最後一節。

## Why Window Functions Matter

`GROUP BY` 會把多列壓成摘要。  
window function 則是在不丟掉原始列的前提下，把群組或排序後的計算結果附回每一列。

很常見的需求：

- 找前一列或下一列
- 分組排名
- running total
- moving average
- 取每組第一筆或最後一筆
- 把資料切成幾個 bucket

## 什麼時候值得用 window function

- 想在每一列旁邊放上年度總額、群組平均值或累積值
- 想做 running total
- 想看前一列 / 下一列的值
- 想在每個群組內做排名或編號
- 想看某個視窗的第一個值、最後一個值

## `GROUP BY` vs Window Function

如果你不確定該用哪個，可以先問自己：

- 我最後還需要保留每一列明細嗎

如果答案是：

- `否`：通常先想 `GROUP BY`
- `是`：通常先想 window function

## The Basic `OVER` Pattern

window function 的核心骨架通常是：

```sql
SELECT
    col_a,
    col_b,
    some_window_function(...) OVER (
        PARTITION BY ...
        ORDER BY ...
    ) AS result_col
FROM some_table;
```

可以先這樣理解：

- `PARTITION BY`：先分組，但不會像 `GROUP BY` 一樣壓扁資料
- `ORDER BY`：決定 window 內的順序
- frame：決定目前這一列實際看得到哪些列

如果沒有 `PARTITION BY`，通常表示整份結果就是同一個 window。

## Numbering and Ranking

### `ROW_NUMBER()`

最直接的用途是替排序後的資料編號。

```sql
SELECT
    year,
    athlete,
    ROW_NUMBER() OVER (ORDER BY year DESC) AS row_n
FROM results;
```

常用在：

- 每組挑一筆代表列
- top-N per group
- 先編號再做 paging

如果加上 `PARTITION BY`，編號會在每個分組內重新開始。

```sql
SELECT
    country,
    athlete,
    ROW_NUMBER() OVER (
        PARTITION BY country
        ORDER BY medals DESC
    ) AS medal_rank_in_country
FROM athlete_medals;
```

### `RANK()` vs. `DENSE_RANK()`

- `RANK()`：遇到 ties 會跳號
- `DENSE_RANK()`：遇到 ties 不跳號

```sql
SELECT
    country,
    medals,
    RANK() OVER (ORDER BY medals DESC) AS rank_n,
    DENSE_RANK() OVER (ORDER BY medals DESC) AS dense_rank_n
FROM medal_totals;
```

如果你的問題是「並列第一之後下一名算第三名還是第二名」，本質上就是在選 `RANK()` 還是 `DENSE_RANK()`。

## Relative Row Access

### `LAG()` and `LEAD()`

- `LAG(col, n)`：看前 `n` 列
- `LEAD(col, n)`：看後 `n` 列

```sql
SELECT
    year,
    champion,
    LAG(champion, 1) OVER (ORDER BY year) AS last_champion,
    LEAD(champion, 1) OVER (ORDER BY year) AS next_champion
FROM champions;
```

這兩個函數很適合：

- 年對年比較
- 判斷是否連霸
- 比較目前值與上一期值

### 常見延伸：直接算變化量

```sql
SELECT
  SalesPerson,
  SalesYear,
  CurrentQuota,
  CurrentQuota
  - LAG(CurrentQuota) OVER (PARTITION BY SalesYear ORDER BY ModifiedDate) AS quota_change
FROM SaleGoal;
```

## First and Last Value

### `FIRST_VALUE()`

```sql
SELECT
    year,
    city,
    FIRST_VALUE(city) OVER (ORDER BY year) AS first_host_city
FROM hosts;
```

它常用來回答「這個 partition 的第一筆是什麼」。

### `LAST_VALUE()` Needs a Frame

`LAST_VALUE()` 是很容易踩坑的函數。  
如果不明確指定 frame，很多時候你拿到的其實只是「目前這列的值」，不是整個 partition 的最後值。

```sql
SELECT
    year,
    city,
    LAST_VALUE(city) OVER (
        ORDER BY year
        RANGE BETWEEN UNBOUNDED PRECEDING
              AND UNBOUNDED FOLLOWING
    ) AS last_host_city
FROM hosts;
```

先記住這個心智模型：

- 預設 frame 常只看到從開頭到目前列
- 想拿整個 partition 的最後值時，通常要把 frame 明確延伸到 `UNBOUNDED FOLLOWING`

## Aggregate Window Functions

一般 aggregate：

```sql
SELECT year, SUM(medals) AS medals
FROM country_medals
GROUP BY year;
```

aggregate window 版本：

```sql
SELECT
    year,
    medals,
    SUM(medals) OVER (ORDER BY year) AS medals_rt
FROM country_medals;
```

差別在於：

- `GROUP BY`：只保留摘要列
- `SUM(...) OVER (...)`：保留每一列，同時附上累積值

常見用途：

- `SUM(...) OVER (...)`：running total
- `AVG(...) OVER (...)`：moving average
- `MAX(...) OVER (...)`：rolling max 或 cumulative max

## Standard Deviation over a Window

window function 不只拿來做加總與排名，也能做更進階的統計。

```sql
SELECT
  SalesPerson,
  SalesYear,
  CurrentQuota,
  STDEV(CurrentQuota) OVER () AS standard_dev
FROM SaleGoal;
```

也可以限制在每個 partition 內：

```sql
SELECT
  SalesPerson,
  SalesYear,
  CurrentQuota,
  STDEV(CurrentQuota)
    OVER (PARTITION BY SalesYear ORDER BY SalesYear) AS stdev_by_year
FROM SaleGoal;
```

這類寫法適合拿來做：

- 群組內波動程度
- 每期數值的分散程度
- 變異度快速檢查

## Frames: Which Rows Are Visible

frame 會決定目前這列在做 window 計算時，到底能看到哪幾列。

常見寫法：

```sql
ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING
ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING
```

例如三期 moving average：

```sql
SELECT
    year,
    medals,
    AVG(medals) OVER (
        ORDER BY year
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS medals_ma_3
FROM country_medals;
```

例如兩列 rolling sum：

```sql
SELECT
    year,
    medals,
    SUM(medals) OVER (
        ORDER BY year
        ROWS BETWEEN 1 PRECEDING AND CURRENT ROW
    ) AS medals_rt_2
FROM country_medals;
```

實務上若你是明確想用「前幾列、後幾列」的概念，`ROWS BETWEEN` 往往比 `RANGE BETWEEN` 更直觀，也更常用。

## `NTILE()` for Bucketing and Paging

`NTILE(n)` 會把排序後的資料分成大致平均的 `n` 個 buckets。

```sql
SELECT
    country,
    medals,
    NTILE(4) OVER (ORDER BY medals DESC) AS quartile
FROM medal_totals;
```

適合情境：

- 把資料切成 quartile / tercile
- 粗略的 performance bucket
- 分頁式批次處理心智模型

要注意的是，`NTILE()` 的結果高度依賴 `ORDER BY`；沒有排序就沒有有意義的 bucket。

## CTE + Window Function

CTE 和 window function 很常一起用，尤其在你需要先編號、再從編號結果挑某一筆時。

```sql
WITH quota_ranked AS (
  SELECT
    CurrentQuota,
    ROW_NUMBER() OVER (
      PARTITION BY CurrentQuota
      ORDER BY CurrentQuota
    ) AS quota_list
  FROM SaleGoal
)
SELECT *
FROM quota_ranked
WHERE quota_list = 1;
```

這個模式很適合：

- 做每組第一筆 / 最後一筆
- 去重
- 保留某個排序條件下的代表列

## PostgreSQL Pivoting with `CROSSTAB`

當你要把：

| country | year | awards |
| --- | --- | --- |
| CHN | 2008 | 74 |
| CHN | 2012 | 56 |
| USA | 2008 | 125 |

轉成：

| country | 2008 | 2012 |
| --- | --- | --- |
| CHN | 74 | 56 |
| USA | 125 | 147 |

就可以考慮 PostgreSQL 的 `tablefunc` extension 與 `CROSSTAB()`.

### Enable `tablefunc`

```sql
CREATE EXTENSION IF NOT EXISTS tablefunc;
```

### Basic `CROSSTAB()` Pattern

```sql
SELECT *
FROM CROSSTAB($$
    SELECT
        country,
        year,
        COUNT(*)::INTEGER AS awards
    FROM summer_medals
    WHERE medal = 'Gold'
    GROUP BY country, year
    ORDER BY country, year
$$) AS ct (
    country VARCHAR,
    "2008" INTEGER,
    "2012" INTEGER
);
```

重點先記三件事：

- source query 通常要先整理成 `row_key, category, value`
- source query 的排序要穩定，常見是 `ORDER BY row_key, category`
- `AS ct (...)` 需要你明確寫出 pivot 後的欄位型別

## Practical Reminders

- 先問自己要不要保留明細列，這會決定你是用 `GROUP BY` 還是 window function。
- `ROW_NUMBER()` 很適合 top-N per group，但若要保留 ties，通常改想 `RANK()` 或 `DENSE_RANK()`。
- `LAST_VALUE()` 若結果看起來怪，先檢查 frame。
- moving average、rolling sum 這類問題，多半都值得優先想 `ROWS BETWEEN`。
- `CROSSTAB()` 很方便，但輸出欄位必須事先定義，對高度動態欄位不一定是最自然的工具。

[Back to Databases](README.md)

## 實務心法

- `PARTITION BY` 決定你要在哪個群組內看問題
- `ORDER BY` 決定你怎麼定義時間、先後與累積
- `LEAD()` / `LAG()` 非常適合 period-over-period 分析
- `ROW_NUMBER()` 是去重、排序與每組首筆問題的萬用工具
- 先想清楚你要保留明細還是只要摘要，這會直接決定要用 `GROUP BY` 還是 window function
