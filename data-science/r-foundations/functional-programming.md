[Data Science](../README.md) › [R Foundations](README.md) › 函數式程式設計

# 函數式程式設計 (Functional Programming: for, apply, purrr)

「對很多樣本 / 檔案 / 基因 / 參數組合做同一件事」是分析裡最常見的模式。R 有三種寫法：`for` 迴圈、base R 的 `apply` 家族、purrr 的 `map()` 系列。差別不在少打幾行，而在**回傳型別是否明確**與**單一失敗會不會讓整批中止**。Python 的對應寫法（comprehension、generator）見 [控制流程](../python-foundations/control-flow.md) 與 [迭代器與生成器](../python-foundations/iterator.md)。

## 選哪一種

| 情境 | 用什麼 | 原因 |
| --- | --- | --- |
| 每步依賴上一步結果（模擬、累加、收斂） | `for` / `while` | 狀態更新最直觀 |
| 有副作用（寫檔、畫圖、印訊息） | `for` 或 `purrr::walk()` | 不需要回傳值 |
| matrix 的列 / 欄摘要 | `apply()`、`rowMeans()` 等 | 軸向運算；能用 `rowSums()` 就別用 `apply()` |
| list / data frame 欄位逐一處理，只用 base R | `lapply()` / `vapply()` | 無依賴 |
| list、巢狀 JSON、參數表、需要容錯 | purrr | 型別明確、`safely()`、`pmap()` |
| 分組摘要 | dplyr `summarise(.by = )` | 比 `tapply()` 好讀，見 [Tidyverse 工作流](tidyverse-workflow.md) |

> 先想清楚三件事：迭代的是什麼結構、每個元素做什麼、最後要 list 還是 vector。想不清楚就硬把 loop 改成 `apply`，通常比原本更難讀。

`for` 迴圈本身不慢；慢的是在迴圈裡讓物件逐步長大。預先配置與向量化見 [寫出有效率的 R](writing-efficient-r-code.md)。

## apply 家族 (base R)

| 函式 | 輸入 | 回傳 | 注意 |
| --- | --- | --- | --- |
| `apply(X, MARGIN, FUN)` | matrix / array | vector 或 matrix | 對 data frame 使用會先轉成 matrix，混合型別全變字串 |
| `lapply(X, FUN)` | list / data frame 欄位 | 永遠是 list | 最穩定 |
| `sapply(X, FUN)` | 同上 | 盡量簡化成 vector / matrix | 結果型別依資料而變，可能悄悄回傳 list |
| `vapply(X, FUN, FUN.VALUE)` | 同上 | 依 `FUN.VALUE` 契約簡化 | 不符契約就報錯；程式中優先用它取代 `sapply()` |
| `mapply(FUN, ...)` / `Map()` | 多個平行輸入 | 簡化 / list | 對應 purrr 的 `map2()` / `pmap()` |
| `tapply(X, INDEX, FUN)` | vector + 分組 | 依組摘要 | |

```r
stock <- list(name = "Apple", ticker = "AAPL", price = 126.5, good_deal = TRUE)

lapply(stock, class)                              # list，每個元素一個結果
sapply(stock, class)                              # 具名 character vector
vapply(stock, class, FUN.VALUE = character(1))    # 同上，但型別有保證

# 每欄算同一組摘要：每次回傳長度 2 → sapply 簡化成 2 × p matrix
simple_summary <- function(x) c(mean = mean(x), sd = sd(x))
sapply(mtcars[, 1:3], simple_summary)
vapply(mtcars[, 1:3], simple_summary, FUN.VALUE = numeric(2))

# matrix：每個基因（列）的變異數；1 = 列、2 = 欄
expr <- matrix(rnorm(20), nrow = 5, dimnames = list(paste0("g", 1:5), NULL))
apply(expr, 1, var)
```

`sapply()` 的陷阱：輸入為空時回傳 `list()`；某次結果長度不同時回傳 list 而不是 matrix。後續程式若假設是 vector 就會在少數資料上才出錯，`vapply()` 會在當下報錯。

## purrr 基礎

### `map()` 與 typed variants

