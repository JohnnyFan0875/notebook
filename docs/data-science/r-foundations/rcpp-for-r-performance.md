# Rcpp for R Performance

當 R 端的向量化、preallocation、專用函式與 profiling 都做過之後，仍然有明確 bottleneck，`Rcpp` 就是把那一小段熱點改寫成 C++ 的常見入口。

重點不是把整個分析專案都改寫成 C++，而是只把最值得的那幾個函式降到較低層。

## When Rcpp Is Worth Considering

`Rcpp` 最適合這類情境：

- 有明確 profiling 證據顯示 bottleneck 在少數函式
- 該函式包含大量逐元素 loop、累積計算或模擬
- 單靠 R 端向量化不容易再改善
- 你想保留 R 作為主流程，但把核心運算換成 compiled code

Key point: `Rcpp` 是後段優化工具，不是 R workflow 的起點。

## The Basic Tradeoff

可以先用很粗略的方式理解：

- R: 寫分析流程快、互動高、彈性強
- C++: 寫起來比較重，但單次執行常更快

因此比較合理的策略通常是：

1. 用 R 把問題與資料流程講清楚
2. 找出真正慢的局部
3. 只把那一小塊搬到 `Rcpp`

## Three Common Entry Points

### `evalCpp()`

`evalCpp()` 適合快速試小型 C++ 表達式：

```r
library(Rcpp)

evalCpp("40 + 2")
evalCpp("sqrt(4.0)")
```

它比較像 sandbox，不適合真正封裝工作函式。

### `cppFunction()`

`cppFunction()` 適合直接在 R session 裡定義小型 C++ 函式：

```r
library(Rcpp)

cppFunction("
int timesTwo(int x) {
  return 2 * x;
}
")

timesTwo(21)
```

這最適合：

- 嘗試小想法
- 寫教學範例
- 快速比較 R 與 C++ 版本

### `sourceCpp()`

當函式開始變長或需要獨立檔案管理時，通常改用 `sourceCpp()`：

```cpp
#include <Rcpp.h>
using namespace Rcpp;

// [[Rcpp::export]]
int timesTwo(int x) {
  return 2 * x;
}
```

```r
library(Rcpp)
sourceCpp("code.cpp")
timesTwo(21)
```

`sourceCpp()` 會負責 compile 並把匯出的函式載入 R。

## Minimal Rcpp File Structure

最小可用的 `Rcpp` 檔通常包含三個元素：

```cpp
#include <Rcpp.h>
using namespace Rcpp;

// [[Rcpp::export]]
double add_one(double x) {
  return x + 1.0;
}
```

- `#include <Rcpp.h>`: 載入 Rcpp 的主要 header
- `using namespace Rcpp;`: 讓你可以直接寫 `NumericVector` 而不是 `Rcpp::NumericVector`
- `// [[Rcpp::export]]`: 告訴 Rcpp 這個函式要暴露給 R

如果少了 export attribute，函式通常不會自動變成可在 R 端直接呼叫的介面。

## Control Flow in C++

一個常見使用 Rcpp 的理由，是某段邏輯天生就比較適合 loop：

- `if / else if / else`
- `for`
- `while`
- `do ... while`

對 R 而言，逐元素 loop 在大資料上常有成本；對 C++ 而言，這反而是自然寫法。

例如：

```cpp
// [[Rcpp::export]]
int sign_code(int x) {
  if (x < 0) {
    return -1;
  } else if (x == 0) {
    return 0;
  } else {
    return 1;
  }
}
```

如果 bottleneck 本來就是大量條件判斷加迭代，這類局部改寫很常有價值。

## Working with R Vectors in C++

`Rcpp` 最重要的一組抽象，是能直接對應 R 物件的 vector classes：

- `NumericVector`
- `IntegerVector`
- `LogicalVector`
- `CharacterVector`
- `List`

例如：

```cpp
// [[Rcpp::export]]
double first_value(NumericVector x) {
  return x[0];
}
```

