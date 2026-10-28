[Data Science](../README.md) › [Databases](README.md) › 交易與錯誤處理

# 交易與錯誤處理 (Transactions and Error Handling)

交易 (transaction) 讓多個語句**全部成功或全部撤銷**，中途失敗不會留下半套資料（例如扣了庫存卻沒建出貨單、刪了舊樣本表卻沒寫入新表）。概念在各資料庫相同，差異在語法與錯誤處理機制。

## ACID

| 性質 | 意義 | 沒有它會怎樣 |
| --- | --- | --- |
| Atomicity 原子性 | 全部成功或全部撤銷 | 中途失敗留下半套更新 |
| Consistency 一致性 | 交易前後都滿足 constraint（外鍵、`CHECK`、`UNIQUE`） | 出現孤兒列、不合法的值 |
| Isolation 隔離性 | 並行交易互不干擾到什麼程度，由隔離層級決定 | 讀到別人未提交或中途改變的資料 |
| Durability 持久性 | `COMMIT` 後即使當機也不會遺失 | 已回報成功的寫入消失 |

## PostgreSQL vs SQL Server 對照

| 概念 | PostgreSQL | SQL Server (T-SQL) |
| --- | --- | --- |
| 開始 / 提交 / 回滾 | `BEGIN;` / `COMMIT;` / `ROLLBACK;` | `BEGIN TRAN;` / `COMMIT TRAN;` / `ROLLBACK TRAN;` |
| 部分回滾 | `SAVEPOINT s;` / `ROLLBACK TO SAVEPOINT s;` | `SAVE TRAN s;` / `ROLLBACK TRAN s;` |
| 捕捉錯誤 | PL/pgSQL `BEGIN ... EXCEPTION WHEN ... THEN ... END` | `BEGIN TRY ... END TRY BEGIN CATCH ... END CATCH` |
| 拋出錯誤 | `RAISE EXCEPTION '...'` | `THROW`（建議）/ `RAISERROR` |
| 錯誤資訊 | `SQLSTATE`、`SQLERRM`、`GET STACKED DIAGNOSTICS` | `ERROR_NUMBER()`、`ERROR_MESSAGE()`、`ERROR_LINE()` |
| 出錯後的交易狀態 | 進入 aborted：之後的語句都失敗，只能 `ROLLBACK`（或回到 savepoint） | 多數錯誤只讓該語句失敗、交易繼續；`SET XACT_ABORT ON` 改成整筆回滾 |
| 檢查交易狀態 | — | `@@TRANCOUNT`、`XACT_STATE()` |
| 預設隔離層級 | `READ COMMITTED` | `READ COMMITTED` |
| 沒寫 `BEGIN` 時 | autocommit：每個語句自成一筆交易 | 同左 |

## 基本操作

```sql
BEGIN;

UPDATE inventory SET quantity = quantity - 5 WHERE item_id = 10;

SAVEPOINT after_inventory;                -- 交易內可退回的位置

UPDATE shipping_queue SET status = 'queued' WHERE item_id = 10;

ROLLBACK TO SAVEPOINT after_inventory;    -- 只撤銷 savepoint 之後的更新

COMMIT;                                   -- inventory 的更新被提交
```

| 指令 | 作用 |
| --- | --- |
| `ROLLBACK` | 撤銷整筆交易 |
| `ROLLBACK TO SAVEPOINT s` | 撤銷 `s` 之後的變更，交易繼續；`s` 不存在會報錯 |
| `RELEASE SAVEPOINT s` | 移除 savepoint（不撤銷變更） |
| 同名 savepoint | 新的遮蔽舊的；釋放新的之後舊的又可用 |

> 手動修資料時的保險：`BEGIN;` → `UPDATE ...` → 用 `SELECT` 檢查結果與影響列數 → 確定才 `COMMIT;`，不對就 `ROLLBACK;`。

## 隔離層級

並行交易可能產生的異常，以及各層級能防止哪些：

| 異常 | 情境 |
| --- | --- |
| dirty read | 讀到別人**尚未提交**的變更（對方之後可能回滾） |
| non-repeatable read | 同一交易內讀同一列兩次，中間被別人改掉而值不同 |
| phantom read | 同一條件查兩次，中間別人插入新列而列數不同 |
| serialization anomaly | 每筆交易單獨看都合理，並行結果卻不等於任何一種依序執行的結果 |

| 隔離層級 | dirty | non-repeatable | phantom | serialization |
| --- | --- | --- | --- | --- |
| `READ UNCOMMITTED` | 可能（PostgreSQL 視同 `READ COMMITTED`） | 可能 | 可能 | 可能 |
| `READ COMMITTED`（預設） | 防止 | 可能 | 可能 | 可能 |
| `REPEATABLE READ` | 防止 | 防止 | 標準允許；PostgreSQL 防止 | 可能 |
| `SERIALIZABLE` | 防止 | 防止 | 防止 | 防止 |

```sql
BEGIN ISOLATION LEVEL SERIALIZABLE;      -- PostgreSQL；也可 BEGIN; SET TRANSACTION ISOLATION LEVEL ...
UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;
COMMIT;
```

越嚴格越安全，但衝突越多：`SERIALIZABLE` 下衝突的交易會以 serialization failure（SQLSTATE `40001`）失敗，**應用程式必須準備重試**。分析查詢多半只讀，預設的 `READ COMMITTED` 即可；需要多個查詢看到同一個快照時用 `REPEATABLE READ`。

## PostgreSQL：PL/pgSQL 例外處理

`EXCEPTION` 只能用在 PL/pgSQL 區塊（`DO $$ ... $$` 或 function）裡，行為類似 `try ... except`：出錯時區塊內的變更**自動回滾**到區塊開始時（隱含 savepoint），再執行 handler。

