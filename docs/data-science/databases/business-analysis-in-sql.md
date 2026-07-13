# Business Analysis in SQL

這篇整理商業分析裡常見的 SQL 指標與查詢框架。重點不是背特定產品的 KPI 名詞，而是理解怎麼把訂單、使用者與時間序列資料整理成可以回答商業問題的分析表。

## 適合處理的問題

- 每月營收、成本、利潤怎麼算
- 註冊數、DAU、MAU 是否成長
- 活躍使用者的月留存是否穩定
- ARPU、每位使用者訂單數分布是否健康
- 如何把多段分析查詢整理成能交付給主管的報表

## 常見資料表心智模型

商業分析 SQL 常圍繞幾張核心表：

- `orders`: 訂單主表，通常有 `order_id`、`user_id`、`order_date`
- `order_items`: 訂單明細，通常有 `order_id`、`item_id`、`quantity`
- `products` 或 `meals`: 商品維表，通常有售價與成本
- `users`: 使用者主表，必要時補註冊資訊

如果資料沒有直接提供 KPI 欄位，通常要先從事件表或交易表推導出來。

## Revenue, Cost, Profit

最基本的商業分析問題，是先把收入與成本算對。

### Revenue

如果明細表保存的是商品數量，營收通常是：

```sql
SELECT
  DATE_TRUNC('month', o.order_date)::date AS month,
  SUM(p.price * oi.quantity) AS revenue
FROM orders AS o
JOIN order_items AS oi
  ON oi.order_id = o.order_id
JOIN products AS p
  ON p.product_id = oi.product_id
GROUP BY month
ORDER BY month;
```

### Cost

成本常來自商品成本欄位、庫存補貨表或履約成本表。核心想法一樣是先把單位成本對上數量再加總。

```sql
SELECT
  DATE_TRUNC('month', o.order_date)::date AS month,
  SUM(p.cost * oi.quantity) AS cost
FROM orders AS o
JOIN order_items AS oi
  ON oi.order_id = o.order_id
JOIN products AS p
  ON p.product_id = oi.product_id
GROUP BY month
ORDER BY month;
```

### Profit

實務上不要急著在同一層 query 直接硬湊。先把 revenue 與 cost 各自整理成可驗證的中間表，再合併通常比較穩。

```sql
WITH monthly_revenue AS (
  SELECT
    DATE_TRUNC('month', o.order_date)::date AS month,
    SUM(p.price * oi.quantity) AS revenue
  FROM orders AS o
  JOIN order_items AS oi
    ON oi.order_id = o.order_id
  JOIN products AS p
    ON p.product_id = oi.product_id
  GROUP BY month
),
monthly_cost AS (
  SELECT
    DATE_TRUNC('month', o.order_date)::date AS month,
    SUM(p.cost * oi.quantity) AS cost
  FROM orders AS o
  JOIN order_items AS oi
    ON oi.order_id = o.order_id
  JOIN products AS p
    ON p.product_id = oi.product_id
  GROUP BY month
)
SELECT
  r.month,
  r.revenue,
  c.cost,
  r.revenue - c.cost AS profit
FROM monthly_revenue AS r
JOIN monthly_cost AS c
  ON c.month = r.month
ORDER BY r.month;
```

## User-Centric Metrics

對 B2C 或產品型公司，很多時候先看的不是財務報表，而是使用者成長與留存。

### Registrations

如果沒有明確的 `registered_at`，有時會用「第一次下單時間」當作註冊時間代理值。

```sql
WITH reg_dates AS (
  SELECT
    user_id,
    MIN(order_date)::date AS registration_date
  FROM orders
  GROUP BY user_id
)
SELECT
  DATE_TRUNC('month', registration_date)::date AS registration_month,
  COUNT(*) AS registrations
FROM reg_dates
GROUP BY registration_month
ORDER BY registration_month;
```

### Active Users

DAU / MAU 的核心不是訂單數，而是在一段時間內有沒有發生活動。

```sql
SELECT
  DATE_TRUNC('month', order_date)::date AS active_month,
  COUNT(DISTINCT user_id) AS mau
FROM orders
GROUP BY active_month
ORDER BY active_month;
```

### Running Total

累積註冊數很常用 window function 完成：

```sql
WITH registrations AS (
  SELECT
    DATE_TRUNC('month', registration_date)::date AS registration_month,
    COUNT(*) AS regs
  FROM (
    SELECT user_id, MIN(order_date)::date AS registration_date
    FROM orders
    GROUP BY user_id
  ) AS first_orders
  GROUP BY registration_month
)
SELECT
  registration_month,
  regs,
  SUM(regs) OVER (ORDER BY registration_month) AS regs_running_total
FROM registrations
ORDER BY registration_month;
```

