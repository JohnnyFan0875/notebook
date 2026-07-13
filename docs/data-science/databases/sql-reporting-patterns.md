# SQL Reporting Patterns

這篇整理比較偏「報表交付」的 SQL 心智模型。  
重點不是單一資料庫方言，而是當你要把原始資料整理成可讀、可驗證、可交付的表格時，常會遇到哪些問題。

## Reporting Is Not Just Querying

報表 SQL 通常不只是把資料查出來，而是把資料整理成可以回答問題的形狀。

常見目標：

- 把多張表整成一張 summary table
- 建出對業務可理解的分類欄位
- 算比例、成長率、排名、rolling metric
- 處理型別混亂與 `NULL`
- 控制排序、限制筆數、讓結果更像報表而不是原始 dump

## Plan the Query Before Writing It

在動手前，先把這幾個問題問完通常能少走很多彎路：

- 需要從哪些表取資料
- 這些表該怎麼 join 或 union
- 哪些欄位需要即時計算
- 哪些 filters 是報表定義的一部分
- 是否需要排序、分頁或 top-N

這個步驟很像先畫報表 spec。  
如果需求講不清楚，SQL 常會越寫越長，最後連自己都很難驗證。

## Build Derived Reporting Fields with `CASE`

報表常需要把原始欄位轉成更可讀的分類欄位。

例如把 `gender` 和 `age` 合成 `demographic_group`：

```sql
SELECT
    gender,
    age,
    CASE
        WHEN age BETWEEN 13 AND 25 AND gender = 'M' THEN 'Male Age 13-25'
        WHEN age > 25 AND gender = 'M' THEN 'Male Age 26+'
        WHEN age BETWEEN 13 AND 25 AND gender = 'F' THEN 'Female Age 13-25'
        WHEN age > 25 AND gender = 'F' THEN 'Female Age 26+'
        ELSE 'Other'
    END AS demographic_group
FROM athletes;
```

這類欄位很常成為：

- `GROUP BY` 的分類維度
- dashboard filter
- 報表列標籤

實務上要注意兩件事：

- `CASE` 規則要互斥，避免重疊條件
- 最好保留 `ELSE`，避免漏掉不在預期範圍內的資料

## Type Cleanup Is Part of Reporting

報表工作很常卡在資料型別，而不是商業邏輯本身。

常見問題：

- 對字串欄位做數值 aggregate
- 用文字欄位去 join 整數欄位
- 日期其實是字串

典型錯誤像是：

```sql
SELECT AVG(first_name)
FROM athletes;
```

或：

```sql
SELECT country, continent
FROM countries AS c1
JOIN continents AS c2
  ON c1.continent_id = c2.id;
```

如果兩邊型別不一致，通常就需要先 `CAST()`。

```sql
SELECT CAST(birthdate AS date)
FROM athletes;

SELECT *
FROM table_a AS a
JOIN table_b AS b
  ON a.id = CAST(b.id AS varchar);
```

心智模型上，`CAST()` 不是補丁，而是把資料恢復成可運算、可比較、可 join 的狀態。

## Join Carefully for Reporting

報表 query 很容易因為 join 不夠精準而重複計數。

特別要注意：

- join key 是否唯一
- 是否需要 composite key
- `LEFT JOIN` 後的 `NULL` 代表沒有對到，不一定是原始缺值

如果單一欄位 join 會重複，常要補上第二個條件：

```sql
SELECT *
FROM players AS p
JOIN matches AS m
  ON p.id = m.id
 AND p.year = m.year;
```

比起「先 join 再看結果怪不怪」，更穩的習慣是先確認每層資料的 grain。

## Window Functions for Report Columns

報表很常需要在不壓掉明細的情況下，直接附上總計或比較值。

例如整體總計：

```sql
SELECT
    country_id,
    athlete_id,
    SUM(bronze) OVER () AS total_bronze
FROM summer_games;
```

例如分國家 subtotal：

```sql
SELECT
    country_id,
    athlete_id,
    SUM(bronze) OVER (PARTITION BY country_id) AS country_bronze
FROM summer_games;
```

這種做法很適合：

- 每列都要看到 overall total
- 每列都要看到 group subtotal
- 明細列旁邊需要直接帶 benchmark

## Layered Calculations

有些指標不能在同一層直接寫完，尤其是：

- aggregation 之後還要再算比例
- 先 group 再做 window
- 先算前一期再算成長率

這時候通常要分層。

```sql
WITH team_points AS (
    SELECT
        team_id,
        SUM(points) AS points
    FROM matches
    GROUP BY team_id
)
SELECT
    team_id,
    points,
    points / SUM(points) OVER () AS perc_of_total
FROM team_points;
```

一個很重要的判斷原則是：

- 同層就能解的，不要硬拆太多層
- 需要先產生中間 grain 的，就不要勉強寫成一層

## Ratios and Percent of Total

報表裡的比例欄位非常常見，例如：

- 佔全體比例
- 佔部門比例
- per-game / per-capita 指標

例如：

```sql
WITH team_points AS (
    SELECT
        team_id,
        SUM(points) AS points
    FROM matches
    GROUP BY team_id
)
SELECT
    team_id,
    points,
    points / SUM(points) OVER () AS perc_of_total
FROM team_points;
```

或分隊內占比：

```sql
SELECT
    team_id,
    player_id,
    points,
    points / SUM(points) OVER (PARTITION BY team_id) AS perc_of_team
FROM player_points;
```

比例問題本質上通常是「某個 numerator 除以哪一個 denominator」，先把分母說清楚最重要。

## Period-over-Period Change

成長率或變化率通常會用 `LAG()`。

```sql
SELECT
    DATE_PART('month', date) AS month_n,
    SUM(revenue) AS current_rev,
    LAG(SUM(revenue)) OVER (
        ORDER BY DATE_PART('month', date)
    ) AS prev_rev,
    SUM(revenue)
      / NULLIF(
          LAG(SUM(revenue)) OVER (
              ORDER BY DATE_PART('month', date)
          ),
          0
        ) - 1 AS perc_change
FROM monthly_sales
GROUP BY month_n
ORDER BY month_n;
```

這裡最重要的保護是 `NULLIF(..., 0)`，避免分母為零。

## Rolling Metrics

rolling window 很適合報表中的短期趨勢欄位。

例如 7 期 rolling revenue：

```sql
SELECT
    date,
    SUM(SUM(revenue)) OVER (
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS weekly_revenue
FROM daily_sales
GROUP BY date
ORDER BY date;
```

這種寫法的心智模型是：

- 先把每天聚合到正確 grain
- 再對聚合後的結果做 rolling 計算

## Handle Nulls Explicitly

報表裡的 `NULL` 很少可以直接丟給使用者自己解讀。

常見做法是 `COALESCE()`：

```sql
SELECT
    country,
    COALESCE(golds, 0) AS golds
FROM medal_summary;
```

但要先分清楚：

- 這個 `NULL` 是真的缺資料
- 還是 join 沒對到
- 還是 subtotal / total row 的語意

不要一看到 `NULL` 就全部改成 `0`。

## Practical Reminders

- 報表 query 的第一步通常不是寫 SQL，而是先釐清 grain、欄位定義與分母。
- `CASE` 很適合建報表分類欄位，但規則要可維護。
- 遇到怪錯誤時，先檢查型別與 join key。
- 比例、成長率、rolling metric 很常需要分層計算。
- `LEFT JOIN` 產生的 `NULL` 要小心解讀，不一定代表原始資料缺失。

[Back to Databases](README.md)
