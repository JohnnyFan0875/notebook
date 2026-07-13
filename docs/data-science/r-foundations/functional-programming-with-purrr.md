# Functional Programming with purrr

`purrr` 是 R 裡把「對很多元素重複做同一件事」整理得更穩定的一套工具。它的重點不是炫技，而是把 iteration 寫成回傳型別更明確、可組合、也更容易加上錯誤處理的資料流程。

## Why `purrr`

很多分析腳本一開始都像這樣：

```r
birdfiles <- list.files(pattern = ".csv")
list_of_birdfiles <- list()

for (i in birdfiles) {
  list_of_birdfiles[[i]] <- read.csv(i)
}
```

這不是錯，但當你開始需要：

- 對每個檔案做同樣轉換
- 對每個子資料集跑同一個模型
- 保留輸出型別一致
- 遇到單一錯誤時不要整個流程中斷

`purrr` 通常會比手寫 `for` loop 更清楚。

## Functional Iteration Mindset

`purrr` 的基本問題是：

1. 我要迭代哪個資料結構
2. 我要對每個元素做什麼
3. 我希望最後回傳什麼型別

最常見的情況是 list iteration：

```r
files <- list.files()
d <- map(files[1:10], readr::read_csv)
```

這樣的思路比手動建立空 list 再逐格填值更接近「宣告我要把同一個函數套到每個元素」。

## Pipes Make the Workflow Readable

`purrr` 幾乎總是和 pipe 一起出現：

```r
output <- function_one() %>%
  function_two()
```

pipe 的價值不是少打一個暫存變數，而是讓資料流向更直觀。這在多步 list 操作時特別重要。

## `map()` Returns a List

`map()` 的預設回傳值是 list。當每個元素的結果長度不一定相同，或結果本身還是複雜物件時，這很合理。

例如從巢狀 list 中抽欄位：

```r
map(livingthings, ~ .x[["species"]])
map(gh_repos, ~ map(.x, "forks"))
```

這種寫法適合：

- 每個元素回傳 data frame
- 每個元素回傳 model object
- 每個元素回傳另一個 list

## `map_*()` Typed Variants

如果你知道每次迭代都應該回傳單一字串、數值或邏輯值，就不要只用 `map()`，改用 typed variants：

- `map_chr()`
- `map_dbl()`
- `map_int()`
- `map_lgl()`

例如把巢狀資料中的標題抽成字串向量：

```r
map_chr(sw_films, "title")
```

這樣的好處是：

- 回傳型別更明確
- 若某個元素不能轉成預期型別，會更早暴露問題
- 後續接 `sort()`、`set_names()` 或統計函數更直接

## Setting and Using Names

對 list 來說，名字常常比位置更重要。

課程裡有一個很實用的模式：

```r
sw_films <- sw_films %>%
  set_names(map_chr(sw_films, "title"))
```

這讓後續操作更好讀，因為你不再只看到 `[[3]]`，而是能用語意化名稱存取元素。

另一個常見模式是「先抽值，再同時設名稱」：

```r
map_chr(sw_films, ~ .x[["episode_id"]]) %>%
  set_names(map_chr(sw_films, "title")) %>%
  sort()
```

這非常適合整理：

- 檔名到物件的對照
- 標題到摘要值的對照
- 群組到模型輸出的對照

## Formula Shorthand

`purrr` 很常用公式簡寫：

```r
map(list_of_means, ~ data.frame(a = rnorm(n = 200, mean = .x)))
```

這裡的 `.x` 表示目前迭代到的元素。這種寫法適合短小轉換；如果邏輯變複雜，改成具名函數通常會比較清楚。

## Repeating Analysis Across Many Objects

`purrr` 很適合把同一份分析套到多個子資料集。

例如對多個教育資料集各自擬合線性模型：

```r
models <- education_data %>%
  map(~ lm(income ~ education_level, data = .x)) %>%
  map(summary)
```

這種模式在 notebook 裡很值得記住，因為它經常出現在：

- split-apply-model workflows
- 多組參數模擬
- 多資料表清理
- 多 API 回傳結果整理

## `map2()` for Two Parallel Inputs

當每次 iteration 需要兩個平行輸入時，用 `map2()`。

例如平均數和標準差要一起決定模擬資料：