### Growth

月成長常用 `LAG()` 取前一期數值再計算變化率。

```sql
WITH maus AS (
  SELECT
    DATE_TRUNC('month', order_date)::date AS active_month,
    COUNT(DISTINCT user_id) AS mau
  FROM orders
  GROUP BY active_month
)
SELECT
  active_month,
  mau,
  ROUND(
    (mau - LAG(mau) OVER (ORDER BY active_month))::numeric
    / NULLIF(LAG(mau) OVER (ORDER BY active_month), 0),
    2
  ) AS growth
FROM maus
ORDER BY active_month;
```

### Retention

留存的基本問題是：上個月活躍的使用者，有多少人在這個月仍然活躍。

```sql
WITH user_activity AS (
  SELECT DISTINCT
    DATE_TRUNC('month', order_date)::date AS active_month,
    user_id
  FROM orders
)
SELECT
  previous.active_month,
  ROUND(
    COUNT(DISTINCT current.user_id)::numeric
    / GREATEST(COUNT(DISTINCT previous.user_id), 1),
    2
  ) AS retention
FROM user_activity AS previous
LEFT JOIN user_activity AS current
  ON previous.user_id = current.user_id
 AND previous.active_month = current.active_month - INTERVAL '1 month'
GROUP BY previous.active_month
ORDER BY previous.active_month;
```

這種寫法是 period-over-period retention 的基本版本。如果要做 cohort retention，就需要先固定 cohort 起點，再追蹤 cohort 在後續月份的存活。

## Unit Economics and Distributions

只看平均值通常不夠。商業分析常需要把單位經濟與分布一起看。

### ARPU

ARPU 是 average revenue per user，常用來看平均每位活躍或付費使用者帶來多少收入。分母定義一定要先講清楚。

```sql
WITH monthly_revenue AS (
  SELECT
    DATE_TRUNC('month', o.order_date)::date AS month,
    SUM(p.price * oi.quantity) AS revenue
  FROM orders AS o
  JOIN order_items AS oi
    ON oi.order_id = o.order_id
  JOIN products AS p
    ON p.product_id = oi.product_id
  GROUP BY month
),
monthly_users AS (
  SELECT
    DATE_TRUNC('month', order_date)::date AS month,
    COUNT(DISTINCT user_id) AS active_users
  FROM orders
  GROUP BY month
)
SELECT
  r.month,
  r.revenue,
  u.active_users,
  ROUND(r.revenue::numeric / NULLIF(u.active_users, 0), 2) AS arpu
FROM monthly_revenue AS r
JOIN monthly_users AS u
  ON u.month = r.month
ORDER BY r.month;
```

### Order Distribution and Quartiles

當你想知道「平均每位使用者下幾單」是否被少數重度使用者拉高，就要看分布。

```sql
WITH user_orders AS (
  SELECT
    user_id,
    COUNT(DISTINCT order_id) AS orders
  FROM orders
  GROUP BY user_id
)
SELECT
  ROUND(PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY orders)::numeric, 2) AS orders_p25,
  ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY orders)::numeric, 2) AS orders_p50,
  ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY orders)::numeric, 2) AS orders_p75,
  ROUND(AVG(orders)::numeric, 2) AS avg_orders
FROM user_orders;
```

如果 `avg_orders` 明顯高於中位數，通常代表分布右偏，少數高活躍使用者正在拉高平均值。

## Nested Queries for Business Questions

很多商業問題不是單次 `GROUP BY` 就能回答，這時 nested query 會很自然。

### `IN` with a Subquery

先找出符合條件的 entity，再回頭查主表，是很常見的模式。

```sql
SELECT *
FROM customers
WHERE customer_id IN (
  SELECT DISTINCT customer_id
  FROM orders
  WHERE order_date >= DATE '2024-01-01'
);
```

適合用在：

- 找最近有下單的使用者
- 找曾經買過特定品類的客戶
- 找出符合某個事件條件的主體，再補查詳細屬性

### Correlated Subquery

當子查詢需要參照外層列時，就是 correlated subquery。

```sql
SELECT
  m.movie_id,
  m.title
FROM movies AS m
WHERE 5 < (
  SELECT COUNT(*)
  FROM renting AS r
  WHERE r.movie_id = m.movie_id
);
```

這種寫法適合回答：

- 哪些商品被購買次數高於某個門檻
- 哪些電影評分數至少達到一定數量
- 哪些使用者的訂單數高於其所屬群體的某個標準

### `EXISTS`

如果重點是判斷「有沒有符合條件的相關列」，`EXISTS` 常比 `IN` 更貼近語意。

