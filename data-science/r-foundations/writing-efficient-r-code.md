[Data Science](../README.md) › [R Foundations](README.md) › 寫出有效率的 R

# 寫出有效率的 R (Writing Efficient R Code)

R 是為了「寫得快」而不是「跑得快」設計的。多數分析程式只有少數幾行是瓶頸，所以優化的順序是：**先量測 → 找熱點 → 改成更像 R 的寫法 → 還不夠才平行化或 Rcpp**。Python 的對應內容見 [效能與擴展](../python-foundations/performance-and-scaling/README.md)。

## 優化流程

```
程式真的慢嗎？（在實際資料量下）
  └─ 是 → profvis 找出最慢的幾行
            └─ 1. 移除重複計算、不必要的中間物件
               2. 向量化 / 改用專用函式（rowSums、matrixStats、data.table）
               3. 迴圈內不要讓物件長大：預先配置、結果先放 list 最後合併
               4. bench::mark 比較改寫前後（結果相同、速度確實變快）
               5. 仍是瓶頸：獨立任務 → 平行化；單一緊密迴圈 → Rcpp
```

> 沒有量測就優化，常常是花一小時把只佔 1% 時間的程式加速 10 倍。

## 量測：計時、benchmark、profiling

```r
# 1. 粗略計時
system.time(fit <- lm(y ~ ., data = df))      # elapsed 是牆鐘時間

# 2. 比較替代寫法：bench::mark 預設會檢查各寫法結果是否相同
bench::mark(
  loop   = { s <- 0; for (v in x) s <- s + v; s },
  vector = sum(x),
  iterations = 50
)                                             # 看 median 與 mem_alloc 欄

# 3. 找熱點：逐行顯示時間與記憶體（RStudio / Positron 內顯示火焰圖）
profvis::profvis({
  df <- read_and_clean("data.csv")
  res <- run_models(df)
})

# base R 的 profiler（profvis 底層也是它）
Rprof("profile.out"); run_models(df); Rprof(NULL)
summaryRprof("profile.out")$by.self |> head()
```

| 工具 | 回答什麼 | 備註 |
| --- | --- | --- |
| `system.time()` | 這段要多久 | 單次測量，有雜訊 |
| `bench::mark()` | A、B 哪個快、記憶體用多少 | 自動驗證結果一致；`microbenchmark` 是較舊的替代 |
| `profvis::profvis()` | 時間花在哪幾行 | 抽樣式 profiler，太短的程式抓不到 |
| `lobstr::obj_size()` | 物件佔多少記憶體 | 比 `object.size()` 正確計算共享部分 |
| `tracemem(x)` | `x` 何時被複製 | 找出意外的 copy-on-modify |

## 向量化與專用函式

R 的向量運算在 C 層迴圈，比在 R 層逐元素處理快得多。

| 慢寫法 | 快寫法 |
| --- | --- |
| `for` 逐元素相加 | `x + y` |
| `apply(m, 1, sum)` / `apply(m, 2, mean)` | `rowSums(m)` / `colMeans(m)` |
| `apply(m, 1, var)`、`apply(m, 1, median)` | `matrixStats::rowVars(m)`、`rowMedians(m)` |
| `for` + `if` 逐列判斷 | `ifelse()`、`dplyr::if_else()`、`case_when()` |
| 逐列取兩欄較大值 | `pmax(a, b)` |
| `sapply(x, function(v) v %in% set)` | `x %in% set`（內部用 hash） |
| 對每個基因跑 `t.test()` | `matrixStats` / `genefilter::rowttests()`，或 limma 一次擬合 |
| 每組用迴圈 subset 再算 | `data.table` 的 `by=`、`dplyr::summarise(.by = )` |

```r
# 例：基因 × 樣本矩陣的 CPM 與過濾，全向量化
lib  <- colSums(counts)
cpm  <- t(t(counts) / lib) * 1e6        # 每欄除以自己的 library size
# 或 sweep(counts, 2, lib, "/") * 1e6
keep <- rowSums(cpm >= 1) >= 3          # 至少 3 個樣本 CPM ≥ 1
```

> 單細胞計數矩陣 90% 以上是 0，用 `Matrix` 套件的稀疏矩陣（`dgCMatrix`）可省下數十倍記憶體；`as.matrix()` 一個 3 萬基因 × 10 萬細胞的矩陣約需 24 GB（3×10⁹ × 8 bytes）。

## 記憶體：不要讓物件在迴圈中長大

R 的物件是 **copy-on-modify**：每次 `c(x, i)` 或 `rbind(df, row)` 都會配置一塊新記憶體並把舊資料整份複製過去，n 次迴圈的總成本是 O(n²)。

```r
# 差：每次都複製
x <- c()
for (i in 1:n) x <- c(x, i^2)

# 好：預先配置
x <- numeric(n)
for (i in seq_len(n)) x[i] <- i^2       # seq_len(n) 在 n = 0 時不會跑出 1:0

# 最好：向量化
x <- (1:n)^2

# 累積 data frame：先放 list，最後一次合併
res <- vector("list", length(files))
for (i in seq_along(files)) res[[i]] <- process(files[[i]])
out <- dplyr::bind_rows(res)             # 或 data.table::rbindlist(res)
```

| 陷阱 | 說明 |
| --- | --- |
| 迴圈中 `rbind()` / `c()` / `paste0()` 累積 | O(n²) 複製；改預先配置或 list |
| 修改 data frame 的單一格 `df[i, j] <- v` 在迴圈中 | 每次可能複製整欄；先取出 vector 處理完再放回 |
| 保留大量中間物件 | 用 `rm()` 後 `gc()`，或把步驟包進函式讓區域變數自然釋放 |
| `1:length(x)` | `x` 長度 0 時變成 `c(1, 0)`；用 `seq_along(x)` |

## 選對資料結構與套件

| 情境 | 選擇 |
| --- | --- |
| 全數值、同型別 | `matrix`（比 data frame 快，可用矩陣代數） |
| 千萬列以上的分組 / join | [data.table](data-table-joins-and-reshaping.md)（就地修改、多執行緒） |
| 讀大 CSV | `data.table::fread()`、`vroom`、`arrow::read_csv_arrow()` |
| 比記憶體大的資料 | `arrow` / `duckdb` 延遲查詢，見 [匯入資料](importing-data.md) |
| 稀疏計數矩陣 | `Matrix::dgCMatrix`；Bioconductor 的 `DelayedArray` / `HDF5Array` 放在磁碟上 |
| 大量字串比對 | `stringi` / `stringr`（ICU），見 [正規表示式](regular-expressions.md) |

## 下一步：平行化與 Rcpp

| 瓶頸型態 | 工具 | 筆記 |
| --- | --- | --- |
| 許多彼此獨立的任務（每個樣本、每個 bootstrap、參數格點） | `future` / `furrr` / `parallel` | [平行運算](parallel-programming-in-r.md) |
| 單一緊密迴圈、每步依賴上一步（MCMC、動態規劃） | Rcpp | [Rcpp](rcpp-for-r-performance.md) |
| 線性代數密集（大矩陣乘法、SVD） | 換用最佳化的 BLAS（OpenBLAS、MKL、macOS Accelerate） | 不必改程式 |

平行化有啟動與資料傳輸成本，小任務常常反而變慢；先把單核版本寫對、寫快，再平行化。

> 效率不是唯一目標。為了 5% 的加速把程式寫得難以閱讀，維護成本通常高於省下的時間。
