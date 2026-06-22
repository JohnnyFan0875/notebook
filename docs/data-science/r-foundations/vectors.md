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

## Common Mistakes

- 混入不同型別元素，讓 R 自動 coercion 成不預期的型別。
- 忘記 R 會做 recycling，導致運算看似成功但邏輯錯誤。
- 把 vector 當成純 scalar 使用，忽略很多函數其實會整批處理。
