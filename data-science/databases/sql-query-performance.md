[Data Science](../README.md) › [Databases](README.md) › 查詢效能

# 查詢效能 (SQL Query Performance)

查詢變慢時，先量測、再看執行計畫、最後才改寫或加 index。寫出來的 SQL 只描述「要什麼」，planner / optimizer 決定「怎麼做」；效能問題通常出在它選的路徑，或你給它的輸入太大。

## 診斷流程

```
1. 寫清楚：只選需要的欄、先過濾再 join、確認 join 沒有膨脹
        ↓
2. 看計畫：EXPLAIN（預估）→ EXPLAIN ANALYZE（實際執行）
        ↓
3. 找最貴的節點：全表掃描、大量排序、預估列數 ≠ 實際列數
        ↓
4. 改寫查詢 / 更新統計 / 加 index
        ↓
5. 重新量測：多跑幾次比趨勢（第一次常是冷快取）
```

| | PostgreSQL | SQL Server |
| --- | --- | --- |
| 預估計畫 | `EXPLAIN` | Estimated Execution Plan（SSMS Ctrl+L） |
| 實際計畫 | `EXPLAIN (ANALYZE, BUFFERS)` | Actual Execution Plan（Ctrl+M）+ `SET STATISTICS TIME, IO ON` |
| 主要指標 | actual time、rows、`Buffers: shared hit/read` | CPU / elapsed time、**logical reads**（讀了幾個 8 KB 頁） |
| 全表掃描 | `Seq Scan` | `Table Scan` / `Clustered Index Scan` |
| 用到 index | `Index Scan`、`Index Only Scan`、`Bitmap Heap Scan` | `Index Seek` |
| 更新統計 | `ANALYZE table;` | `UPDATE STATISTICS table;` |
| 列出 index | `SELECT * FROM pg_indexes WHERE tablename = 't';` | `EXEC sp_helpindex 't';` |

## 讀 `EXPLAIN ANALYZE`

```sql
EXPLAIN (ANALYZE, BUFFERS)              -- ANALYZE 會真的執行；寫入語句包在 BEGIN ... ROLLBACK 裡測
SELECT c.name, a.species
FROM cheeses AS c
JOIN animals AS a ON c.species = a.species
WHERE c.age > 10;
```

```
Hash Join  (cost=1.09..2.30 rows=4 width=64) (actual time=0.03..0.04 rows=37 loops=1)
  Hash Cond: (c.species = a.species)
  ->  Seq Scan on cheeses c  (cost=0.00..1.12 rows=4 width=64) (actual ... rows=37 loops=1)
        Filter: (age > 10)
        Rows Removed by Filter: 3
  ->  Hash  ...
Planning Time: 0.1 ms
Execution Time: 0.1 ms
```

| 看什麼 | 怎麼解讀 |
| --- | --- |
| 由內往外讀 | 縮排最深的節點先執行，結果往上傳 |
| `cost=啟動..總成本` | planner 的相對估計值，不是毫秒；只能比較同一查詢的不同計畫 |
| `rows`（預估）vs `actual rows` | 差 10 倍以上表示統計資訊不準或條件太複雜，planner 可能選錯 join 方式 → 先 `ANALYZE` |
| `loops` | 節點執行次數；實際總列數 = rows × loops（Nested Loop 內側常很大） |
| `Rows Removed by Filter` | 讀了又丟掉的列多 → 可能需要 index |
| `Sort Method: external merge Disk` | 排序記憶體不夠寫到磁碟；減少輸入或調 `work_mem` |
| `Buffers: shared read` | 從磁碟讀的頁數；`hit` 是快取命中 |

### 常見節點

| 節點（PostgreSQL / SQL Server） | 何時出現 | 何時是問題 |
| --- | --- | --- |
| `Seq Scan` / `Table Scan` | 讀整張表 | 大表只取少數列時；小表或要讀大部分列時反而最快 |
| `Index Scan` / `Index Seek` | 依 index 定位少量列 | 選擇性低（要讀大半張表）時比 seq scan 慢 |
| `Index Only Scan` | 需要的欄全在 index 內 | — |
| `Nested Loop` / `Nested Loops` | 一側小、另一側能用 index 查 | 兩側都大時很慢（常是預估列數錯誤） |
| `Hash Join` / `Hash Match` | 大表等值 join | 記憶體不足時溢出到磁碟 |
| `Merge Join` | 兩側已排序 | 需要額外排序時 |
| `Sort` | `ORDER BY`、`DISTINCT`、`UNION`、merge join | 輸入很大時 |
| `HashAggregate` / `GroupAggregate` | `GROUP BY` | — |

## Index

B-tree index 是依 key 排序的結構，讓查詢從 O(n) 的全表掃描變成 O(log n) 的定位。代價是額外空間與每次寫入都要維護。

```sql
CREATE INDEX idx_variants_gene ON variants (gene_id);                  -- 單欄
CREATE INDEX idx_variants_chrom_pos ON variants (chrom, pos);          -- 複合：順序重要
CREATE INDEX idx_lab_patient ON lab_results (patient_id) INCLUDE (test_date, value);  -- covering（PG 11+、SQL Server）
CREATE INDEX idx_orders_open ON orders (created_at) WHERE status = 'open';           -- partial（PG、SQL Server filtered index）
CREATE INDEX CONCURRENTLY idx_x ON big_table (x);                      -- PostgreSQL：不鎖表建立（不能在交易內）
```

