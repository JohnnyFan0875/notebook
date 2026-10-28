# Functional Programming in R: for, apply and purrr

重複套用同一邏輯有三種寫法：`for` 迴圈（狀態需要逐步更新時）、base R 的 `apply` 家族（`lapply` / `sapply` / `vapply`）、`purrr` 的 `map()` 系列（回傳型別一致、錯誤容忍、巢狀資料）。本篇依序介紹，最後是 purrr 進階的 predicate、`compose()`、`partial()`。

## The apply Family

`apply` 家族用來把同一個函數套到資料結構中的多個元素上。它的核心問題不是「可不可以少寫 loop」，而是「我現在處理的是 matrix、list 還是 data frame，每次套用後希望回傳什麼型別」。

### Mental Model

先想清楚三件事：

1. input structure 是什麼
2. 每個元素要套什麼函數
3. output 要保留 list，還是簡化成 vector / matrix

### Quick Reference

| Function | Best For | Return Tendency |
| --- | --- | --- |
| `apply()` | matrix / array 的列或欄 | usually vector or matrix |
| `lapply()` | list 或 data frame 欄位 | list |
| `sapply()` | 想在 `lapply()` 基礎上自動簡化 | vector or matrix when possible |
| `vapply()` | 需要明確保證回傳型別 | strict, safer simplified output |
| `tapply()` | 依群組對向量做彙總 | grouped summaries |
| `mapply()` | 多個輸入一起逐元素套函數 | simplified multi-input output |

### lapply

`lapply()` 會保留 list 結構，適合當每個元素的回傳型別不一定一致時：

```r
stock_list <- list(
  stock_name = "Apple",
  ticker = "AAPL",
  price = 126.5,
  good_deal = TRUE
)

lapply(stock_list, FUN = class)
```

如果你只是想先確認每個元素型別，`lapply()` 很穩。

### sapply

當每個元素的輸出長得很一致時，`sapply()` 會嘗試把結果簡化：

```r
sapply(stock_list, FUN = class)
```

這通常比 `lapply()` 更方便閱讀，但也因為自動簡化，結果型別有時會比預期更難掌控。

### vapply

`vapply()` 的用途是「我想要簡化結果，但不想把型別交給 R 猜」。

```r
vapply(stock_list, FUN = class, FUN.VALUE = character(1))
```

`FUN.VALUE` 是你對每次輸出的型別契約。例如：

- `character(1)` 表示每次都應回傳長度 1 的字串
- `numeric(1)` 表示每次都應回傳長度 1 的數值

和 `sapply()` 相比，`vapply()` 的好處是：

- 回傳型別更穩定
- 若某次輸出不符合預期，會提早報錯
- 在函數化分析流程中更容易除錯

如果這份結果後面還要再接別的分析步驟，`vapply()` 往往比 `sapply()` 更安全。

### apply a Custom Summary

對多欄數值資料做同一份摘要，是 `apply` 類函數的常見用法：

```r
simple_summary <- function(x) {
  c(mean = mean(x), sd = sd(x))
}

sapply(stock_return, FUN = simple_summary)
```

這種模式很適合：

- 每欄都做相同彙總
- 每個資產都算同一組風險與報酬指標
- 每個變數都套相同清理函數

### Choosing Between Loop and apply

- 如果你需要逐步更新狀態，通常還是 `for` / `while` 更自然。
- 如果你只是把同一個函數套到一批元素上，`apply` 類函數通常更簡潔。
- 如果回傳型別很重要，優先考慮 `vapply()`，避免 `sapply()` 的自動簡化帶來不確定性。

### Common Mistakes

- 對 data frame 使用 `apply()` 後，資料先被強制轉型成 matrix，造成型別意外改變。
- 以為 `sapply()` 永遠回傳 vector，結果某些情況回傳 matrix 或 list。
- 忘記 `vapply()` 的 `FUN.VALUE` 是契約，不符合時其實應該把它當成資料或邏輯錯誤訊號。
- 把複雜副作用流程硬塞進 `apply`，反而比普通 loop 更難讀。
- 沒先想清楚 input 與 output 結構，只是機械地把 loop 改寫成 `apply`。

