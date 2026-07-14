# SQL Server Query Performance

這篇整理 SQL Server 查詢效能調校時最常用的觀察點。重點不是一開始就改 schema 或狂加 index，而是先用 SQL Server 自帶的統計與 execution plan 看出瓶頸在哪裡。

## 一個實用的診斷順序

1. 先把 query 改到容易閱讀
2. 確認過濾條件與 join 條件是否能提早縮小資料量
3. 開啟 `STATISTICS TIME` 與 `STATISTICS IO`
4. 看 estimated execution plan
5. 再決定要不要補 index、改寫查詢，或調整資料存放方式

## 先把查詢寫清楚

效能調校前，先把 SQL 寫成自己看得懂的版本。  
很多慢 query 的問題，不是 optimizer 太神秘，而是查詢本身把條件、子查詢與計算欄位塞得太亂。

例如：

- 避免不必要的 `SELECT *`
- 讓 join 條件與 filter 條件分開排版
- 先確認 `WHERE` 是否在最有效的地方縮小資料集

## `WHERE` 的處理順序很重要

SQL Server 的 `WHERE` 先於 `SELECT` 別名處理，所以這種寫法會出錯：

```sql
SELECT
  PlayerName,
  Team,
  DRebound + ORebound AS TotalRebounds
FROM PlayerStats
WHERE TotalRebounds >= 1000
ORDER BY TotalRebounds DESC;
```

如果過濾條件依賴計算欄位，應改成：

- 直接在 `WHERE` 重寫運算式
- 或先包成子查詢 / CTE，再在外層過濾

這不只是語法問題，也會影響 query shape 與 optimizer 的選擇空間。

## `SET STATISTICS TIME ON`

第一個常用工具是時間統計：

```sql
SET STATISTICS TIME ON;

SELECT ...
FROM ...
WHERE ...;

SET STATISTICS TIME OFF;
```

常見輸出會包含：

- `CPU time`
- `elapsed time`

### 怎麼看 `CPU time` 與 `elapsed time`

- `CPU time`: server processor 真正花在處理 query 的時間
- `elapsed time`: 整體經過時間

實務上可以這樣理解：

- `elapsed time` 比較接近使用者感受到的慢不慢
- `CPU time` 比較適合看查詢本身處理成本

但兩者都不是看一次就下結論。  
同一支 query 可能因為快取、並行、伺服器當下負載不同而波動，所以至少要跑多次看趨勢。

### 不要只看單次測量

一筆 `elapsed time = 2032 ms` 不代表真實水準。  
比較穩的做法是：

- 連跑幾次
- 看平均值
- 比較調整前後的整體趨勢

## `SET STATISTICS IO ON`

第二個核心工具是頁面讀取統計：

```sql
SET STATISTICS IO ON;

SELECT ...
FROM ...
WHERE ...;

SET STATISTICS IO OFF;
```

這會顯示每張表的讀取情況，例如：

- `Scan count`
- `logical reads`
- `physical reads`
- `read-ahead reads`

### `logical reads` 特別重要

SQL Server 以 page 為基本讀取單位，每頁通常是 8 KB。  
`logical reads` 可以理解成 query 為了完成工作，總共讀了多少資料頁。

心智模型上：

- `logical reads` 越高，通常表示 query 接觸的資料範圍越大
- 如果改寫 query 後 `logical reads` 明顯下降，通常是很有價值的改善

很多時候，`logical reads` 比單次 elapsed time 更穩定，因為它比較不受當下機器忙碌程度影響。

## 什麼是 index

index 本質上是幫資料建立更快的尋找路徑，避免每次都掃整張表。

適合改善的場景通常是：

- 常用在 `WHERE` 條件的欄位
- 常用在 join key 的欄位
- 需要快速定位少量資料列的查詢

但 index 不是免費的，它會增加：

- 額外儲存空間
- insert / update / delete 的維護成本

## Clustered 與 Nonclustered Index

### Clustered index

可以把 clustered index 想成字典：

- 資料頁本身依照 index key 排序
- 一張表只能有一個 clustered index
- 很適合支援範圍查詢與有序存取

### Nonclustered index

可以把 nonclustered index 想成教科書後面的索引：

- index 自己有排序結構
- 指向實際資料頁
- 一張表可以有多個 nonclustered index

這兩種 index 的差別，核心不在名詞，而在資料頁是不是依照 key 本身排列。

## B-tree 心智模型

SQL Server index 常以 B-tree 結構組織，可以粗略理解成：

- root node
- branch nodes
- leaf / page nodes

這種設計讓 SQL Server 不必從第一列一路掃到最後一列，而是可以快速縮小搜尋範圍。

## Table Scan、Index Seek、Index Scan

看 execution plan 時，先學會區分幾種最常見的存取方式：

- `Table Scan`: 整張表掃描
- `Index Scan`: 掃描整個 index 或大範圍 index
- `Index Seek`: 直接定位到較小範圍資料

`Index Seek` 通常比 `Table Scan` 更令人安心，但也不要把它當成唯一目標。  
如果表很小，或條件本來就要讀大部分資料，scan 也可能是合理選擇。

## Execution Plan 要看什麼

execution plan 可以回答很多關鍵問題：

- 有沒有用到 index
- 用了哪種 join
- 是否有 sort
- 哪些 operator 代價最高

在 SSMS 中，estimated execution plan 很適合先看 optimizer 預估會怎麼跑。  
如果還要驗證實際執行狀況，再搭配真正執行與統計輸出一起判讀。

## 常見 operator

### Join operators

執行計畫常見的 join operator 包括：

- `Nested Loops`
- `Hash Match`
- `Merge Join`

通常可以這樣粗略理解：

- `Nested Loops`: 一側較小、另一側可快速查找時常見
- `Hash Match`: 大量資料配對時常見
- `Merge Join`: 雙方已排序或容易排序時可能出現

### `Sort`

如果 query 有 `ORDER BY`、`DISTINCT` 或某些聚合操作，常會看到 `Sort`。  
sort 本身可能就是成本來源，所以要先問：

- 是否真的需要排序
- 是否可以先過濾再排序
- 是否有適合的 index 能減少排序成本

## Query rewrite 常比硬加 index 更有效

很多查詢其實可以先從重寫開始：

- 先過濾，再 join
- 把重複子查詢改寫成較清楚的 `EXISTS`、join 或 CTE
- 降低中間結果大小
- 移除不必要欄位與排序

如果改寫後 `logical reads` 從 54 降到 18，通常代表你真的讓 SQL Server 少做了工作，而不只是碰巧快了一次。

## 比較查詢時要看趨勢，不要只看一次

實務上比較兩種寫法時，至少同時看：

- 平均 elapsed time
- CPU time
- logical reads
- execution plan 裡是否出現不同 operator 或不同資料存取方式

這樣比較能分辨：

- 是真的查得更少
- 還是只是剛好吃到 cache
- 或只是當下伺服器比較空閒

## 實務心法

- 效能調校前，先把 query 寫清楚
- `SET STATISTICS TIME ON` 用來看時間
- `SET STATISTICS IO ON` 用來看資料頁讀取成本
- execution plan 用來理解 SQL Server 到底怎麼跑
- index 是針對查詢模式設計，不是越多越好
- 能先減少資料量，通常比事後補救更有效
