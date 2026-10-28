[Data Science](../README.md) › [R Foundations](README.md) › 平行運算

# 平行運算 (Parallel Programming in R)

R 預設只用一個核心。當工作可以拆成**彼此獨立**的子任務（每個樣本、每個 bootstrap 重抽、每組參數、每個染色體），就能分給多個 worker 同時跑。平行化有啟動、資料傳輸與記憶體成本，所以前提是單核版本已經量測過、寫快了（見 [寫出有效率的 R](writing-efficient-r-code.md)）。Python 版見 [平行運算](../python-foundations/performance-and-scaling/parallel.md)。

## 能不能、值不值得平行化

| 適合 | 不適合 |
| --- | --- |
| 對很多檔案 / 樣本做同樣處理 | 每步依賴上一步（MCMC 單鏈、迭代最佳化） |
| bootstrap、permutation、交叉驗證 fold | 單一任務只花幾毫秒（overhead 大於收益） |
| 參數格點、模擬重複 | 瓶頸是磁碟 I/O 或網路（多 worker 搶同一顆硬碟） |
| 每個基因 / 每個區域各自擬合模型 | 需要共享大量可變狀態 |

> 一個任務若只需幾毫秒，先把多個任務合併成較大的 chunk 再分給 worker。

## 選工具

| 工具 | 介面 | 特點 |
| --- | --- | --- |
| `parallel`（base R） | `parLapply()`、`mclapply()` | 無依賴；要手動 export 物件與載入套件 |
| `future` + `furrr` / `future.apply` | `future_map()`、`future_lapply()` | 程式與後端分離：同一份程式用 `plan()` 切換本機、多核、HPC |
| `BiocParallel` | `bplapply(X, FUN, BPPARAM = )` | Bioconductor 標準；DESeq2 等的 `parallel = TRUE` 用的就是它 |
| `foreach` + `doFuture` | `foreach(...) %dofuture% {}` | 舊程式常見 |
| `mirai` | `mirai_map()` | 新一代輕量後端，purrr ≥ 1.1 的 `in_parallel()` 用它 |

建議：新程式用 **future 生態系**；在 Bioconductor 流程中用 **BiocParallel** 傳給套件函式。

## future + furrr

```r
library(future)
library(furrr)

plan(multisession, workers = 4)        # 背景 R session；所有平台可用

res <- future_map(files, \(f) process_sample(f),
                  .options = furrr_options(seed = TRUE),   # 平行亂數可重現
                  .progress = TRUE)

plan(sequential)                        # 用完恢復，避免後續程式意外平行
```

| `plan()` | 說明 |
| --- | --- |
| `sequential` | 不平行（除錯時先用它跑一遍） |
| `multisession` | 背景 R session，Windows / macOS / Linux 都可用 |
| `multicore` | fork 現有 process，省記憶體；**Windows 與 RStudio 內不可用** |
| `cluster` | 多台機器 |
| `future.batchtools::batchtools_slurm` | 每個 future 提交成一個 Slurm job |

future 會自動偵測函式用到的全域變數與套件並傳給 worker，比 `parallel` 少很多手動設定。底層概念：`future(expr)` 立刻回傳一個「之後才取值」的物件，`value(f)` 等它完成並取出結果。

```r
f <- future(slow_model(df))            # 非同步開始執行
# ... 主 session 繼續做別的事 ...
fit <- value(f)                        # 需要時才阻塞等待
```

## parallel（base R）

```r
library(parallel)

n_workers <- parallelly::availableCores(omit = 1)   # 見下方「核心數」
cl <- makeCluster(n_workers)

clusterEvalQ(cl, library(dplyr))       # worker 是全新的 R session：要載入套件
clusterExport(cl, c("ref_table", "min_count"))  # 並送入需要的物件
clusterSetRNGStream(cl, iseed = 42)    # 平行亂數可重現

res <- parLapply(cl, files, process_sample)
res <- parLapplyLB(cl, files, process_sample)   # 任務耗時差很多時：load balancing

stopCluster(cl)                        # 不關會留下背景 process
```

