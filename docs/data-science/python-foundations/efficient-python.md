# Python: Efficient Code Patterns

Python 效能優化最常見的誤區，不是「不會寫快」，而是太早做微調，或把本來能交給 built-ins、NumPy、pandas 的工作留在 Python loop 裡。

更穩定的做法是：

1. 先量測。
2. 找出真正的 bottleneck。
3. 改變解法的形狀，而不是先改語法細節。

## What Efficient Usually Means

有效率的程式通常同時在乎兩件事：

- runtime
- memory footprint

兩者不一定永遠同方向。有些做法更快，但會多吃記憶體；有些做法節省記憶體，但會犧牲可讀性或速度。所以優化前先確認你在解哪一種問題。

## Measure Before You Guess

如果沒有量測，優化常常只是把直覺包裝成信心。

在 notebook 或 IPython 中，`%timeit` 幾乎是最方便的起點。

```python
import numpy as np

%timeit np.random.rand(1000)
```

常見用法：

- `%timeit expr`：量單行表達式
- `%%timeit`：量整個 code cell
- `%timeit -n10 -r2 expr`：指定 loops 與 runs
- `%timeit -o expr`：保留結果物件，之後可看 `.timings`

實務上要注意：

- 比較方式要使用同一份資料
- 先量大方向，不要一開始就比較奈秒級差異
- 只因為 A 比 B 快，不代表這個差距在真實 bottleneck 上重要

## Profile the Hot Path

當你知道「程式慢」，下一步不是瞎改，而是找哪一行、哪一段最慢。

如果只看總執行時間，常常看不出真正的熱點。這時可以用 line profiler 類工具。

```python
%load_ext line_profiler
%lprun -f my_function my_function(data)
```

它適合回答：

- 是哪一行最耗時
- loop 裡哪個操作最重
- 是前處理、查詢、還是轉換最慢

同樣地，如果問題偏向記憶體，可以用 memory profiler 類工具觀察每行的額外配置。

```python
%load_ext memory_profiler
%mprun -f my_function my_function(data)
```

重點不是記住工具名稱，而是建立習慣：先定位，再重寫。

## Prefer Built-Ins Over Handwritten Loops

很多手寫 loop，其實都在重做 Python 已經幫你優化好的事。

### `range()`

```python
nums = range(0, 11)
even_nums = range(2, 11, 2)
```

`range()` 代表的是惰性序列，不會像手動建立 list 一樣立刻把所有值放進記憶體。

### `enumerate()`

```python
for i, value in enumerate(values):
    ...
```

如果你正在寫：

```python
for i in range(len(values)):
    value = values[i]
```

通常 `enumerate()` 會更自然，也比較不容易寫出 index bug。

### `zip()`

```python
for name, score in zip(names, scores):
    ...
```

它通常比手動依 index 拼接多個序列更乾淨。

### `map()`

```python
squares = list(map(lambda x: x ** 2, nums))
```

如果邏輯已經是「把同一個函式套到每個元素」，`map()` 或 comprehension 通常會比手寫 append loop 更簡潔。

## Comprehensions Are Often Better Than Append Loops

```python
# slower to read and usually slower to run
totals = []
for row in rows:
    totals.append(sum(row))

# better
totals = [sum(row) for row in rows]
```

comprehension 的好處：

- 意圖更集中
- 少了顯式 append 樣板
- 通常比手寫 loop 更快

但也不要把太複雜的商業邏輯塞進單一 comprehension。可讀性一旦崩掉，就不值得。

## Pick the Right Data Structure

很多效能問題不是 loop 太慢，而是資料結構選錯。

### Membership Testing: Prefer `set` for Fast Lookups

```python
names_set = set(names)

if "Zubat" in names_set:
    ...
```

如果你一直在做 membership check:

- `x in list` 需要線性掃描
- `x in set` 通常接近常數時間

這在去重、過濾、黑名單/白名單檢查時很常見。

### Counting: Prefer `collections.Counter`

```python
from collections import Counter

type_counts = Counter(poke_types)
```

如果你正在手寫：

```python
counts = {}
for x in items:
    counts[x] = counts.get(x, 0) + 1
```

那通常可以先考慮 `Counter`。

### Missing Keys: Prefer `defaultdict`

```python
from collections import defaultdict

groups = defaultdict(list)
for key, value in pairs:
    groups[key].append(value)
```