## Functional Programming with purrr

`purrr` 是 R 裡把「對很多元素重複做同一件事」整理得更穩定的一套工具。它的重點不是炫技，而是把 iteration 寫成回傳型別更明確、可組合、也更容易加上錯誤處理的資料流程。

### Why `purrr`

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

### Functional Iteration Mindset

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

### Pipes Make the Workflow Readable

`purrr` 幾乎總是和 pipe 一起出現：

```r
output <- function_one() %>%
  function_two()
```

pipe 的價值不是少打一個暫存變數，而是讓資料流向更直觀。這在多步 list 操作時特別重要。

### `map()` Returns a List

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

### `map_*()` Typed Variants

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

### Setting and Using Names

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

### Formula Shorthand

`purrr` 很常用公式簡寫：

```r
map(list_of_means, ~ data.frame(a = rnorm(n = 200, mean = .x)))
```

這裡的 `.x` 表示目前迭代到的元素。這種寫法適合短小轉換；如果邏輯變複雜，改成具名函數通常會比較清楚。

### Repeating Analysis Across Many Objects

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

### `map2()` for Two Parallel Inputs

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

### `pmap()` for Many Inputs

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

### Error-Tolerant Mapping with `safely()`

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

### `transpose()` Reorganizes Safe Results

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

### `possibly()` for Default Fallbacks

如果你不需要保留完整錯誤物件，只想在失敗時給預設值，用 `possibly()` 會更簡潔。

它的心智模型是：

- 成功就回傳正常結果
- 失敗就回傳你指定的 fallback value

這適合用在你已經知道「失敗時怎麼補一個安全值」的場景，例如：

- 轉型失敗就回 `NA`
- 某欄不存在就回空字串
- 某次抓取失敗就回空 list

### Working with Nested Lists

課程大量用到像 `sw_films`、GitHub API 回傳資料這種巢狀 list。這提醒了一個實務重點：

- `purrr` 很適合處理不規則、非矩形資料
- 與其急著先 `unnest`，很多時候先 `map()` 抽欄位更穩

例如：

```r
map_chr(sw_films, "title")
map(gh_repos, ~ map(.x, "forks"))
```

這種策略在處理 JSON、API 回傳物件和 web scraping 結果時尤其常見。

### Choosing Between `for`, `apply`, and `purrr`

可以用下面的簡化原則：

- 需要最直接、可逐步更新狀態的流程時，用 `for`
- 已經是矩陣或 data frame 軸向彙總時，常先想到 `apply` 家族
- 已經是 list、巢狀資料、參數組合或要加錯誤處理時，優先考慮 `purrr`

`purrr` 不是為了取代所有 loop，而是讓 list-oriented workflows 更一致。

### Practical Workflow

一個很常見的 `purrr` 工作流是：

1. 先把輸入整理成 list 或參數表
2. 用 `map()` / `map_*()` 做單一輸入 iteration
3. 用 `map2()` / `pmap()` 做多輸入 iteration
4. 需要穩定性時加上 `safely()` 或 `possibly()`
5. 必要時用 `transpose()` 或後續整理函式拆開結果
6. 再把輸出轉回 vector、tibble、模型摘要或報表

### Takeaways

- `purrr` 的核心不是語法縮寫，而是把 iteration 的輸入、操作與輸出型別說清楚
- `map()` 家族特別適合 list、巢狀資料與批次分析
- typed maps 比純 `map()` 更容易提早發現資料問題
- `map2()` 和 `pmap()` 很適合參數化模擬與批次建模
- `safely()`、`possibly()` 和 `transpose()` 是讓流程更耐髒資料的關鍵工具

## Functional Programming with purrr Advanced

基礎 `purrr` 重點是把 iteration 寫得穩定；進階 `purrr` 則更像是在組裝一套可重用的資料流程。這一層開始關心的不只是 `map()`，而是如何把 predicate、function operator 與巢狀 list 操作組成更乾淨的工作流。

### A More Functional View of R

這份課程反覆強調兩件事：

- everything that exists is an object
- everything that happens is a function call

在 R 裡，函數本身也可以被：

