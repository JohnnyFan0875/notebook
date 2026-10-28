[Data Science](../README.md) › [R Foundations](README.md) › 控制流程

# 控制流程 (Control Flow)

條件判斷與迴圈的 R 寫法。觀念與 [Python 控制流程](../python-foundations/control-flow.md) 相同，差別在 R 以向量化為主：**對整個 vector 做事時用向量化函式，只有狀態需要逐步更新時才寫迴圈**。

## 比較與邏輯運算子

| 運算子 | 意義 | 作用範圍 |
| --- | --- | --- |
| `>` `>=` `<` `<=` `==` `!=` | 比較 | 逐元素，回傳 logical vector |
| `&` `\|` `!` | AND / OR / NOT | 逐元素，用於篩選資料 |
| `&&` `\|\|` | AND / OR（短路） | 只接受長度 1，用於 `if` / `while` |
| `xor()`、`any()`、`all()` | 互斥或、任一、全部 | 把 vector 收斂成單一值 |
| `%in%` | 屬於集合 | 逐元素 |

```r
x <- c(3, 12, 20)
x > 5 & x < 15                 # FALSE TRUE FALSE   逐元素
c(TRUE, TRUE) && TRUE          # R ≥ 4.3.0：Error，長度 > 1 不再只看第一個元素
length(x) > 0 && x[1] > 5      # 短路：左邊 FALSE 就不算右邊，可防止越界
NA & FALSE                     # FALSE；NA & TRUE 是 NA
```

> `if` 的條件必須是**長度 1、非 NA** 的 logical。`if (x > 5)` 遇到長度 > 1 的 `x` 在 R ≥ 4.2.0 直接報錯；遇到 `NA` 報 `missing value where TRUE/FALSE needed`。需要時用 `isTRUE()`、`any()`、`all()` 收斂。

## 條件判斷

```r
# if / else if / else：第一個成立的分支就停止
label <- if (x[1] < 0) {
  "negative"
} else if (x[1] == 0) {
  "zero"
} else {
  "positive"
}

# 向量版：每個元素各自判斷
ifelse(x > 10, "high", "low")                   # base R，會丟失 Date / factor 屬性
dplyr::if_else(x > 10, "high", "low")           # 型別嚴格，可指定 missing =
dplyr::case_when(                               # 多分支
  x < 5  ~ "low",
  x < 15 ~ "mid",
  .default = "high"                             # dplyr ≥ 1.1.0；舊版寫 TRUE ~ "high"
)

# 依字串選分支
switch("median", mean = mean(x), median = median(x), stop("unknown stat"))
```

| 情境 | 用 |
| --- | --- |
| 單一判斷（參數、檔案是否存在） | `if` / `else` |
| 整欄二分 | `if_else()` / `ifelse()` |
| 整欄多分支、區間分類 | `case_when()` 或 `cut()` |
| 依字串選方法 | `switch()` |

## 迴圈

```r
# for：逐一處理檔案、樣本、參數
files <- list.files("data", pattern = "\\.csv$", full.names = TRUE)
results <- vector("list", length(files))        # 先配置好長度
for (i in seq_along(files)) {                   # 不要寫 1:length(files)，空 vector 會跑 1、0
  results[[i]] <- readr::read_csv(files[i], show_col_types = FALSE)
}
combined <- dplyr::bind_rows(results)

# while：條件成立就繼續
price <- 52.1
while (price <= 52.5) price <- price * runif(1, 0.99, 1.01)

# repeat：不知道要跑幾次，但知道何時停
i <- 0
repeat {
  i <- i + 1
  if (i >= 3) break
}

for (s in samples) {
  if (s %in% failed) next                       # 跳過這次
  ...
}
```

> 迴圈內 `x <- c(x, new)` 每次都複製整個物件，n 大時呈 O(n²)。先用 `vector("list", n)` 配置，或改用 `lapply()` / `purrr::map()`，最後 `bind_rows()`。

## 何時不寫迴圈

| 想做 | 迴圈寫法 | 向量化 / 函數式寫法 |
| --- | --- | --- |
| 整個 vector 運算 | `for (i ...) y[i] <- log(x[i])` | `log(x)` |
| 每欄摘要 | `for (col ...) mean(df[[col]])` | `colMeans(df)`、`summarize(across(...))` |
| 矩陣每列 | `for (g ...) mean(m[g, ])` | `rowMeans(m)` |
| 條件取代 | `for (i ...) if (x[i] < 0) x[i] <- 0` | `x[x < 0] <- 0` 或 `pmax(x, 0)` |
| 每個 list 元素套函式 | `for (el ...) f(el)` | `lapply()` / `purrr::map()`，見 [函數式程式設計](functional-programming.md) |

迴圈本身不慢，慢的是「在迴圈裡長大物件」與「逐元素呼叫本來可以整批處理的函式」。效能量測見 [寫出有效率的 R](writing-efficient-r-code.md)。
