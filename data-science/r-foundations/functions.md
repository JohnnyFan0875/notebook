# Functions in R

函數是把重複邏輯包裝成可重用工具的基本單位。當同一段資料處理、統計摘要或欄位轉換開始重複出現時，就該考慮抽成函數，而不是繼續複製貼上。

## Function Structure

R 函數的基本形式如下：

```r
func_name <- function(arguments) {
  body
}
```

函數通常由三部分組成：

- arguments: 輸入資料與選項
- body: 實際執行的邏輯
- return value: 最終輸出

R 會自動回傳最後一個 expression，但在流程較長時，明確使用 `return()` 會更清楚。

## Required and Optional Arguments

有些參數是必填的，有些可以給預設值：

```r
add <- function(x, value = 1) {
  x + value
}

add(7)
# [1] 8

add(7, value = 3)
# [1] 10
```

像 `na.rm = TRUE` 這類參數就是很典型的 optional argument。它們常用來控制缺失值處理、輸出格式或行為細節。

## Calling Arguments by Position or Name

R 函數可以用「位置」或「名稱」傳參數。

```r
mean(numbers, 0.1, TRUE)
mean(na.rm = TRUE, trim = 0.1, x = numbers)
mean(numbers, trim = 0.1, na.rm = TRUE)
```

實務上比較穩定的做法是：

- 常見、直觀的前幾個參數可依位置傳入
- 不那麼常見或容易混淆的參數改用名稱

這樣既不會太冗長，也能降低位置傳錯的風險。

## Function Names Should Describe an Action

函數名稱最好包含動詞，讓讀者一眼知道它做什麼。

例如：

- `clean_scores()`
- `calc_geometric_mean()`
- `run_linear_regression()`

比起過度簡短或歷史包袱很重的名稱，這種命名更適合 notebook 筆記與分析專案。

## Generalize Instead of Hard-Coding

很多初學者會先寫出只能處理單一資料集的函數，然後很快就卡住。

例如把檔名、變數名都寫死：

```r
import_test_scores <- function(filename) {
  test_scores_raw <- readr::read_csv(filename)

  test_scores_raw |>
    dplyr::select(person_id, first_name, last_name, test_date, score)
}
```

這種做法比直接把 `"test_scores_geography.csv"` 寫死在函數裡更好，因為：

- 重用性更高
- 更容易測試
- 更容易移到別的資料集

## Reading Documentation

不確定函數接受哪些參數時，先查說明文件：

```r
?mean
?matrix
```

這一步很重要，因為很多錯誤不是函數做不到，而是參數沒有設對。

你也可以直接看函數參數列表：

```r
args(mean)
args(median)
args(cor)
```

這對理解 default arguments 和 `...` 很有幫助。

## Default Arguments

預設值應該直接寫在函數 signature 裡，而不是在函數內部補救。

```r
toss_coin <- function(n_flips, p_head = 0.5) {
  coin_sides <- c("head", "tail")
  weights <- c(p_head, 1 - p_head)
  sample(coin_sides, n_flips, replace = TRUE, prob = weights)
}
```

常見的 default 類型包括：

- 布林值，例如 `na.rm = FALSE`
- 數值，例如 `conf.level = 0.95`
- `NULL`，表示「若使用者沒提供，就稍後再決定」
- 一個依賴其他參數的值

好預設值的標準不是花俏，而是讓大多數常見呼叫可以直接工作。

## Forwarding Arguments with `...`

當你想把額外參數往下傳給別的函數時，可以使用 `...`。

```r
calc_geometric_mean <- function(x, ...) {
  exp(mean(log(x), ...))
}
```

`...` 很方便，但也有代價：

- 讀函數的人不一定知道哪些參數最後會被接受
- 拼錯參數名時，有時不容易立刻發現

所以只有在確實需要把選項往下傳時再用。

## Example: Arithmetic Returns

把單次計算抽成函數後，才容易在不同價格序列上重用：

```r
arith_returns <- function(x) {
  diff(x) / x[-length(x)]
}

prices <- c(23.4, 23.8, 22.3)
arith_returns(prices)
# [1]  0.01709402 -0.06302521
```

這種寫法的好處是：

- 核心公式只定義一次
- 後續可以直接套到別的向量
- 更容易測試長度、缺失值與極端案例

## Returning Early

R 會自動回傳最後一個 expression，但在遇到錯誤條件或特殊情況時，提早 `return()` 往往更清楚。

```r
simple_sum <- function(x) {
  if (anyNA(x)) {
    return(NA)
  }

  total <- 0
  for (value in x) {
    total <- total + value
  }

  total
}
```

這種 early return 很適合：

- 前置條件不成立
- 缺失值或空輸入要走特例
- 後續運算已經沒有意義

## Input Validation

函數一旦開始重用，就不能假設使用者永遠傳對資料。

基本檢查通常包括：

- 類型是否正確
- 長度是否合理
- 值域是否合理
- 是否含有不允許的 `NA`

例如 geometric mean 只對正數有意義：

```r
calc_geometric_mean <- function(x, na.rm = FALSE) {
  if (!is.numeric(x)) {
    stop("x must be numeric.")
  }

  if (any(x <= 0, na.rm = TRUE)) {
    stop("x contains non-positive values, so geometric mean is undefined.")
  }

  exp(mean(log(x), na.rm = na.rm))
}
```

如果專案裡已經使用 `assertive` 或類似工具，也可以把常見檢查交給套件處理。

## Errors, Warnings, and Messages

R 函數不一定只能「算成功」或「直接爆掉」，還有幾種常見訊號：

- `stop()`：直接中止，表示結果不可靠或條件不成立
- `warning()`：繼續執行，但提醒使用者結果可能需要注意
- `message()`：提供一般資訊，不一定代表問題

一個簡單原則是：

- 無法產生可信結果時用 `stop()`
- 還能產生結果，但有風險時用 `warning()`

## Coercion and Defensive Defaults

有些參數表面上看起來是單一布林值，但使用者可能傳進長度大於 1 的向量，或型別不完全對。

像 `na.rm` 這類參數，必要時可以先標準化，再交給核心計算：

- 只取第一個值
- 明確轉成 logical
- 對奇怪輸入提供 warning 或 error

這種 defensive programming 會讓函數在 notebook 之外也更穩定。

## Design Guidelines

- 函數名稱要描述動作，例如 `calc_returns()`、`clean_dates()`。
- 優先讓函數只做一件事，避免一個函數同時清理、建模、畫圖。
- 對容易出錯的輸入先做基本檢查，例如長度、型別、是否含缺失值。
- 把可調參數放進 argument，不要寫死在函數裡。
- default arguments 直接寫進 signature，不要在函數中散落補丁邏輯。
- 只有真的要向下游函數轉交選項時才用 `...`。
- 能提早判斷失敗條件時，就 early return 或 `stop()`，不要把壞資料一路往下傳。

## Common Mistakes

- 只是把一長段 script 包進函數，卻沒有明確輸入與輸出。
- 依賴外部全域變數，導致函數難以重現。
- 沒處理 `NA`、空向量或長度不足的情況。
- 為了省一行而過度省略 `return()` 或參數命名，讓程式可讀性下降。
- 把檔名、欄位名或分析情境寫死，讓函數無法泛化。
- 過度依賴位置傳參數，導致像 `TRUE`、`FALSE` 這種值語意不清。
- 使用 `...` 卻沒有想清楚它最後要傳給誰。
