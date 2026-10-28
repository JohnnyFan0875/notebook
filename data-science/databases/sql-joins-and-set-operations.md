[Data Science](../README.md) › [Databases](README.md) › JOIN 與集合運算

# JOIN 與集合運算 (Joins and Set Operations)

JOIN 把表**橫向**拼接（增加欄位），集合運算把結果**縱向**堆疊或比較（增減列）。選對操作之前，先預期結果會有幾列、哪裡會出現 `NULL`。

## JOIN 類型

| JOIN | 保留哪些列 | 沒對到的一側 | 典型用途 |
| --- | --- | --- | --- |
| `INNER JOIN` | 兩邊都有 match 的列 | 丟掉 | 只分析兩邊都存在的實體 |
| `LEFT JOIN` | 左表全部 | 右表欄位為 `NULL` | 主表是分析單位（樣本），附加資訊可能缺 |
| `RIGHT JOIN` | 右表全部 | 左表欄位為 `NULL` | 通常改寫成交換順序的 `LEFT JOIN` |
| `FULL JOIN` | 兩邊全部 | 各自補 `NULL` | 對帳、兩份清單的 overlap 與孤兒列 |
| `CROSS JOIN` | 所有組合（m × n 列） | — | 日期 × 類別骨架、參數格點 |
| self join | 同一張表的兩個角色 | 依 JOIN 類型 | 主管 / 部屬、前後事件 |

```sql
-- INNER：兩邊都有
SELECT s.sample_id, s.tissue, r.rin
FROM samples AS s
INNER JOIN rna_qc AS r
  ON s.sample_id = r.sample_id;

-- LEFT：保留所有樣本，沒有 QC 的 rin 為 NULL
SELECT s.sample_id, r.rin
FROM samples AS s
LEFT JOIN rna_qc AS r
  ON s.sample_id = r.sample_id;

-- FULL：兩份清單比對；COALESCE 取得共同 key
SELECT COALESCE(a.sample_id, b.sample_id) AS sample_id,
       a.sample_id IS NOT NULL AS in_metadata,
       b.sample_id IS NOT NULL AS in_fastq
FROM metadata AS a
FULL JOIN fastq_files AS b
  ON a.sample_id = b.sample_id;

-- self join：同一張表的兩個角色要用清楚的 alias
SELECT child.name, parent.name AS manager
FROM employees AS child
LEFT JOIN employees AS parent
  ON child.manager_id = parent.employee_id;

-- 多欄 key：少一個條件就會誤配
SELECT *
FROM visits AS v
JOIN labs AS l
  ON v.patient_id = l.patient_id
 AND v.visit_date = l.visit_date;
```

| 寫法 | 說明 |
| --- | --- |
| `ON a.id = b.id` | 最明確，欄位名不同也能用 |
| `USING (id)` | 兩邊同名時的簡寫，結果只留一個 `id` 欄 |
| `NATURAL JOIN` | 自動用所有同名欄位 join；schema 一改結果就變（例如兩表都加了 `created_at`），**避免使用** |

### `LEFT JOIN` 的條件放 `ON` 還是 `WHERE`

```sql
-- 想保留所有樣本，只附上 2024 年的 QC
SELECT s.sample_id, r.rin
FROM samples AS s
LEFT JOIN rna_qc AS r
  ON s.sample_id = r.sample_id
 AND r.run_year = 2024;          -- 放 ON：沒有 2024 QC 的樣本仍保留（rin 為 NULL）

-- 錯：右表條件放 WHERE，NULL 列被過濾掉，LEFT JOIN 退化成 INNER JOIN
SELECT s.sample_id, r.rin
FROM samples AS s
LEFT JOIN rna_qc AS r ON s.sample_id = r.sample_id
WHERE r.run_year = 2024;
```

## 列數膨脹 (Fan-out)

JOIN 的結果列數 = 每個 key 在左表的列數 × 在右表的列數，加總。key 在右表不唯一時，左表的列會被複製，之後的 `SUM` / `COUNT` 就會重複計算。

```sql
-- samples: 每個 sample 一列（n_reads）
-- annotations: 一個 sample 有多個標籤
SELECT SUM(s.n_reads)                 -- 被重複計算：有 2 個標籤的樣本算兩次
FROM samples AS s
JOIN annotations AS a USING (sample_id);

-- 改法 1：先把多的一側聚合到 key 的層級 (grain)，再 join
WITH a1 AS (
  SELECT sample_id, STRING_AGG(tag, ',') AS tags   -- MySQL: GROUP_CONCAT
  FROM annotations
  GROUP BY sample_id
)
SELECT SUM(s.n_reads)
FROM samples AS s
JOIN a1 USING (sample_id);

-- 改法 2：只需要「有沒有」時，用 EXISTS（不會複製列）
SELECT SUM(n_reads)
FROM samples AS s
WHERE EXISTS (SELECT 1 FROM annotations AS a WHERE a.sample_id = s.sample_id);
```

