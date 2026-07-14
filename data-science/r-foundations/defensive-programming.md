# Defensive Programming in R

Defensive programming 的核心不是把程式寫得悲觀，而是讓常見錯誤更早被發現、更容易被理解，並盡量不要一路傳染到後面的分析結果。

在 R workflow 裡，這通常意味著三件事：

- 先避免明顯會出錯的寫法
- 對輸入與中間結果做基本檢查
- 讓檔案、函數與錯誤訊息保持一致

## Goal

一個防禦性夠好的 R script，應該做到：

- 問題能早一點暴露
- 錯誤訊息能幫助定位
- 小失誤不會悄悄變成錯誤結論

這種思路在資料清理、統計分析與報表自動化特別重要。

## Prefer `TRUE` and `FALSE` over `T` and `F`

`TRUE` 和 `FALSE` 是保留邏輯值，`T` 和 `F` 只是一般名稱。

因此：

- `TRUE <- 5` 會直接報錯
- `T <- 5` 則可能被重新賦值，造成難查的邏輯錯誤

實務上最好直接養成習慣：

- 寫 `TRUE`
- 寫 `FALSE`
- 不要依賴 `T`
- 不要依賴 `F`

## Use `isTRUE()` for Explicit Checks

當你真的要確認某個條件是單一且明確的 `TRUE` 時，`isTRUE()` 比直接 `if (x)` 更穩定。

```r
isTRUE(TRUE)
isTRUE(2)
```

這樣可以避免把非零數字、長度不對的邏輯向量，或其他模糊輸入誤當成布林條件。

## Warnings and Errors

R 至少有兩種常見的問題訊號：

- `warning()`：提醒有風險，但程式仍繼續執行
- `stop()`：中止執行，表示條件已經不適合再往下算

```r
warning("You have been warned!")
stop("Standard deviation must be positive")
```

簡單判斷原則：

- 還能產出有意義的結果，用 `warning()`
- 再算下去會誤導人，用 `stop()`

## Catching Errors with `try()`

有些步驟可以容忍失敗，這時可以先攔住錯誤，再決定怎麼處理。

```r
result <- try("Scotland" + "World cup", silent = TRUE)

if (inherits(result, "try-error")) {
  message("Computation failed")
}
```

這種模式適合批次流程，但不要拿來掩蓋本來就應該修掉的核心 bug。

## DRY over Copy-Paste

防禦性程式設計和 DRY 很有關係。

DRY = do not repeat yourself  
WET = write everything twice

經驗法則：

1. 複製貼上一次通常還能接受
2. 第二次就該開始警覺
3. 第三次通常代表應該抽函數、抽設定或抽共用流程

重複越多，修 bug 時漏改其中一份的風險越高。

## The Copy-and-Paste Rule

如果同一段資料清理、模型設定或繪圖格式開始重複出現，通常可以抽成：

- 一個函數
- 一個共用常數
- 一段 reusable pipeline

防禦性的重點不是省字數，而是避免邏輯分叉。

## Style Consistency Helps Catch Bugs

一致的格式會讓錯誤更容易被看到。

例如：

```r
res <- t.test(x, paired = FALSE)
```

通常比下面更容易掃描與除錯：

```r
res<-t.test(x,paired=FALSE)
```

這不只是美觀問題，還是降低認知負擔的方式。

## Static Analysis with `lintr`

`lintr` 可以幫你在執行前先抓出一些風格和潛在問題。

```r
lintr::lint("code.R")
```

它不會取代測試，但很適合當早期警報系統。

## File Naming Matters

R script 都存在檔案裡，所以命名規則本身就是防呆的一部分。

好檔名的目標是：

- 容易搜尋
- 容易排序
- 在 shell、git、網址和自動化流程中不容易出錯

## Prefer Hyphens, Avoid Spaces

像這樣的檔名通常比空白檔名穩定：

- `cluster-analysis.R`
- `load-survival-data.R`
- `plot-residuals.R`

避免：

- `file name.R`
- `my final script.R`

原因包括：

- shell 操作要額外加引號
- 網址或部分工具會把空白轉成 `%20`
- 搜尋、排序和 tab completion 都更麻煩

## Avoid Underscore-Heavy Search Problems

課程也提到一個很實務的小點：某些搜尋情境下，`file_name` 會比較像單一 token，未必像連字號那樣容易被切開。

這不是絕對規則，但若你重視檔案可搜尋性，kebab-case 常常是穩定選項。

## Use Consistent Extensions

同類型腳本應使用一致副檔名，例如統一用 `.R`。

這有助於：

- 編輯器辨識
- 檔案排序
- 自動化工具處理

## Keep a Predictable Project Layout

當專案變大，固定的目錄慣例會比臨時命名更重要。

一個常見思路是：

- `R/` 放腳本
- `input/` 放原始資料
- `output/` 放產出結果

如果每個分析專案都沿用接近的結構，切換上下文會更容易。

## Start Small

防禦性程式設計不一定要從完整測試框架開始。

先從這些最小習慣開始就很有幫助：

- 不用 `T` / `F`
- 對關鍵輸入加 `stop()`
- 對可疑但可繼續的情況加 `warning()`
- 減少複製貼上
- 固定檔名規則
- 用 `lintr` 掃描 script

這些小習慣累積起來，通常就能明顯降低 script 變脆弱的速度。

## Common Traps

- 把 `T` 或 `F` 當成永遠安全的布林值
- 遇到錯誤就全部用 `try()` 包起來，卻沒有真正處理失敗
- 同一段邏輯複製貼上很多份
- 檔名含空白、大小寫混亂或規則不一致
- 把 warning 該處理的問題當成沒事
- 把應該 `stop()` 的情況默默吞掉

## Related Notes

- [Functions in R](functions.md)
- [Control Flow in R](control-flow.md)
