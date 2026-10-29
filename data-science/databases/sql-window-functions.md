[Data Science](../README.md) › [Databases](README.md) › 視窗函數

# 視窗函數 (Window Functions)

Window function 在**保留每一列**的同時，附上群組或排序後的計算結果：排名、前後列比較、累計、移動平均。`GROUP BY` 把多列壓成一列；window function 不壓。語法在 PostgreSQL、SQL Server、MySQL 8+、SQLite、DuckDB、Snowflake、BigQuery 大致相同。

| 需要 | 用 |
| --- | --- |
| 只要摘要列 | `GROUP BY` |
| 明細列 + 群組統計（組平均、組內佔比、排名） | window function |

## 骨架

```sql
SELECT
  col_a,
  func(...) OVER (
    PARTITION BY grp          -- 分組計算，但不壓扁；省略 = 整份結果一組
    ORDER BY t                -- 組內順序；排名、LAG、累計都需要
    ROWS BETWEEN ... AND ...  -- frame：目前這列看得到哪些列
  ) AS result
FROM some_table;
```

window function 在 `WHERE` / `GROUP BY` / `HAVING` **之後**計算，所以不能直接放在 `WHERE` 裡過濾；要包一層 CTE，或用 `QUALIFY`（DuckDB、Snowflake、BigQuery）。

## 函式速查

| 類別 | 函式 | 說明 |
| --- | --- | --- |
| 編號 | `ROW_NUMBER()` | 1, 2, 3, 4（同分也不同號，順序任意） |
| 排名 | `RANK()` | 1, 2, 2, 4（同分同名次，之後跳號） |
| | `DENSE_RANK()` | 1, 2, 2, 3（不跳號） |
| | `PERCENT_RANK()`、`CUME_DIST()` | 相對排名 0–1、累積比例 |
| 分桶 | `NTILE(n)` | 依排序切成 n 組，各組列數最多差 1 |
| 前後列 | `LAG(x, k, default)` / `LEAD(x, k, default)` | 前 / 後第 k 列的值；超出範圍回傳 `default`（預設 `NULL`） |
| 首尾 | `FIRST_VALUE(x)` / `LAST_VALUE(x)` / `NTH_VALUE(x, n)` | 受 frame 影響，見下方 |
| 聚合 | `SUM`、`AVG`、`COUNT`、`MIN`、`MAX`、`STDDEV`（SQL Server：`STDEV`） | 有 `ORDER BY` 時變成累計 |

```sql
SELECT
  country,
  athlete,
  medals,
  ROW_NUMBER() OVER (PARTITION BY country ORDER BY medals DESC) AS rn,
  RANK()       OVER (PARTITION BY country ORDER BY medals DESC) AS rnk,
  DENSE_RANK() OVER (PARTITION BY country ORDER BY medals DESC) AS drnk,
  NTILE(4)     OVER (ORDER BY medals DESC)                      AS quartile,
  medals - AVG(medals) OVER (PARTITION BY country)              AS diff_from_country_mean
FROM athlete_medals;
```

## 前後列：`LAG` / `LEAD`

```sql
SELECT
  patient_id,
  visit_date,
  hba1c,
  LAG(hba1c)  OVER w                         AS prev_hba1c,
  hba1c - LAG(hba1c) OVER w                  AS change,
  visit_date - LAG(visit_date) OVER w        AS days_since_last,   -- PostgreSQL / DuckDB 日期相減 = 天數
  LEAD(visit_date) OVER w IS NULL            AS is_last_visit
FROM visits
WINDOW w AS (PARTITION BY patient_id ORDER BY visit_date);          -- 具名 window，重複使用
```

> 忘了 `PARTITION BY patient_id`，第一次就診的 `LAG` 會拿到**上一位病人**的值。縱貫資料的 `LAG` 幾乎都需要依個體分組。

## Frame：目前這列看得到哪些列

| 寫法 | 意義 |
| --- | --- |
| （有 `ORDER BY`、沒寫 frame） | 預設 `RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW`：從頭到目前列，**含同值的列** |
| （沒有 `ORDER BY`） | 整個 partition |
| `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` | 前 2 列到目前列（3 列移動平均） |
| `ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING` | 置中 3 列 |
| `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING` | 整個 partition |
| `RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW` | 依值的範圍（時間窗）；PostgreSQL 11+、DuckDB |

