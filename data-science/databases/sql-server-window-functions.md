# SQL Server Window Functions

這篇整理 SQL Server 裡最常用的 window function 心智模型。window function 的核心價值，是在不把資料壓扁成單列摘要的前提下，同時保留明細列與群組層級資訊。

## 什麼時候值得用 window function

- 想在每一列旁邊放上年度總額、群組平均值或累積值
- 想做 running total
- 想看前一列 / 下一列的值
- 想在每個群組內做排名或編號
- 想看某個視窗的第一個值、最後一個值

## Window Function Mental Model

window function 的基本骨架通常是：

```sql
function_name(...) OVER (
  PARTITION BY ...
  ORDER BY ...
)
```

可以先這樣理解：

- `PARTITION BY`: 把資料切成多個視窗
- `ORDER BY`: 定義每個視窗內的排序順序

如果沒有 `PARTITION BY`，通常表示整張結果表就是同一個 window。

## Aggregate over a Window

window function 很適合把聚合結果直接附回每一列。

```sql
SELECT
  SalesPerson,
  SalesYear,
  CurrentQuota,
  SUM(CurrentQuota) OVER (PARTITION BY SalesYear) AS yearly_total
FROM SaleGoal;
```

這樣每一列都還在，但同時多了一欄該年度總額。

### 為什麼這和 `GROUP BY` 不同

- `GROUP BY` 會把很多列壓成一列
- window aggregate 會保留原本每一列

這就是 window function 最值得用的地方。

## `PARTITION BY`

如果用年份做 partition：

```sql
SELECT
  SalesPerson,
  SalesYear,
  CurrentQuota,
  COUNT(*) OVER (PARTITION BY SalesYear) AS quota_per_year
FROM SaleGoal;
```

計數會在每個年份重新開始。  
也就是說，partition 是邏輯上的「分組視窗」，但不會像 `GROUP BY` 一樣消掉明細列。

## `FIRST_VALUE()` and `LAST_VALUE()`

### First / last value in a window

```sql
SELECT
  SalesPerson,
  SalesYear,
  CurrentQuota,
  FIRST_VALUE(CurrentQuota)
    OVER (PARTITION BY SalesYear ORDER BY ModifiedDate) AS start_quota,
  LAST_VALUE(CurrentQuota)
    OVER (PARTITION BY SalesYear ORDER BY ModifiedDate) AS end_quota,
  ModifiedDate AS mod_date
FROM SaleGoal;
```

這個模式很適合回答：

- 每年一開始與結束時的 quota 是多少
- 每個客戶第一筆與最後一筆狀態是什麼
- 某段旅程的起點與終點值

### 注意 `ORDER BY`

對 `FIRST_VALUE()` 與 `LAST_VALUE()` 來說，`ORDER BY` 幾乎是語意核心，因為沒有順序就沒有「第一個」或「最後一個」。

## `LEAD()` and `LAG()`

這兩個函數非常適合做 period-over-period 分析。

### `LEAD()`: next row

```sql
SELECT
  SalesPerson,
  SalesYear,
  CurrentQuota,
  LEAD(CurrentQuota)
    OVER (PARTITION BY SalesYear ORDER BY ModifiedDate) AS next_quota,
  ModifiedDate AS mod_date
FROM SaleGoal;
```

適合回答：

- 下一次 quota 是多少
- 下一期價格是多少
- 下一個事件發生在什麼值

### `LAG()`: previous row

```sql
SELECT
  SalesPerson,
  SalesYear,
  CurrentQuota,
  LAG(CurrentQuota)
    OVER (PARTITION BY SalesYear ORDER BY ModifiedDate) AS previous_quota,
  ModifiedDate AS mod_date
FROM SaleGoal;
```

適合回答：

- 和上一期相比成長多少
- 與前一筆狀態相比是否變化
- 前一次交易金額是多少

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

## Running Total

如果在 window 裡加上 `ORDER BY`，就可以得到累積效果。

```sql
SELECT
  SalesPerson,
  SalesYear,
  CurrentQuota,
  SUM(CurrentQuota)
    OVER (PARTITION BY SalesYear ORDER BY ModifiedDate) AS running_total,
  ModifiedDate
FROM SaleGoal;
```

這是 very common pattern，適合：

- 累積營收
- 累積配額
- 累積訂單數

## `ROW_NUMBER()`

`ROW_NUMBER()` 會在每個 window 內做連續編號。

```sql
SELECT
  SalesPerson,
  SalesYear,
  CurrentQuota,
  ROW_NUMBER()
    OVER (PARTITION BY SalesPerson ORDER BY SalesYear) AS quota_by_sales_person
FROM SaleGoal;
```

### 適合用途

- 每個人各自的第幾筆紀錄
- 每個群組中依時間排序後的序號
- 去重前先標記每組哪一筆要保留

`ROW_NUMBER()` 幾乎一定需要 `ORDER BY`，因為沒有排序就沒有穩定序號。

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

## `GROUP BY` vs Window Function

如果你不確定該用哪個，可以先問自己：

- 我最後還需要保留每一列明細嗎

如果答案是：

- `否`：通常先想 `GROUP BY`
- `是`：通常先想 window function

## 實務心法

- `PARTITION BY` 決定你要在哪個群組內看問題
- `ORDER BY` 決定你怎麼定義時間、先後與累積
- `LEAD()` / `LAG()` 非常適合 period-over-period 分析
- `ROW_NUMBER()` 是去重、排序與每組首筆問題的萬用工具
- 先想清楚你要保留明細還是只要摘要，這會直接決定要用 `GROUP BY` 還是 window function