這些 class 讓你不用手刻 R 的底層 `SEXP` 介面，就能直接讀寫 R 向量。

## Two API Habits to Memorize

最常用的操作通常就兩個：

- `x.size()`: 向量長度
- `x[i]`: 第 `i` 個元素

```cpp
// [[Rcpp::export]]
double sum_cpp(NumericVector x) {
  double total = 0.0;
  for (int i = 0; i < x.size(); i++) {
    total += x[i];
  }
  return total;
}
```

Key point: C++ indexing 從 `0` 開始，不是從 `1` 開始。

## The Biggest R-to-C++ Footgun: Indexing

R:

```r
x[1]
x[length(x)]
```

C++:

```cpp
x[0]
x[x.size() - 1]
```

這是最容易出錯的一點。很多 R 使用者第一次寫 Rcpp 時，不是邏輯錯，而是把 R 的 1-based indexing 直覺帶進了 C++。

## Random Number Generation

`Rcpp` 也能直接呼叫 R 的亂數機制。

單一數值：

```cpp
double x = R::rnorm(0, 1);
double y = R::runif(-2, 2);
```

向量版本：

```cpp
NumericVector x = rnorm(10, 0, 2);
```

也可以手動在 loop 裡逐個產生：

```cpp
NumericVector x(10);
for (int i = 0; i < 10; i++) {
  x[i] = R::rnorm(0, 2);
}
```

當你的 bottleneck 是大量模擬時，這個能力特別實用。

## Rejection Sampling Example

Rcpp 很適合包裝「反覆抽樣直到條件成立」這種流程，例如 rejection sampling：

```cpp
// [[Rcpp::export]]
NumericVector positive_draws(int n) {
  NumericVector x(n);

  for (int i = 0; i < n; i++) {
    double d;
    do {
      d = R::rnorm(2, 2);
    } while (d < 0);

    x[i] = d;
  }

  return x;
}
```

這類邏輯在純 R 中也能寫，但如果抽樣次數大、條件判斷頻繁，C++ loop 往往更合適。

## Error Handling

就算是為了速度改寫，也不代表可以放棄輸入檢查：

```cpp
// [[Rcpp::export]]
int safe_square(int x) {
  if (x < 0) {
    stop("x must be non-negative");
  }
  return x * x;
}
```

`stop()` 能把錯誤往 R 端拋回來，所以使用者仍然能得到熟悉的 error message。

## Practical Workflow

一條穩定的 Rcpp 使用流程通常是：

1. 先用 R 寫出正確版本。
2. 用 profiling 確認真的慢在那裡。
3. 先用 `cppFunction()` 寫最小可行 C++ 版本。
4. 確認結果與 R 版本一致。
5. 函式成熟後，再搬到 `.cpp` 檔並用 `sourceCpp()` 管理。

這樣可以避免一開始就把除錯與編譯複雜度拉太高。

## When Not to Use Rcpp

- 只是一般資料整理或 grouped summary，通常 tidyverse / data.table 就夠了
- 慢點來自 I/O、資料庫或網路，不是 CPU 計算
- bottleneck 還沒被 profiling 證明
- 小幅提速換來大量維護成本時

如果你只是想加速一個本來就能向量化的 base R 操作，通常應該先修 R 寫法，而不是急著開 C++。

## Common Mistakes

- 還沒確認 bottleneck 就先寫 Rcpp
- 把整個專案都往 C++ 搬，而不是只搬熱點函式
- 忘記 C++ 是 0-based indexing
- 沒有 `// [[Rcpp::export]]` 就期待函式能直接在 R 端呼叫
- 在 session 裡原型還沒穩定就過早拆成複雜 `.cpp` 結構

## Where It Fits in the Bigger Picture

`Rcpp` 最適合放在這個優化順序的後段：

1. 向量化
2. 減少重複計算與 object growth
3. profiling / benchmarking
4. 平行化或 `Rcpp`

也就是說，`Rcpp` 不是「讓 R 變快的唯一方法」，而是當 R 層已經合理後，用來處理剩餘計算熱點的工具。