| 函式 | 回傳 | 用途 |
| --- | --- | --- |
| `map()` | list | 每個結果是 data frame、模型、list |
| `map_chr()` / `map_dbl()` / `map_int()` / `map_lgl()` | 對應型別的 vector | 每個結果長度為 1；型別不符就報錯 |
| `map2(.x, .y, f)` | list | 兩個平行輸入 |
| `pmap(.l, f)` | list | 參數表的每一列跑一次 |
| `imap(.x, f)` | list | 同時用到元素與名稱（`.y` 是名稱或索引） |
| `walk()` / `walk2()` | 輸入本身（隱形） | 只為副作用：寫檔、存圖 |
| `list_rbind()` / `list_cbind()` | data frame | 把 list of data frames 綁起來（取代 `map_dfr()`） |

```r
library(purrr)

# 匿名函式三種寫法：R ≥ 4.1 的 \(x) 是目前建議寫法
map_dbl(1:3, \(x) x^2)
map_dbl(1:3, ~ .x^2)                       # purrr 公式簡寫，舊程式常見
map_dbl(1:3, function(x) x^2)

# 用名稱或位置抽巢狀 list 的元素（處理 JSON / API 回傳）
map_chr(sw_films, "title")
map(gh_repos, \(repo) map(repo, "forks"))  # 兩層巢狀

# 先抽值，再用另一個欄位當名稱
map_int(sw_films, "episode_id") |>
  set_names(map_chr(sw_films, "title")) |>
  sort()
```

### 典型工作流：讀很多樣本檔並合併

```r
files <- list.files("counts", pattern = "\\.tsv$", full.names = TRUE) |>
  set_names(\(f) tools::file_path_sans_ext(basename(f)))    # 名稱 = 樣本 ID

counts <- files |>
  map(\(f) readr::read_tsv(f, show_col_types = FALSE), .progress = TRUE) |>
  list_rbind(names_to = "sample_id")        # 名稱變成一欄，不會丟失樣本來源
```

`set_names()` 是關鍵：之後的結果都帶著樣本名稱，不必再靠位置 `[[3]]` 對回去。

### 對每組資料擬合模型

```r
models <- split(mtcars, ~ cyl) |>              # list of data frames
  map(\(df) lm(mpg ~ wt, data = df))

map(models, broom::tidy) |> list_rbind(names_to = "cyl")
map_dbl(models, \(m) summary(m)$r.squared)
```

tibble 版本是 `nest()` + `mutate(model = map(data, ...))`，見 [tidyr 資料重塑](data-reshaping-with-tidyr.md)；建模解讀見 [解釋型建模](explanatory-modeling-in-r.md)。

### 多個輸入：`map2()` 與 `pmap()`

```r
means <- list(0, 5, 10); sds <- list(1, 2, 3)
sims <- map2(means, sds, \(m, s) rnorm(200, mean = m, sd = s))

# 參數表的每一列 = 一次模擬；欄名對應函式參數名
params <- tibble::tibble(mean = c(0, 5), sd = c(1, 2), n = c(100, 200))
sims <- pmap(params, \(mean, sd, n) rnorm(n, mean, sd))

# 只為副作用：每組各存一張圖
walk2(plots, paste0("fig/", names(plots), ".png"), \(p, f) ggplot2::ggsave(f, p))
```

## 容錯：`safely()`、`possibly()`

批次處理幾百個樣本時，一個壞檔不應讓整批中止，但要知道是誰壞了。

| 函式 | 失敗時回傳 | 適用 |
| --- | --- | --- |
| `safely(f)` | `list(result = NULL, error = <condition>)` | 需要知道**為什麼**失敗 |
| `possibly(f, otherwise = NA)` | `otherwise` 指定的值 | 只需要預設值，不在乎原因 |
| `quietly(f)` | 結果 + 擷取的 output / warnings / messages | 收集警告 |
| `insistently()` / `slowly()` | 重試 / 限速 | 呼叫不穩定的 API |

```r
x <- list(1, 10, "a")

res <- map(x, safely(log))
res <- list_transpose(res)          # 從「每筆一個 result/error」轉成「result 一組、error 一組」
failed <- !map_lgl(res$error, is.null)
names(x)[failed]                    # 哪幾筆失敗
res$error[failed] |> map_chr(conditionMessage)

map(x, possibly(log, otherwise = NULL)) |> compact()   # 失敗回 NULL，最後一次清掉
map_dbl(x, possibly(log, otherwise = NA_real_))        # 保留位置，失敗為 NA
```

