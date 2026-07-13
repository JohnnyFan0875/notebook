# PostgreSQL Transactions and Exception Handling

這篇整理 PostgreSQL 裡 transaction 與例外處理的基本心智模型。  
重點不是背所有語法，而是理解什麼時候要把多個 statement 綁在一起、怎麼局部回滾、以及出錯時怎麼保留足夠的診斷資訊。

## Why Transactions Matter

transaction 的核心價值是把多個資料變更當成一個原子單位處理。

典型情境：

- 同一個業務動作需要更新多張表
- 兩個 `UPDATE` 必須同時成功或同時失敗
- 修正資料時不想讓中間狀態被提交

如果少了 transaction，流程中間一旦失敗，就可能留下半套資料。

## Basic Transaction Block

```sql
BEGIN;

UPDATE patient_intake
SET priority = 1
WHERE name = 'Prisha Ahmed';

UPDATE patient_intake
SET priority = 2
WHERE name = 'Oscar Parker';

COMMIT;
```

可以先這樣理解：

- `BEGIN`：開始一個 transaction
- `COMMIT`：把 transaction 內的變更正式提交
- `ROLLBACK`：放棄 transaction 內尚未提交的變更

`BEGIN TRANSACTION;` 與 `BEGIN;` 在日常使用上可視為同義。

## Rollback for Mistakes

如果 transaction 還沒 `COMMIT`，就可以直接回滾：

```sql
BEGIN TRANSACTION;

UPDATE cookies
SET quantity = 13
WHERE name = 'Biscuits';

ROLLBACK;
```

這很適合：

- 手動修資料時發現更新錯了
- 多步驟腳本中途驗證失敗
- 想先試跑修改再決定是否提交

## One Transaction, Multiple Statements

transaction 很重要的一個特性是可以把多個 statement 一起回滾。

```sql
BEGIN TRANSACTION;

UPDATE cookies
SET deliciousness = 11
WHERE name = 'Cats Tongue';

UPDATE cookies
SET deliciousness = 8
WHERE name = 'Gingerbread';

ROLLBACK;
```

如果最後回滾，前面所有尚未提交的更新都會一起取消。

## Partial Undo with Savepoints

有時候你不想整個 transaction 都回滾，只想退回其中一段。這時候就用 `SAVEPOINT`。

```sql
BEGIN TRANSACTION;

UPDATE inventory
SET quantity = quantity - 5
WHERE item_id = 10;

SAVEPOINT inventory_step;

UPDATE shipping_queue
SET status = 'queued'
WHERE item_id = 10;

ROLLBACK TO inventory_step;

COMMIT;
```

心智模型：

- `SAVEPOINT name`：在 transaction 內設一個可退回的位置
- `ROLLBACK TO name`：只回到該 savepoint 之後的狀態
- `RELEASE SAVEPOINT name`：釋放 savepoint

### Savepoint Reminders

- `ROLLBACK` 沒有 `TO` 會回滾整個 transaction。
- `ROLLBACK TO` 指到不存在的 savepoint 會報錯。
- 同一個 transaction 裡，新的同名 savepoint 會遮蔽較早的同名 savepoint。

## Isolation Levels and Concurrency

transaction 不只處理「自己寫錯」的問題，也處理多個 session 同時操作時的可預期性。

PostgreSQL 會透過 isolation level 幫你約束可見性與併發效果。

```sql
START TRANSACTION ISOLATION LEVEL SERIALIZABLE;

UPDATE accounts
SET balance = balance - 100
WHERE account_id = 1;

COMMIT;
```

課程裡特別提到兩個概念：

- isolation level 是幫助你推理結果的規則
- 越嚴格的 isolation 通常意味著越保守的併發行為

實務上先記住：

- `READ COMMITTED` 是很多日常工作負載的常見預設
- `SERIALIZABLE` 追求最強的一致性推理，但衝突與重試成本可能更高

## PL/pgSQL Exception Basics

當你進入 `DO $$ ... $$` block、function 或更程序化的邏輯時，就可以用 `EXCEPTION`。

```sql
DO $$
BEGIN
    PERFORM SQRT('a');
EXCEPTION
    WHEN others THEN
        RAISE INFO 'Boom!';
END;
$$ LANGUAGE plpgsql;
```

這裡的心智模型很像其他語言的 `try ... except`：

- `BEGIN ... END`：主邏輯
- `EXCEPTION`：錯誤處理區
- `WHEN others THEN`：generic catch-all handler

## Catch Specific Errors When Possible

