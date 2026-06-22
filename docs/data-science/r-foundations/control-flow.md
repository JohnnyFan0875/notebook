# Control Flow in R

控制流程用來決定「什麼條件下執行什麼事」以及「哪些步驟需要重複執行」。R 雖然支援完整的流程控制，但在資料分析情境中，應先偏好向量化與彙總函數，只有在狀態需要逐步更新時才使用 loop。

## Relational Operators

條件判斷最基本的是比較運算：

| Operator | Meaning |
| --- | --- |
| `>` | greater than |
| `>=` | greater than or equal to |
| `<` | less than |
| `<=` | less than or equal to |
| `==` | equal to |
| `!=` | not equal to |

```r
today_price <- 54.33
yesterday_price <- 55.24

today_price < yesterday_price
# [1] TRUE
```

## if / else

當邏輯是「符合條件才做事」時，用 `if` 最清楚：

```r
signal <- if (today_price < yesterday_price) {
  "down"
} else {
  "up_or_flat"
}
```

如果你的條件是針對整個向量逐元素判斷，通常應考慮向量化寫法，而不是用單一 `if`。

## repeat

`repeat` 會無限執行，直到你主動 `break`。它適合用在「不知道要跑幾次，但知道停止條件」的情況。

```r
i <- 0

repeat {
  i <- i + 1
  if (i >= 3) break
}
```

風險在於忘記寫停止條件，就會變成 infinite loop。

## while

`while` 適合在條件為真時持續更新狀態：

```r
price <- 52.1

while (price <= 52.5) {
  price <- price * runif(1, 0.99, 1.01)
}
```

這類寫法常見於模擬、逐步搜尋、門檻觸發與資料清理直到滿足條件為止。

## for

`for` 適合明確地逐個元素處理：

```r
for (number in 1:5) {
  print(number)
}
```

對分析工作來說，`for` 常用於：

- 逐一處理多個欄位或檔案
- 迭代模型設定
- 對多個資產或群組重複執行相同步驟

## When Not to Loop

下面這類情境通常優先考慮向量化或 `apply` 類函數：

- 對整個向量做數學運算
- 對 data frame 每欄做同一個摘要統計
- 對 list 中每個元素套用同一個函數

Key point: loop 不一定錯，但如果資料結構本來就支援向量化，loop 往往會讓程式更長、更慢，也更難檢查。

## Common Mistakes

- 用 `if` 判斷整個向量，卻以為它會逐元素處理。
- `while` 條件永遠不會改變，造成無限迴圈。
- 在 `for` 迴圈中反覆長大物件，讓效能變差。
- 本來可以直接用 `mean(x, na.rm = TRUE)` 或 `sapply()`，卻手動寫冗長迴圈。
