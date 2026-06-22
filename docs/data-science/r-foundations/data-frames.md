# Data Frames in R

data frame 是 R 最常見的表格式資料結構。它可以視為「多個等長 vector 按欄位綁在一起」，每一欄可以有自己的型別。

## Creating a Data Frame

```r
name <- c("Dan", "Dan", "Dan", "Rob", "Rob", "Rob")
payment <- c(100, 200, 150, 50, 75, 100)

debt <- data.frame(name, payment)
```

如果一開始就知道欄位名稱，直接在建立時命名通常比後改更清楚：

```r
debt <- data.frame(friend = name, money = payment)
```

## Renaming Columns

```r
colnames(debt) <- c("friend", "money")
```

欄位名稱不只是美觀問題。清楚、穩定的欄名會直接影響後續的 subset、merge 與視覺化可讀性。

## Subsetting

data frame 常見的取值方式有三種：

```r
debt[3:6, ]
debt[1:3, 2]
debt$payment
```

如果你想保留 data frame 形狀，而不是讓單欄被簡化成 vector，可以加上 `drop = FALSE`：

```r
debt[1:3, 2, drop = FALSE]
```

這在寫函數或可重用腳本時很重要，因為輸出型別穩定才能避免下游報錯。

## Mental Model

把 data frame 想成：

- rows: 觀測值
- columns: 變數
- each column: 一個 vector

這個心智模型能幫助你判斷什麼操作應該逐欄做，什麼操作應該逐列做。

## Common Mistakes

- 取單欄時忘記會掉成 vector，導致下游程式期待 data frame 卻收到 vector。
- 用模糊欄名，後續很難看出欄位含義。
- 以為所有欄位型別都一樣；其實 data frame 本來就允許 mixed types。
