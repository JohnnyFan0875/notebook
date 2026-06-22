# Categorical Data in R

R 用 factor 來表示類別資料。它看起來像字串標籤，但底層其實是整數編碼加上 levels 對照表，所以理解 factor 的結構很重要。

## Creating a Factor

```r
answers <- c("stock", "bond", "bond", "stock")
investment <- factor(answers)

investment
levels(investment)
class(investment)
```

factor 很適合表示：

- 類別標籤
- 問卷選項
- 分組欄位
- 有固定集合的狀態值

## Levels and Integer Codes

factor 底層不是直接存字串，而是存整數代碼對應到 level：

```r
as.integer(investment)
levels(investment)
```

Key point: `as.integer(factor_x)` 取到的是 level 編碼，不是你以為的原始商業意義數值。

## Binning with cut()

連續數值常需要切成區間，這時 `cut()` 很實用：

```r
buckets <- c(0, 10, 20, 30, 40, 50)
ranking_grouped <- cut(ranking, breaks = buckets)
```

這能把連續變數轉成可分組分析的區間類別，例如：

- 分數區間
- 年齡帶
- 風險等級
- 金額級距

## When to Use Factors Carefully

factor 很方便，但也容易踩坑：

- 若資料只是文字標籤且還會頻繁改寫，先保留 `character` 可能更單純。
- 若有明確順序，應進一步思考是否要用 ordered factor。
- 匯入資料時若自動變 factor，要先確認這是不是你要的行為。

## Common Mistakes

- 把 factor 當成普通數字做運算。
- 看到 `as.integer()` 的輸出，就誤以為那是原始類別值。
- 沒看 `levels()` 就直接建模或排序，導致順序解讀錯誤。
