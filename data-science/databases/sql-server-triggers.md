# SQL Server Triggers

這篇整理 SQL Server 中 trigger 的用途、類型與維護方式。trigger 很強，但也很容易把商業邏輯藏進資料庫裡，讓除錯與效能分析變得更困難，所以適合把它當成一種要謹慎使用的機制，而不是預設解法。

## What a Trigger Is

trigger 是一種特殊的 stored procedure，會在特定資料庫事件發生時自動執行。

常見事件類型包括：

- DML: `INSERT`, `UPDATE`, `DELETE`
- DDL: `CREATE`, `ALTER`, `DROP`
- `LOGON`

## Main Trigger Categories

### By Scope

- table / view trigger
- database-level trigger
- server-level trigger

### By Behavior

- `AFTER`: 原始語句先成功執行，再執行 trigger
- `INSTEAD OF`: 阻止原始語句，改由 trigger 內的替代邏輯執行

心智模型上，`AFTER` 比較像 post-action hook，`INSTEAD OF` 比較像 interception layer。

## Basic `AFTER` Trigger

```sql
CREATE TRIGGER ProductsTrigger
ON Products
AFTER INSERT
AS
  PRINT 'An insert of data was made in the Products table.';
```

適合用在：

- 寫入 audit trail
- 補同步歷史表
- 在成功變更後觸發後續資料清理或通知

## `inserted` and `deleted`

SQL Server 的 DML trigger 會自動提供兩張特殊表：

- `inserted`
- `deleted`

它們不是永久表，而是 trigger 執行期間可用的邏輯資料集。

| Trigger event | `inserted` | `deleted` |
| --- | --- | --- |
| `INSERT` | new rows | none |
| `UPDATE` | new version of rows | old version of rows |
| `DELETE` | none | removed rows |

這是理解 SQL Server trigger 的核心。  
尤其要記得 trigger 是 statement-level，不是 row-level，所以 `inserted` / `deleted` 可能同時包含多列，不能只用 scalar 心態寫。

### Example: Archive Deleted Rows

```sql
CREATE TRIGGER TrackRetiredProducts
ON Products
AFTER DELETE
AS
  INSERT INTO RetiredProducts (Product, Measure)
  SELECT Product, Measure
  FROM deleted;
```

這個模式很常見，因為刪除後原表資料已不在，但 `deleted` 還保存被移除的列內容，可拿來寫歷史表。

## `INSTEAD OF` Triggers

`INSTEAD OF` trigger 會攔截原始操作，常見用途是禁止某些變更，或把操作轉成受控版本。

```sql
CREATE TRIGGER PreventDiscountsDelete
ON Discounts
INSTEAD OF DELETE
AS
  PRINT 'Deleting discounts is not allowed.';
```

適合場景：

- 防止刪除敏感資料
- 防止更新關鍵欄位
- 對 view 提供可控寫入邏輯
- 在真正寫入前先做驗證

### Example: Validate Before Insert

```sql
CREATE TRIGGER ConfirmStock
ON Orders
INSTEAD OF INSERT
AS
  IF EXISTS (
    SELECT 1
    FROM Products AS p
    INNER JOIN inserted AS i
      ON i.Product = p.Product
    WHERE i.Quantity > p.Quantity
  )
  BEGIN
    PRINT 'Insufficient stock.';
  END
  ELSE
  BEGIN
    INSERT INTO Orders (Customer, Product, Quantity, OrderDate, TotalAmount)
    SELECT Customer, Product, Quantity, OrderDate, TotalAmount
    FROM inserted;
  END;
```

這種設計能把寫入規則留在資料庫層，但也代表應用程式端不一定一眼看得出資料被攔截的原因。

## Common Use Cases

### Data Integrity and Business Rules

trigger 可直接在資料庫層阻止不合法的變更，例如：

- 不允許刪除關鍵客戶
- 不允許更新特定狀態訂單
- 不允許建立或刪除某些 schema objects

### Auditing

trigger 很常被用來建立 audit trail。

```sql
CREATE TRIGGER OrdersAudit
ON Orders
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
  DECLARE @Insert bit = 0;
  DECLARE @Delete bit = 0;

  IF EXISTS (SELECT * FROM inserted) SET @Insert = 1;
  IF EXISTS (SELECT * FROM deleted) SET @Delete = 1;

  INSERT INTO OrdersAuditLog (action_type, changed_at)
  VALUES (
    CASE
      WHEN @Insert = 1 AND @Delete = 1 THEN 'UPDATE'
      WHEN @Insert = 1 THEN 'INSERT'
      WHEN @Delete = 1 THEN 'DELETE'
    END,
    SYSDATETIME()
  );
END;
```

如果只是要知道誰做了什麼、何時做，這種方式很直接；但若 audit 要求高可靠性與低 overhead，通常也要比較 SQL Server 原生 auditing / CDC / temporal tables 等替代方案。

