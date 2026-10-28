[Data Science](../README.md) › [Databases](README.md) › 報表查詢模式

# 報表查詢模式 (SQL Reporting Patterns)

把原始資料整理成可交付的摘要表：衍生分類欄位、型別清理、佔比、成長率、移動平均、小計與總計。多數錯誤不在語法，而在 **grain（一列代表什麼）**、**分母**與 **`NULL` 的語意**沒先講清楚。

## 寫之前先回答

| 問題 | 例子 |
| --- | --- |
| 輸出一列代表什麼（grain）？ | 每個病人？每次就診？每月每科別？ |
| 資料從哪些表來、怎麼 join？ | join key 唯一嗎？（見 [列數膨脹](sql-joins-and-set-operations.md#列數膨脹-fan-out)） |
| 比例的分母是什麼？ | 佔全體、佔同組、佔前一期？ |
| 哪些過濾是報表定義的一部分？ | 排除測試帳號、只算完成的檢驗 |
| `NULL` 要顯示成什麼？ | 沒資料、未對到、還是小計列？ |

## 衍生分類欄位：`CASE`

```sql
SELECT
  patient_id,
  age,
  CASE
    WHEN age IS NULL THEN 'unknown'
    WHEN age < 18    THEN '<18'
    WHEN age < 40    THEN '18-39'
    WHEN age < 65    THEN '40-64'
    ELSE '65+'
  END AS age_group
FROM patients;
```

| 規則 | 原因 |
| --- | --- |
| 條件由上往下評估，第一個成立就停 | 用遞增的單邊門檻（`< 18`、`< 40`）就不會重疊或留洞 |
| 先處理 `NULL` | 否則 `NULL` 會落到 `ELSE`，被誤歸為 `65+` |
| 保留 `ELSE` | 沒有 `ELSE` 時不符合的值會變成 `NULL`，不易察覺 |

條件計數（一次算多個指標）：

```sql
SELECT
  department,
  COUNT(*)                                          AS n,
  SUM(CASE WHEN result = 'positive' THEN 1 ELSE 0 END) AS n_positive,
  AVG(CASE WHEN result = 'positive' THEN 1.0 ELSE 0 END) AS positive_rate
  -- PostgreSQL / DuckDB 也可寫 COUNT(*) FILTER (WHERE result = 'positive')
FROM tests
GROUP BY department;
```

## 型別清理：`CAST`

| 症狀 | 原因 | 修正 |
| --- | --- | --- |
| `AVG(first_name)` 報錯 | 對文字做數值聚合 | 確認欄位語意 |
| join 對不到或報型別錯 | 一邊 `int`、一邊 `varchar` | `ON a.id = CAST(b.id AS INTEGER)`；長期修正 schema |
| `'10' < '9'` 為真 | 數字存成字串，按字典序比較 | `CAST(x AS NUMERIC)` |
| 日期排序亂掉 | 日期存成 `'3/1/2024'` 字串 | `CAST(d AS DATE)` 或各方言的 `TO_DATE`（見 [方言速查](sql-dialect-cheatsheet.md)） |
| 比例都是 0 | **整數除法**：`30 / 100 = 0` | 分子乘 `1.0` 或 `CAST(... AS NUMERIC)` |

> 整數除法：PostgreSQL、SQL Server、SQLite 中兩個整數相除會捨去小數；MySQL、DuckDB、Snowflake 回傳小數。跨平台寫法一律讓分子先變成小數（`x * 1.0 / y`）。

## 佔比 (Percent of Total)

```sql
-- 先聚合到隊伍層級，再除以總和
WITH team_points AS (
  SELECT team_id, SUM(points) AS points
  FROM matches
  GROUP BY team_id
)
SELECT
  team_id,
  points,
  points * 1.0 / SUM(points) OVER ()                      AS share_of_total,   -- 分母：全部
  ROUND(100.0 * points / SUM(points) OVER (), 1)          AS pct_of_total
FROM team_points;

-- 組內佔比：分母改成同組總和
SELECT
  team_id,
  player_id,
  points * 1.0 / SUM(points) OVER (PARTITION BY team_id) AS share_of_team
FROM player_points;
```

`SUM(...) OVER ()` 是 window function：保留每一列，同時附上整體總和（見 [Window Functions](sql-window-functions.md)）。

## 成長率 (Period-over-Period)

```sql
WITH monthly AS (
  SELECT
    DATE_TRUNC('month', order_date) AS month,      -- 保留年份；只取月份數字會把不同年的 1 月混在一起
    SUM(revenue)                    AS revenue
  FROM orders
  GROUP BY 1
)
SELECT
  month,
  revenue,
  LAG(revenue) OVER (ORDER BY month)                                 AS prev_revenue,
  revenue * 1.0 / NULLIF(LAG(revenue) OVER (ORDER BY month), 0) - 1  AS pct_change
FROM monthly
ORDER BY month;
```

| 保護 | 作用 |
| --- | --- |
| `NULLIF(x, 0)` | 分母為 0 時變成 `NULL`，結果為 `NULL` 而不是除以零錯誤 |
| 先聚合成月再 `LAG` | `LAG` 看的是「上一列」，grain 必須是一列一期 |
| 補齊缺月 | 某月沒有資料時，`LAG` 會跳到更早的月份；先與完整月份序列 `LEFT JOIN`（PostgreSQL `generate_series`） |

## 移動平均 (Rolling)

```sql
WITH daily AS (
  SELECT order_date, SUM(revenue) AS revenue
  FROM orders
  GROUP BY order_date
)
SELECT
  order_date,
  revenue,
  AVG(revenue) OVER (
    ORDER BY order_date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW      -- 最近 7 列
  ) AS revenue_ma7
FROM daily
ORDER BY order_date;
```

`ROWS` 數的是列不是天：有缺日時「7 列」會跨超過 7 天。缺日要先補齊，或改用以時間為單位的 `RANGE BETWEEN INTERVAL '6 days' PRECEDING AND CURRENT ROW`（PostgreSQL 11+、DuckDB）。

## 小計與總計：`ROLLUP` / `CUBE` / `GROUPING SETS`

不必用 `UNION ALL` 拼多段查詢，`GROUP BY` 的擴充一次輸出明細、小計與總計。

| 語法 | 產生的層次 | 適用 |
| --- | --- | --- |
| `ROLLUP (a, b)` | `(a, b)`、`(a)`、`()` | 有階層：年 → 國家 → 總計 |
| `CUBE (a, b)` | `(a, b)`、`(a)`、`(b)`、`()` | 每個維度的邊際總計；維度多時列數暴增 |
| `GROUPING SETS (...)` | 只列出指定的組合 | 報表需求明確 |

```sql
SELECT
  m.year_of_release,
  c.country,
  COUNT(*)                     AS n_rentals,
  ROUND(AVG(r.rating), 2)      AS avg_rating,
  GROUPING(c.country)          AS is_country_total     -- 1 = 這列是彙總列
FROM renting AS r
LEFT JOIN customers AS c ON c.customer_id = r.customer_id
LEFT JOIN movies    AS m ON m.movie_id    = r.movie_id
GROUP BY ROLLUP (m.year_of_release, c.country);

-- 只要特定層次
-- GROUP BY GROUPING SETS ((country, genre), (country), (genre), ())
```

彙總列的維度欄是 `NULL`，與真正缺值的 `NULL` 長得一樣；用 `GROUPING(col)` 區分，再以 `CASE` 改成 `'Total'` 標籤。MySQL 寫法是 `GROUP BY a, b WITH ROLLUP`。

## 相關子查詢 (Correlated Subquery)

子查詢引用外層的列，對每一列各算一次，適合「和自己的群組比」：

```sql
-- 高於自己科別平均住院天數的病人
SELECT p.patient_id, p.department, p.los_days
FROM admissions AS p
WHERE p.los_days > (
  SELECT AVG(q.los_days)
  FROM admissions AS q
  WHERE q.department = p.department
);
```

同樣的需求用 window function 通常更快也更好讀：先算 `AVG(los_days) OVER (PARTITION BY department)`，外層再過濾。只檢查存在性時改用 `EXISTS`（見 [semi join](sql-joins-and-set-operations.md#semi-join-與-anti-join)）。

## `NULL` 要明確處理

```sql
SELECT country, COALESCE(golds, 0) AS golds
FROM medal_summary;
```

| `NULL` 的來源 | 可以補 0 嗎 |
| --- | --- |
| 該事件確實沒發生（沒得獎） | 可以 |
| `LEFT JOIN` 沒對到 | 視情況；可能是資料缺漏，應該標示出來 |
| 測量值缺失 | 不行，補 0 會讓平均值偏低 |
| `ROLLUP` 的彙總列 | 不行，改成 `'Total'` 標籤 |