```sql
-- join 前檢查 key 是否唯一：有回傳列就代表會膨脹
SELECT sample_id, COUNT(*)
FROM annotations
GROUP BY sample_id
HAVING COUNT(*) > 1;
```

> 每次 join 前先問：「這張表一列代表什麼？」（grain）。join 後比對列數：`LEFT JOIN` 後列數變多，表示右表 key 不唯一。pandas 的 `merge(validate="one_to_one")`、dplyr 的 `relationship = "one-to-one"` 會自動檢查（見 [合併資料（pandas）](../python-foundations/pandas/reshape-merge.md)、[dplyr join](../r-foundations/joining-data-with-dplyr.md)）。

## 集合運算

| 運算 | 結果 | 去重 |
| --- | --- | --- |
| `UNION` | 兩個結果上下合併 | 是（有排序 / hash 成本） |
| `UNION ALL` | 上下合併 | 否；確定不重複或需要保留重複時用，較快 |
| `INTERSECT` | 兩邊都有的列 | 是 |
| `EXCEPT`（Oracle 舊版：`MINUS`） | 在左邊、不在右邊的列 | 是 |

```sql
SELECT gene_id FROM study_a_hits
UNION                       -- 兩個研究的聯集
SELECT gene_id FROM study_b_hits;

SELECT gene_id FROM study_a_hits
INTERSECT                   -- 兩個研究都顯著
SELECT gene_id FROM study_b_hits;

SELECT gene_id FROM study_a_hits
EXCEPT                      -- 只在 A 顯著
SELECT gene_id FROM study_b_hits;
```

- 兩邊欄位數相同、對應欄位型別相容；欄名取第一個查詢的。
- 比較的是**整列**值，不像 JOIN 依條件配對、拼接欄位。
- 集合運算把兩個 `NULL` 視為相同（與 `=` 比較不同）。

## Semi join 與 anti join

只想知道「右表有沒有對應」時，不需要把右表欄位帶進來，也就不會有列數膨脹。

| | 問題 | 寫法 |
| --- | --- | --- |
| semi join | 左表哪些列在右表**有**對應？ | `WHERE EXISTS (...)`、`WHERE id IN (SELECT ...)` |
| anti join | 左表哪些列在右表**找不到**？ | `WHERE NOT EXISTS (...)`、`LEFT JOIN ... WHERE b.id IS NULL` |

```sql
-- semi join：有定序資料的病人
SELECT p.*
FROM patients AS p
WHERE EXISTS (
  SELECT 1 FROM sequencing AS s
  WHERE s.patient_id = p.patient_id
);

-- anti join：有 metadata 但沒有 FASTQ 的樣本（資料品質檢查最常用）
SELECT m.*
FROM metadata AS m
WHERE NOT EXISTS (
  SELECT 1 FROM fastq_files AS f
  WHERE f.sample_id = m.sample_id
);

-- 等價寫法：LEFT JOIN 後取右表為 NULL 的列（判斷欄要用右表的 key 或 NOT NULL 欄）
SELECT m.*
FROM metadata AS m
LEFT JOIN fastq_files AS f ON f.sample_id = m.sample_id
WHERE f.sample_id IS NULL;
```

> anti join 不要用 `NOT IN (SELECT ...)`：子查詢只要有一個 `NULL`，整個條件就變成 `UNKNOWN`，結果是空的（見 [NULL 三值邏輯](sql-query-foundations.md#null三值邏輯)）。

## 選擇指南

| 需求 | 用 |
| --- | --- |
| 要把右表欄位帶進結果 | JOIN（先確認 key 唯一） |
| 只判斷存在 / 不存在 | `EXISTS` / `NOT EXISTS` |
| 兩份同結構清單的聯集、交集、差集 | `UNION` / `INTERSECT` / `EXCEPT` |
| 單純把多個來源接起來 | `UNION ALL` |
| 區間重疊（變異位點落在哪個基因） | 範圍條件 join，見 [DuckDB 與 Parquet](duckdb-and-parquet.md#區間-join基因組座標) |
