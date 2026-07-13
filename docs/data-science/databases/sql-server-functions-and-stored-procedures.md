# SQL Server Functions and Stored Procedures

這篇整理 SQL Server 裡 user-defined function 與 stored procedure 的基本心智模型。重點不是把所有語法背熟，而是先分清楚什麼情況該用 UDF，什麼情況該用 stored procedure。

## Why These Two Matter

它們都屬於把重複邏輯封裝起來的做法，常見價值包括：

- 減少重複 SQL
- 提高可讀性
- 支援模組化設計
- 在資料庫端直接封裝常用邏輯

但兩者能做的事不一樣，這個差異比語法細節更重要。

## UDF vs. Stored Procedure

| 面向 | UDF | Stored Procedure |
| --- | --- | --- |
| 回傳 | 必須回傳值 | 可回傳或不回傳 |
| 回傳型態 | scalar 或 table | result set、output parameter、status code |
| 可否嵌入 `SELECT` | 可以 | 不行 |
| `INSERT/UPDATE/DELETE` | 受限制，不是主要用途 | 可以 |
| output parameter | 不支援 | 支援 |
| 錯誤處理 | 不是強項 | 可搭配 `TRY...CATCH` |
| 適合用途 | 純運算、查詢封裝 | 多步驟資料處理、流程控制 |

先記一句話：

- 想把邏輯當成 expression 放進查詢裡，用 UDF
- 想執行一段流程、更新資料、回傳多種輸出，用 stored procedure

## Scalar UDF

scalar UDF 回傳單一值。

```sql
CREATE FUNCTION dbo.GetTomorrow()
RETURNS date
AS
BEGIN
    RETURN (
        SELECT DATEADD(day, 1, GETDATE())
    );
END;
```

這很適合：

- 單一數值轉換
- 日期換算
- 封裝重複的商業公式

### Scalar UDF with Parameters

```sql
CREATE FUNCTION dbo.GetRideHrsOneDay (@DateParm date)
RETURNS numeric
AS
BEGIN
    RETURN (
        SELECT SUM(DurationHours)
        FROM dbo.Rides
        WHERE CAST(StartDate AS date) = @DateParm
    );
END;
```

### Executing Scalar UDFs

可以直接放進 `SELECT`：

```sql
SELECT dbo.GetTomorrow();
```

也可以把結果存進變數：

```sql
DECLARE @TotalRideHrs numeric;

EXEC @TotalRideHrs =
    dbo.GetRideHrsOneDay
    @DateParm = '2017-01-15';
```

## Table-Valued Functions

table-valued function 會回傳一張表，因此很適合封裝可被後續查詢接續使用的結果集。

### Inline Table-Valued Function

inline TVF 通常最簡潔，直接回傳一段 `SELECT`。

```sql
CREATE FUNCTION dbo.SumLocationStats (@EndDate datetime)
RETURNS TABLE
AS
RETURN (
    SELECT
        PickupLocationID,
        COUNT(*) AS TripCount,
        AVG(FareAmount) AS AvgFare
    FROM dbo.Trips
    WHERE PickupDate <= @EndDate
    GROUP BY PickupLocationID
);
```

心智模型：

- 沒有 table variable
- `RETURN (SELECT ...)`
- 很像可參數化的 view

### Multi-Statement Table-Valued Function

如果邏輯需要多步驟，就會用 MSTVF。

```sql
CREATE FUNCTION dbo.CountTripAvgFareDay (
    @TripDate date
)
RETURNS @TripCountAvgFare TABLE (
    TripCount int,
    AvgFare numeric(10,2)
)
AS
BEGIN
    INSERT INTO @TripCountAvgFare
    SELECT
        COUNT(*),
        AVG(FareAmount)
    FROM dbo.Trips
    WHERE CAST(PickupDate AS date) = @TripDate;

    RETURN;
END;
```

心智模型：

- 先宣告要回傳的 table variable
- 在 `BEGIN ... END` 中逐步填資料
- 最後 `RETURN`

## `ALTER FUNCTION` and `CREATE OR ALTER`

課程裡有一個很實用的 SQL Server 習慣：`CREATE OR ALTER`。

```sql
CREATE OR ALTER FUNCTION dbo.SumLocationStats (
    @EndDate datetime = '2017-01-01'
)
RETURNS TABLE
AS
RETURN (
    SELECT ...
);
```

這比手動判斷「到底要 `CREATE` 還是 `ALTER`」更省事，也更適合反覆調整開發中的 routine。

