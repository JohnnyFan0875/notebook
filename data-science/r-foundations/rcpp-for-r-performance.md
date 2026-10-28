[Data Science](../README.md) › [R Foundations](README.md) › Rcpp

# Rcpp：用 C++ 加速熱點 (Rcpp for R Performance)

向量化、預先配置、專用函式都做過，profiling 仍指向同一個迴圈時，Rcpp 讓你只把那一小段改寫成 C++，主流程留在 R。典型對象是**每一步依賴上一步**、無法向量化的迴圈：MCMC、動態規劃（序列比對）、遞迴濾波、rejection sampling。許多 Bioconductor 套件（DESeq2、scran）的核心也是這樣寫的。

## 何時值得用

| 適合 | 不適合 |
| --- | --- |
| profiling 證明瓶頸集中在少數函式 | 瓶頸在 I/O、資料庫、網路 |
| 逐元素迴圈、每步依賴前一步 | 能向量化或已有專用函式（`rowSums`、`cumsum`、matrixStats） |
| 大量模擬、迭代演算法 | 一般分組摘要、join（用 data.table / dplyr） |
| 需要 C++ 函式庫（Armadillo、Eigen、Boost） | 小幅加速卻大幅增加維護成本 |

前置步驟見 [寫出有效率的 R](writing-efficient-r-code.md)。

## 環境準備

Rcpp 需要 C++ 編譯器：

