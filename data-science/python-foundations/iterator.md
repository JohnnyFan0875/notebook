[Data Science](../README.md) › [Python Foundations](README.md) › 迭代器與生成器

# 迭代器與生成器 (Iterators & Generators)

`for` 迴圈背後是迭代器協定 (iterator protocol)。懂了它，就能用 generator 逐筆處理比記憶體還大的檔案（FASTQ、VCF、大型 CSV），而不必一次全部讀進來。

## Iterable vs Iterator

| | Iterable | Iterator |
| --- | --- | --- |
| 定義 | 能交給 `iter()` 產生 iterator 的物件 | 會記住目前位置、用 `next()` 一個個吐值的物件 |
| 例子 | `list`、`tuple`、`dict`、`set`、`str`、`range` | `iter(list)`、`enumerate(...)`、`zip(...)`、`map(...)`、檔案物件、generator |
| 可重複迭代？ | 可以，每次 `for` 都產生新 iterator | **不行，用完就耗盡** |
| 需要的方法 | `__iter__()` | `__iter__()`（回傳自己）+ `__next__()`（耗盡時丟 `StopIteration`） |

```python
nums = [10, 20, 30]
it = iter(nums)
next(it), next(it), next(it)    # 10, 20, 30
# next(it)                      # StopIteration
next(it, None)                  # 給預設值就不會丟例外

e = enumerate(["a", "b", "c"])  # enumerate / zip / map 都是一次性的
next(e)                         # (0, 'a')
list(e)                         # [(1, 'b'), (2, 'c')]
list(e)                         # []：已耗盡
```

> 常見 bug：把 `zip(...)` 或 generator 存成變數後迭代兩次，第二次什麼都沒有。需要重複用就先 `list(...)`。

## `enumerate` 與 `zip`

```python
genes = ["TP53", "BRCA1", "EGFR"]
pvals = [0.001, 0.2, 0.03]

for i, g in enumerate(genes, start=1):     # 同時取索引與值
    ...

pairs = list(zip(genes, pvals))            # [('TP53', 0.001), ...]
names, ps = zip(*pairs)                    # unzip：用 * 展開
lookup = dict(zip(genes, pvals))           # 快速建 dict

list(zip("abc", [1, 2]))                   # [('a', 1), ('b', 2)]：依最短的截斷，不會警告
# zip(genes, pvals[:2], strict=True)       # 3.10+：長度不同直接丟 ValueError（建議用）
```

> 兩個平行 list 長度不一致常代表資料錯位（例如過濾了基因卻沒過濾 p 值）。用 `strict=True` 讓錯誤立刻浮現。

## 推導式 (Comprehensions)

```python
squares = [n * n for n in range(6)]               # list：[0, 1, 4, 9, 16, 25]
sq_map = {n: n * n for n in range(4)}             # dict：{0: 0, 1: 1, 2: 4, 3: 9}
bases = {c.upper() for c in "aTgCaa"}             # set：{'A', 'T', 'G', 'C'}
evens = [n for n in range(10) if n % 2 == 0]      # 過濾
labels = ["sig" if p < 0.05 else "ns" for p in pvals]   # 條件運算式放前面
flat = [x for row in [[1, 2], [3]] for x in row]  # 巢狀：順序同兩層 for → [1, 2, 3]
```

超過一層條件或兩層迴圈就改回一般 `for`，可讀性比較重要。

## 生成器 (Generators)：惰性求值

generator 是最容易寫的 iterator：值在需要時才算，不會一次放進記憶體。

| | list comprehension `[...]` | generator expression `(...)` |
| --- | --- | --- |
| 何時計算 | 立刻全部算完 | 迭代時一個個算 |
| 記憶體 | 與資料量成正比 | 幾乎固定 |
| 可重複迭代 | 可 | 一次性 |
| 適合 | 資料小、要多次使用、要 `len()` | 大檔、串流、只走一遍（如丟給 `sum()`） |

