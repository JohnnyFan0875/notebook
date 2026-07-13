# SQL Server Transactions and Error Handling

這篇整理 SQL Server 裡 transaction 與錯誤處理的基本心智模型，重點放在 `TRY...CATCH`、`THROW`、`RAISERROR`、`@@TRANCOUNT`、`XACT_STATE()` 與 `XACT_ABORT`。

## Basic Transaction Pattern

```sql
BEGIN TRAN;

UPDATE accounts
SET balance = balance - 100
WHERE account_id = 1;

UPDATE accounts
SET balance = balance + 100
WHERE account_id = 2;

COMMIT TRAN;
```

先記住：

- `BEGIN TRAN`：開始 transaction
- `COMMIT TRAN`：提交
- `ROLLBACK TRAN`：回滾

## `TRY...CATCH`

SQL Server 最常見的錯誤處理骨架是：

```sql
BEGIN TRY
    -- risky work
END TRY
BEGIN CATCH
    -- error handling
END CATCH;
```

心智模型：

- `TRY` 裡出錯才會跳進 `CATCH`
- 沒出錯就直接略過 `CATCH`
- `CATCH` 裡可以回滾、記錄錯誤、或重新丟錯

## Transaction + `TRY...CATCH`

實務上通常會一起寫：

```sql
BEGIN TRY
    BEGIN TRAN;

    -- multiple statements

    COMMIT TRAN;
END TRY
BEGIN CATCH
    IF @@TRANCOUNT > 0
        ROLLBACK TRAN;
END CATCH;
```

這是 SQL Server 最常見的安全模板之一。

## `@@TRANCOUNT`

`@@TRANCOUNT` 代表目前 session 的 transaction 層數。

- `BEGIN TRAN`：`@@TRANCOUNT + 1`
- `COMMIT TRAN`：`@@TRANCOUNT - 1`
- `ROLLBACK TRAN`：通常直接回到 `0`

所以在 `CATCH` 裡常看到：

```sql
IF @@TRANCOUNT > 0
    ROLLBACK TRAN;
```

它的重點不是知道精確數字，而是先確認現在是否仍有開著的 transaction。

## `XACT_STATE()`

比 `@@TRANCOUNT` 更關鍵的是 `XACT_STATE()`，因為它會告訴你 transaction 目前還能不能提交。

- `1`：transaction 還開著，而且可提交
- `-1`：transaction 還開著，但已經 doomed，只能回滾
- `0`：目前沒有 active transaction

常見模板：

```sql
BEGIN TRY
    BEGIN TRAN;

    -- risky work

    COMMIT TRAN;
END TRY
BEGIN CATCH
    IF XACT_STATE() = -1
        ROLLBACK TRAN;

    IF XACT_STATE() = 1
        ROLLBACK TRAN;

    SELECT ERROR_MESSAGE() AS error_message;
END CATCH;
```

實務上可以簡化成「只要 `XACT_STATE() <> 0` 就回滾」，但理解 `1` 與 `-1` 的差別很重要。

## `RAISERROR` vs `THROW`

課程裡很明確提到：Microsoft 現在更推薦 `THROW`。

### `RAISERROR`

```sql
RAISERROR('No staff member with such id.', 16, 1);
RAISERROR('No %s with id %d.', 16, 1, 'staff member', 15);
```

特點：

- 支援格式化 placeholder
- 舊式 codebase 很常見

### `THROW`

```sql
THROW 52000, 'This is an example', 1;
```

或在 `CATCH` 裡直接重拋：

```sql
BEGIN CATCH
    THROW;
END CATCH;
```

`THROW` 的好處是語意更直接，也更符合新式 SQL Server 寫法。

## Choosing Between `RAISERROR` and `THROW`

- 新程式優先想 `THROW`
- 舊系統若大量用格式化錯誤字串，仍可能看到 `RAISERROR`
- 想保留原始錯誤時，在 `CATCH` 裡直接 `THROW;` 很實用

## Error Info Functions

在 `CATCH` 裡常用的 error functions 包括：

- `ERROR_MESSAGE()`
- `ERROR_NUMBER()`
- `ERROR_LINE()`
- `ERROR_PROCEDURE()`

例如：

```sql
BEGIN CATCH
    SELECT
        ERROR_NUMBER() AS error_number,
        ERROR_MESSAGE() AS error_message,
        ERROR_LINE() AS error_line,
        ERROR_PROCEDURE() AS error_procedure;
END CATCH;
```

這很適合記錄到 audit / error table。

## Nested `TRY...CATCH`

課程裡也展示了 nested `TRY...CATCH`。  
實務上重點不是把層數寫多，而是理解：

- 內層可以處理自己的錯誤
- 外層可再補 fallback 邏輯
- 錯誤資訊要盡量在最靠近出錯點的地方先保留

## `XACT_ABORT`

`SET XACT_ABORT ON` 會影響錯誤發生時 transaction 的行為。

一個很重要的實務提醒是：它和 `RAISERROR` / `THROW` 的互動不完全一樣，所以不要只背其中一邊的範例就套到所有錯誤來源。

如果你在 transaction 裡高度重視「一旦出錯就快速失敗並回滾」，`XACT_ABORT` 值得特別了解。

## Practical Safe Template

```sql
BEGIN TRY
    BEGIN TRAN;

    -- business statements

    COMMIT TRAN;
END TRY
BEGIN CATCH
    IF XACT_STATE() <> 0
        ROLLBACK TRAN;

    SELECT
        ERROR_NUMBER() AS error_number,
        ERROR_MESSAGE() AS error_message,
        ERROR_LINE() AS error_line;

    THROW;
END CATCH;
```

這個模板的價值是：

- 保證 transaction 不會懸掛
- 先清理 transaction 狀態
- 保留足夠診斷資訊
- 最後把錯誤往外拋給呼叫端

## Practical Reminders

- `@@TRANCOUNT` 告訴你有沒有 transaction，但 `XACT_STATE()` 才告訴你還能不能提交。
- 新 code 優先考慮 `THROW`。
- `CATCH` 裡先處理 transaction 狀態，再談記錄或重拋。
- 不要只靠巢狀 transaction 名稱推理 commit 行為，先確認 `@@TRANCOUNT` 的實際效果。

[Back to Databases](README.md)
