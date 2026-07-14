# SQL Server Basics

這篇整理 SQL Server 入門時最常碰到、但不一定會出現在通用 SQL 教材裡的基本習慣。重點不是把 `SELECT`、`GROUP BY` 全部重講，而是把 T-SQL 初學者最常看到的 `TOP`、基本 CRUD、以及 join 使用習慣先整理清楚。

## SQL Server and T-SQL

先分兩層理解：

- SQL Server：Microsoft 的 relational database system
- T-SQL：SQL Server 常用的 SQL dialect，也就是 Transact-SQL

很多查詢觀念仍然是通用 SQL，但在語法細節上，SQL Server 會有自己的寫法。

## `TOP` Instead of `LIMIT`

在 SQL Server 裡，取前幾筆資料很常用 `TOP`，而不是 `LIMIT`。

```sql
SELECT TOP (5) artist
FROM artists;
```

這和其他系統常見的：

```sql
SELECT artist
FROM artists
LIMIT 5;
```

概念相近，但語法位置不同。

### `TOP ... PERCENT`

SQL Server 也支援用百分比取樣：

```sql
SELECT TOP (5) PERCENT artist
FROM artists;
```

這種寫法在跨資料庫 SQL 裡比較少見，所以如果你要寫 portable query，要先確認目標系統是否支援。

### `TOP` Should Usually Pair with `ORDER BY`

如果你想要的是「最新 10 筆」、「最早 10 筆」、「最高分前 10 筆」，一定要搭配 `ORDER BY`。

```sql
SELECT TOP (10) product_id, year_intro
FROM products
ORDER BY year_intro DESC, product_id;
```

重點是：

- `TOP` 只負責裁列數
- `ORDER BY` 才負責定義哪幾列會被留下

如果沒有排序，`TOP` 的結果通常只適合快速 preview，不適合業務判讀。

### Mixed Sort Directions

`ORDER BY` 可以對不同欄位指定不同方向：

```sql
SELECT TOP (10)
  appearances,
  year_intro
FROM products
ORDER BY
  year_intro DESC,
  appearances DESC;
```

這在 top-N 排序裡很常見，因為第一欄決定主排序，第二欄拿來打破 tie。

## Basic DDL: `CREATE TABLE`

SQL Server 入門最常見的 DDL 是建立表：

```sql
CREATE TABLE test_table (
  test_date DATE,
  test_name VARCHAR(20),
  test_int  INT
);
```

建立表時最先要想的通常是：

- table / column 命名
- 每個欄位存什麼型別
- 欄位長度與精度是否足夠

這些雖然不只 SQL Server 需要，但在 T-SQL 練習裡很常一起出現。

## Basic DML: `INSERT`, `UPDATE`, `DELETE`

### `INSERT`

最穩的做法通常是明確列欄位：

```sql
INSERT INTO table_name (col1, col2, col3)
VALUES ('value1', 'value2', value3);
```

這比省略欄位名稱更安全，因為：

- 可讀性更高
- schema 變動時比較不容易 silently 出錯

### `INSERT ... SELECT`

SQL Server 很常直接把查詢結果寫進另一張表：

```sql
INSERT INTO table_name (col1, col2, col3)
SELECT
  column1,
  column2,
  column3
FROM other_table
WHERE some_condition = 1;
```

實務上很重要的一個習慣是：

- 不要偷懶寫 `SELECT *`
- 明確列出來源與目標欄位

這能避免來源表結構調整後，匯入邏輯悄悄錯位。

### `UPDATE`

```sql
UPDATE table_name
SET
  column1 = value1,
  column2 = value2
WHERE some_key = 123;
```

最重要的提醒不是語法，而是：

- `UPDATE` 前先確認 `WHERE`
- 沒有 `WHERE` 往往代表你要更新整張表

### `DELETE`

```sql
DELETE
FROM table_name
WHERE some_key = 123;
```

和 `UPDATE` 一樣，真正的風險通常不是不會寫，而是忘了 `WHERE`。

## `DELETE` vs. `TRUNCATE TABLE`

如果你要清掉整張表，SQL Server 常見兩種操作：

```sql
DELETE FROM table_name;
```

或：

```sql
TRUNCATE TABLE table_name;
```

可以先這樣記：

- `DELETE`: row-level delete，通常可加 `WHERE`
- `TRUNCATE TABLE`: 一次清空整張表，不是逐列刪

所以：

- 如果你要刪部分資料，用 `DELETE ... WHERE ...`
- 如果你明確要清空整張 staging / temp-like table，`TRUNCATE TABLE` 會更直接

不過在正式資料表上動 `TRUNCATE` 前，仍要先確認資料生命週期與權限設計。

## Join Mental Model

這份入門課也很強調 SQL Server 裡的 join 基礎。雖然 join 不是 SQL Server 專屬，但有幾個實務習慣值得留下。

### `INNER JOIN`

```sql
SELECT
  album.album_id,
  album.title,
  artist.name
FROM album
INNER JOIN artist
  ON artist.artist_id = album.artist_id;
```

`INNER JOIN` 只保留兩邊都有 match 的列。

### `LEFT JOIN`

```sql
SELECT
  Admitted.Patient_ID,
  Admitted,
  Discharged
FROM Admitted
LEFT JOIN Discharged
  ON Discharged.Patient_ID = Admitted.Patient_ID;
```

`LEFT JOIN` 會保留左表全部資料，右表沒有 match 時補 `NULL`。

這通常是分析最常用的 outer join，因為：

- 比較符合「主資料表 + 補充資料表」的閱讀方向
- 可以直接看出哪些資料沒有 match

### `RIGHT JOIN`

```sql
SELECT
  Admitted.Patient_ID,
  Admitted,
  Discharged
FROM Discharged
RIGHT JOIN Admitted
  ON Admitted.Patient_ID = Discharged.Patient_ID;
```

`RIGHT JOIN` 和 `LEFT JOIN` 在邏輯上常可互換，只是主表寫在另一邊。

實務上很多團隊會偏好：

- 盡量用 `LEFT JOIN`
- 透過調整表順序，避免過度依賴 `RIGHT JOIN`

這樣通常比較好讀，也比較容易維持 join chain 的一致方向。

### When No Match Appears

在 outer join 結果裡看到 `NULL`，通常不是錯誤，而是在告訴你：

- 主表有這筆資料
- 但對應的 join table 沒有找到 match

這正是 outer join 很有價值的地方。

## Practical Reminders

- 在 SQL Server 中，先把 `TOP` 當成 `LIMIT` 的對應心智模型。
- `TOP` 要有業務意義，通常就必須搭配 `ORDER BY`。
- `INSERT ... SELECT` 不要配 `SELECT *`，欄位請明確列出。
- `UPDATE` 與 `DELETE` 前先確認 `WHERE`，這比背語法更重要。
- `TRUNCATE TABLE` 是清空整張表，不適合當成一般條件刪除的替代品。
- `RIGHT JOIN` 雖然可用，但很多情況改寫成 `LEFT JOIN` 會更直觀。

[Back to Databases](README.md)
