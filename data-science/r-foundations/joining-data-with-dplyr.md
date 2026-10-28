[Data Science](../README.md) › [R Foundations](README.md) › dplyr 合併資料

# dplyr 合併資料 (Joining Data with dplyr)

join 是最容易「沒報錯但結果已經錯」的步驟：key 不唯一會讓列數爆增，型別或大小寫不一致會讓資料悄悄消失。動手前先回答三個問題：**每張表一列代表什麼（grain）？用哪些欄位對齊（key）？要保留交集、左表全部，還是兩邊全部？** SQL 對照見 [SQL JOIN 與集合運算](../databases/sql-joins-and-set-operations.md)，pandas 對照見 [reshape 與 merge](../python-foundations/pandas/reshape-merge.md)。

## join 類型

| 函式 | 保留 | 加入右表欄位？ | 典型用途 | SQL / pandas |
| --- | --- | --- | --- | --- |
| `inner_join()` | 兩邊都配對到的列 | 是 | 只分析交集 | `INNER JOIN` / `how="inner"` |
| `left_join()` | 左表全部 | 是，沒配對補 `NA` | 主表補註解（**最常用**） | `LEFT JOIN` / `how="left"` |
| `right_join()` | 右表全部 | 是 | 等同交換左右再 left join | `RIGHT JOIN` |
| `full_join()` | 兩邊全部 | 是 | 稽核兩份清單的覆蓋 | `FULL OUTER JOIN` / `how="outer"` |
| `semi_join()` | 左表中有配對的列 | **否** | 用另一表當篩選條件 | `WHERE EXISTS` / `isin()` |
| `anti_join()` | 左表中**沒**配對的列 | 否 | 找對不上的 key（QC） | `WHERE NOT EXISTS` / `~isin()` |
| `cross_join()` | 所有組合 | 是 | 建完整格子（也可用 `expand_grid()`） | `CROSS JOIN` |

```r
library(dplyr)

# 基本：明確寫 key，不要依賴自動找同名欄
counts_annot <- counts |> left_join(gene_annot, by = "gene_id")

# key 名稱不同、多個 key：join_by()（dplyr ≥ 1.1.0）
inventories |> inner_join(inventory_parts, by = join_by(id == inventory_id))
batmobile |>
  inner_join(batwing, by = join_by(part_num, color_id),
             suffix = c("_batmobile", "_batwing"))      # 非 key 的同名欄加後綴
# 舊寫法：by = c("id" = "inventory_id")

# 篩選型 join
samples |> semi_join(passed_qc, by = "sample_id")       # 只留通過 QC 的樣本
samples |> anti_join(gene_annot, by = "gene_id")        # 哪些基因沒有註解？
```

## 非等值 join

dplyr ≥ 1.1.0 的 `join_by()` 支援不等式、區間與最近值，基因體座標比對很常用。

```r
# 變異位點落在哪個基因區間（同染色體、pos 在 start–end 之間）
variants |>
  left_join(genes, by = join_by(chrom, between(pos, start, end)))

# 每個樣本對應「採樣日之前最近一次」的檢驗值
samples |>
  left_join(labs, by = join_by(patient_id, closest(sample_date >= lab_date)))
```

大量區間重疊（百萬筆以上）改用 `GenomicRanges::findOverlaps()` 或 `data.table::foverlaps()`，見 [data.table 合併與重塑](data-table-joins-and-reshaping.md)。

## 基數 (cardinality) 與列數爆增

| 關係 | 例子 | join 後列數 |
| --- | --- | --- |
| one-to-one | 樣本 ↔ 樣本 metadata | 不變 |
| many-to-one | 讀數表 → 基因註解（每基因一列） | 不變（left join） |
| one-to-many | 病人 → 多次就診 | 變多（預期中） |
| many-to-many | 兩邊 key 都重複 | 乘積式爆增，**幾乎都是錯誤** |

```r
# join 前：確認 lookup 表的 key 唯一
gene_annot |> count(gene_id) |> filter(n > 1)

# join 時：宣告預期關係，違反就報錯（dplyr ≥ 1.1.0）
counts |> left_join(gene_annot, by = "gene_id", relationship = "many-to-one")

# inner join 會悄悄丟掉對不上的列：unmatched = "error" 讓它報錯（檢查 x 與 y 兩邊）
counts |> inner_join(gene_annot, by = "gene_id", unmatched = "error")

# join 後：驗證
stopifnot(nrow(counts_annot) == nrow(counts))
counts_annot |> summarize(missing_symbol = sum(is.na(symbol)))
```

> dplyr ≥ 1.1.0 偵測到 many-to-many 時會發出 warning。不要用 `suppressWarnings()` 蓋掉，回頭檢查 key。

## key 對不上的常見原因

| 原因 | 例子 | 修正 |
| --- | --- | --- |
| 型別不同 | `"001"`（character）vs `1`（numeric） | 匯入時固定 `col_types`；join 前統一型別 |
| 版本後綴 | `ENSG00000141510.17` vs `ENSG00000141510` | `str_remove(id, "\\.\\d+$")` |
| 大小寫 / 空白 | `"tp53 "` vs `"TP53"` | `str_trim()`、`str_to_upper()` |
| 基因 symbol 別名 | `"p53"`、舊 symbol | 改用穩定 ID（Ensembl / Entrez）join |
| 染色體命名 | `"chr1"` vs `"1"` | 統一一種慣例 |
| 數值 key 的浮點誤差 | 計算後的 `0.30000000000000004` | 不要用浮點數當 key |
| `NA` key | dplyr 預設 `NA` 會互相配對 | `na_matches = "never"`（同 SQL 行為） |

## 檢查清單

1. 寫下每張表的 grain，以及 join 後預期的 grain。
2. key 明確寫在 `by`；lookup 表先檢查唯一性。
3. 依問題選 join 類型；不確定時先 `left_join()`，再看哪些 `NA`。
4. 用 `anti_join()` 找出對不上的 key，確認原因後再決定要不要丟。
5. join 後檢查列數、`NA` 數、關鍵分組摘要是否合理。