| `parallel` 函式 | 用途 |
| --- | --- |
| `makeCluster()` / `stopCluster()` | 建立 / 關閉 PSOCK cluster（所有平台） |
| `parLapply()` / `parSapply()` | 平行版 `lapply` / `sapply`，靜態平均分配 |
| `parLapplyLB()` | 動態分配，任務耗時不均時較快 |
| `mclapply(X, FUN, mc.cores = )` | fork 版本，Linux / macOS 才有效；Windows 上 `mc.cores > 1` 會報錯 |
| `clusterEvalQ()` / `clusterExport()` | 在 worker 上執行程式 / 傳送物件 |

## BiocParallel

```r
library(BiocParallel)

param <- MulticoreParam(workers = 4)           # Linux / macOS
param <- SnowParam(workers = 4)                # Windows
register(param)                                # 設為預設

res <- bplapply(samples, align_and_count, BPPARAM = param)

# 套件函式的平行選項
dds <- DESeq2::DESeq(dds, parallel = TRUE, BPPARAM = param)
```

## 可重現性：平行亂數

各 worker 若用同一個 seed 會產生**完全相同**的亂數，bootstrap 就白做了；若都不設 seed 則無法重現。

| 工具 | 正確做法 |
| --- | --- |
| furrr | `.options = furrr_options(seed = 123)` |
| future.apply | `future_lapply(..., future.seed = 123)` |
| parallel | `clusterSetRNGStream(cl, iseed = 123)` |
| BiocParallel | `MulticoreParam(RNGseed = 123)` |

這些都使用 L'Ecuyer-CMRG 產生器給每個任務獨立的亂數流。結果與 worker 數無關（future 系列），所以 2 核和 8 核跑出相同結果。

## 核心數與記憶體

| 注意點 | 說明 |
| --- | --- |
| `detectCores()` 在 HPC 上會回報整台節點的核心數 | 用 `parallelly::availableCores()`：會讀取 Slurm / PBS 分配的核心數與 `mc.cores` 設定 |
| 保留核心給系統 | `availableCores(omit = 1)` |
| 每個 worker 都有自己的資料副本 | 4 個 worker × 8 GB 物件 = 32 GB；大資料改成每個 worker 自己讀它需要的部分（傳檔名而非資料） |
| 巢狀平行 | worker 裡又用多執行緒 BLAS / data.table，總執行緒超過核心數反而變慢；在 worker 內設 `data.table::setDTthreads(1)`、`RhpcBLASctl::blas_set_num_threads(1)` |
| 記憶體不足 | 分批（chunk）處理：每批完成就寫出結果並釋放 |

> 平行版本也要量測：2、4、8 個 worker 各跑一次。若時間不再下降，瓶頸可能已變成 I/O 或記憶體。

## 規模再大：HPC 與工作流引擎

單機多核不夠時，有兩條路：

| 方式 | 適合 |
| --- | --- |
| `future.batchtools` / `clustermq` | 留在 R 內，把 `future_map()` 的每個任務提交成 HPC job |
| Snakemake / Nextflow | 多個外部工具串成的流程、需要斷點續跑，見 [工作流引擎](../../computing/workflow-engines/README.md) |
| sparklyr | 資料本身大到單機放不下，見 [Data Engineering](../data-engineering/README.md) |

## 常見錯誤

| 錯誤 | 症狀 / 修正 |
| --- | --- |
| worker 找不到套件或物件 | `could not find function`；用 future（自動偵測）或 `clusterEvalQ` / `clusterExport` |
| 沒 `stopCluster()` | 背景 R process 累積吃記憶體 |
| 在 Windows 用 `mclapply` / `multicore` | 不會平行或報錯；改 `multisession` / `SnowParam` |
| 沒設定平行亂數 | 結果無法重現，或各 worker 產生相同亂數 |
| worker 數越多越好 | 超過核心數、記憶體或 I/O 頻寬後反而變慢 |
| 在 worker 內寫同一個檔案 | 互相覆蓋；每個任務寫自己的檔，或回傳結果由主 session 寫 |