雖然 `WHEN others` 很方便，但實務上更穩的是針對你預期的錯誤分開處理。

例如：

```sql
DO $$
BEGIN
    INSERT INTO sales (name, quantity, cost)
    VALUES ('cookie', -1, NULL);
EXCEPTION
    WHEN check_violation THEN
        RAISE INFO 'Quantity can not be less than 0.';
    WHEN not_null_violation THEN
        RAISE INFO 'Cost can not be null.';
END;
$$ LANGUAGE plpgsql;
```

課程裡明確提到的例子包含：

- `unique_violation`
- `not_null_violation`

這種寫法比全部都用 `WHEN others` 更容易維護，也更容易讓錯誤訊息精準對應業務問題。

## Exception Handlers Have Overhead

一個很實用的提醒是：`EXCEPTION` clause 不是免費的。

- 它會增加執行成本
- 不應把 exception handling 當成一般流程控制的第一選擇

比較好的習慣通常是：

- 能先用 constraint、validation、`WHERE` 條件避免的錯誤，先避免
- 真正需要攔截失敗並記錄時，再加 `EXCEPTION`

## Logging Errors Inside PostgreSQL

有時候只 `RAISE INFO` 還不夠，還想把錯誤寫進表裡。

```sql
DO $$
BEGIN
    UPDATE inventory SET cost = 35.0 WHERE name = 'Macaron';
    UPDATE inventory SET cost = 3.50 WHERE name = 'Panellets';
EXCEPTION
    WHEN others THEN
        INSERT INTO errors (msg) VALUES ('Max cost is 10!');
        RAISE INFO 'Max cost is 10!';
END;
$$ LANGUAGE plpgsql;
```

這種模式適合：

- 保留錯誤歷史
- 讓後續流程或報表可查錯誤記錄
- 在批次工作中留下最小可用診斷資料

## `GET STACKED DIAGNOSTICS`

如果想拿到更完整的錯誤內容，可以在 `EXCEPTION` 裡使用 `GET STACKED DIAGNOSTICS`。

```sql
DO $$
DECLARE
    exc_message TEXT;
    exc_detail  TEXT;
BEGIN
    UPDATE inventory SET cost = 35.0 WHERE name = 'Macaron';
    UPDATE inventory SET cost = 3.50 WHERE name = 'Panellets';
EXCEPTION
    WHEN others THEN
        GET STACKED DIAGNOSTICS
            exc_message = MESSAGE_TEXT,
            exc_detail  = PG_EXCEPTION_DETAIL;

        INSERT INTO errors (msg, detail)
        VALUES (exc_message, exc_detail);
END;
$$ LANGUAGE plpgsql;
```

這通常比手寫固定字串更有用，因為你能保留 PostgreSQL 原生錯誤上下文。

## Useful Diagnostic Fields

這份課程整理了幾個特別值得記的 diagnostics 欄位：

- `RETURNED_SQLSTATE`：錯誤代碼
- `MESSAGE_TEXT`：主要錯誤訊息
- `PG_EXCEPTION_DETAIL`：更細的 detail
- `PG_EXCEPTION_HINT`：可能的 hint
- `PG_EXCEPTION_CONTEXT`：發生錯誤時的呼叫堆疊 / context

如果你要建 `errors` logging table，這幾個欄位通常就很夠用。

```sql
DO $$
DECLARE
    v_state   TEXT;
    v_msg     TEXT;
    v_detail  TEXT;
    v_context TEXT;
BEGIN
    -- some risky work
EXCEPTION WHEN others THEN
    GET STACKED DIAGNOSTICS
        v_state   = RETURNED_SQLSTATE,
        v_msg     = MESSAGE_TEXT,
        v_detail  = PG_EXCEPTION_DETAIL,
        v_context = PG_EXCEPTION_CONTEXT;

    INSERT INTO errors (msg, state, detail, context)
    VALUES (v_msg, v_state, v_detail, v_context);
END;
$$ LANGUAGE plpgsql;
```

## Practical Reminders

- 多個 statement 必須一起成功時，就應該主動想 transaction。
- 想局部回滾時，用 `SAVEPOINT`，不要急著整筆 `ROLLBACK`。
- 例外處理優先針對具體錯誤型別，而不是永遠 `WHEN others`。
- `EXCEPTION` 有成本，避免把它當成一般邏輯分支。
- 如果錯誤值得追蹤，優先記 `SQLSTATE`、message、detail、context，而不只是自訂一句文字。

[Back to Databases](README.md)