### DDL Auditing with `EVENTDATA()`

DDL trigger 可以監控 schema 變更。

```sql
CREATE TRIGGER DatabaseAudit
ON DATABASE
FOR CREATE_TABLE, ALTER_TABLE, DROP_TABLE
AS
  INSERT INTO DatabaseAuditLog (
    event_type,
    database_name,
    object_name,
    login_name,
    command_text,
    event_time
  )
  VALUES (
    EVENTDATA().value('(/EVENT_INSTANCE/EventType)[1]', 'NVARCHAR(50)'),
    EVENTDATA().value('(/EVENT_INSTANCE/DatabaseName)[1]', 'NVARCHAR(50)'),
    EVENTDATA().value('(/EVENT_INSTANCE/ObjectName)[1]', 'NVARCHAR(100)'),
    EVENTDATA().value('(/EVENT_INSTANCE/LoginName)[1]', 'NVARCHAR(100)'),
    EVENTDATA().value('(/EVENT_INSTANCE/TSQLCommand/CommandText)[1]', 'NVARCHAR(MAX)'),
    EVENTDATA().value('(/EVENT_INSTANCE/PostTime)[1]', 'DATETIME')
  );
```

這種寫法很適合追蹤誰改了 table、view 或 procedure。

### Blocking Dangerous Operations

有些 trigger 會直接 rollback 高風險操作。

```sql
CREATE TRIGGER PreventDatabaseDelete
ON ALL SERVER
FOR DROP_DATABASE
AS
BEGIN
  PRINT 'Dropping databases is not allowed.';
  ROLLBACK;
END;
```

這類設計威力很大，也因此更需要清楚的治理與文件。

## Metadata and Discovery

trigger 的難點之一是「不夠顯眼」。查不到它們，團隊就很容易忘記資料庫還有隱性邏輯。

### Database-level Trigger Metadata

```sql
SELECT *
FROM sys.triggers;
```

常用欄位：

- `name`
- `parent_class_desc`
- `create_date`
- `modify_date`
- `is_disabled`
- `is_instead_of_trigger`

### Server-level Trigger Metadata

```sql
SELECT *
FROM sys.server_triggers;
```

### Event Mapping

```sql
SELECT *
FROM sys.trigger_events;
```

當你需要知道 trigger 綁定哪些事件，例如 `INSERT`, `UPDATE`, `DROP_TABLE`，這張系統表很有用。

## Lifecycle Operations

### Disable / Enable

```sql
DISABLE TRIGGER PreventNewDiscounts ON Products;
ENABLE TRIGGER PreventNewDiscounts ON Products;
```

database-level 與 server-level trigger 也可以用對應 scope 操作：

```sql
DISABLE TRIGGER PreventViewsModifications ON DATABASE;
ENABLE TRIGGER PreventViewsModifications ON DATABASE;

DISABLE TRIGGER DisallowLinkedServers ON ALL SERVER;
ENABLE TRIGGER DisallowLinkedServers ON ALL SERVER;
```

### Alter

```sql
ALTER TRIGGER PreventOrdersUpdate
ON Orders
INSTEAD OF UPDATE
AS
  PRINT 'Orders cannot be updated directly.';
```

### Drop

```sql
DROP TRIGGER PreventNewDiscounts;
DROP TRIGGER PreventViewsModifications ON DATABASE;
DROP TRIGGER DisallowLinkedServers ON ALL SERVER;
```

## Advantages

- 可直接在資料庫層保護資料完整性
- 能統一執行 business rule，不依賴單一應用程式
- 適合建立 audit 與 change tracking
- 對 DDL / server event 也能攔截或記錄

## Disadvantages

- 邏輯不夠顯眼，client app 往往看不到
- 除錯時不容易追到 trigger 副作用
- 容易把商業規則藏成隱性耦合
- 寫得不好會造成額外 server overhead
- 多列操作若用單列思維去寫，很容易出錯

## Practical Guidance

- 優先把 trigger 當成資料庫治理工具，不是一般應用邏輯的預設承載層
- 寫 trigger 時預設一次會處理多列，不要假設只有一列被修改
- 重要 trigger 一定要補文件，至少說明 scope、event、目的與副作用
- 定期查 `sys.triggers` / `sys.server_triggers`，避免系統裡存在被遺忘的隱性規則
- 如果只是單純資料驗證，先比較 constraint、default、computed column 或 application-layer validation 是否更簡單

## Mental Checklist

- 這個需求真的需要 trigger 嗎
- 應該用 `AFTER` 還是 `INSTEAD OF`
- 是否正確使用 `inserted` / `deleted`
- 多列操作會不會壞掉
- 是否需要 audit、rollback 或通知
- 團隊是否能夠看見並維護這段隱性邏輯