這會比每次先判斷 key 在不在 dict 中更清楚。

### Readable Lightweight Records: `namedtuple`

如果你的 tuple 已經有明確欄位意義，用 `namedtuple` 可以讓程式更容易讀，同時保留輕量結構。

## Use `itertools` Instead of Nested Loop Plumbing

`itertools` 常見價值不是「比較神奇」，而是把常見組合邏輯交給已實作好的 iterator 工具。

```python
from itertools import combinations

pairs = list(combinations(items, 2))
```

如果你正在手寫雙層或三層 nested loops 來產生成對、排列、組合，先想想：

- `product()`
- `permutations()`
- `combinations()`

是不是已經能直接表達你的意圖。

## Eliminate Loops When the Real Operation Is Bulk

有些 loop 的本質其實不是「逐筆依賴前一步」，而只是因為你還沒把問題改寫成 bulk operation。

### Use `map(sum, rows)` Instead of Manual Totals

```python
totals = list(map(sum, rows))
```

這類寫法不一定永遠勝過 comprehension，但常常可以讓程式更貼近「對每列做同一件事」的意圖。

### Use NumPy for Numeric Bulk Work

```python
import numpy as np

arr = np.array(rows)
avgs = arr.mean(axis=1)
```

當資料是純數值、且操作本質上是整批矩陣/向量運算時，NumPy 往往能遠勝 Python loop。

## Broadcasting Beats Manual Elementwise Loops

```python
import numpy as np

values = np.array([1, 2, 3, 4])
result = values * 2
```

這種寫法不是語法糖，而是把 elementwise work 交給 NumPy 的底層實作。

相對地，Python list 不支援真正的 broadcasting：

```python
values = [1, 2, 3, 4]
# values * 2 只是重複串接，不是數值乘法
```

所以如果你正在做大量數值逐元素轉換，NumPy 通常是更自然的容器。

## Move Invariants Outside the Loop

有些 loop 沒辦法完全消失，但仍然可以寫得更好。

核心原則：

- 每次迭代都一樣的計算，不要放在 loop 內
- 需要整批做一次的轉型，先在 loop 外處理
- loop 內只保留每筆都必須做的最小工作

```python
threshold = np.mean(attacks)

for name, attack in zip(names, attacks):
    if attack > threshold:
        ...
```

而不是：

```python
for name, attack in zip(names, attacks):
    threshold = np.mean(attacks)
    if attack > threshold:
        ...
```

這種重複計算在大迴圈中很容易變成無意義成本。

## pandas: Avoid Row-by-Row Work

對 DataFrame 來說，效率排序大致可以這樣記：

1. vectorized column operation
2. `.apply()` when needed
3. `.itertuples()` if you truly must iterate
4. `.iterrows()` as the slow path

如果你還在做：

```python
for i in range(len(df)):
    ...
```

通常代表問題還沒有被改寫成 pandas 最擅長的形式。

更完整的 DataFrame 效能整理放在 [pandas/performance.md](pandas/performance.md)。

## Memory Still Matters

快不快不是唯一問題，記憶體暴增也會讓程式變慢或直接失敗。

常見觀念：

- `range()` 比預先建好大 list 更省
- iterator / generator 通常比一次 materialize 全部資料更省
- `set` / `dict` 查找快，但本身也有額外記憶體成本
- NumPy array 通常比 Python object list 更緊湊，特別是純數值資料

如果問題是大型資料處理，記憶體配置方式常常和 runtime 同樣重要。

## Efficient Thinking Checklist

當某段程式慢時，可以先問：

- 我有量過它嗎
- 我知道最慢的是哪一行嗎
- 這個 loop 是否其實可以改成 built-in、comprehension、`map()`、`zip()`、`Counter`、`set`、`itertools`
- 這個問題是否本質上是 bulk numeric work，應該交給 NumPy
- 對 pandas 而言，是否應該改成 vectorized column operation
- loop 裡是否有重複做的一次性計算

## Practical Takeaways

- 先量測，再優化。
- 先選對資料結構，再談語法細節。
- built-ins、`collections`、`itertools` 常常就是最簡單的加速工具。
- 如果工作是整批數值運算，優先考慮 NumPy。
- 如果工作是 DataFrame 轉換，優先考慮 pandas 向量化。
- 真正大的效能提升，通常來自「少寫 Python-level loops」。