```sql
SELECT
  m.movie_id,
  m.title
FROM movies AS m
WHERE EXISTS (
  SELECT 1
  FROM renting AS r
  WHERE r.movie_id = m.movie_id
    AND r.rating IS NOT NULL
);
```

這對「是否存在至少一次事件」特別好用，例如：

- 曾經被評分過的商品
- 至少有一次回購的客戶
- 至少有一次異常紀錄的裝置

## OLAP-Style Aggregation

當一般 `GROUP BY` 不夠，需要同時看明細、小計與總計時，可以用 OLAP aggregation extensions。

### `ROLLUP`

`ROLLUP` 適合有層級感的聚合，例如年 -> 國家 -> 總計。

```sql
SELECT
  m.year_of_release,
  c.country,
  COUNT(*) AS n_rentals,
  COUNT(DISTINCT r.movie_id) AS n_movies,
  ROUND(AVG(r.rating), 2) AS avg_rating
FROM renting AS r
LEFT JOIN customers AS c
  ON c.customer_id = r.customer_id
LEFT JOIN movies AS m
  ON m.movie_id = r.movie_id
GROUP BY ROLLUP (m.year_of_release, c.country)
ORDER BY c.country, m.year_of_release;
```

這樣可以一次得到：

- 年份 + 國家的細分結果
- 每個年份的小計
- 整體總計

### `CUBE`

`CUBE` 會產生所有維度組合的小計。  
當你想同時看各維度邊際總計時很方便，但結果量也可能明顯膨脹。

### `GROUPING SETS`

如果只想要某些特定層次，不想像 `CUBE` 一樣把所有組合都展開，`GROUPING SETS` 通常更精準。

```sql
SELECT
  country,
  genre,
  COUNT(*) AS n_rentals
FROM fact_rentals
GROUP BY GROUPING SETS (
  (country, genre),
  (country),
  (genre),
  ()
);
```

這種寫法適合報表需求已明確定義時使用。

## Executive Report Patterns

主管報表不只是把多張圖貼在一起，而是把幾個可解釋的指標整理成一個穩定輸出。

常見查詢模式包括：

- 用 `WITH` 把中間步驟拆開，讓 revenue、users、retention 各自可驗證
- 用 `SUM(...) OVER (...)` 算 running total
- 用 `LAG(...) OVER (...)` 算月增率
- 用 `RANK() OVER (...)` 做 top users、top products、top months
- 用 `ROLLUP` / `GROUPING SETS` 產出小計與總計
- 用 nested query 或 `EXISTS` 先篩出符合條件的分析對象
- 先把月度指標整理成一張寬表，再交給 BI 或 Markdown 報告層使用

例如找出高營收使用者：

```sql
WITH user_revenues AS (
  SELECT
    o.user_id,
    SUM(p.price * oi.quantity) AS revenue
  FROM orders AS o
  JOIN order_items AS oi
    ON oi.order_id = o.order_id
  JOIN products AS p
    ON p.product_id = oi.product_id
  GROUP BY o.user_id
)
SELECT
  user_id,
  revenue,
  RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
FROM user_revenues;
```

## Why CTEs Matter

商業分析 query 很容易長到難以維護。`CTE` 的價值通常不是效能，而是：

- 把商業邏輯拆成可命名的步驟
- 讓每段中間結果可以單獨檢查
- 降低重複子查詢帶來的閱讀成本
- 讓報表 query 更接近分析敘事

對 notebook 風格來說，這類查詢比一大坨巢狀 subquery 更適合保留。

## 常見陷阱

- 沒先定義分母，例如 ARPU 的分母到底是全部註冊者、活躍使用者，還是付費使用者
- 把訂單列直接拿去算使用者數，忘了 `COUNT(DISTINCT user_id)`
- 用平均值解釋高度偏態分布，卻沒補中位數或分位數
- 把 growth 寫成當月差值，卻誤稱百分比成長
- 留存計算時沒有先把時間粒度標準化，例如有些資料按日、有些按月
- 使用 correlated subquery 時忽略它可能在大表上帶來昂貴成本
- 使用 `CUBE` 或 `ROLLUP` 後沒有意識到 `NULL` 可能代表 subtotal / total，而不是真的缺值
- 在同一層 query 混太多邏輯，導致很難驗證 revenue 與 cost 是否真的算對

## Mental Checklist

- 先定義 KPI，再寫 SQL
- 先決定時間粒度：day、week、month
- 優先建立可重用的中間表或 CTE
- 成長與留存通常需要 window function 或 self join
- 需要多層彙總時，先想 `ROLLUP` / `GROUPING SETS`
- 需要條件化對象篩選時，先想 subquery / `EXISTS`
- 平均值之外，常要補 distribution 指標
- 報表最終目標是可解釋，不只是把 query 跑出來
