# Vectors in R

vector 是 R 最基本的資料結構。很多運算之所以可以直接對整批資料生效，是因為 R 預設就是以 vector 為核心在設計。

## What a Vector Is

vector 是「同一型別元素的有序集合」：

```r
prices <- c(159.4, 160.3, 161.3)
grocery <- c("apple", "orange", "cereal")
```

一個單一數值在 R 裡本質上也可以視為長度為 1 的 vector。

## Named Vectors

當資料本身帶有自然索引時，幫 vector 命名會更好讀：

```r
apple_stock <- c(159.4, 160.3, 161.3)
names(apple_stock) <- c("Monday", "Tuesday", "Wednesday")

apple_stock
```

這對時間點、資產代碼、群組名稱都很方便。

## Vectorized Arithmetic

R 會自動把相同位置的元素一起運算：

```r
dan <- c(100, 200, 150)
rob <- c(50, 75, 100)

monthly_total <- dan + rob
sum(monthly_total)
```

同樣的觀念也適用於減法、乘法與比較運算。

## Vectorized Comparison

比較運算在 R 裡也是向量化的。不是只得到一個 `TRUE` 或 `FALSE`，而是通常會得到一整個 logical vector：

```r
linkedin <- c(16, 9, 13, 5, 2, 17, 14)
linkedin > 10
# [1]  TRUE FALSE  TRUE FALSE FALSE  TRUE  TRUE
```

如果兩邊都是等長向量，R 會逐位置比較：

```r
facebook <- c(17, 7, 5, 16, 8, 13, 14)
facebook <= linkedin
# [1] FALSE  TRUE  TRUE FALSE FALSE  TRUE  TRUE
```

這很重要，因為很多 subset、篩選和條件運算，都是先產生 logical vector，再用它挑資料。

## Logical Vectors

logical vector 是 R 分析流程裡非常核心的中介物件：

```r
is_popular <- linkedin > 10
is_popular
# [1]  TRUE FALSE  TRUE FALSE FALSE  TRUE  TRUE
```

它常被拿來做：

- 條件篩選
- 多個條件的組合
- `sum()`、`any()`、`all()` 這類摘要判斷

實務上可以把 logical vector 想成一個與原資料等長的條件遮罩。

## Comparing More Than Numbers

比較運算不只適用於數值。字串也可以比較，而且是依字典序：

```r
"Hello" > "Goodbye"
# [1] TRUE
```

布林值也能被比較，因為 `TRUE` 和 `FALSE` 在某些情況下會被 coercion：

```r
TRUE < FALSE
# [1] FALSE
```

這類行為可以幫助理解 R 的底層規則，但實務上除非很明確知道自己在做什麼，否則不要把布林值比較當成主要資料分析寫法。

## Recycling

當一邊是長向量、一邊是長度 1 的數值時，R 會自動重複短的那邊：

```r
a <- c(2.2, 12, 7)
a * 2
```

這很方便，但也要小心。若兩個向量長度不一致且不是整除關係，R 仍可能繼續運算，只是結果不一定符合你的本意。

## Why Vectors Matter

理解 vector 後，很多 R 行為就會變得合理：

- `mean(x)`、`sum(x)` 是對整個向量摘要
- `x > 0` 會回傳一個 logical vector
- data frame 的每一欄本質上也是一個 vector
- `x[x > 0]` 這類寫法其實是在用 logical vector 做 subsetting

## Common Mistakes

- 混入不同型別元素，讓 R 自動 coercion 成不預期的型別。
- 忘記 R 會做 recycling，導致運算看似成功但邏輯錯誤。
- 把 vector 當成純 scalar 使用，忽略很多函數其實會整批處理。