| 適合建 index | 不划算 |
| --- | --- |
| 大表上常出現在 `WHERE`、`JOIN ... ON`、`ORDER BY` 的欄位 | 小表（整張讀比較快） |
| 選擇性高（每個值只對應少數列）：ID、日期 | 選擇性低：性別、布林、只有幾種值的狀態 |
| 外鍵欄（PostgreSQL 不會自動建） | 寫入遠多於讀取的表（每個 index 都拖慢 INSERT / UPDATE） |

**複合 index 的最左前綴**：`(chrom, pos)` 能用在 `WHERE chrom = 'chr1'`、`WHERE chrom = 'chr1' AND pos BETWEEN ...`，但不能用在只有 `WHERE pos = 123`。等值條件的欄放前面、範圍條件的欄放後面。

### 讓 index 失效的寫法

| 寫法 | 問題 | 改法 |
| --- | --- | --- |
| `WHERE YEAR(order_date) = 2024` | 對欄位套函式，無法比對排序好的 key | `WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01'` |
| `WHERE LOWER(email) = 'a@b.com'` | 同上 | 建 expression index：`CREATE INDEX ON users (LOWER(email))` |
| `WHERE name LIKE '%son'` | 開頭是萬用字元 | 前綴比對 `'Jo%'`；全文 / 子字串搜尋用 `pg_trgm` 或全文索引 |
| `WHERE id_text = 123` | 隱含型別轉換 | 兩邊型別一致 |
| `WHERE a = 1 OR b = 2` | 單一 index 難以涵蓋 | 兩欄各自有 index（bitmap OR），或改寫成 `UNION ALL` |
| `WHERE price * 1.05 > 100` | 欄位在運算式內 | 移項：`price > 100 / 1.05` |

### Clustered vs nonclustered（SQL Server）

| | Clustered | Nonclustered |
| --- | --- | --- |
| 比喻 | 字典本身依字母排序 | 書末索引，指回內文頁碼 |
| 資料頁 | 依 key 實際排序存放 | 另存一份排序結構，指向資料列 |
| 數量 | 每表一個（通常是主鍵） | 多個 |
| 適合 | 範圍查詢、依 key 順序讀取 | 特定欄位的查找 |

PostgreSQL 沒有持續維持的 clustered index（`CLUSTER` 指令只排序一次）；資料表是 heap，所有 index 都是另外的結構。

## 改寫查詢

| 手法 | 說明 |
| --- | --- |
| 不用 `SELECT *` | 只取需要的欄；欄式資料庫（Snowflake、BigQuery、DuckDB）掃描量直接下降，也讓 index-only scan 成為可能 |
| 先過濾再 join / 聚合 | 縮小 join 與 `GROUP BY` 的輸入 |
| 檢查 join 膨脹 | 列數暴增時後面每一步都變慢（見 [列數膨脹](sql-joins-and-set-operations.md#列數膨脹-fan-out)） |
| 存在性用 `EXISTS` | 不需要右表欄位時，比 `JOIN` + `DISTINCT` 少做很多事 |
| 相關子查詢 → window function | 避免每列重算一次子查詢 |
| `UNION` → `UNION ALL` | 確定不重複時省掉去重排序 |
| 中間結果重複使用 | 存成 temp table（可加 index、`ANALYZE`）；CTE 在 PostgreSQL 12+ 預設會被內聯，不保證只算一次 |
| 分頁 | `OFFSET 100000` 仍要先讀過前 10 萬列；改用 keyset：`WHERE id > :last_id ORDER BY id LIMIT 50` |

```sql
-- 中間結果要用多次：temp table
CREATE TEMP TABLE warm_countries AS
SELECT country FROM climate WHERE temp_annual > 22;
ANALYZE warm_countries;

SELECT COUNT(*) FROM athletes AS a JOIN warm_countries AS w USING (country);
```

## 量測的注意事項

- 第一次執行常是冷快取（資料從磁碟讀），之後變快不代表改寫有效；比較時多跑幾次，或比較不受快取影響的指標。
- SQL Server 的 `logical reads` 比 elapsed time 穩定：改寫後從 54 頁降到 18 頁，代表真的少讀了資料，而不是剛好伺服器比較閒。
- `CPU time` 反映查詢本身的運算量；`elapsed time` 還包含等待 I/O、鎖、網路，比較接近使用者的感受。
- 開發環境的小資料上計畫可能完全不同；用接近正式資料量的資料測試。

## 資料量再大

| 手段 | 適用 |
| --- | --- |
| Partitioning（依日期、染色體分區） | 超大表且查詢幾乎都帶分區鍵條件；讓 planner 跳過無關分區（partition pruning） |
| Materialized view | 重複執行的昂貴聚合；需要定期 `REFRESH` |
| 欄式儲存 / 分析資料庫 | 大量聚合、少數欄位：DuckDB、雲端資料倉儲（見 [DuckDB 與 Parquet](duckdb-and-parquet.md)、[雲端資料倉儲](../data-engineering/cloud-data-warehouses.md)） |
| 在資料庫端完成再取回 | 不要 `SELECT *` 拉回 pandas 再過濾（見 [Python 與 SQLAlchemy](python-sqlalchemy.md#先在資料庫端縮小)） |
