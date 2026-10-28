# Data Structures in R: Vectors, Data Frames and Lists

R 最常用的三種容器：**vector**（同型別、向量化運算的基本單位）、**data frame**（等長 vector 組成的表格）、**list**（可裝任何型別，包括巢狀物件與模型結果）。factor 見 [Categorical Data in R](categorical-data.md)。

## Vectors in R

vector 是 R 最基本的資料結構。很多運算之所以可以直接對整批資料生效，是因為 R 預設就是以 vector 為核心在設計。

### What a Vector Is

vector 是「同一型別元素的有序集合」：

```r
prices <- c(159.4, 160.3, 161.3)
grocery <- c("apple", "orange", "cereal")
```

一個單一數值在 R 裡本質上也可以視為長度為 1 的 vector。

### Named Vectors

當資料本身帶有自然索引時，幫 vector 命名會更好讀：

```r
apple_stock <- c(159.4, 160.3, 161.3)
names(apple_stock) <- c("Monday", "Tuesday", "Wednesday")

apple_stock
```

這對時間點、資產代碼、群組名稱都很方便。

### Vectorized Arithmetic

R 會自動把相同位置的元素一起運算：

```r
dan <- c(100, 200, 150)
rob <- c(50, 75, 100)

monthly_total <- dan + rob
sum(monthly_total)
```

同樣的觀念也適用於減法、乘法與比較運算。

### Vectorized Comparison

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

### Logical Vectors

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

### Comparing More Than Numbers

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

### Recycling

當一邊是長向量、一邊是長度 1 的數值時，R 會自動重複短的那邊：

```r
a <- c(2.2, 12, 7)
a * 2
```

這很方便，但也要小心。若兩個向量長度不一致且不是整除關係，R 仍可能繼續運算，只是結果不一定符合你的本意。

### Why Vectors Matter

理解 vector 後，很多 R 行為就會變得合理：

- `mean(x)`、`sum(x)` 是對整個向量摘要
- `x > 0` 會回傳一個 logical vector
- data frame 的每一欄本質上也是一個 vector
- `x[x > 0]` 這類寫法其實是在用 logical vector 做 subsetting

### Common Mistakes

- 混入不同型別元素，讓 R 自動 coercion 成不預期的型別。
- 忘記 R 會做 recycling，導致運算看似成功但邏輯錯誤。
- 把 vector 當成純 scalar 使用，忽略很多函數其實會整批處理。

## Data Frames in R

data frame 是 R 最常見的表格式資料結構。它可以視為「多個等長 vector 按欄位綁在一起」，每一欄可以有自己的型別。

### Creating a Data Frame

```r
name <- c("Dan", "Dan", "Dan", "Rob", "Rob", "Rob")
payment <- c(100, 200, 150, 50, 75, 100)

debt <- data.frame(name, payment)
```

如果一開始就知道欄位名稱，直接在建立時命名通常比後改更清楚：

```r
debt <- data.frame(friend = name, money = payment)
```

### Renaming Columns

```r
colnames(debt) <- c("friend", "money")
```

欄位名稱不只是美觀問題。清楚、穩定的欄名會直接影響後續的 subset、merge 與視覺化可讀性。

### Subsetting

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

### Mental Model

把 data frame 想成：

- rows: 觀測值
- columns: 變數
- each column: 一個 vector

這個心智模型能幫助你判斷什麼操作應該逐欄做，什麼操作應該逐列做。

### Common Mistakes

- 取單欄時忘記會掉成 vector，導致下游程式期待 data frame 卻收到 vector。
- 用模糊欄名，後續很難看出欄位含義。
- 以為所有欄位型別都一樣；其實 data frame 本來就允許 mixed types。

## Lists in R

當你需要把不同型別、不同形狀的物件包在一起時，R 的 list 是最自然的容器。它和 vector 不同，list 不要求每個元素型別一致。

### Why Lists Exist

分析工作常需要把多種物件放在一起，例如：

- 一個資料表
- 一段 metadata
- 幾個模型物件
- 一組參數設定

這時 list 比 vector 或 data frame 更適合。

### Creating a List

```r
company_name <- "DataCampers Inc."

cash <- data.frame(
  company = c("A", "A", "A", "B", "B", "B", "B"),
  cash_flow = c(1000, 4000, 550, 1500, 1100, 750, 6000),
  year = c(1, 3, 4, 1, 2, 4, 5)
)

my_company <- list(company_name, cash)
```

這個 list 的第一個元素是字串，第二個元素是 data frame。這正是 list 的價值所在。

### Practical Uses

list 在 R 裡非常常見，因為很多函數本來就會回傳 list，例如：

- 模型擬合結果
- API 回應
- 巢狀資料結構
- 多步驟分析的中間結果

當你後面開始使用 `lapply()`、`sapply()` 時，list 也會變成核心資料結構。

### Mental Model

可以把 list 想成一個容器，裡面每個 slot 都能放完全不同的東西。重點不是長得整齊，而是把相關物件組成一個可攜帶、可傳遞的分析單位。

### Common Mistakes

- 以為 list 應該像 data frame 一樣每個元素長度一致。
- 把本來應該拆成欄位的表格資料硬塞進 list，讓後續操作變複雜。
- 不清楚 list 與 vector 的差別，導致 indexing 與回傳型別判讀混亂。
