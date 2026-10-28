[Data Science](../README.md) › [R Foundations](README.md) › 函式

# 函式 (Functions)

同一段清理、摘要或轉換複製貼上第三次時，就該抽成函式：只定義一次邏輯、可以測試、改一處全部生效。Python 版見 [函式](../python-foundations/function.md)；在 dplyr 裡傳欄名的函式見 [dplyr 程式化模式](dplyr-programming-patterns.md)。

## 基本結構

```r
calc_returns <- function(x, lag = 1) {          # 名稱用動詞；預設值寫在 signature
  diff(x, lag = lag) / head(x, -lag)
}
calc_returns(c(23.4, 23.8, 22.3))               # 0.01709402 -0.06302521

# 最後一個 expression 自動回傳；return() 用於提早離開
safe_mean <- function(x) {
  if (length(x) == 0) return(NA_real_)
  mean(x, na.rm = TRUE)
}

# 匿名函式：R ≥ 4.1.0 的簡寫
sapply(1:3, \(i) i^2)                           # 同 function(i) i^2

args(cor); formals(mean); ?mean                 # 查參數
```

| 組成 | 說明 |
| --- | --- |
| arguments | 輸入資料與選項；必填的放前面，有預設值的放後面 |
| body | 邏輯本體 |
| return value | 最後一個 expression，或 `return()` |
| environment | 定義函式時所在的環境，決定找不到的變數去哪裡找（lexical scoping） |

## 參數

### 位置 vs 名稱

```r
mean(numbers, 0.1, TRUE)                        # 難讀：0.1 與 TRUE 是什麼？
mean(numbers, trim = 0.1, na.rm = TRUE)         # 前 1–2 個常用參數用位置，其餘用名稱
```

### 預設值

| 預設類型 | 例子 | 用途 |
| --- | --- | --- |
| 布林 | `na.rm = FALSE` | 開關行為 |
| 數值 | `conf.level = 0.95` | 常見設定 |
| `NULL` | `weights = NULL` | 沒給就稍後決定（`if (is.null(weights)) ...`） |
| 依賴其他參數 | `n = length(x)` | lazy evaluation：用到時才計算 |
| 選項清單 | `method = c("pearson", "spearman")` | 搭配 `match.arg(method)`，預設取第一個並驗證拼字 |

```r
toss_coin <- function(n_flips, p_head = 0.5) {
  sample(c("head", "tail"), n_flips, replace = TRUE, prob = c(p_head, 1 - p_head))
}

summarise_expr <- function(x, method = c("mean", "median")) {
  method <- match.arg(method)                   # 打錯字會報錯並列出可選值
  switch(method, mean = mean(x), median = median(x))
}
```

### 用 `...` 轉交參數

```r
calc_geometric_mean <- function(x, ...) {
  exp(mean(log(x), ...))                        # 例如 na.rm = TRUE 會傳給 mean()
}
```

`...` 的代價：拼錯的參數名會被默默吞掉或傳到意想不到的地方。只在確實要把選項轉交給下游函式時使用。

## 不要寫死

```r
# 差：檔名、欄位寫死，只能處理一個資料集
import_scores <- function() readr::read_csv("test_scores_geography.csv")

# 好：輸入是參數，輸出明確
import_scores <- function(path, cols = c("person_id", "test_date", "score")) {
  readr::read_csv(path, show_col_types = FALSE) |> dplyr::select(dplyr::all_of(cols))
}
```

函式也不要依賴全域變數：

```r
threshold <- 10
flag <- function(x) x > threshold               # 能跑，但結果取決於外部狀態
flag <- function(x, threshold = 10) x > threshold
```

## 輸入檢查與錯誤處理

重用的函式不能假設輸入永遠正確。檢查型別、長度、值域與 `NA`，並在**最早**的地方失敗。

```r
calc_geometric_mean <- function(x, na.rm = FALSE) {
  stopifnot(is.numeric(x), is.logical(na.rm), length(na.rm) == 1)
  if (any(x <= 0, na.rm = TRUE)) {
    stop("x contains non-positive values; geometric mean is undefined.", call. = FALSE)
  }
  exp(mean(log(x), na.rm = na.rm))
}
```

| 訊號 | 用途 | 例子 |
| --- | --- | --- |
| `stop()` | 無法產生可信結果，中止 | 型別錯、必要欄位不存在 |
| `warning()` | 結果可用但有風險，繼續 | 移除了 12 列含 NA 的資料 |
| `message()` | 一般資訊（可用 `suppressMessages()` 關掉） | 進度、讀了幾個檔案 |
| `stopifnot()` | 一行列出多個前提 | `stopifnot(nrow(df) > 0, "id" %in% names(df))` |

### 捕捉錯誤：`tryCatch()`

批次處理時，單一樣本失敗不應讓整個流程中止，但要記錄是誰失敗。

```r
read_one <- function(path) {
  tryCatch(
    readr::read_csv(path, show_col_types = FALSE),
    error   = function(e) { message("skip ", path, ": ", conditionMessage(e)); NULL },
    finally = message("done: ", path)           # 不論成功與否都會執行（關連線、刪暫存）
  )
}

res <- try(log("a"), silent = TRUE)             # 簡化版
inherits(res, "try-error")                      # TRUE
```

`purrr::safely()` / `possibly()` 是函數式版本，見 [函數式程式設計](functional-programming.md)。

> 不要用 `try()` 包住所有東西來「讓程式跑完」。只在預期會失敗、且知道失敗後該怎麼做的地方捕捉。

## 設計原則

| 原則 | 說明 |
| --- | --- |
| 一個函式做一件事 | 清理、建模、畫圖分開，方便單獨測試 |
| 名稱是動詞 | `clean_dates()`、`calc_cpm()`、`run_de()` |
| 輸入輸出明確 | 不讀寫全域變數，不偷偷改檔案 |
| 型別穩定 | 同一函式永遠回傳同一型別（例如永遠是 tibble） |
| 早失敗 | 前提不成立就 `stop()`，不把壞資料往下傳 |
| 邊界情況 | 空 vector、全 `NA`、長度 1、單一 level 的 factor |

風格、檔名、`lintr` 與測試見 [防禦性程式設計](defensive-programming.md)。
