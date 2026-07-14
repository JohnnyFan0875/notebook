# Parallel Programming in R

平行化不是把慢程式「自動變快」的魔法，而是把可以彼此獨立的工作分配給多個 worker 同時處理。只有當工作本身夠獨立、夠重，而且平行化的啟動與資料搬運成本不會吃掉收益時，它才真的值得。

## Should We Parallelize?

先分清楚兩種任務：

- sequential: 後一步依賴前一步結果
- parallel: 多個子任務彼此獨立，可以同時跑

直覺上：

- 一層樓蓋在上一層樓上，是 sequential
- 完工後幫不同窗戶裝玻璃，可能是 parallel

Key point: 能否平行化，不是看程式慢不慢，而是看任務之間有沒有依賴。

## When Parallelism Helps

R 裡常見適合平行化的情境：

- 對很多檔案做同樣清理
- 對很多參數組合做模擬
- 對很多群組各自跑同樣模型
- map-style 工作：一個函數套很多獨立輸入

不太適合的情境：

- 單一任務本身很小
- 步驟之間高度相依
- 需要共享大量 mutable state

平行化常見代價：

- 啟動 worker 成本
- 將資料 / 函數送到 worker 的成本
- 記憶體用量上升
- 除錯變複雜

所以在實務上，平行化通常是 profiling 之後的選項，不是第一步。

## The `parallel` Package and Clusters

base R 常見的平行入口是 `parallel`。

基本 workflow：

```r
library(parallel)

cl <- makeCluster(4)
result <- parLapply(cl, inputs, some_function)
stopCluster(cl)
```

這個 pattern 的核心是：

1. 建立 cluster
2. 把同一個函數 map 到多個輸入
3. 關閉 cluster

如果忘了 `stopCluster()`，worker process 可能會一直留著。

## Choosing Number of Workers

常見做法是先看可用核心數，再保留一部分給系統：

```r
library(parallel)

n_cores <- detectCores() - 2
cl <- makeCluster(n_cores)
```

這樣通常比直接把所有核心都吃滿更穩，尤其在你還同時開著 notebook、browser 或其他分析工具時。

Key point: worker 數不是越多越好。超過資料與任務粒度的合理範圍後，overhead 可能讓總時間反而變差。

## Preparing Workers with `clusterEvalQ()` and `clusterExport()`

worker 不會自動知道你主 session 裡的所有 library 與物件。這是 `parallel` 初學最常踩的坑。

### Load packages on workers

```r
clusterEvalQ(cl, library(dplyr))
```

### Export needed objects

```r
selected_year <- 2015
clusterExport(cl, "selected_year")
```

之後才安全地做：

```r
ls_df <- parLapply(cl, file_list, filterCSV)
```

實務上，`parallel` cluster workflow 幾乎都長這樣：

```r
cl <- makeCluster(n_cores)
clusterEvalQ(cl, library(crucial_package))
clusterExport(cl, "variable_we_need")
result <- parLapply(cl, ls_inputs, our_function)
stopCluster(cl)
```

## `parLapply()` vs `parLapplyLB()`

`parLapply()` 會把工作較平均地切給 worker；如果各任務耗時差很多，某些 worker 可能先閒下來。

這時可以考慮 `parLapplyLB()`，其中 `LB` 是 load balancing：

```r
ls <- parLapplyLB(cl, ls_weights, boot_mean)
```

適合：

- 每個輸入計算時間差異很大
- 想減少某些 worker 提早閒置的情況

Key point: 任務耗時不均時，load balancing 往往比單純增加 worker 更有效。

## Futures: Delayed and Asynchronous Thinking

`future` 生態系比較像是把「這段工作以後再取值」變成第一級概念。

```r
library(future)

task_future <- future({
  print("Hi, here is the report.")
  report
})
```

這時你拿到的是 future object，不是最終值本身。真正要取結果時再用：

```r
value(task_future)
```

可以把 future 想成：

- expression: 要做什麼
- environment: 在什麼上下文做
- resolved: 做完了沒
- value: 完成後的結果

這種 delayed execution 心智模型，在你想先發出多個工作、之後再集中取結果時特別自然。

## `plan()` Controls the Backend

`future` 的執行方式由 `plan()` 決定。

```r
plan(sequential)
plan(multisession, workers = 4)
```

- `sequential`: 不平行，按正常順序執行
- `multisession`: 用多個背景 R session 平行跑

常見 pattern：

```r
plan(multisession, workers = 4)

future_list <- lapply(input_list, function(x) {
  future(calculate(x))
})

result_list <- value(future_list)

plan(sequential)
```

把 `plan(sequential)` 恢復回來是好習慣，能避免後續程式在你沒注意時繼續沿用平行設定。

## `future_map()` for Parallel Mapping

如果你本來就習慣 tidyverse / purrr 風格，`furrr::future_map()` 常比手寫 futures 更順。

```r
plan(multisession, workers = 2)
ls_df <- furrr::future_map(ls_files, read.csv)
plan(sequential)
```

這個 pattern 很適合：

- 對很多檔案做同樣讀取
- 對 list inputs 跑同一個函數
- 想保留 map-style 可讀性

Key point: `future_map()` 讓你在保持 map workflow 的同時，把 backend 換成平行執行。

## Memory Matters

平行化常見的隱形代價是記憶體。多個 worker 可能各自持有資料副本，因此：

- worker 越多，不代表越划算
- 大物件複製可能讓 RAM 很快吃滿
- 某些情況下 bottleneck 其實從 CPU 轉成 memory

課程裡一個很重要的實務點是：面對大資料時，與其一次把全部檔案丟給 worker，不如考慮 chunking。

## Managing Memory by Chunking

如果資料太大，可以分批平行，而不是一次平行所有輸入。

例如概念上：

1. 將檔案清單切成多批
2. 每批用固定 worker 數處理
3. 每批完成就釋放中間結果或寫出

這種做法的好處是：

- 控制瞬時記憶體壓力
- 降低 worker 同時持有大物件的風險
- 比「硬開更多 workers」更穩

## Profiling Parallel Work

平行程式也一樣要 profiling，因為更多 worker 不代表一定更快。

```r
profvis::profvis({
  plan(multisession, workers = 2)
  ls_df <- furrr::future_map(ls_files, read.csv)
  plan(sequential)
})
```

再和更多 workers 比較：

```r
profvis::profvis({
  plan(multisession, workers = 4)
  ls_df <- furrr::future_map(ls_files, read.csv)
  plan(sequential)
})
```

這能幫你回答：

- 2 workers 和 4 workers 差多少
- 時間是不是花在 I/O，而不是計算
- 記憶體與排程 overhead 是否開始吃掉收益

## Practical Workflow

1. 先確認任務彼此獨立，真的有平行化空間。
2. 先用 profiling 或 benchmark 確認值得優化。
3. 如果是 map-style 任務，先考慮 `parLapply()` 或 `future_map()`。
4. 在 `parallel` 裡記得處理 `clusterEvalQ()`、`clusterExport()` 與 `stopCluster()`。
5. 在 `future` 生態裡記得設定與恢復 `plan()`。
6. 對大資料優先思考記憶體與 chunking，而不是只增加 workers。

## Common Mistakes

- 任務本身太小，卻硬做平行化。
- 忘記 worker 不會自動繼承 library 與物件。
- 沒 `stopCluster()`，留下背景 worker。
- 以為 worker 越多一定越快，忽略記憶體與排程成本。
- 平行化前沒先確認 bottleneck 真的是 CPU，而不是 I/O 或資料搬運。
