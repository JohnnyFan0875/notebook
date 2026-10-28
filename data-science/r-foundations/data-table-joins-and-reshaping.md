[Data Science](../README.md) › [R Foundations](README.md) › data.table

# data.table：查詢、合併與重塑 (data.table Joins and Reshaping)

`data.table` 把篩選、計算、分組、更新、join 都壓進同一個語法 `DT[i, j, by]`，而且多數操作**就地修改 (by reference)**、不複製資料，所以在千萬列以上的資料（變異位點表、單細胞 metadata、大型讀數表）明顯比 dplyr 快、省記憶體。dplyr 的對應寫法見 [dplyr 合併資料](joining-data-with-dplyr.md) 與 [tidyr 資料重塑](data-reshaping-with-tidyr.md)。

```
DT[ i,        j,             by       ]
    哪些列     算什麼 / 改什麼   依什麼分組
    （或 join 的表）
```

## 讀寫與基本查詢

```r
library(data.table)

dt <- fread("variants.tsv.gz")                 # 自動偵測分隔符，可直接讀 .gz；多執行緒
fwrite(dt, "out.csv.gz")                       # 寫檔也很快
setDT(df)                                      # data.frame → data.table（就地，不複製）

dt[chrom == "chr17" & qual > 30]               # i：篩列
dt[, .(chrom, pos, ref, alt)]                  # j：選欄（.() = list()）
dt[, .(n = .N, mean_qual = mean(qual)), by = chrom]   # 分組摘要；.N = 列數
dt[order(chrom, -qual)]                        # 排序
dt[, .SD[which.max(qual)], by = gene]          # 每組取最大那列；.SD = 該組子表
dt[, lapply(.SD, mean), by = sample, .SDcols = patterns("^expr_")]   # 多欄同一函式
```

### `:=` 就地更新

```r
dt[, af := alt_count / depth]                  # 新增欄，不需重新指派
dt[qual < 20, filter := "LowQual"]             # 只改符合條件的列
dt[, c("a", "b") := .(x + 1, y * 2)]           # 多欄
dt[, mean_dp := mean(depth), by = sample]      # 組內統計寫回每列
dt[, tmp := NULL]                              # 刪欄

dt2 <- dt                                      # 不是複製！改 dt2 也會改 dt
dt2 <- copy(dt)                                # 真的要副本時
```

> `:=` 與 `set*()` 系列函式就地修改，函式內改到傳入的 data.table 會影響呼叫端的物件。這是效能來源，也是最常見的意外。

## Join

| 寫法 | 結果 | dplyr |
| --- | --- | --- |
| `X[Y, on = .(id)]` | 保留 **Y** 全部列（以 Y 查 X） | `right_join(X, Y)` |
| `X[Y, on = .(id), nomatch = NULL]` | 只留配對成功 | `inner_join()` |
| `X[!Y, on = .(id)]` | X 中沒配對到的列 | `anti_join()` |
| `merge(X, Y, by = "id")` | inner | `inner_join()` |
| `merge(X, Y, by = "id", all.x = TRUE)` | 保留 X | `left_join()` |
| `merge(X, Y, by = "id", all = TRUE)` | 兩邊全部 | `full_join()` |

```r
shipping[demographics, on = .(name)]                      # 保留 demographics 全部 = 以它為主的 left join
customers[web_visits, on = .(name = person)]              # key 名稱不同
purchases[web_visits, on = .(name, date)]                 # 多 key
key_col <- "name"; shipping[demographics, on = key_col]   # key 在變數裡

# join 後直接計算：by = .EACHI 對 i 的每一列各自彙總，不必先產生大表
DT1[DT2, on = .(id), .(n = .N, total = sum(value)), by = .EACHI]

# lookup：把右表欄位就地加到左表（不改變列數）
samples[meta, on = .(sample_id), `:=`(batch = i.batch, sex = i.sex)]   # i. 前綴 = 右表的欄
```

`setkey(dt, id)` 會把表依 key 排序並記住，之後 `dt[J("x")]` 用二分搜尋查找。偶爾 join 一次用 `on =` 就夠；同一組 key 反覆查找才值得 `setkey()`。

### 滾動 join 與區間重疊

```r
# 每筆交易對應「當時或之前最近一筆」報價（同 dplyr closest()）
quotes[trades, on = .(symbol, time), roll = TRUE]         # roll = -Inf 往後找；roll = 60 限 60 秒內

# 基因體區間重疊：變異位點落在哪個基因
setkey(genes, chrom, start, end)                          # y 必須設 key，最後兩個是區間起訖
variants[, `:=`(start = pos, end = pos)]                  # 點也是長度 1 的區間
foverlaps(variants, genes, type = "within")
```

> Bioconductor 的 `GenomicRanges::findOverlaps()` 是生資標準做法，會處理 strand 與座標系統；見 [Bioconductor 入門](../../biology/genomics/sequencing-and-analysis/workflows/bioconductor-introduction.md)。

### join 陷阱

| 問題 | data.table 行為 | 對策 |
| --- | --- | --- |
| key 型別不一致（integer vs character） | 直接報錯 | 先統一：`dt[, id := as.integer(id)]` |
| 兩邊 key 都重複 | 結果超過 `nrow(X) + nrow(Y)` 列時報錯，要求 `allow.cartesian = TRUE` | 先 `dt[, .N, by = key][N > 1]` 找重複，不要直接打開 |
| 一對多只想取一筆 | `mult = "first"` / `"last"` | 確認「第一筆」的意義（先排序） |
| key 語意不同但剛好能 join | 不會報錯 | join 前確認兩邊 key 是同一實體、同一粒度 |
| 完全沒有共同值 | inner 回空表；outer 一堆 `NA` | 先 `intersect(X$id, Y$id)` 檢查覆蓋率 |

## 合併多張表

```r
files <- list.files("per_sample", pattern = "\\.tsv$", full.names = TRUE)
all <- rbindlist(lapply(setNames(files, basename(files)), fread),
                 idcol = "file",          # 保留來源檔名
                 use.names = TRUE,        # 依欄名對齊而非位置
                 fill = TRUE)             # 缺欄補 NA
```

## 重塑：`melt()` / `dcast()`

```r
# 寬 → 長（同 pivot_longer）
sales_long <- melt(sales_wide, id.vars = c("quarter", "department"),
                   variable.name = "year", value.name = "amount")
melt(dt, id.vars = "gene", measure.vars = patterns("^s\\d+"))   # 依欄名 pattern

# 長 → 寬（同 pivot_wider）；公式左邊 = 列，右邊 = 展開成欄
dcast(sales_long, quarter ~ department + year, value.var = "amount")
dcast(expr_long, gene ~ sample, value.var = "count", fill = 0)
dcast(sales_long, season ~ year, value.var = "amount", fun.aggregate = sum)  # 有重複時明確聚合
```

## dplyr 或 data.table？

| 考量 | dplyr | data.table |
| --- | --- | --- |
| 可讀性、團隊共用 | 較好，每步一個動詞 | 語法緊湊，需要熟悉 |
| 速度 / 記憶體（>1e7 列） | 中等 | 快，就地修改 |
| 依賴 | tidyverse 生態系 | 單一套件、無依賴 |
| 資料庫後端 | `dbplyr` 可翻成 SQL | 無 |
| 兩者兼得 | `dtplyr`：寫 dplyr、背後跑 data.table | |

更大的資料（超過記憶體）考慮 `arrow` + `duckdb`，見 [寫出有效率的 R](writing-efficient-r-code.md) 與 [匯入資料](importing-data.md)。
