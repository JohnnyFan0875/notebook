# SQL Server T-SQL Patterns

這篇整理 SQL Server 裡很常用、但不完全屬於「通用 SQL 基礎」的 T-SQL 模式。重點放在 SQL Server 常見的聚合寫法、`NULL` 處理、日期與數學函數、變數、`WHILE` 以及 CTE。

## 什麼時候會用到這篇

- 想在 SQL Server 裡快速做 exploratory aggregation
- 想處理 `NULL` 值，而不只是把它們過濾掉
- 想做日期加減、日期差、年月日拆解
- 想在 T-SQL 中用變數控制流程
- 想用 CTE 拆出中間結果，讓查詢更可讀

## Aggregation for Fast Exploration

資料還在資料庫裡時，最快的第一輪探索通常不是匯出到 pandas，而是先用 SQL 做聚合摘要。

### Basic aggregates

```sql
SELECT
  AVG(InternetUse) AS mean_internet_use,
  MIN(InternetUse) AS min_internet_use,
  MAX(InternetUse) AS max_internet_use
FROM EconomicIndicators;
```

最常先看的聚合包括：

- `COUNT(*)`
- `AVG()`
- `SUM()`
- `MIN()`
- `MAX()`

### Grouped aggregates

```sql
SELECT
  Country,
  AVG(InternetUse) AS mean_internet_use,
  MIN(InternetUse) AS min_internet_use,
  MAX(InternetUse) AS max_internet_use
FROM EconomicIndicators
GROUP BY Country;
```

這個模式很適合拿來看每個國家、產品、部門、月份的摘要差異。

### `HAVING` after grouping

```sql
SELECT
  Country,
  AVG(InternetUse) AS mean_internet_use,
  MIN(GDP) AS smallest_gdp,
  MAX(InternetUse) AS max_internet_use
FROM EconomicIndicators
GROUP BY Country
HAVING MAX(InternetUse) > 100;
```

如果條件是對聚合結果做篩選，就要用 `HAVING`，不要放進 `WHERE`。

## `NULL` Handling in SQL Server

### Detecting `NULL`

```sql
SELECT Country, InternetUse, Year
FROM EconomicIndicators
WHERE InternetUse IS NULL;
```

### Excluding `NULL`

```sql
SELECT Country, InternetUse, Year
FROM EconomicIndicators
WHERE InternetUse IS NOT NULL;
```

要記得：

- `NULL` 不等於 0
- `NULL` 不等於空字串
- `NULL` 不能用 `=`、`<`、`>` 正常比較

### Blank is not `NULL`

如果欄位是空白字串，它仍然不是 `NULL`。  
所以實務上要先分清楚資料缺失是：

- 真正缺值 `NULL`
- 空白字串 `''`
- 特殊代碼，例如 `'N/A'`

## `ISNULL()` and `COALESCE()`

### `ISNULL()`

`ISNULL(expr, fallback)` 會在 `expr` 是 `NULL` 時回傳替代值。

```sql
SELECT
  GDP,
  Country,
  ISNULL(Country, 'Unknown') AS new_country
FROM EconomicIndicators;
```

也可以拿一個欄位去補另一個欄位：

```sql
SELECT
  TradeGDPPercent,
  ImportGoodPercent,
  ISNULL(TradeGDPPercent, ImportGoodPercent) AS new_percent
FROM EconomicIndicators;
```

### `COALESCE()`

如果可能有多個候選值，`COALESCE()` 通常更彈性。

```sql
SELECT
  COALESCE(TradeGDPPercent, ImportGoodPercent, 0) AS trade_percent
FROM EconomicIndicators;
```

心智模型上：

- `ISNULL()`: 兩選一，偏 SQL Server 風格
- `COALESCE()`: 多選一，跨資料庫也常見

## Date Functions in T-SQL

### `DATEPART()`

`DATEPART()` 用來取日期的一部分，例如年、月、日、星期。

```sql
SELECT
  DATEPART(year, ModifiedDate)  AS sales_year,
  DATEPART(month, ModifiedDate) AS sales_month,
  DATEPART(day, ModifiedDate)   AS sales_day
FROM SaleGoal;
```

### `DATENAME()`

如果你要拿到可讀的星期或月份名稱，`DATENAME()` 會比 `DATEPART()` 更直觀。

```sql
SELECT
  DATENAME(weekday, StartDate) AS day_of_week,
  DATENAME(month, StartDate)   AS month_name
FROM CapitalBikeShare;
```

這很常用在報表欄位或 EDA 摘要，但要注意它回傳的是文字，不是可自然排序的數字。

### Sorting weekday labels logically

如果直接對 `DATENAME(weekday, ...)` 排序，通常會得到字母順序，不是星期順序。

```sql
SELECT
  DATENAME(weekday, StartDate) AS day_of_week,
  SUM(Duration) AS total_duration
FROM CapitalBikeShare
GROUP BY DATENAME(weekday, StartDate)
ORDER BY CASE
  WHEN DATENAME(weekday, StartDate) = 'Sunday' THEN 1
  WHEN DATENAME(weekday, StartDate) = 'Monday' THEN 2
  WHEN DATENAME(weekday, StartDate) = 'Tuesday' THEN 3
  WHEN DATENAME(weekday, StartDate) = 'Wednesday' THEN 4
  WHEN DATENAME(weekday, StartDate) = 'Thursday' THEN 5
  WHEN DATENAME(weekday, StartDate) = 'Friday' THEN 6
  WHEN DATENAME(weekday, StartDate) = 'Saturday' THEN 7
END;
```

這是一個很常見的報表技巧：顯示可讀標籤，但另外手動控制排序邏輯。

### `DATEADD()`

`DATEADD(datepart, number, date)` 可以加減日期。

