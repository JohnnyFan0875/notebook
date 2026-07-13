# Writing Efficient R Code

R 的強項是讓你快速思考、探索與寫分析流程，不是要你從一開始就像寫 C 一樣手管每一個 CPU cycle。真正的效率工作，通常不是「把所有程式都寫得像系統程式」，而是先找出 bottleneck，再用最划算的方式改善它。

## The Core Mental Model

效率優化通常應該照這個順序思考：

1. 先確認程式真的慢
2. 找出哪一段最慢
3. 先用更符合 R 思維的寫法改善
4. 只有在值得時，才往更重的工具走

Key point: 不要在沒有 bottleneck 證據時就過早優化。多數 R workflow 的瓶頸只集中在少數幾段程式。

## R vs Lower-Level Languages

R 比較偏向「方便思考與寫分析邏輯」，而不是「手動控制每一步記憶體與執行細節」。

直覺上可以這樣想：

- R: optimized for thinking / writing
- C / C++: optimized for running

這不代表 R 一定慢，而是：

- 高層寫法通常更快完成分析工作
- 真正要追求極致執行效率時，才考慮 lower-level route

所以優化 R 時，第一步通常不是直接改寫成 C++，而是先把 R 程式寫得更像 R。

## Prefer Vectorized Operations

最常見也最值得先做的優化，是把可以向量化的 loop 改成向量化表達。

例如建立整數序列：

```r
x <- 1:n
```

通常就比手寫逐格填值更自然，也更有效率：

```r
x <- vector("numeric", n)
for (i in 1:n) {
  x[i] <- i
}
```

向量化通常適合：

- element-wise arithmetic
- logical filtering
- summary functions
- 常見統計計算

如果 base R 已經有直接函式，例如 `rowSums()`、`colMeans()`、`pmin()`、`ifelse()`，通常先用現成函式比手寫 loop 更好。

## Memory Allocation and Preallocation

R 會自動管理記憶體，但這不代表你可以忽略 allocation 成本。最常見的低效率寫法，是在 loop 裡不斷把物件「長大」。

不建議：

```r
x <- c()
for (i in 1:n) {
  x <- c(x, i)
}
```

更好的做法是先配置好空間：

```r
x <- vector("numeric", n)
for (i in 1:n) {
  x[i] <- i
}
```

Key point: 每次 grow object，R 都可能重新配置記憶體並複製資料。對大迴圈來說，這會很傷。

## Avoid Repeated Copying

除了 `c()` 逐步擴張，另一個常見問題是反覆 `rbind()`、`cbind()` 或在 loop 內一直建立新的大型中間物件。

如果你要累積很多結果，通常更穩的做法是：

- 先存進 list
- 最後一次再合併

這個習慣對 data frame 組裝尤其重要，因為 row-by-row 擴張通常很慢。

## Choose the Right Built-In Tool

很多效率問題，並不是「R 太慢」，而是用了不適合的函式。

常見直覺：

- 向量摘要：`sum()`, `mean()`, `pmax()`
- 矩陣列欄摘要：`rowSums()`, `colMeans()`
- 軸向運算：`apply()` 家族

如果你已經在矩陣或 data frame 上做規律性的軸向操作，先想「有沒有現成的 specialized function」，通常比直接寫一般 loop 更快。

## Profiling Before Optimizing

在優化前，先找到 bottleneck。這就是 profiling 的工作。

R 內建有 `Rprof()`，但通常比較難直接讀；實務上常用 `profvis`：

```r
Rprof("profile.out")
# run code
Rprof(NULL)
```

或更常見地：

```r
profvis::profvis({
  # code to profile
})
```

profiling 的核心概念是：

- 跑程式
- 每隔一小段時間抽樣當下在執行什麼
- 找出時間主要花在哪些函式

Key point: 先用 profiling 找熱點，遠比靠直覺猜哪段最慢可靠。

## Benchmark Small Alternatives Carefully

當你已經知道 bottleneck 在哪裡，下一步才是比較替代寫法。

這時可以用 microbenchmark-style 工具來比較不同實作：

- base R vs vectorized version
- loop vs preallocated loop
- `apply()` vs specialized function

重點不是追求毫秒級排名，而是確認：

- 差異是否穩定
- 差異是否值得增加程式複雜度

如果改善只有一點點，但可讀性大幅下降，通常不划算。

## A Typical Optimization Path

當分析程式變慢時，常見的優化順序可以是：

1. 移除不必要的中間物件與重複計算
2. 改成向量化或專用函式
3. 預先配置輸出容器
4. 用 profiling 確認是否真的改善 bottleneck
5. 還不夠時，再考慮平行化或 C++ 擴充

這比一開始就跳去 `Rcpp` 或平行處理更穩，因為很多慢點其實在更早就能解掉。

## Parallelism Is Not the First Step

現代 CPU 常有多核心，但 base R 預設多數程式仍是單核心執行。這代表平行化確實可能有幫助，但不該是第一個反應。

原因包括：

- 平行化有啟動與資料傳輸成本
- 小任務常因 overhead 變更慢
- 除錯與重現性會更複雜

所以比較好的順序是：

- 先修正明顯低效率寫法
- 再確認 bottleneck 是否真的適合平行化

如果 bottleneck 是大量獨立任務、模擬或 parameter grid，平行化通常比較值得。

## Readability Still Matters

效率不是唯一目標。尤其在 notebook / analysis code 裡，可讀性與可維護性仍然很重要。

更好的程式通常是：

- 已經夠快
- 邏輯仍然清楚
- 方便之後修改與驗證

Warning: 用很難懂的技巧換到極小加速，常常是維護上的虧本交易。

## Practical Workflow

1. 先確認程式慢在哪個實際場景。
2. 用 profiling 找 bottleneck，而不是靠猜。
3. 先看能不能向量化、改用專用函式或減少 object growth。
4. 需要 loop 時先 preallocate。
5. 只有在 bottleneck 仍然明確存在時，才往平行化或 C++ 擴充走。

## Common Mistakes

- 一開始就過早優化，卻沒有 bottleneck 證據。
- 在 loop 裡不斷用 `c()`、`rbind()` 讓物件長大。
- 本來能用向量化或專用函式，卻堅持逐列處理。
- 沒 profiling 就直接猜哪段最慢。
- 為了小幅加速把程式寫得太難懂。
