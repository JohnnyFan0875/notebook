[Data Science](../README.md) › [R Foundations](README.md) › 物件導向

# 物件導向：S3、S4 與 R6 (Object-Oriented Programming)

R 有好幾套物件系統。日常分析碰到最多的是 **S3**（`print()`、`summary()` 為何對 `lm` 和 `data.frame` 表現不同）；生資會大量遇到 **S4**（Bioconductor 的 `SummarizedExperiment`、`GRanges`、`DESeqDataSet` 全是 S4）；**R6** 則是一般語言式的可變物件。讀懂這三套，才看得懂套件文件與錯誤訊息。Python 的 class 見 [類別](../python-foundations/class.md)。

## 三套系統比較

| | S3 | S4 | R6 |
| --- | --- | --- | --- |
| 本質 | 在既有物件上加 `class` 屬性 | 正式定義的 class（slot 有型別） | 建立在 environment 上的 class |
| 方法屬於 | generic function | generic function | 物件本身（`obj$method()`） |
| 語意 | value（修改會複製） | value | **reference**（多個變數指向同一物件） |
| 欄位存取 | `x$name`、`attr()` | `x@slot`（應改用 accessor） | `obj$field` |
| 驗證 | 無，靠慣例 | `validity` 函式 | 自己寫 |
| 典型使用 | base R、tidyverse、`lm`、`htest` | Bioconductor、Matrix | Shiny、API client、有狀態的模擬器 |
| 何時自己寫 | 想讓資料有自訂 `print` / `summary` / `plot` | 寫 Bioconductor 套件、需要嚴格型別與多重 dispatch | 需要封裝並逐步修改狀態 |

> 只是「資料 + 幾個函式」時，一個 list 加普通函式就夠了，不必升級成 OOP。

## S3

S3 物件只是帶了 `class` 屬性的普通物件；generic function 用 `UseMethod()` 依 class 找到 `generic.class` 方法。

```r
# 建構函式：檢查輸入、加上 class
new_qc_report <- function(counts) {
  stopifnot(is.matrix(counts))
  structure(list(counts = counts, libsize = colSums(counts)), class = "qc_report")
}

# 為既有 generic 加方法：名稱是 generic.class，參數要與 generic 一致（保留 ...）
print.qc_report <- function(x, ...) {
  cat("<qc_report>", ncol(x$counts), "samples; median library size",
      median(x$libsize), "\n")
  invisible(x)                              # print 方法慣例：隱形回傳自己
}

summary.qc_report <- function(object, ...) summary(object$libsize)

# 自訂 generic
flag_low <- function(x, ...) UseMethod("flag_low")
flag_low.qc_report <- function(x, min_lib = 1e6, ...) names(x$libsize)[x$libsize < min_lib]
flag_low.default <- function(x, ...) stop("no method for class ", class(x)[1])

rep <- new_qc_report(counts)
rep                                          # 自動呼叫 print.qc_report
```

| 想知道 | 指令 |
| --- | --- |
| 物件的 class（可能多個，依序 dispatch） | `class(x)`；`lm` 的 glm 物件是 `c("glm", "lm")` |
| 是否屬於某 class | `inherits(x, "lm")` |
| 某 generic 有哪些方法 | `methods("summary")` |
| 某 class 有哪些方法 | `methods(class = "lm")` |
| 看方法原始碼 | `getS3method("summary", "lm")` 或 `stats:::summary.lm` |
| 呼叫下一個 class 的方法 | 在方法內 `NextMethod()` |

S3 的風險：任何人都能把 `class(x) <- "lm"` 加到任何東西上，R 不會檢查內容。所以要有建構函式負責驗證，不要在各處手動改 `class`。

## S4（Bioconductor）

S4 class 有正式定義的 slot 與型別，方法可以依**多個參數**的 class dispatch。自己寫 S4 的機會不多，但讀 Bioconductor 物件時需要知道怎麼看。

