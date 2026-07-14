# Object-Oriented Programming with S3 and R6

R 不是只有一種物件系統。實務上最常碰到的是 S3 與 R6：前者偏向輕量、以 generic function 為中心；後者比較像一般程式語言裡可封裝狀態與方法的 class。

這份筆記的重點不是把 OOP 當成語法清單，而是理解什麼時候該把資料加上一層 class，什麼時候需要真正有狀態、可修改的物件。

## S3 的工作模型

S3 很輕。很多時候它只是替既有資料結構加上一個 class，然後讓 generic function 依照 class 選對方法。

```r
x <- 1:5
class(x)

class(x) <- "random_numbers"
class(x)
```

這種設計的重點不是把資料藏起來，而是讓 `print()`、`summary()`、`plot()` 這類 generic function 能對不同物件類型做不同事情。

### Generic 與 method

S3 method 通常遵守 `generic.class` 的命名方式，例如 `print.Date`、`summary.factor`。

```r
my_print <- function(x, ...) {
  UseMethod("my_print")
}

my_print.random_numbers <- function(x, ...) {
  cat("Random numbers:", paste(x, collapse = ", "), "\n")
}

my_print(x)
```

幾個實務重點：

- `UseMethod()` 會根據物件的 class 決定 dispatch 到哪個 method。
- method 的參數通常要保留 generic 的介面，特別是常見的 `...`。
- 如果你的 method 忽略 generic 已提供的參數，後續擴充通常會變得很脆弱。

### 檢查可用 methods

```r
methods("print")
inherits(x, "random_numbers")
```

常用工具：

- `class()` 檢查物件類別。
- `methods()` 看某個 generic 目前有哪些 method。
- `inherits()` 判斷物件是否屬於某個 class。

### 什麼時候用 S3

S3 適合這幾種情境：

- 你已經有一個 vector、list 或 data frame，只想為它定義更好的列印、摘要或繪圖行為。
- 你想延伸既有 R 生態系常見 generic，例如 `print()`、`summary()`、`plot()`。
- 你的重點是資料表示與 dispatch，不是物件內部狀態管理。

如果你的需求只是「資料加上一些對應方法」，S3 往往比建立完整 class 系統更自然。

## R6 的工作模型

R6 比較接近一般開發者熟悉的 class-based OOP。它可以把資料與方法包在一起，並透過 reference semantics 直接修改物件狀態。

```r
library(R6)

Counter <- R6Class(
  "Counter",
  public = list(
    value = 0,
    increment = function(n = 1) {
      self$value <- self$value + n
    }
  )
)

counter <- Counter$new()
counter$increment()
counter$value
```

### `public`、`private`、`active`

R6 class 常見的三個區塊：

- `public`：外部可直接呼叫的方法與欄位。
- `private`：只在物件內部使用的欄位與方法。
- `active`：看起來像欄位、實際上每次讀寫都會執行函數的 active binding。

```r
Person <- R6Class(
  "Person",
  private = list(
    birth_year = 1990
  ),
  active = list(
    age = function(value) {
      if (!missing(value)) stop("age is read only")
      as.integer(format(Sys.Date(), "%Y")) - private$birth_year
    }
  )
)

person <- Person$new()
person$age
```

在 method 內部：

- 用 `self$` 存取 public 成員。
- 用 `private$` 存取 private 成員。

## R6 繼承

R6 支援繼承，可以讓 child class 重用 parent 的欄位與方法。

```r
Thing <- R6Class(
  "Thing",
  public = list(
    describe = function() "generic thing"
  )
)

Book <- R6Class(
  "Book",
  inherit = Thing,
  public = list(
    describe = function() {
      paste("book:", super$describe())
    }
  )
)
```

這裡的重點：

- `inherit = ParentClass` 建立繼承關係。
- `super$method()` 可以呼叫 parent method。
- 如果 child 覆寫 method，最好清楚說明是完全取代還是延伸 parent 行為。

## 為什麼 R6 有 reference semantics

理解 R6，先理解 list 與 environment 的差別。

- list 常在修改時產生複製，概念上比較接近 value semantics。
- environment 是 reference-based，兩個變數可能指向同一份可變狀態。

R6 物件底層建立在 environment 之上，所以這段程式會直接改變同一個物件：

```r
a <- Counter$new()
b <- a

b$increment(10)
a$value
```

這種行為很適合：

- 累積狀態。
- 建立可持續更新的模型物件。
- 在多個 method 之間共享同一份內部資料。

但也要注意副作用。如果你以為是在複製資料，實際上可能只是多拿到同一個 reference。

### Clone

```r
c1 <- Counter$new()
c2 <- c1$clone()
```

`clone()` 可以建立新物件；如果物件裡還包了其他 R6 物件，則要考慮 `clone(deep = TRUE)`，否則巢狀成員仍可能共享參照。

## S3 與 R6 怎麼選

可以先用這個判斷方式：

- 只是想讓某種資料型別擁有客製化 `print()` / `summary()` / `plot()`：先選 S3。
- 需要封裝狀態、方法、私有欄位，並在 method 呼叫之間持續修改物件：選 R6。
- 如果簡單的 list 加上幾個函數就夠了，不要太快把問題升級成 OOP 設計。

## 常見誤區

- 把 S3 當成嚴格 class 系統來用，最後會因為它其實依賴慣例而不是強制封裝而困惑。
- 在 R6 物件間複製參照卻忘了它們共享同一份狀態。
- 還沒釐清資料結構與責任邊界，就先引入 inheritance，通常只會讓程式更難維護。

實務上，S3 與 R6 都是工具。先決定你要擴充的是「資料對 generic 的反應」，還是「一個帶狀態的可變物件」，通常就能選對方向。