- 存進變數
- 放進 list
- 當成其他函數的輸入
- 當成函數回傳值

這就是 `purrr` 進階技巧成立的前提。

### Nested Data Is Normal

`purrr` 很常出現在處理 API 或 JSON 的場景，因為 JSON 在 R 裡通常就是巢狀 list。

像課程中的 `rstudioconf` tweet dataset 就是一個多層 list：

```r
length(rstudioconf)
length(rstudioconf[[1]])
vec_depth(rstudioconf)
```

這類檢查很實用，因為在真正開始抽欄位前，你需要先知道：

- 最外層有多少元素
- 每個元素大概長什麼樣
- 巢狀深度有多深

### `keep()` and `discard()`

當你不是要「轉換」元素，而是要「依條件篩掉或保留」元素時，用 `keep()` / `discard()` 很自然。

```r
over_30000 <- keep(visits2016, ~ sum(.x) > 30000)
under_30000 <- discard(visits2016, ~ sum(.x) > 30000)
```

可以把它們理解成 list 版本的 filter：

- `keep()` 保留符合條件的元素
- `discard()` 移除符合條件的元素

這在 list of vectors、list of data frames、或巢狀 API 回傳值上都很常用。

### Predicates as Reusable Functions

條件本身也可以先抽出來，變成可重用 predicate：

```r
limit <- as_mapper(~ sum(.x) > 30000)
over_mapper <- keep(visits2016, limit)
```

這個思路很重要。當條件開始變長，與其在每次 `keep()` / `discard()` 裡重寫，不如先命名成一個 predicate，再重複使用。

### Combining `map()` with `keep()`

課程有一個很好用的模式：先 map，再在每個子物件內做條件保留。

```r
df_list <- list(iris, airquality) %>% map(head)
map(df_list, ~ keep(.x, is.factor))
```

這代表：

- 外層 `map()` 迭代資料表
- 內層 `keep()` 保留每張表中符合條件的欄位

這種雙層 list thinking 很適合欄位探索、批次檢查和 schema 比對。

### `compact()` Removes `NULL`

當 list 中有許多 `NULL` 結果時，`compact()` 很實用：

```r
list(1, NULL, 3, 4, NULL) %>%
  compact()
```

它不是依一般條件篩選，而是專門拿掉 `NULL`。這在下列情境特別常見：

- 某些 API 回傳欄位缺失
- 某些嘗試失敗後故意回 `NULL`
- 某些步驟選擇性產出結果

### `possibly()` Plus `compact()`

一個很實務的模式是失敗時回 `NULL`，之後一次清掉：

```r
l <- list(1, 2, 3, "a")
possible_log <- possibly(log, otherwise = NULL)
map(l, possible_log) %>% compact()
```

這個 pattern 很值得記住，因為它把流程分成兩步：

1. 失敗時不要中斷，先回 `NULL`
2. 最後再用 `compact()` 清理無效結果

如果你只想保留成功輸出，而不在意完整錯誤資訊，這比 `safely()` 更輕量。

### Cleaning Safe Results with `transpose()`

對 `safely()` 產生的 list，`transpose()` 仍然是整理關鍵：

```r
map(l, safe_log) %>% transpose()
```

重點不是語法本身，而是資料結構轉換：

- 原本是每筆一個 `result/error`
- 轉成一個 results 集合和一個 errors 集合

這樣更方便後續：

- 單獨檢查失敗原因
- 批次抽取成功值
- 接著再 `compact()` 或轉成 tibble

### `flatten()` Removes One Nesting Level

當 list 只是多包了一層，不需要保留那一層結構時，可以用 `flatten()`：

```r
my_list <- list(
  list(a = 1),
  list(b = 2)
)

flatten(my_list)
```

這個操作的重點是：

- 降低一層巢狀
- 保留內部元素
- 讓後續抽值或命名更直接

它很適合在 API 整理或分批運算結果合併時做第一步結構簡化。

### `as_mapper()` Creates Reusable Mappers

公式寫法 `~ .x * 2` 很方便，但如果同一個 transformation 要重複使用，可以先轉成 mapper：

