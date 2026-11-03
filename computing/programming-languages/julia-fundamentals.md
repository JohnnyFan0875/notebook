[Computing](../README.md) › [程式語言](README.md) › Julia 基礎

# Julia 基礎 (Julia Fundamentals)

Julia 為科學運算設計：寫起來像 Python / R / MATLAB，執行時由 JIT 編譯成機器碼，迴圈也能接近 C 的速度，不必像 Python 一樣靠向量化或改寫成 C 擴充。常見於數值模擬、微分方程、最佳化、統計與部分生資工具（BioJulia）。進階語法見 [Julia 進階模式](julia-intermediate-patterns.md)。

| 特色 | 說明 |
| --- | --- |
| JIT 編譯 | 第一次呼叫函式時編譯（會慢），之後很快 |
| 多重分派 (multiple dispatch) | 依**所有參數的型別**選擇要執行的方法，是組織程式的核心方式 |
| 1-based 索引、column-major | 與 R、MATLAB、Fortran 相同；與 Python / NumPy 不同 |
| 廣播 (broadcasting) | 點語法 `.+`、`f.(x)` 逐元素運算 |
| 型別可選 | 不寫型別也能跑；寫了用於分派與文件 |

## 安裝與環境

```bash
# 安裝：官方建議用 juliaup 管理版本
winget install --name Julia --id 9NJNWW8PVKMN -e -s msstore   # Windows
curl -fsSL https://install.julialang.org | sh        # macOS / Linux

julia                       # 啟動 REPL
julia script.jl             # 執行腳本
```

```julia
# REPL 中按 ] 進入套件模式
] activate .                # 使用目前資料夾的專案環境（Project.toml + Manifest.toml）
] add DataFrames CSV        # 安裝並寫入 Project.toml
] instantiate               # 依 Manifest.toml 重建環境（可重現）
```

> `Project.toml` / `Manifest.toml` 的角色相當於 Python 的 `pyproject.toml` / `uv.lock`、R 的 `renv.lock`。

## 型別與變數

```julia
x = 3
typeof(3), typeof(3.14), typeof(true), typeof("Jane"), typeof('a')
# (Int64, Float64, Bool, String, Char)

parse(Int64, "1")           # 1：字串 → 數字（不會自動轉換）
parse(Float64, "1.5")       # 1.5
string(1)                   # "1"
```

## 字串

```julia
name = "Jane"                                  # 雙引號 = String，單引號 = Char
poem = """Beware the Jabberwock, my son!
The jaws that bite, the claws that catch!"""   # 多行字串

"Hello " * name                                # 串接用 *（不是 +）
row, seat = 4, 12
"Your seat is row $row, seat $seat."           # 內插
"The product is $(row * seat)"                 # 內插運算式
```

## 陣列與廣播

```julia
names = ["Ana", "Ben", "Cara"]
typeof(names), eltype(names)          # (Vector{String}, String)

names[1]                              # "Ana"：索引從 1 開始
names[end]                            # "Cara"
names[1:2]                            # ["Ana", "Ben"]：範圍包含結尾

x = String[]                          # 空的 String 向量
push!(x, "first")                     # ! 結尾 = 會修改參數的函式（慣例）

a = [1, 2, 3]; b = [10, 20, 30]
a .+ 2                                # [3, 4, 5]
a .+ b                                # [11, 22, 33]
a .* 5                                # [5, 10, 15]
sqrt.(a)                              # 函式也能廣播
a * 5                                 # 純量乘向量可以不加點；但 a * b 是矩陣乘法 → 維度錯誤
```

> 沒加點時，運算子是**線性代數**意義（`*` 是矩陣乘法），逐元素運算一定要用 `.*`、`.^`、`f.(x)`。

## 控制流程

```julia
if score >= 90
    println("Excellent")
elseif score >= 70
    println("Good effort")
else
    println("Keep trying")
end

for name in names                     # 迴圈與 if 都以 end 結束
    println(name)
end

counter = 1
while counter <= 3
    counter += 1
end
```

比較運算子：`==`、`!=`、`<`、`<=`、`>`、`>=`；邏輯：`&&`、`||`、`!`。

## 函式與多重分派

```julia
function double(x)
    return x * 2
end
double_short(x) = x * 2               # 單行定義

double(x::String) = x * x             # 同名函式、不同參數型別 → 不同方法
double(x::Bool) = !x

double(2)        # 4
double(10.0)     # 20.0
double("ab")     # "abab"
double(true)     # false
methods(double)  # 列出所有方法
```

多重分派依**所有**參數的型別選方法（Python 的方法只依第一個參數 `self` 的類別），所以不同套件定義的型別與函式可以自然組合。

## DataFrames 與 CSV

```julia
using DataFrames, CSV

df = DataFrame(
    day = ["Wednesday", "Monday", "Thursday"],
    distance = [2000, 5000, 3500],
    time = [14.99, 31.68, 22.02],
    raining = [true, false, true],
)
df = CSV.read("run.csv", DataFrame)          # 讀 CSV

first(df, 3); names(df); size(df); describe(df)   # 檢視

df[2, 3]            # 第 2 列第 3 欄的值
df[:, :distance]    # 一欄（複本）；df.distance 或 df[!, :distance] 不複製
df[2:4, :]          # 多列
df[:, 1:3]          # 多欄

sort(df, :distance)
filter(row -> row.day == "Monday", df)
filter(row -> row.distance <= 3000 && row.raining, df)

df.speed = (df.distance ./ 1000) ./ (df.time ./ 60)   # 新欄位：km/h，用廣播
```

| 操作 | Julia DataFrames | pandas |
| --- | --- | --- |
| 讀檔 | `CSV.read(f, DataFrame)` | `pd.read_csv(f)` |
| 取欄 | `df.col`、`df[!, :col]` | `df["col"]` |
| 篩選 | `filter(row -> cond, df)`、`subset(df, :col => ByRow(f))` | `df[cond]`、`df.query()` |
| 分組彙總 | `combine(groupby(df, :g), :x => mean)` | `df.groupby("g")["x"].mean()` |

## 常見錯誤

| 錯誤 | 說明 |
| --- | --- |
| 以為索引從 0 開始 | Julia 從 1 開始，`end` 是最後一個 |
| `"a" + "b"` | 字串串接用 `*` |
| 逐元素運算忘了點 | `a * b` 是矩陣乘法 |
| 混用 `String` 與 `Char` | `"a"` 與 `'a'` 不同型別 |
| 文字沒有 `parse` 就當數字用 | 不會自動轉換 |
| 第一次執行很慢就以為 Julia 慢 | 那是 JIT 編譯時間，見 [進階模式：量測時間](julia-intermediate-patterns.md#量測執行時間) |
