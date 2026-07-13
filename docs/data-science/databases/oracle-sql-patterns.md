# Oracle SQL Patterns

這篇整理 Oracle SQL 裡比較值得特別記住的語法與使用習慣。  
重點不是重講所有 SQL 基礎，而是把 Oracle 跟一般 ANSI SQL 或其他資料庫相比，較常出現的特徵集中起來。

## Oracle Database vs. PL/SQL

先分清楚兩件事：

- Oracle Database：Oracle 的 relational database system
- PL/SQL：Oracle 在 SQL 之外再加上的 procedural extension

如果你只是寫查詢、聚合、join，多半還是在寫 SQL。  
如果你需要變數、流程控制、stored program unit，才會更靠近 PL/SQL。

## What Is Actually Oracle-Specific

很多 Oracle 教材會把 `SELECT`、`JOIN`、`GROUP BY`、`HAVING`、query execution order 一起教，但這些概念大多不是 Oracle 專屬。

Oracle 比較值得額外記住的，是這幾類：

- `DUAL`
- `NVL()`
- `TO_CHAR()`, `TO_DATE()`, `TO_NUMBER()`
- `TRUNC()`
- set operator 裡的 `MINUS`
- 某些 aggregate / format function 的 Oracle 用法

## DUAL

`DUAL` 是 Oracle 裡常見的一列表。

它的用途不是存業務資料，而是讓你在沒有真實 table 的情況下，仍能執行 expression、formatting 或型別轉換。

例如：

```sql
SELECT TO_DATE('2016-01-31', 'YYYY-MM-DD')
FROM DUAL;
```

或：

```sql
SELECT TO_NUMBER('$15,000.75', '$999,999.99')
FROM DUAL;
```

可以先把它理解成：「我只是想算一個 expression，但 SQL 還是需要一個 `FROM` 目標。」

## NULL Handling with NVL

Oracle 常見的空值處理函數是 `NVL(x, y)`。

意思是：

- 如果 `x` 不是 `NULL`，回傳 `x`
- 如果 `x` 是 `NULL`，回傳 `y`

```sql
SELECT NVL(HireDate, DATE '2004-11-19')
FROM Employee;
```

實務心智模型：

- `NVL()` 很 Oracle
- `COALESCE()` 比較 portable

如果你的查詢只會跑在 Oracle，`NVL()` 很自然。  
如果你在寫跨資料庫 SQL，`COALESCE()` 往往比較穩。

## Formatting and Type Conversion

Oracle 很常用 format model 來做數值與日期的轉換。

### TO_CHAR

`TO_CHAR()` 常拿來把 number 或 date 轉成字串格式。

數字格式化：

```sql
SELECT UnitPrice, TO_CHAR(UnitPrice, '$999.99')
FROM InvoiceLine;
```

常見 format token：

- `$`：貨幣符號
- `9`：數字位置
- `0`：補零
- `.`：小數點位置
- `,`：千分位

日期格式化：

```sql
SELECT TO_CHAR(BirthDate, 'DD-MON-YYYY')
FROM Employee;
```

常見日期 token：

- `YYYY`：四位數年份
- `MM`：兩位數月份
- `MON`：三字月份縮寫
- `MONTH`：完整月份名稱
- `DD`：月份中的日
- `DY`：星期縮寫
- `DAY`：完整星期名稱

### TO_DATE

`TO_DATE()` 用來把字串轉成 date。

```sql
SELECT TO_DATE('2016-01-31', 'YYYY-MM-DD')
FROM DUAL;
```

重點不是背所有 token，而是：

- 字串格式要和 format mask 對齊
- 轉換失敗通常就是資料字串和 mask 不匹配

### TO_NUMBER

`TO_NUMBER()` 用來把字串解析成數值。

```sql
SELECT TO_NUMBER('$15,000.75', '$999,999.99')
FROM DUAL;
```

這在匯入資料、清理 legacy string number 或處理報表欄位時很常見。

## ROUND vs. TRUNC

`ROUND()` 和 `TRUNC()` 都能處理小數，但語意不同。

### ROUND

```sql
SELECT
    Total,
    ROUND(Total, 1) AS round_1,
    ROUND(Total, 0) AS whole
FROM Invoice;
```

`ROUND(x, m)` 會做四捨五入。

### TRUNC

```sql
SELECT
    Total,
    ROUND(Total, 1) AS rounded_1,
    TRUNC(Total, 1) AS trunc_1
FROM Invoice;
```

`TRUNC(x, m)` 直接截斷，不做四捨五入。

像 `1.99`：

- `ROUND(1.99, 1)` 會變 `2.0`
- `TRUNC(1.99, 1)` 會變 `1.9`

這在財務、報表格式與規則計算上差很多。

## Aggregate Notes

Oracle 教學裡常把這些 group function 放在一起：

- `SUM()`
- `AVG()`
- `MEDIAN()`
- `MIN()`
- `MAX()`
- `COUNT()`

其中比較值得特別記一下的是 `MEDIAN()`，因為不是每個常見 SQL 環境都像 Oracle 一樣把它當成這麼直接的 aggregate function 使用。

```sql
SELECT
    AVG(Milliseconds),
    MEDIAN(Milliseconds)
FROM Track;
```

如果你在不同資料庫間切換，遇到沒有 `MEDIAN()` 的系統，往往要改用 percentile 類函數或 window function 模擬。

## Set Operators

Oracle 的 query order 說明裡，常把這些 set operator 放在一起：

- `UNION`
- `UNION ALL`
- `INTERSECT`
- `MINUS`

其中 `MINUS` 可以理解成「左邊結果集減掉右邊結果集」。

如果你更常接觸 PostgreSQL 或某些 ANSI SQL 文件，常會看到對應概念寫成 `EXCEPT`。  
在 Oracle 語境裡，這個角色常由 `MINUS` 承擔。

## Query Processing Order Still Matters

雖然這不是 Oracle 專屬，但 Oracle 教材很常用它來解釋：

1. `FROM` / `JOIN`
2. `WHERE`
3. `GROUP BY`
4. `HAVING`
5. `SELECT`
6. `DISTINCT`
7. set operators
8. `ORDER BY`

這也是為什麼：

- alias 通常不能在 `WHERE`、`GROUP BY`、`HAVING` 直接用
- alias 通常可以在 `ORDER BY` 用

如果你需要更完整的基礎版本，可以回看 [SQL Query Foundations](sql-query-foundations.md)。

## Practical Reminders

- Oracle 專用函數很多，但先抓高頻的 `NVL`、`TO_CHAR`、`TO_DATE`、`TRUNC`、`DUAL` 就很夠用。
- 寫跨資料庫 SQL 時，要特別注意 `NVL`、`MINUS` 這類非通用語法。
- `TO_CHAR()` 和 `TO_DATE()` 的核心是 format mask，不是函數名本身。
- `ROUND` 和 `TRUNC` 都能改變小數位數，但商業語意不同，不能互換。
- 如果課程內容只是 `JOIN`、`GROUP BY`、`HAVING`，先優先套用通用 SQL 心智模型，不必把它們誤認成 Oracle 專屬知識。

[Back to Databases](README.md)
