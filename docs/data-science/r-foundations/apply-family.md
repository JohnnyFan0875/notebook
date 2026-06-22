# The apply Family

`apply` 家族用來把同一個函數套到資料結構中的多個元素上。它的核心問題不是「可不可以少寫 loop」，而是「我現在處理的是 matrix、list 還是 data frame，每次套用後希望回傳什麼型別」。

## Mental Model

先想清楚三件事：

1. input structure 是什麼
2. 每個元素要套什麼函數
3. output 要保留 list，還是簡化成 vector / matrix

## Quick Reference

| Function | Best For | Return Tendency |
| --- | --- | --- |
| `apply()` | matrix / array 的列或欄 | usually vector or matrix |
| `lapply()` | list 或 data frame 欄位 | list |
| `sapply()` | 想在 `lapply()` 基礎上自動簡化 | vector or matrix when possible |
| `vapply()` | 需要明確保證回傳型別 | strict, safer simplified output |
| `tapply()` | 依群組對向量做彙總 | grouped summaries |
| `mapply()` | 多個輸入一起逐元素套函數 | simplified multi-input output |

## lapply

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

## sapply

當每個元素的輸出長得很一致時，`sapply()` 會嘗試把結果簡化：

```r
sapply(stock_list, FUN = class)
```

這通常比 `lapply()` 更方便閱讀，但也因為自動簡化，結果型別有時會比預期更難掌控。

## apply a Custom Summary

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

## Choosing Between Loop and apply

- 如果你需要逐步更新狀態，通常還是 `for` / `while` 更自然。
- 如果你只是把同一個函數套到一批元素上，`apply` 類函數通常更簡潔。
- 如果回傳型別很重要，優先考慮 `vapply()`，避免 `sapply()` 的自動簡化帶來不確定性。

## Common Mistakes

- 對 data frame 使用 `apply()` 後，資料先被強制轉型成 matrix，造成型別意外改變。
- 以為 `sapply()` 永遠回傳 vector，結果某些情況回傳 matrix 或 list。
- 把複雜副作用流程硬塞進 `apply`，反而比普通 loop 更難讀。
- 沒先想清楚 input 與 output 結構，只是機械地把 loop 改寫成 `apply`。
