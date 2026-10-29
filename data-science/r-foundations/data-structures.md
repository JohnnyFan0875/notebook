[Data Science](../README.md) › [R Foundations](README.md) › 資料結構

# 資料結構 (Data Structures: Vector, Matrix, Data Frame, List)

R 的一切運算都建立在幾種容器上：**vector** 是向量化運算的基本單位，**matrix** 是同型別的二維陣列（表現量矩陣），**data frame** 是等長 vector 組成的表格，**list** 可以裝任何東西（模型結果、巢狀 JSON）。factor 見 [類別資料](categorical-data.md)。

| 結構 | 維度 | 元素型別 | 典型用途 | Python 對應 |
| --- | --- | --- | --- | --- |
| atomic vector | 1 | 同一型別 | 一欄數值、一組基因名 | 1-D `np.ndarray` / `pd.Series` |
| matrix / array | 2 / n | 同一型別 | counts 矩陣（基因 × 樣本） | 2-D `np.ndarray` |
| data frame / tibble | 2 | 每欄可不同 | 樣本 metadata、tidy 表 | `pd.DataFrame` |
| list | 1（可巢狀） | 任意 | 模型物件、API 回應、多個結果打包 | `list` / `dict` |
| factor | 1 | 整數碼 + levels | 分組、處理組別 | `pd.Categorical` |

> 一個數字在 R 裡就是長度 1 的 vector，沒有獨立的 scalar 型別。

## Vector

### 型別與強制轉換 (coercion)

| 型別 | 例子 | `typeof()` | 缺值 |
| --- | --- | --- | --- |
| logical | `TRUE`, `FALSE` | `"logical"` | `NA` |
| integer | `1L`, `1:3` | `"integer"` | `NA_integer_` |
| double | `1`, `2.5`, `1e-8` | `"double"` | `NA_real_`；另有 `NaN`、`Inf` |
| character | `"TP53"` | `"character"` | `NA_character_` |

`c()` 混合型別時會自動往「較通用」的方向轉：**logical → integer → double → character**。

```r
c(1, "a", TRUE)            # "1" "a" "TRUE"   全變字串
c(1, TRUE, FALSE)          # 1 1 0
sum(c(TRUE, FALSE, TRUE))  # 2   logical 加總 = 計數
mean(x > 10)               # 大於 10 的比例

as.numeric(c("1.5", "abc"))  # 1.5 NA + warning：解析失敗變 NA，要檢查
is.numeric(1L); is.character("a"); class(1:3)   # "integer"
```

> 讀進來的數值欄若混入 `"<0.01"`、`"N/A"`，整欄會變 character；`as.numeric()` 後一定要看多出幾個 `NA`。

### 建立、命名與取值

```r
expr <- c(TP53 = 8.2, BRCA1 = 5.1, MYC = 11.3)   # named vector
names(expr)                     # "TP53" "BRCA1" "MYC"
seq(0, 1, by = 0.25); rep(c("ctrl", "trt"), each = 3); seq_len(5)

expr[2]            # 依位置（R 從 1 開始）
expr[-1]           # 負號 = 排除，不是倒數
expr["MYC"]        # 依名稱
expr[expr > 6]     # 依 logical 遮罩
expr[c("MYC", "TP53")]
which(expr > 6)    # 回傳位置：TP53 1, MYC 3
```

### 向量化運算與 recycling

```r
dan <- c(100, 200, 150); rob <- c(50, 75, 100)
dan + rob                  # 150 275 250   逐位置運算
dan * 2                    # 長度 1 的 2 被 recycle
1:6 + c(0, 10)             # 1 12 3 14 5 16   長度整除：靜默 recycle
1:5 + c(0, 10)             # 有 warning：長度不整除，但仍算出結果

linkedin <- c(16, 9, 13, 5, 2, 17, 14)
facebook <- c(17, 7, 5, 16, 8, 13, 14)
linkedin > 10              # TRUE FALSE TRUE FALSE FALSE TRUE TRUE
facebook <= linkedin       # FALSE TRUE TRUE FALSE FALSE TRUE TRUE
any(linkedin > 15); all(linkedin > 1)
```

> recycling 是 R 最容易「看似成功但邏輯錯誤」的地方：只有長度 1 的 recycle 是安全的直覺用法，其他情況請先確認長度相同。

### 比較與相等

| 想做 | 寫法 | 陷阱 |
| --- | --- | --- |
| 浮點數相等 | `isTRUE(all.equal(0.1 + 0.2, 0.3))` | `0.1 + 0.2 == 0.3` 是 `FALSE` |
| 屬於集合 | `x %in% c("A", "B")` | `x == c("A", "B")` 會 recycle 逐位比較 |
| 含 NA 的比較 | `x > 5 & !is.na(x)` | `NA > 5` 是 `NA`，不是 `FALSE` |
| 字串比較 | `"Hello" > "Goodbye"` → `TRUE` | 字典序依 locale，跨系統可能不同 |

## Matrix 與 Array

matrix 是**同一型別**的二維 vector（帶 `dim` 屬性），計算比 data frame 快，是表現量資料的標準格式（列 = 基因、欄 = 樣本）。