```r
simdata <- map2(
  list_of_means,
  list_of_sd,
  ~ data.frame(a = rnorm(n = 200, mean = .x, sd = .y))
)
```

可以把 `map2()` 想成：

- 第一個 list 提供 `.x`
- 第二個 list 提供 `.y`
- 兩者按位置一起迭代

## `pmap()` for Many Inputs

當輸入不只兩組，而是一整個參數表時，`pmap()` 更自然。

```r
simdata <- pmap(
  inputs_list,
  function(means, sd, samplesize) {
    data.frame(a = rnorm(n = samplesize, mean = means, sd = sd))
  }
)
```

`pmap()` 適合：

- 多參數模擬
- 對每列設定跑同一個函數
- 把參數表直接轉成一批結果物件

如果你的心智模型已經是「每一列參數代表一次執行」，通常就該想到 `pmap()`。

## Error-Tolerant Mapping with `safely()`

真實資料流程常常不是每個元素都能成功處理。`safely()` 可以讓 mapping 不因單一失敗而整批中斷。

```r
a <- list("unknown", 10) %>%
  map(safely(function(x) x * 10, otherwise = NA_real_))
```

每個元素都會回傳一個 list，裡面至少有：

- `$result`
- `$error`

這樣的好處是：

- 成功與失敗都被保留下來
- 可以事後檢查哪幾筆出錯
- 不需要因一筆髒資料重跑整個流程

## `transpose()` Reorganizes Safe Results

`safely()` 的輸出常常是「每個元素各自帶一個 result/error」，這不一定方便後續整理。課程示範了一個很重要的搭配：

```r
a <- list("unknown", 10) %>%
  map(safely(function(x) x * 10, otherwise = NA_real_)) %>%
  transpose()
```

`transpose()` 之後，資料結構會從：

- 每筆一個 `result/error` pair

變成：

- 一個 `result` list
- 一個 `error` list

這樣更容易：

- 只抽成功結果
- 只檢查錯誤訊息
- 後續轉成向量或 tibble

## `possibly()` for Default Fallbacks

如果你不需要保留完整錯誤物件，只想在失敗時給預設值，用 `possibly()` 會更簡潔。

它的心智模型是：

- 成功就回傳正常結果
- 失敗就回傳你指定的 fallback value

這適合用在你已經知道「失敗時怎麼補一個安全值」的場景，例如：

- 轉型失敗就回 `NA`
- 某欄不存在就回空字串
- 某次抓取失敗就回空 list

## Working with Nested Lists

課程大量用到像 `sw_films`、GitHub API 回傳資料這種巢狀 list。這提醒了一個實務重點：

- `purrr` 很適合處理不規則、非矩形資料
- 與其急著先 `unnest`，很多時候先 `map()` 抽欄位更穩

例如：

```r
map_chr(sw_films, "title")
map(gh_repos, ~ map(.x, "forks"))
```

這種策略在處理 JSON、API 回傳物件和 web scraping 結果時尤其常見。

## Choosing Between `for`, `apply`, and `purrr`

可以用下面的簡化原則：

- 需要最直接、可逐步更新狀態的流程時，用 `for`
- 已經是矩陣或 data frame 軸向彙總時，常先想到 `apply` 家族
- 已經是 list、巢狀資料、參數組合或要加錯誤處理時，優先考慮 `purrr`

`purrr` 不是為了取代所有 loop，而是讓 list-oriented workflows 更一致。

## Practical Workflow

一個很常見的 `purrr` 工作流是：

1. 先把輸入整理成 list 或參數表
2. 用 `map()` / `map_*()` 做單一輸入 iteration
3. 用 `map2()` / `pmap()` 做多輸入 iteration
4. 需要穩定性時加上 `safely()` 或 `possibly()`
5. 必要時用 `transpose()` 或後續整理函式拆開結果
6. 再把輸出轉回 vector、tibble、模型摘要或報表

## Takeaways

- `purrr` 的核心不是語法縮寫，而是把 iteration 的輸入、操作與輸出型別說清楚
- `map()` 家族特別適合 list、巢狀資料與批次分析
- typed maps 比純 `map()` 更容易提早發現資料問題
- `map2()` 和 `pmap()` 很適合參數化模擬與批次建模
- `safely()`、`possibly()` 和 `transpose()` 是讓流程更耐髒資料的關鍵工具
