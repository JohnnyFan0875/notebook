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

## Reading Documentation

不確定函數接受哪些參數時，先查說明文件：

```r
?mean
?matrix
```

這一步很重要，因為很多錯誤不是函數做不到，而是參數沒有設對。

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

## Design Guidelines

- 函數名稱要描述動作，例如 `calc_returns()`、`clean_dates()`。
- 優先讓函數只做一件事，避免一個函數同時清理、建模、畫圖。
- 對容易出錯的輸入先做基本檢查，例如長度、型別、是否含缺失值。
- 把可調參數放進 argument，不要寫死在函數裡。

## Common Mistakes

- 只是把一長段 script 包進函數，卻沒有明確輸入與輸出。
- 依賴外部全域變數，導致函數難以重現。
- 沒處理 `NA`、空向量或長度不足的情況。
- 為了省一行而過度省略 `return()` 或參數命名，讓程式可讀性下降。