```r
m <- matrix(1:6, nrow = 2)            # 依欄填 (column-major)：第一欄是 1 2
dim(m); nrow(m); ncol(m)              # 2 3
rownames(m) <- c("geneA", "geneB"); colnames(m) <- paste0("s", 1:3)

m["geneA", ]                          # 一列 → 掉成 named vector
m[, 2, drop = FALSE]                  # 保持 matrix
t(m); m %*% t(m)                      # 轉置、矩陣乘法（* 是逐元素）
rowMeans(m); colSums(m)               # 比 apply(m, 1, mean) 快
log2(m + 1)                           # 向量化，維度保留

as.matrix(df[, c("x", "y")])          # data frame → matrix：有字串欄會整個變 character
```

> 生資套件把 counts 矩陣、樣本 metadata、基因註解打包成 `SummarizedExperiment`；它的 `assay()` 就是 matrix，`colData()` 是 data frame。見 [Bioconductor 入門](../../biology/bioinformatics-tools/bioconductor.md)。

## Data Frame

data frame = 多個**等長** vector 按欄綁在一起，每欄型別可不同；列是觀測、欄是變數。

```r
debt <- data.frame(
  friend = c("Dan", "Dan", "Dan", "Rob", "Rob", "Rob"),
  money  = c(100, 200, 150, 50, 75, 100)
)
str(debt); head(debt); summary(debt)
names(debt) <- c("friend", "payment")      # 改欄名

debt[3:6, ]                    # 列
debt[1:3, 2]                   # 單欄 → 掉成 vector
debt[1:3, 2, drop = FALSE]     # 保持 data frame
debt$payment                   # 單欄 vector（$ 會部分比對名稱，寫程式時改用 [["payment"]]）
debt[debt$payment > 100, ]     # 條件篩選；欄位有 NA 時會產生全 NA 的列
subset(debt, payment > 100)    # 會丟掉 NA 列
debt$log_pay <- log(debt$payment)   # 新增欄
```

### data.frame vs tibble

tidyverse 的 tibble 是較嚴格的 data frame，dplyr 輸出預設都是 tibble。

| 行為 | `data.frame` | `tibble` |
| --- | --- | --- |
| `df[, 1]` | 掉成 vector | 永遠是 tibble |
| `df$ab`（只有 `abc` 欄） | 部分比對，回傳 `abc` | `NULL` + warning |
| 列名 (row names) | 支援 | 不支援，用 `rownames_to_column()` 轉成欄 |
| 印出 | 全部印 | 只印前 10 列與欄型別 |
| 字串轉 factor | R 4.0 以前預設會轉（`stringsAsFactors`） | 不轉 |

> 很多 Bioconductor 物件依賴 row names（基因 ID）。轉成 tibble 前先 `rownames_to_column("gene_id")`，否則 ID 會消失。

## List

list 的每個元素可以是不同型別、不同長度；模型物件（`lm()` 結果）、`jsonlite::fromJSON()` 回應、`split()` 結果都是 list。

```r
run <- list(
  name   = "batch_01",
  counts = data.frame(gene = c("A", "B"), n = c(10, 3)),
  params = list(min_count = 5, method = "TMM")
)

run["name"]          # 子 list（仍是 list）
run[["name"]]        # 元素本身："batch_01"
run$params$method    # 巢狀取值："TMM"
run[["params"]][["min_count"]]
str(run, max.level = 1)

run$note <- "rerun"  # 新增元素
run$note <- NULL     # 刪除元素
length(run); names(run)

fit <- lm(mpg ~ wt, data = mtcars)
is.list(fit); names(fit)          # coefficients、residuals...
by_cyl <- split(mtcars, mtcars$cyl)   # list of data frames，接 lapply / purrr::map
```

| 運算子 | 回傳 | 比喻 |
| --- | --- | --- |
| `x[i]` | 同型別的子集（list 還是 list） | 拿到裝著貨物的車廂 |
| `x[[i]]` | 單一元素本身 | 拿出車廂裡的貨物 |
| `x$name` | 同 `x[["name"]]`，但會部分比對 | 方便互動使用 |

逐元素處理 list 見 [函數式程式設計](functional-programming.md)。

## 常見錯誤

| 錯誤 | 結果 | 對策 |
| --- | --- | --- |
| 混入不同型別 | 整個 vector 變 character | `str()` 檢查；匯入時指定 `col_types` |
| 長度不一致卻運算 | recycle 出錯誤結果 | 檢查 `length()`；用 `stopifnot(length(x) == length(y))` |
| 單欄 / 單列取值掉成 vector | 下游期待 data frame 而報錯 | `drop = FALSE` 或改用 tibble |
| 用 `[` 取 list 元素 | 拿到 list 而不是值 | 取值用 `[[` |
| `$` 部分比對 | 拿到錯的欄 | 程式中用 `[["col"]]` |
| `1:length(x)` 遇到空 vector | 得到 `1 0`，迴圈跑兩次 | 用 `seq_along(x)` |
