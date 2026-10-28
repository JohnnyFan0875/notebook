[Data Science](../README.md) › [Python Foundations](README.md) › 控制流程

# 控制流程 (Control Flow)

控制流程決定程式「做一次判斷」、「逐一處理一批資料」還是「重複到條件改變」。R 的對應寫法見 [R 控制流程](../r-foundations/control-flow.md)。

| 結構 | 執行模式 | 何時用 |
| --- | --- | --- |
| `if` / `elif` / `else` | 條件成立就執行**一次** | 分類、規則分支 |
| `for` | 對 iterable 的**每個元素**執行一次 | 遍歷已知資料（首選） |
| `while` | 條件成立就**一直重複** | 次數未知、停止條件已知（重試、收斂） |
| `match` / `case`（3.10+） | 依值或結構比對 | 多分支且依資料形狀分派 |

## 縮排就是語法

Python 不用 `{}` 或 `end` 標示區塊：冒號 `:` 開啟區塊、下一層縮排是區塊內容、縮排退回代表結束。統一用 4 個空白，不要混用 tab。

## 條件判斷

```python
price = 120
if price > 100:
    label = "expensive"
elif price > 50:
    label = "mid-range"
else:
    label = "cheap"

label = "expensive" if price > 100 else "cheap"   # 條件運算式（一行版）

# 邏輯運算：and / or / not；in / not in 做成員檢查
if "HT91" in products and min(products.values()) > 5:
    ...
if 0 < pvalue <= 0.05:                           # 比較可串接，等同 0 < p and p <= 0.05
    ...
```

### Truthiness 與 `None`

| 視為 `False` | 視為 `True` |
| --- | --- |
| `False`、`None`、`0`、`0.0`、`""`、`[]`、`{}`、`set()` | 其他幾乎所有值 |

```python
if not records:            # 空 list → 進入
    ...
if value is None:          # 檢查 None 用 is，不用 ==
    ...
if count:                  # 陷阱：count == 0 時也會跳過，意思是「非 0」而不是「有值」
    ...
```

> NumPy array 與 pandas Series 不能直接放進 `if`（`ValueError: truth value ... is ambiguous`），要明講 `.any()`、`.all()` 或 `.empty`。

## `for` 迴圈

`for` 直接拿出 iterable 的每個元素，不需要先寫 `1:n` 計數範圍（MATLAB / R 習慣要改）。

```python
for gene in ["TP53", "EGFR"]:            # list
    ...
for char in "ATGC":                      # 字串逐字元
    ...
for key, value in products.items():      # dict：同時取 key 與 value
    ...
for i in range(1, 6):                    # range(start, stop)：含 start、不含 stop → 1..5
    ...
for i, gene in enumerate(genes, start=1):  # 需要索引時用 enumerate，不用 range(len(...))
    ...
for g, p in zip(genes, pvalues):         # 平行走兩個序列
    ...
for row in X:                            # 2D NumPy array：每次拿到一整列
    ...
```

### 累積結果 → comprehension

```python
# 空容器 + 迴圈 + 條件
expensive = []
for key, value in products.items():
    if value > 25:
        expensive.append(key)

# 邏輯簡單時改寫成 comprehension，意思相同
expensive = [key for key, value in products.items() if value > 25]

any(p < 0.05 for p in pvalues)           # 是否至少一個顯著
all(len(s) == 150 for s in reads)        # 是否全部等長
```

comprehension、generator 的完整說明見 [迭代器與生成器](iterator.md)。

> DataFrame 不要用 `iterrows()` 逐列處理，優先用向量化運算；見 [Efficient Python](performance-and-scaling/efficient-python.md) 與 [pandas 效能](pandas/performance.md)。

## `while` 迴圈

```python
# 重試直到成功或超過上限
attempt = 0
while attempt < 3:
    attempt += 1
    if try_download():
        break

# 數值收斂：停止條件來自數值本身
error, n_iter = 50.0, 0
while error > 1e-6 and n_iter < 1000:   # 一定要有上限，避免無限迴圈
    error /= 4
    n_iter += 1
```

| 能用 `for` 就用 `for` 的理由 |
| --- |
| 不容易寫出無限迴圈（不會忘記更新計數器） |
| 直接表達「對這些元素逐一操作」 |

## `break`、`continue`、`else`

| 關鍵字 | 作用 |
| --- | --- |
| `break` | 立刻結束整個迴圈 |
| `continue` | 跳過本輪剩下的程式，進下一輪 |
| `for ... else` / `while ... else` | `else` 區塊只在**沒有被 `break`** 時執行 |
| `pass` | 什麼都不做的佔位 |

```python
for line in lines:
    if line.startswith("#"):
        continue                 # 跳過註解行
    if not line.strip():
        break                    # 遇到空行就停

for gene in genes:
    if gene in blacklist:
        print("found", gene)
        break
else:
    print("no blacklisted gene") # 整個迴圈跑完都沒 break 才執行
```

## `match` / `case`（Python 3.10+）

```python
def describe(record):
    match record:
        case {"type": "SNV", "ref": r, "alt": a}:
            return f"SNV {r}>{a}"
        case {"type": "indel", "length": n} if n > 50:
            return "large indel"
        case {"type": "indel"}:
            return "indel"
        case _:
            return "unknown"
```

`match` 是結構比對 (structural pattern matching)，不只是 switch：可以拆解 dict、tuple、class 並加 guard（`if`）。單純比較值時，`if`/`elif` 或查表用的 dict 通常更簡單。