```sql
SELECT
  day, v,
  SUM(v) OVER (ORDER BY day)                          AS cum_range,  -- 同一天的兩列都拿到含兩列的總和
  SUM(v) OVER (ORDER BY day ROWS UNBOUNDED PRECEDING) AS cum_rows,   -- 逐列累加
  AVG(v) OVER (ORDER BY day ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS ma3
FROM t;
-- day v  cum_range cum_rows
-- 1   10 10        10
-- 2   5  20        15
-- 2   5  20        20
-- 3   1  21        21
```

| 陷阱 | 原因 | 改法 |
| --- | --- | --- |
| 累計值在同值處跳一大格 | 預設 frame 是 `RANGE`，同值列一起算 | 明寫 `ROWS UNBOUNDED PRECEDING`，或讓 `ORDER BY` 唯一（加 id） |
| `LAST_VALUE` 回傳目前列的值 | 預設 frame 只到目前列 | `ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING`，或改用 `FIRST_VALUE(x) OVER (ORDER BY t DESC)` |
| 移動平均前幾列不足視窗長度 | 前 2 列只平均 1、2 個值 | 需要時用 `COUNT(*) OVER (同 frame)` 標記不完整的列 |
| `ROWS` 跨過缺漏的日期 | `ROWS` 數列不數天 | 先補齊日期，或用 `RANGE` + `INTERVAL` |

## 每組 top-N 與去重

```sql
-- 每位病人最近一次檢驗
WITH ranked AS (
  SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY test_date DESC, test_id DESC) AS rn
  FROM lab_results
)
SELECT * FROM ranked WHERE rn = 1;

-- DuckDB / Snowflake / BigQuery：QUALIFY 直接過濾 window 結果
SELECT *
FROM lab_results
QUALIFY ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY test_date DESC) = 1;
```

| 需求 | 用 |
| --- | --- |
| 每組剛好 1 列（去重、最新一筆） | `ROW_NUMBER()`；`ORDER BY` 加唯一欄（id）作 tie-breaker，結果才可重現 |
| 每組前 N 名，同分都保留 | `RANK()` / `DENSE_RANK()` `<= N` |

## Pivot：長表轉寬表

通用寫法是條件聚合，任何資料庫都能用：

```sql
SELECT
  country,
  SUM(CASE WHEN year = 2008 THEN awards END) AS y2008,
  SUM(CASE WHEN year = 2012 THEN awards END) AS y2012
  -- PostgreSQL / DuckDB：SUM(awards) FILTER (WHERE year = 2008)
FROM medals
GROUP BY country;
```

| country | year | awards | → | country | y2008 | y2012 |
| --- | --- | --- | --- | --- | --- | --- |
| CHN | 2008 | 74 | | CHN | 74 | 56 |
| CHN | 2012 | 56 | | USA | 125 | 147 |
| USA | 2008 | 125 | | | | |
| USA | 2012 | 147 | | | | |

各平台的專用語法：

| 平台 | 語法 |
| --- | --- |
| PostgreSQL | `tablefunc` extension 的 `crosstab()` |
| SQL Server、Snowflake、Oracle | `PIVOT (SUM(awards) FOR year IN (2008, 2012))` |
| DuckDB | `PIVOT medals ON year USING sum(awards)`（欄位自動產生） |

```sql
-- PostgreSQL crosstab
CREATE EXTENSION IF NOT EXISTS tablefunc;

SELECT *
FROM crosstab($$
    SELECT country, year, COUNT(*)::INTEGER AS awards   -- 來源必須是 (row_key, category, value)
    FROM summer_medals
    WHERE medal = 'Gold'
    GROUP BY country, year
    ORDER BY country, year                              -- 必須依 row_key、category 排序
$$) AS ct (
    country VARCHAR,
    "2008"  INTEGER,                                    -- 輸出欄位與型別必須事先寫死
    "2012"  INTEGER
);
```

> 單參數 `crosstab(sql)` 依**出現順序**填欄：某國缺 2008 的資料時，2012 的值會被填進 `"2008"` 欄。類別可能有缺時，改用雙參數版 `crosstab(source_sql, 'SELECT DISTINCT year FROM ... ORDER BY 1')`，或直接用條件聚合。

類別多、欄位會變動時，在 SQL 裡 pivot 不如取長表回 pandas（`pivot_table`）或 R（`pivot_wider`）處理，見 [重塑與合併](../python-foundations/pandas/reshape-merge.md)、[tidyr](../r-foundations/data-reshaping-with-tidyr.md)。