```python
total = sum(n * n for n in range(10_000_000))     # 不會建出千萬元素的 list

def read_fasta(path):
    """逐筆產生 (header, sequence)，檔案再大記憶體也只放一筆。"""
    header, chunks = None, []
    with open(path) as fh:
        for line in fh:                           # 檔案物件本身就是 iterator，逐行讀
            line = line.rstrip()
            if line.startswith(">"):
                if header is not None:
                    yield header, "".join(chunks)
                header, chunks = line[1:], []
            elif line:
                chunks.append(line)
    if header is not None:
        yield header, "".join(chunks)

for name, seq in read_fasta("genome.fa"):         # yield 讓函式暫停並保留狀態
    gc = (seq.count("G") + seq.count("C")) / len(seq)

# generator pipeline：每一步都是惰性的
long_seqs = (s for _, s in read_fasta("genome.fa") if len(s) > 1000)
n_long = sum(1 for _ in long_seqs)
```

> 逐行讀檔用 `for line in fh`，不要用 `fh.readlines()`（後者一次讀成整個 list）。正式分析用 Biopython `SeqIO.parse` 或 `pysam`，它們也是 generator。

## `itertools` 常用工具

| 函式 | 作用 | 例子 → 結果 |
| --- | --- | --- |
| `chain(a, b)` | 依序串接多個 iterable | `chain([1, 2], "ab")` → `1, 2, 'a', 'b'` |
| `islice(it, start, stop, step)` | 對 iterator 切片 | `islice(range(100), 10, 20, 2)` → `10, 12, …, 18` |
| `zip_longest(a, b, fillvalue=)` | zip 但補齊較短者 | `zip_longest("abc", [1, 2])` → `('c', None)` |
| `product(a, repeat=k)` | 笛卡兒積 | `product("ACGT", repeat=2)` → 16 種 2-mer |
| `permutations(x, k)` / `combinations(x, k)` | 排列 / 組合 | `combinations([1, 2, 3], 2)` → `(1,2), (1,3), (2,3)` |
| `groupby(sorted_x, key=)` | 把**連續**相同 key 分組 | 必須先排序 |
| `pairwise(x)`（3.10+） | 相鄰兩兩配對 | `pairwise([1, 2, 3])` → `(1,2), (2,3)` |
| `batched(x, n)`（3.12+） | 每 n 個一批 | `batched(range(5), 2)` → `(0,1), (2,3), (4,)` |
| `accumulate(x)` | 累積和（或自訂運算） | `accumulate([1, 2, 3])` → `1, 3, 6` |

```python
import itertools as it

kmers = ["".join(p) for p in it.product("ACGT", repeat=2)]   # 'AA', 'AC', ..., 'TT'

animals = ["ant", "bat", "ape", "bear"]
{k: list(g) for k, g in it.groupby(sorted(animals), key=lambda s: s[0])}
# {'a': ['ant', 'ape'], 'b': ['bat', 'bear']}；沒排序的話 'a' 會被拆成兩組

for batch in it.batched(sample_ids, 100):         # 分批送 API 或資料庫
    ...

head = list(it.islice(read_fasta("genome.fa"), 5))  # 只看前 5 筆，不讀完整個檔
```

## 自訂 iterator 類別

需要額外方法或屬性時才手寫 class；只是要逐筆產生值，用 generator function 更簡單。

```python
class Countdown:
    def __init__(self, start):
        self.current = start
    def __iter__(self):
        return self                   # 自己就是 iterator → 一次性
    def __next__(self):
        if self.current <= 0:
            raise StopIteration       # 少了這行，for 迴圈不會停
        self.current -= 1
        return self.current + 1

c = Countdown(3)
list(c), list(c)                      # [3, 2, 1], []

def countdown(n):                     # 等價的 generator 寫法
    while n > 0:
        yield n
        n -= 1
```

`map` / `filter` 的用法見 [函式](function.md#lambda-與高階函式-higher-order-functions)；大量數值運算別用 Python 迴圈，見 [Efficient Python](performance-and-scaling/efficient-python.md)。