```sql
DO $$
DECLARE
    v_state   TEXT;
    v_msg     TEXT;
    v_detail  TEXT;
    v_context TEXT;
BEGIN
    INSERT INTO sales (name, quantity, cost) VALUES ('cookie', -1, NULL);
EXCEPTION
    WHEN check_violation THEN                  -- 1. 先處理預期的特定錯誤
        RAISE NOTICE 'Quantity can not be less than 0.';
    WHEN not_null_violation THEN
        RAISE NOTICE 'Cost can not be null.';
    WHEN others THEN                           -- 2. 其他錯誤：保留完整診斷資訊再記錄
        GET STACKED DIAGNOSTICS
            v_state   = RETURNED_SQLSTATE,
            v_msg     = MESSAGE_TEXT,
            v_detail  = PG_EXCEPTION_DETAIL,
            v_context = PG_EXCEPTION_CONTEXT;
        INSERT INTO errors (state, msg, detail, context)
        VALUES (v_state, v_msg, v_detail, v_context);
        RAISE;                                 -- 3. 記錄後重新拋出，不要吞掉錯誤
END;
$$ LANGUAGE plpgsql;
```

| 常用條件名 | SQLSTATE | 何時 |
| --- | --- | --- |
| `unique_violation` | `23505` | 違反 `UNIQUE` / 主鍵 |
| `foreign_key_violation` | `23503` | 外鍵找不到 |
| `not_null_violation` | `23502` | `NOT NULL` 欄為空 |
| `check_violation` | `23514` | 違反 `CHECK` |
| `division_by_zero` | `22012` | 除以零 |
| `serialization_failure` | `40001` | 隔離衝突，應重試 |

| 診斷欄位 | 內容 |
| --- | --- |
| `RETURNED_SQLSTATE` | 錯誤代碼 |
| `MESSAGE_TEXT` | 主要訊息 |
| `PG_EXCEPTION_DETAIL` / `PG_EXCEPTION_HINT` | 細節 / 提示 |
| `PG_EXCEPTION_CONTEXT` | 發生位置的呼叫堆疊 |

> `EXCEPTION` 區塊有成本（每次進入都建立 savepoint）。能用 constraint、`WHERE` 條件或 `ON CONFLICT` 事先避免的錯誤，不要靠例外處理當流程控制。另外，若 handler 把錯誤寫進 `errors` 表後沒有重新拋出，外層交易仍會提交，呼叫端以為成功了。

## SQL Server：`TRY...CATCH`

```sql
SET XACT_ABORT ON;                     -- 任何執行期錯誤都讓整筆交易變成 doomed，避免部分提交

BEGIN TRY
    BEGIN TRAN;

    UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;
    UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;

    COMMIT TRAN;
END TRY
BEGIN CATCH
    IF XACT_STATE() <> 0               -- 1. 先清理交易狀態
        ROLLBACK TRAN;

    INSERT INTO error_log (number, message, line, proc_name)   -- 2. 記錄（在回滾之後，才不會一起被撤銷）
    VALUES (ERROR_NUMBER(), ERROR_MESSAGE(), ERROR_LINE(), ERROR_PROCEDURE());

    THROW;                             -- 3. 重新拋出原始錯誤給呼叫端
END CATCH;
```

| 函式 / 設定 | 值 | 意義 |
| --- | --- | --- |
| `@@TRANCOUNT` | `BEGIN TRAN` +1、`COMMIT` −1、`ROLLBACK` 歸 0 | 有沒有開著的交易（巢狀時看層數） |
| `XACT_STATE()` | `1` | 有交易且可提交 |
| | `-1` | 有交易但已 doomed，只能回滾 |
| | `0` | 沒有交易 |
| `SET XACT_ABORT ON` | | 執行期錯誤時自動回滾整筆交易；遠端 / 分散式交易時必要 |

| | `THROW` | `RAISERROR` |
| --- | --- | --- |
| 建議 | 新程式使用 | 舊程式碼常見 |
| 語法 | `THROW 52000, 'No staff member with such id.', 1;`（錯誤號 ≥ 50000） | `RAISERROR('No %s with id %d.', 16, 1, 'staff', 15);` |
| 在 `CATCH` 重拋原錯誤 | `THROW;` | 無法原樣重拋 |
| 格式化字串 | 先用 `FORMATMESSAGE()` 組好 | 內建 `%s`、`%d` |
| 中斷批次 | 是 | 依嚴重度，severity 16 不會中斷 |

> 巢狀 `BEGIN TRAN` 不是真正的巢狀交易：內層 `COMMIT` 只把 `@@TRANCOUNT` 減 1，真正提交要等最外層；任何一層 `ROLLBACK`（不帶 savepoint 名稱）都會撤銷全部。需要局部回滾時用 `SAVE TRAN`。

## 從 Python 控制交易

```python
from sqlalchemy import create_engine, text

engine = create_engine("postgresql+psycopg://user:pw@host/db")

# engine.begin()：區塊正常結束自動 COMMIT，拋出例外自動 ROLLBACK
with engine.begin() as conn:
    conn.execute(text("UPDATE inventory SET quantity = quantity - :n WHERE item_id = :id"),
                 {"n": 5, "id": 10})
    conn.execute(text("INSERT INTO shipping_queue (item_id, status) VALUES (:id, 'queued')"),
                 {"id": 10})
```

SQLAlchemy 2.x 的 `engine.connect()` 不會自動提交，寫入後要呼叫 `conn.commit()`；詳見 [Python 與 SQLAlchemy](python-sqlalchemy.md#交易與寫入)。R 用 `DBI::dbWithTransaction(con, { ... })`。