| 平台 | 安裝 |
| --- | --- |
| Windows | 對應 R 版本的 [Rtools](https://cran.r-project.org/bin/windows/Rtools/) |
| macOS | `xcode-select --install`（Command Line Tools） |
| Linux | `build-essential`（Debian / Ubuntu）或 `gcc-c++` |

```r
pkgbuild::has_build_tools(debug = TRUE)       # 檢查編譯器是否可用
Rcpp::evalCpp("40 + 2")                       # 42：能編譯就代表環境 OK
```

## 三種寫法

| 寫法 | 用途 |
| --- | --- |
| `evalCpp("expr")` | 測試單一 C++ 運算式 |
| `cppFunction("...")` | 在 R session 內定義小函式，原型與比較用 |
| `sourceCpp("file.cpp")` | 獨立 `.cpp` 檔，編譯後把 `// [[Rcpp::export]]` 的函式載入 R |
| 放進套件的 `src/` | 正式使用；`usethis::use_rcpp()` 自動設定，見 [套件開發](package-development.md) |

```r
library(Rcpp)

cppFunction("
double sum_cpp(NumericVector x) {
  double total = 0;
  for (R_xlen_t i = 0; i < x.size(); i++) total += x[i];
  return total;
}")
sum_cpp(c(1, 2, 3.5))                         # 6.5
```

`.cpp` 檔的最小結構：

```cpp
#include <Rcpp.h>
using namespace Rcpp;           // 可直接寫 NumericVector 而非 Rcpp::NumericVector

// [[Rcpp::export]]             // 少了這行，R 端看不到這個函式
NumericVector ema(NumericVector x, double alpha) {
  // 指數移動平均：每一步依賴上一步，無法向量化
  R_xlen_t n = x.size();
  NumericVector out(n);
  out[0] = x[0];
  for (R_xlen_t i = 1; i < n; i++) {
    out[i] = alpha * x[i] + (1 - alpha) * out[i - 1];
  }
  return out;
}
```

```r
sourceCpp("ema.cpp")
ema(c(1, 2, 3), alpha = 0.5)                  # 1.00 1.50 2.25

# 一定要和 R 版本比對結果，再比速度
ema_r <- function(x, a) { out <- x; for (i in 2:length(x)) out[i] <- a * x[i] + (1 - a) * out[i - 1]; out }
bench::mark(ema_r(x, 0.1), ema(x, 0.1))       # check = TRUE 會驗證兩者相同
```

## R 型別與 C++ 型別對照

| R | Rcpp 類別 | 單一值 |
| --- | --- | --- |
| numeric vector | `NumericVector` | `double` |
| integer vector | `IntegerVector` | `int` |
| logical vector | `LogicalVector` | `bool` |
| character vector | `CharacterVector` | `String` / `std::string` |
| matrix | `NumericMatrix`（`m(i, j)`、`m.nrow()`） | |
| list / data frame | `List` / `DataFrame` | |

| 操作 | R | C++ |
| --- | --- | --- |
| 長度 | `length(x)` | `x.size()` |
| 第一個元素 | `x[1]` | `x[0]` |
| 最後一個元素 | `x[length(x)]` | `x[x.size() - 1]` |
| 建立長度 n 的零向量 | `numeric(n)` | `NumericVector x(n);` |
| 缺值判斷 | `is.na(x[i])` | `NumericVector::is_na(x[i])` |
| 拋出錯誤 | `stop("...")` | `stop("...")`（會變成 R 的 error） |

> **最常見錯誤**：C++ 從 0 開始索引。把 R 的 `for (i in 1:n)` 直接翻成 `for (i = 1; i <= n; i++)` 會越界讀取記憶體，結果可能是錯誤數字而不是報錯。

## 亂數與輸入檢查

```cpp
// [[Rcpp::export]]
NumericVector positive_draws(int n, double mu, double sd) {
  if (n < 0) stop("n must be non-negative");
  NumericVector x(n);
  for (int i = 0; i < n; i++) {
    double d;
    do { d = R::rnorm(mu, sd); } while (d < 0);   // rejection sampling：抽到正值為止
    x[i] = d;
  }
  return x;
}
```

- `R::rnorm()`、`R::runif()` 用的是 R 的亂數產生器，所以 R 端 `set.seed()` 一樣有效、結果可重現；不要改用 C++ 的 `std::rand()`。
- 向量版 sugar：`Rcpp::rnorm(n, mu, sd)` 一次產生整個向量。
- Rcpp sugar 還提供 `sum()`、`mean()`、`ifelse()`、`is_na()` 等向量化函式，寫法接近 R。

## 進階：線性代數

| 套件 | 用途 |
| --- | --- |
| RcppArmadillo | 矩陣運算語法接近 MATLAB（`arma::mat`、`solve()`、`inv()`） |
| RcppEigen | Eigen 函式庫，含稀疏矩陣 |
| RcppParallel | 多執行緒迴圈（thread-safe 的資料結構） |

```cpp
// [[Rcpp::depends(RcppArmadillo)]]
#include <RcppArmadillo.h>

// [[Rcpp::export]]
arma::vec ols(const arma::mat& X, const arma::vec& y) {
  return arma::solve(X, y);                     // 最小平方解
}
```

## 工作流程與常見錯誤

1. 先用 R 寫出正確版本並保留，作為對照與測試。
2. profiling 確認瓶頸。
3. `cppFunction()` 寫最小版本，`bench::mark()` 確認結果相同且確實較快。
4. 穩定後搬到 `.cpp` 檔；長期使用就放進套件並寫 testthat 測試。

| 錯誤 | 後果 / 做法 |
| --- | --- |
| 1-based 索引直覺 | 越界讀寫，結果錯誤或 R 當掉 |
| 忘了 `// [[Rcpp::export]]` | R 端找不到函式 |
| 用 `int` 存長度或大的計數 | 超過 2³¹−1 溢位；長度用 `R_xlen_t`，累加用 `double` |
| 沒處理 `NA` | C++ 不會自動傳遞 `NA`；`NA_INTEGER` 是一個很大的負數，會被當成普通值計算 |
| 修改傳入的 `NumericVector` | Rcpp 傳的是 reference，會**直接改到 R 端的原物件**；需要時先 `clone(x)` |
| 還沒 profiling 就整段搬到 C++ | 除錯與編譯成本高，加速卻集中在別處 |