> `possibly(..., otherwise = NA)` 會把錯誤藏起來。正式流程中至少記錄失敗的筆數與名稱，否則下游統計會在少了幾個樣本的情況下照常產出。

## 進階：list 篩選與重組

| 函式 | 作用 | 例子 |
| --- | --- | --- |
| `keep(.x, pred)` / `discard()` | 依條件保留 / 移除元素 | `keep(df_list, \(d) nrow(d) > 0)` |
| `compact()` | 移除 `NULL` 與長度 0 的元素 | 配合 `possibly(otherwise = NULL)` |
| `detect()` / `detect_index()` | 第一個符合條件的元素 / 位置 | |
| `every()` / `some()` | 全部 / 任一符合 | `every(files, file.exists)` |
| `list_flatten()` | 去掉一層巢狀（取代 `flatten()`） | |
| `list_transpose()` | 內外層互換（取代 `transpose()`） | 整理 `safely()` 結果 |
| `pluck(x, "a", 1)` / `pluck_depth()` | 安全取深層元素 / 巢狀深度（取代 `vec_depth()`） | 缺少時回 `NULL` 而非報錯 |
| `reduce(.x, f)` / `accumulate()` | 兩兩累積 | `reduce(df_list, dplyr::left_join, by = "gene_id")` |

```r
# 每張表只保留 factor 欄位：外層迭代表、內層篩欄位
list(iris, airquality) |> map(\(df) keep(df, is.factor))

# 先檢查巢狀結構再決定怎麼抽
length(tweets); length(tweets[[1]]); pluck_depth(tweets)

# 多個樣本表依 gene_id 依序合併成一張寬表
reduce(list(cts_a, cts_b, cts_c), dplyr::full_join, by = "gene_id")
```

## 進階：把函式當成物件

R 裡函式和其他物件一樣，可以存進變數、放進 list、當參數傳、當回傳值。purrr 提供幾個「產生新函式」的工具。

| 函式 | 作用 | 例子 |
| --- | --- | --- |
| `partial(f, ...)` | 預先填入參數 | `mean_na <- partial(mean, na.rm = TRUE)` |
| `compose(f, g, h)` | 組成管線，**預設由右往左**執行 | `compose(round, mean)` = `round(mean(x))` |
| `negate(pred)` | 反轉條件 | `discard` ≈ `keep` + `negate` |
| `as_mapper(~ ...)` | 把公式轉成可命名、可重用的函式 | 現在用 `\(x)` 直接命名即可 |

```r
# 重複的 lm |> tidy |> filter 改成一個函式，避免第 4 次複製貼上時出現錯字
tidy_sig_lm <- compose(
  \(tbl) dplyr::filter(tbl, p.value < 0.05),     # 3. 最後執行
  broom::tidy,                                   # 2.
  partial(lm, data = iris, na.action = na.fail)  # 1. 最先執行
)

list(Petal.Length ~ Petal.Width,
     Petal.Width  ~ Sepal.Width,
     Sepal.Width  ~ Sepal.Length) |>
  map(tidy_sig_lm)

rounded_mean <- compose(partial(round, digits = 2), partial(mean, na.rm = TRUE))
rounded_mean(c(1.234, 5.678, NA))                # 3.46

is_small <- \(x) mean(x) < 100
map_lgl(98:102, negate(is_small))                # FALSE FALSE TRUE TRUE TRUE
```

`compose(..., .dir = "forward")` 可改成由左往右，順序和 pipe 一致，較不易搞混。

## 舊寫法對照（purrr ≥ 1.0）

| 舊 | 新 |
| --- | --- |
| `map_dfr(x, f)` / `map_dfc()` | `map(x, f) \|> list_rbind()` / `list_cbind()` |
| `flatten()` | `list_flatten()` |
| `transpose()` | `list_transpose()` |
| `vec_depth()` | `pluck_depth()` |
| `~ .x + 1` | `\(x) x + 1`（公式仍可用，但官方建議匿名函式） |
| `%>%` | `\|>`（R ≥ 4.1） |

## 平行化

`map()` 系列換成 furrr 的 `future_map()` 即可平行執行，設定方式見 [平行運算](parallel-programming-in-r.md)。purrr ≥ 1.1 也提供 `in_parallel()` 搭配 mirai。
