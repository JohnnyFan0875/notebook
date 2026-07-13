# Python: Control Flow

控制流程的核心不是記住 `if`、`for`、`while` 的語法，而是知道什麼情況下要做一次判斷、什麼情況下要遍歷一個序列、以及什麼情況下需要持續重複直到條件改變。

## Mental Model

可以先用這個簡化版心智模型：

- `if`: 檢查一次條件
- `for`: 對一個 iterable 中的每個元素做事
- `while`: 只要條件成立就持續做事

## Whitespace Is Part of the Syntax

Python 和很多其他語言不一樣，縮排不是排版偏好，而是語法本身的一部分。

```python
if 5 == 5:
    print("True")
```

這裡的縮排代表 `print("True")` 屬於 `if` 區塊。

實務上可以把它理解成：

- 冒號 `:` 開啟一個區塊
- 下一層縮排表示區塊內容
- 縮排退回去，代表區塊結束

如果你有 R、JavaScript 或 MATLAB 背景，這個差異通常是最先需要重新適應的地方，因為 Python 不靠 `{}` 或 `end` 來標示區塊。

## `if`, `elif`, `else`

```python
price = 120

if price > 100:
    print("expensive")
elif price > 50:
    print("mid-range")
else:
    print("cheap")
```

這類結構適合：

- 單次分類
- 規則分支
- 根據條件選擇不同行為

### Logical Operators

```python
if "HT91" in products_dict and min(products_dict.values()) > 5:
    ...

if "HT91" in products_dict or min(products_dict.values()) < 5:
    ...
```

實務上最常見的是：

- `and`: 所有條件都要成立
- `or`: 任一條件成立即可
- `not`: 對布林條件取反

## `for` Loops

`for` loop 適合「遍歷一個已知 iterable」。

```python
prices = [10, 20, 30]

for price in prices:
    print(price)
```

這裡的重點不是 index，而是每次直接拿到元素本身。

如果你有 MATLAB 背景，這一點特別值得記：

- MATLAB 初學常把 `for` 想成「讓 counter 往前跑」
- Python 更自然的心智模型是「依序拿出 iterable 裡的每個元素」

所以很多 Python `for` 不需要先寫 `1:n` 這種計數範圍，因為資料本身就能被直接遍歷。

### Loop Through Strings

```python
username = "alice"

for char in username:
    print(char)
```

字串本身也是 iterable，所以可以逐字元遍歷。

### Loop Through Dictionaries

字典最常見的三種遍歷方式：

```python
products_dict = {"AG32": 87.99, "HT91": 21.50}

for key, value in products_dict.items():
    print(key, value)
```

```python
for key in products_dict.keys():
    print(key)

for value in products_dict.values():
    print(value)
```

實務上：

- 要同時拿 key 和 value，用 `.items()`
- 只要 key，用直接 `for key in products_dict:` 或 `.keys()`
- 只要 value，用 `.values()`

如果你把 `dict` 想成有欄位名稱的記錄集合，`.items()` 幾乎就是最接近「逐筆拿欄位名與內容」的迭代方式。

## `range()`

`range()` 很常和 `for` 搭配，用來產生整數序列。

```python
for i in range(1, 6):
    print(i)
```

記法：

- `range(start, stop)`
- 包含 `start`
- 不包含 `stop`

所以 `range(1, 6)` 會得到 `1, 2, 3, 4, 5`。

當你真的只需要重複固定次數，`range()` 很自然；但如果你已經有 list、dict、array、DataFrame，就優先直接迭代它們，而不是硬把問題改寫成 index loop。

### Loop Through Arrays and Tables

很多資料工作最後不是在 loop 數字，而是在 loop 結構。

```python
import numpy as np

X = np.array([[1, 2, 3], [4, 5, 6]])

for row in X:
    print(row)
```

這裡每次拿到的是一整列，不是 row index。

如果是 pandas DataFrame，雖然也能逐列迭代：

```python
for idx, row in df.iterrows():
    print(idx, row["fruit"], row["color"])
```

但實務上通常還是優先考慮 vectorized 操作，只有在逐列邏輯真的必要時才退回 loop。

## Build Results Incrementally

很多入門 loop 的本質都是：

1. 先建立一個空容器
2. 遍歷資料
3. 只把符合條件的結果存進去

```python
expensive_products = []

for key, value in products_dict.items():
    if value > 25:
        expensive_products.append(key)
```

這是理解 comprehension 的前一步。當邏輯變簡單後，才值得再改寫成 comprehension。

## `while` Loops

`while` 適合「重複次數不先固定，而是看條件何時不成立」的情境。

```python
num_purchases = 0
stock = 5

while num_purchases < stock:
    num_purchases += 1
```

常見使用情境：

- 等待某個狀態改變
- 持續重試直到成功或超限
- 不知道會跑幾次，但知道停止條件

### A Convergence-Style Example

有些 `while` 不是在處理使用者輸入，而是在做逐步逼近。

```python
error = 50.0

while error > 1:
    error = error / 4
```

這種寫法很適合表達：

- iterative refinement
- optimization loop
- numerical stopping condition

Key point: `while` 的停止條件不一定來自外部事件，也可能來自某個數值已經收斂到可接受範圍。

### `if` vs `while`

差別不是語法，而是執行次數。

- `if`：條件成立就進去一次
- `while`：條件成立就持續重複

如果你只是想做一次條件判斷，不要誤用 `while`。

## `break`

有時候 loop 的停止條件不是只靠外層 `while` 或 `for` 自然結束，而是想在迴圈中途提早終止。

```python
while num_purchases < stock:
    if num_purchases == 3:
        break
    num_purchases += 1
```

`break` 也可以用在 `for` loop：

```python
for price in prices:
    if price > 100:
        break
```

適用情境：

- 找到第一個符合條件的值就停
- 偵測到錯誤或特殊狀況就提前結束
- 避免不必要的後續迭代

## Membership Checks Inside Control Flow

搭配 `in` / `not in`，很多條件會更直觀。

```python
if "OS31" in products_dict:
    ...

if "OS31" not in products_dict:
    ...
```

這種寫法通常比先取 keys 再做多餘轉換更直接。

## Choosing Between `for` and `while`

優先順序通常是：

1. 如果你在遍歷某個 iterable，先用 `for`
2. 如果你在等待條件變化，才用 `while`

因為：

- `for` 比較不容易寫出無限迴圈
- `for` 直接表達「對這些元素逐一操作」
- `while` 比較適合事件驅動或狀態驅動的邏輯

## Comparison Expressions Drive Control Flow

很多 control flow 最後其實都建立在 comparison expression 上。

例如：

```python
2 < 3        # True
3 <= 3       # True
2 == 3       # False
"carl" < "chris"   # True
```

這提醒兩件事：

- `if` 和 `while` 最終都在吃布林值
- 某些型別可以比較大小，但不同型別未必可以直接比較

## Practical Checklist

- 一次判斷：`if`
- 逐一遍歷資料：`for`
- 重複直到條件改變：`while`
- 提早結束迴圈：`break`
- 同時拿字典 key / value：`.items()`
- 篩選累積結果：空容器 + loop + condition

## Takeaways

- `if`、`for`、`while` 的差異，核心在於執行模式，不只是語法。
- 大多數資料遍歷工作優先用 `for`。
- `while` 適合未知次數、已知停止條件的流程。
- `break` 是中途終止，而不是主要控制結構。
- 會寫 loop 只是起點，接下來才是判斷何時該改成 comprehension、built-ins 或向量化。
