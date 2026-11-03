[Computing](../README.md) › [程式語言](README.md) › Julia 進階模式

# Julia 進階模式 (Julia Intermediate Patterns)

接續 [Julia 基礎](julia-fundamentals.md)：更多迭代方式、不可變與鍵值資料結構、彈性的函式簽章、量測效能，以及 DataFrame 的缺值處理。

## 迭代

```julia
shopping = ["Apples", "Bread", "Carrots"]

for (i, item) in enumerate(shopping)   # 同時要索引與值
    println("$i => $item")
end

r = 1:2:9                               # 範圍：起點 1、間隔 2、終點 9 → 1, 3, 5, 7, 9
first(r), step(r), last(r)              # (1, 2, 9)
collect(r)                              # 轉成陣列 [1, 3, 5, 7, 9]

for (x, y) in zip([1, 2], ["a", "b"]) end   # 平行走訪

vals = [1, 2, 3]
println(vals...)                        # splat：展開成多個參數 → println(1, 2, 3)
```

## 資料結構

| 結構 | 可變 | 例子 | 何時用 |
| --- | --- | --- | --- |
| `Vector` | 是 | `[1, 2, 3]` | 會增減的同型別資料 |
| `Tuple` | 否 | `(10, "Hello", true)` | 固定形狀的一組值、函式回傳多個值 |
| `NamedTuple` | 否 | `(name = "Anthony", city = "Sydney")` | 輕量的具名紀錄 |
| `Dict` | 是 | `Dict("ticker" => "AAPL")` | 依 key 查值 |
| `struct` | 否（`mutable struct` 可變） | 自訂型別 | 有固定欄位的領域物件，搭配多重分派 |

```julia
t = (10, 20, 30, 40)
t[1], t[2:3]                     # (10, (20, 30))
# t[1] = 5、push!(t, 50)         → 錯誤：tuple 不可變

person = (name = "Anthony", country = "Australia")
person.name                      # "Anthony"

stock = Dict{String, Any}("ticker" => "AAPL", "price" => 131.86)   # 宣告 key / value 型別
stock["volume"] = 62_128_300     # 新增或更新
get(stock, "pe", missing)        # key 不存在時回傳預設值
haskey(stock, "price")           # true
for (k, v) in stock              # 走訪 key-value 配對
    println("$k => $v")
end
keys(stock); values(stock)

struct Sample                    # 自訂不可變型別
    id::String
    reads::Int
end
s = Sample("S1", 1200)
s.reads                          # 1200
```

> 型別宣告越貼近實際資料越好：`Dict{String, Float64}` 比 `Dict{String, Any}` 清楚也快；但不要在還不確定資料形狀時就過度限制。

## 函式簽章

```julia
f(a, b = 2) = a + b                            # 預設值
repeat_str(s::String, n::Integer = 2) = s ^ n  # 型別標註；字串 ^ n = 重複 n 次
person(name; location = "Taipei") = "$name lives in $location"   # ; 之後是關鍵字參數
person("Ana"; location = "Tainan")
greet(names...) = println(join(names, ", "))   # 可變數量參數 (varargs)

(x -> x^2 + 3)(2)                              # 匿名函式 → 7
map(x -> 2x + x^2 + 1, [1, 2, 3])              # [4, 9, 16]；2x 是 2*x 的簡寫
map((x, y) -> x + y, [1, 2, 3], [10, 10, 10])  # 多個輸入 → [11, 12, 13]

add_values(x, y) = x + y                       # 多重分派：一般情況
add_values(x::String, y::String) = x * y       # 字串時改為串接
```

`map(f, xs)` 與廣播 `f.(xs)` 結果相同；廣播在多個陣列、純量混合時更簡潔。

## 量測執行時間

```julia
@time my_function()          # 時間 + 記憶體配置；第一次呼叫包含 JIT 編譯時間

using BenchmarkTools          # ] add BenchmarkTools
@btime my_function()          # 多次執行取最小值，排除編譯時間
@benchmark my_function()      # 完整的分布統計
```

| 現象 | 原因 |
| --- | --- |
| 第一次 `@time` 很慢 | 包含編譯；看第二次以後 |
| 配置 (allocations) 很多 | 常是型別不穩定（變數在迴圈中改變型別）或在全域範圍跑迴圈 |
| 全域變數迴圈慢 | 把程式碼包進函式；Julia 對函式內的程式碼才能完整最佳化 |

> 效能關鍵：**程式碼放進函式、維持型別穩定**。Julia 的迴圈本身就快，不需要刻意向量化。

## DataFrame 清理與缺值

```julia
using DataFrames, Statistics

rename!(df, :Adj_Close => :adj_close)        # 改欄名（! = 原地修改）
filter(row -> row.Close > 100, df)

describe(df)                                 # nmissing 欄：每欄缺值數
dropmissing(df, :Close)                      # 移除 Close 缺值的列（回傳新 DataFrame）
dropmissing!(df, :Close)                     # 原地版本
df.Close = coalesce.(df.Close, 130.0)        # 以固定值填補
mean(skipmissing(df.Close))                  # 計算時略過缺值；mean(df.Close) 遇到 missing 回傳 missing
```

> 刪除或填補缺值都很好寫，但不一定是對的統計選擇；缺值機制與填補方法見 [缺失值](../../data-science/data-manipulation-and-eda/README.md)。

## 與 Python / R 互通

| 套件 | 用途 |
| --- | --- |
| `PythonCall.jl` | 在 Julia 中呼叫 Python 套件（`pyimport("numpy")`） |
| `RCall.jl` | 在 Julia 中呼叫 R（`R"..."` 字串巨集） |
| `juliacall`（Python 端） | 在 Python 中呼叫 Julia |

原則：能在 Julia 內完成就留在 Julia，只有生態系真的缺時才跨語言。

## 常見錯誤

| 錯誤 | 說明 |
| --- | --- |
| 需要增減元素卻用 tuple | tuple 不可變，改用 `Vector` 或 `Dict` |
| 相信第一次的 `@time` | 包含編譯時間 |
| 在全域範圍寫效能關鍵的迴圈 | 包進函式 |
| `dropmissing!` 前沒想過偏誤 | 缺值可能不是隨機的 |
| 太早加嚴格的型別標註 | 限制了泛用性，卻不一定更快（Julia 會依實際型別編譯） |