```sql
SELECT DATEADD(day, 30, '2020-06-21')  AS plus_30_days,
       DATEADD(day, -30, '2020-06-21') AS minus_30_days;
```

這很適合拿來做：

- 到期日計算
- 前後 N 天 / 月 / 年
- 滾動視窗邊界

### `DATEDIFF()`

`DATEDIFF(datepart, startdate, enddate)` 用來算差距。

```sql
SELECT
  DATEDIFF(day, '2020-05-22', '2020-06-21') AS difference_1,
  DATEDIFF(day, '2020-07-21', '2020-06-21') AS difference_2;
```

很常見的用途是：

- 距今天幾天
- 兩次事件相差幾天 / 幾月
- 流程耗時

## Math Functions in T-SQL

### `ROUND()`

```sql
SELECT
  ROUND(DurationSeconds, 0)  AS round_to_whole,
  ROUND(DurationSeconds, 1)  AS round_to_one_decimal,
  ROUND(DurationSeconds, -1) AS round_to_ten,
  ROUND(DurationSeconds, -2) AS round_to_hundred
FROM Incidents;
```

負的 precision 很實用，因為可以把數字直接四捨五入到十位、百位。

### Truncating with `ROUND()`

`ROUND(number, length, 1)` 可以做截斷而不是一般四捨五入。

```sql
SELECT
  ROUND(DurationSeconds, 0)    AS rounding_to_whole,
  ROUND(DurationSeconds, 0, 1) AS truncating_to_whole
FROM Incidents;
```

### Other handy math functions

```sql
SELECT
  ABS(-2.77) AS abs_decimal,
  ABS(-2)    AS abs_int,
  SQRT(9)    AS sqrt_9;
```

常見還包括：

- `ABS()`
- `SQRT()`
- `POWER()`
- `CEILING()`
- `FLOOR()`

## Temporal EDA Quick Checks

交易型資料很常先做一些時間欄位的 sanity check，快速抓出明顯不合理的 records。

```sql
SELECT *
FROM CapitalBikeShare
WHERE StartDate > GETDATE()
   OR EndDate > GETDATE()
   OR StartDate > EndDate;
```

這類查詢很適合當第一輪資料檢查，尤其在：

- 裝置時間校正可能出錯
- 分散式系統跨來源收資料
- 你還不確定欄位可信度時

## Formatting for Human-Readable Output

如果結果主要是要給人看，而不是給下游計算，`FORMAT()` 可以讓輸出更接近報表。

```sql
SELECT
  FORMAT(SUM(Duration), 'n', 'en-us') AS duration_n,
  FORMAT(SUM(Duration), '#,0.00') AS duration_custom
FROM CapitalBikeShare;
```

不過實務上要記得：

- `FORMAT()` 偏 presentation
- 如果結果還要再排序、比較或做數值運算，盡量保留原始 numeric 欄位

## Variables in T-SQL

T-SQL 很常用變數把中間值存起來，尤其在 stored procedure、批次腳本與流程控制裡。

### Declaring variables

```sql
DECLARE @Snack VARCHAR(10);
DECLARE @Counter INT;
DECLARE @Price DECIMAL(10,2);
```

常見型別包括：

- `VARCHAR(n)`
- `INT`
- `DECIMAL(p, s)` / `NUMERIC(p, s)`

### Assigning values

可以用 `SET`：

```sql
DECLARE @Snack VARCHAR(10);
SET @Snack = 'Cookies';
```

也可以用 `SELECT`：

```sql
DECLARE @Snack VARCHAR(10);
SELECT @Snack = 'Candy';
```

簡單記法：

- `SET` 比較明確，適合單一變數賦值
- `SELECT` 在 T-SQL 中也常見，尤其是從查詢結果取值

## `WHILE` Loops

T-SQL 支援 `WHILE` 進行流程控制，但實務上要保守使用，因為很多逐列問題其實應該先想集合化解法。

```sql
DECLARE @ctr INT;
SET @ctr = 1;

WHILE @ctr < 10
BEGIN
  PRINT @ctr;
  SET @ctr = @ctr + 1;
END;
```

### 什麼時候要小心

- 大量資料逐筆處理通常很慢
- 能用 set-based query、window function 或 CTE 解決時，通常不要先寫 loop

## CTEs in T-SQL

CTE 很適合把複雜查詢拆成可讀的中間步驟。

### Basic CTE syntax

```sql
WITH CTEName (Col1, Col2) AS (
  SELECT Col1, Col2
  FROM SomeTable
)
SELECT *
FROM CTEName;
```

### Example: aggregate first, then join back

```sql
WITH MaxBloodPressureByAge (Age, MaxBloodPressure) AS (
  SELECT
    Age,
    MAX(BloodPressure) AS MaxBloodPressure
  FROM Patients
  GROUP BY Age
)
SELECT
  p.PatientName,
  p.Age,
  p.BloodPressure
FROM Patients AS p
JOIN MaxBloodPressureByAge AS m
  ON p.Age = m.Age
 AND p.BloodPressure = m.MaxBloodPressure;
```

這個模式非常實用，因為它把：

1. 先聚合
2. 再回接明細

的流程寫得很清楚。

## 實務心法

- `HAVING` 是分組後的過濾，不是 `WHERE` 的替代拼法
- `ISNULL()` 適合快速替補，`COALESCE()` 適合多層 fallback
- `DATEADD()` 和 `DATEDIFF()` 幾乎是 SQL Server 日期處理的基本功
- `DATENAME()` 很適合做可讀標籤，但排序通常要自己補 `CASE`
- 變數與 `WHILE` 很方便，但先確認問題能不能用集合式 SQL 解決
- CTE 是可讀性與除錯的好朋友，尤其在中間結果需要命名時