```r
mult <- as_mapper(~ .x * 2)
ten_times <- as_mapper(~ .x * 10)
map(1:5, ten_times)
```

可以把 `as_mapper()` 想成把匿名函數轉成可命名、可重複套用的 transformation object。

這在以下場景很好用：

- 同一個轉換要套到很多 list
- 想先把邏輯命名再組合
- 想把 predicate 或 mapper 傳進別的函數

### `negate()` Inverts a Predicate

當你已經有一個 predicate，只想要它的反面，不需要再重寫一次條件：

```r
under_hundred <- as_mapper(~ mean(.x) < 100)
not_under_hundred <- negate(under_hundred)
map_lgl(98:102, under_hundred)
```

`negate()` 的價值在於避免條件邏輯分散。你先寫出一個清楚的「正向條件」，再需要時反轉它。

### `partial()` Prefills Arguments

`partial()` 可以先把某些參數綁定起來，產生一個新的函數：

```r
mean_na_rm <- partial(mean, na.rm = TRUE)
lm_iris <- partial(lm, data = iris)
```

這很適合：

- 固定常用選項
- 減少重複參數
- 在 `map()` 裡傳入已配置好的函數

例如不再每次都重寫 `na.rm = TRUE`，而是先建立一個一致版本的平均函數。

### `compose()` Builds Pipelines of Functions

當你想把多個小函數組成一個可重複套用的大函數時，用 `compose()`。

課程中的模式很值得保留：

```r
tidy_iris_lm <- compose(
  as_mapper(~ dplyr::filter(.x, p.value < 0.05)),
  broom::tidy,
  partial(stats::lm, data = iris, na.action = na.fail)
)
```

這表示一個輸入公式會依序經過：

1. `lm(...)`
2. `tidy()`
3. `filter(...)`

之後就能直接：

```r
list(
  Petal.Length ~ Petal.Width,
  Petal.Width ~ Sepal.Width,
  Sepal.Width ~ Sepal.Length
) %>% map(tidy_iris_lm)
```

這是進階 `purrr` 很重要的觀念: 與其反覆貼上同一段 pipeline，不如把 pipeline 本身做成函數。

### `partial()` Plus `compose()`

這兩者常常一起用：

```r
rounded_mean <- compose(
  partial(round, digits = 2),
  partial(mean, na.rm = TRUE)
)
```

或：

```r
rounded_mean <- compose(
  partial(round, digits = 1),
  partial(mean, trim = 2, na.rm = TRUE)
)
```

好處是你可以把一個常用分析習慣變成可重複使用的單一函數，例如：

- 先算平均
- 自動忽略缺失值
- 再固定四捨五入位數

### Cleaner Code Through Reusable Components

課程中用一連串重複 `lm(...) %>% tidy() %>% filter(...)` 的例子說明，重複貼上最容易藏 typo，也最難維護。

`purrr` 的進階價值不只是少寫幾行，而是把程式拆成：

- 小而清楚的 predicate
- 可重用的 mapper
- 已經預填參數的函數
- 已經組好的函數管線

這會讓批次分析更容易檢查，也比較不會在第 4 次複製貼上時出現隱性錯字。

### Practical Workflow

進階 `purrr` 常見工作流可以整理成：

1. 先理解巢狀資料的深度與結構
2. 用 `map()` / `map_*()` 抽值或轉換
3. 用 `keep()` / `discard()` 做 predicate-based filtering
4. 用 `possibly()` / `safely()` 讓流程容錯
5. 用 `compact()` / `transpose()` / `flatten()` 清理結果結構
6. 用 `partial()`、`compose()`、`as_mapper()` 產生可重用函數

### Takeaways

- 進階 `purrr` 的核心是把 function 當成可操作物件
- `keep()`、`discard()`、`compact()` 很適合 list 清理與條件篩選
- `partial()` 能把常見參數習慣封裝起來
- `compose()` 讓整段分析 pipeline 變成單一可重用函數
- `as_mapper()` 與 `negate()` 有助於建立可命名、可重用的條件與 transformation
- 處理 JSON 或 API 回傳資料時，先理解巢狀結構，再決定何時抽值、何時降維、何時清掉失敗結果