## `SCHEMABINDING`

SQL Server 也能在 function 上使用 `WITH SCHEMABINDING`：

```sql
CREATE OR ALTER FUNCTION dbo.GetRideHrsOneDay (@DateParm date)
RETURNS numeric
WITH SCHEMABINDING
AS
BEGIN
    RETURN ...
END;
```

高層理解就好：

- 它會把 function 和依賴的 schema 綁得更緊
- 有助於避免底層物件被隨意改動而破壞 function

## Stored Procedures

stored procedure 比較像「在資料庫裡封裝一段工作流程」。

```sql
CREATE PROCEDURE dbo.cuspGetRideHrsOneDay
    @DateParm date,
    @RideHrsOut numeric OUTPUT
AS
BEGIN
    SELECT
        @RideHrsOut = SUM(DurationHours)
    FROM dbo.Rides
    WHERE CAST(StartDate AS date) = @DateParm;
END;
```

常見用途：

- 封裝 CRUD 流程
- 先更新再查詢
- 回傳 output parameter 或狀態碼
- 集中業務邏輯與權限控制

## Output Parameters vs. Return Values

這是 stored procedure 很容易混淆的地方。

### Output Parameter

- 用來回傳額外資料
- 可同時有多個
- 常拿來回傳 row count、訊息、計算結果

```sql
DECLARE @RideHrs numeric;

EXEC dbo.cuspGetRideHrsOneDay
    @DateParm = '2017-01-15',
    @RideHrsOut = @RideHrs OUTPUT;
```

### Return Value

- 通常拿來回傳 status code
- 慣例上 `0` 常表示 success，非 `0` 代表某種失敗或特殊狀態

```sql
DECLARE @ReturnValue int;

EXEC @ReturnValue =
    dbo.cusp_TripSummaryUpdate
    @TripDate = '2017-01-05',
    @TripHours = 300;
```

先記住：

- output parameter：資料
- return value：狀態

## Common Procedure Shapes

課程裡用了很典型的 CRUD procedure 範例，像是：

- `...Create`
- `...Read`
- `...Update`
- `...Delete`

這種命名雖然不一定是唯一標準，但對閱讀大型 SQL Server codebase 很有幫助。

## Ways to Execute Procedures

stored procedure 常見執行方式有三種：

- 沒有 output parameter 或 return value
- 有 output parameter
- 同時接 output parameter 與 return value

```sql
EXEC dbo.cusp_TripSummaryRead
    @TripDate = '2017-01-05';
```

```sql
DECLARE @RowCount int;
DECLARE @ReturnValue int;

EXEC @ReturnValue =
    dbo.cusp_TripSummaryDelete
    @TripDate = '2017-01-05',
    @RowCountOut = @RowCount OUTPUT;
```

## Procedures Can Use `TRY...CATCH`

這也是 procedure 和 UDF 的一個關鍵差異。

```sql
ALTER PROCEDURE dbo.cusp_TripSummaryCreate
    @TripDate date,
    @TripHours numeric(18,0),
    @ErrorMsg nvarchar(max) = NULL OUTPUT
AS
BEGIN
    BEGIN TRY
        INSERT INTO dbo.TripSummary (TripDate, TripHours)
        VALUES (@TripDate, @TripHours);
    END TRY
    BEGIN CATCH
        SET @ErrorMsg = ERROR_MESSAGE();
        THROW;
    END CATCH
END;
```

如果你需要：

- 寫資料
- 攔截錯誤
- 回傳訊息
- 做流程控制

stored procedure 通常會比 UDF 更自然。

## Temporal EDA Routines

這份課還示範了一個很實務的方向：把常用的時間分析邏輯封裝進 function 或 procedure。

例如：

- 把 weekday 排序邏輯封裝起來
- 把幣別或距離轉換封裝成 UDF
- 把 borough / pickup / shift 的彙總封裝成 procedure

這種做法的價值不是「所有分析都寫進資料庫」，而是把反覆出現、定義穩定的計算抽出來。

## Practical Reminders

- 純查詢運算先想 UDF，尤其是 inline TVF。
- 需要 output parameter、狀態碼、資料修改或錯誤處理時，先想 stored procedure。
- `CREATE OR ALTER` 很適合開發期反覆調整 routine。
- `SCHEMABINDING` 是一種強綁定工具，不要隨手加，但知道它的用途很重要。
- procedure 的 return value 和 output parameter 不要混用概念。

[Back to Databases](README.md)