```r
# 定義（了解即可）
setClass("Sample", representation(id = "character", libsize = "numeric"),
         validity = function(object) if (object@libsize < 0) "libsize must be >= 0" else TRUE)
setGeneric("libsize", function(x) standardGeneric("libsize"))
setMethod("libsize", "Sample", function(x) x@libsize)

s <- new("Sample", id = "S1", libsize = 2.3e7)
libsize(s)                                   # 用 accessor
s@libsize                                    # 能用但不建議：繞過套件的介面

# 檢視陌生的 S4 物件（例如 DESeqDataSet）
isVirtualClass("SummarizedExperiment")
is(dds)                                      # 完整繼承鏈
slotNames(dds)
showMethods("counts")                        # 哪些 class 有 counts() 方法
getMethod("counts", "DESeqDataSet")          # 看實作
?"counts,DESeqDataSet-method"                # S4 方法的說明頁寫法
```

| Bioconductor 物件 | 常用 accessor |
| --- | --- |
| `SummarizedExperiment` | `assay()`、`colData()`、`rowData()`、`rowRanges()` |
| `DESeqDataSet` | `counts()`、`sizeFactors()`、`design()`、`results()` |
| `GRanges` | `seqnames()`、`start()`、`end()`、`strand()`、`mcols()` |

> 一律用 accessor，不要直接 `@` 取 slot：內部結構隨版本變動，accessor 會維持相容並做驗證。物件概念見 [Bioconductor 入門](../../biology/bioinformatics-tools/bioconductor.md)。

新一代的 **S7**（R Consortium 開發，CRAN 套件 `S7`）試圖整合 S3 與 S4，目前仍在發展中，讀到時知道它是 S3/S4 的後繼即可。

## R6

R6 物件內含資料與方法，用 `obj$method()` 呼叫，**修改會直接改到物件本身**。

```r
library(R6)

Counter <- R6Class("Counter",
  public = list(
    value = 0,
    initialize = function(start = 0) self$value <- start,   # $new() 時呼叫
    add = function(n = 1) {
      self$value <- self$value + n
      invisible(self)                        # 回傳 self 可串接：$add()$add()
    }
  ),
  private = list(secret = 42),               # 只能在方法內以 private$ 取用
  active = list(
    double = function(value) {               # 看起來像欄位、實際是函式
      if (!missing(value)) stop("double is read-only")
      self$value * 2
    }
  )
)

a <- Counter$new()
a$add(5)$add(1)
a$value                                      # 6
a$double                                     # 12

# 繼承：super$ 呼叫父類方法
LoggedCounter <- R6Class("LoggedCounter", inherit = Counter,
  public = list(add = function(n = 1) { message("add ", n); super$add(n) })
)
```

### Reference semantics

R6 建立在 environment 上，而 environment 不會在指派時複製：

```r
a <- Counter$new()
b <- a                                       # b 和 a 是同一個物件
b$add(10)
a$value                                      # 10：a 也變了

c <- a$clone()                               # 真正的複本
d <- a$clone(deep = TRUE)                    # 欄位裡還有 R6 物件時，要 deep clone
```

| 區塊 | 用途 | 方法內存取 |
| --- | --- | --- |
| `public` | 外部可用的欄位與方法 | `self$` |
| `private` | 內部狀態與輔助函式 | `private$` |
| `active` | 讀寫時執行函式（計算屬性、唯讀欄位） | `self$` |
| `initialize` | 建構時執行 | |

## 常見誤區

| 誤區 | 後果 / 正確做法 |
| --- | --- |
| 把 S3 當成有強制檢查的 class | S3 只靠慣例；用建構函式集中驗證 |
| S3 方法不保留 `...` 或改了參數名 | dispatch 後參數對不上；方法 signature 要與 generic 相容 |
| 對 S4 物件用 `$` 或 `@` 硬取資料 | 套件更新就壞；用 accessor |
| R6 `b <- a` 以為是複本 | 兩者共享狀態；需要獨立物件用 `$clone()` |
| 在純資料分析腳本中引入繼承層級 | 先釐清資料結構與責任，函式通常就夠了 |
