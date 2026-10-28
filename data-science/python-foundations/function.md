[Data Science](../README.md) › [Python Foundations](README.md) › 函式

# 函式 (Functions)

函式把一段邏輯包成可重用、可測試的單位。這篇從參數設計、作用域 (scope)、閉包 (closure)，到 decorator、context manager 與 `functools` 工具。

## 參數設計

| 寫法 | 收到的型別 | 用途 |
| --- | --- | --- |
| `def f(a, b)` | — | 必填位置參數 |
| `def f(a, b=2)` | — | 預設值：表達「大多數呼叫都這樣用」 |
| `def f(*args)` | `tuple` | 不定數量位置參數 |
| `def f(**kwargs)` | `dict` | 不定數量關鍵字參數 |
| `def f(a, *, alpha=0.05)` | — | `*` 之後只能用關鍵字傳（keyword-only），避免位置傳錯 |
| `def f(x, /, y)` | — | `/` 之前只能用位置傳（positional-only，3.8+） |

```python
def average(*args):
    return sum(args) / len(args)

def average_kwargs(**kwargs):
    return sum(kwargs.values()) / len(kwargs)

average(15, 29, 4)                       # 16.0
average_kwargs(a=15, b=29, c=4)          # 16.0

# 呼叫端用 * / ** 展開 (unpacking)：先展開，再照一般規則配對參數
values = [15, 29, 4, 13]
average(*values)                         # 15.25
average(*[15, 29], *[4, 13])             # 可合併多段
average_kwargs(**{"a": 15}, **{"b": 29}) # 22.0

def filter_genes(pvalues, *, alpha=0.05, method="fdr_bh"):
    ...
filter_genes(p, alpha=0.01)              # OK
# filter_genes(p, 0.01)                  # TypeError：強迫呼叫端寫清楚是哪個參數
```

> 參數結構固定時優先用明確參數；`*args, **kwargs` 主要用在 wrapper / decorator，把參數原封不動往下傳。

### 陷阱：可變預設值 (Mutable Default Argument)

預設值只在 `def` 執行時**建立一次**，之後每次呼叫共用同一個物件。

```python
def add_item(item, bucket=[]):           # 錯：所有呼叫共用同一個 list
    bucket.append(item)
    return bucket

add_item(1); add_item(2)                 # [1, 2]  上一次的結果留下來了

def add_item(item, bucket=None):         # 對：用 None 當哨兵值
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

## 回傳值

```python
def summarize(x):
    return min(x), max(x)                # 其實回傳一個 tuple

lo, hi = summarize([3, 1, 4])            # 呼叫端 unpack：1, 4
```

沒有 `return` 的函式回傳 `None`。回傳很多欄位時，改用 `dict`、`namedtuple` 或 `dataclass` 比 5 個值的 tuple 好讀。

## 作用域 (Scope)：LEGB

名稱查找順序：**L**ocal → **E**nclosing（外層函式）→ **G**lobal（模組）→ **B**uilt-in（`len`、`sum`）。

| 情境 | 行為 |
| --- | --- |
| 函式內只**讀**外層變數 | 可以，照 LEGB 找到 |
| 函式內對同名變數**賦值** | 建立新的 local 變數，不影響外層 |
| `global x` | 賦值作用在模組層的 `x` |
| `nonlocal x` | 賦值作用在最近一層外層函式的 `x` |

```python
x = 7
def change_local_only():
    x = 42                               # 新的 local x
change_local_only(); x                   # 7

def change_global():
    global x
    x = 42
change_global(); x                       # 42

def counter():
    n = 0
    def inc():
        nonlocal n
        n += 1
        return n
    return inc
c = counter(); c(); c()                  # 2
```

> 避免用 `global` 共享可變狀態，改成參數傳入、回傳結果；狀態多時考慮 class。

## 閉包 (Closure)

內部函式會記住外層作用域的值，即使外層函式已經結束。decorator、factory function、`partial` 都建立在這個機制上。

```python
def raise_val(n):
    def inner(x):
        return x ** n
    return inner

square = raise_val(2)
square(5)                                # 25
[c.cell_contents for c in square.__closure__]   # [2]：閉包捕捉到的值

# 陷阱：延遲綁定 (late binding)——閉包記的是變數，不是當下的值
funcs = [lambda x: x * i for i in range(3)]
[f(10) for f in funcs]                   # [20, 20, 20]，不是 [0, 10, 20]
funcs = [lambda x, i=i: x * i for i in range(3)]  # 用預設值當下綁定 → [0, 10, 20]
```

## Lambda 與高階函式 (Higher-order Functions)

```python
from functools import reduce

words = ["a", "ab", "abc"]
list(map(lambda w: w + "!", words))      # ['a!', 'ab!', 'abc!']
list(filter(lambda w: len(w) > 1, words))# ['ab', 'abc']
reduce(lambda a, b: a + b, words)        # 'aababc'

[w + "!" for w in words]                 # 多數情況 comprehension 比 map/filter 好讀

pairs = [(0, 3), (1, 2), (3, 0)]
sorted(pairs, key=lambda e: e[1])        # 依第 2 個元素：[(3, 0), (1, 2), (0, 3)]
sorted(pairs, key=lambda e: e[1], reverse=True)

s = [2, 3, 1]
sorted(range(len(s)), key=lambda k: s[k])  # argsort：[2, 0, 1]（NumPy 用 np.argsort）

from operator import itemgetter
sorted(pairs, key=itemgetter(1))         # 等同 lambda e: e[1]
```

## Docstring 與型別註記 (Type Hints)

```python
def normalize(counts: list[int], scale: float = 1e6) -> list[float]:
    """Convert raw counts to counts per `scale` (CPM by default).

    Args:
        counts: Raw read counts per gene.
        scale: Library-size scaling factor.

    Returns:
        Normalized values in the same order as `counts`.
    """
    total = sum(counts)
    return [c / total * scale for c in counts]

normalize.__doc__                        # 原始 docstring
import inspect; inspect.getdoc(normalize)  # 清掉縮排，多行 docstring 用這個
help(normalize)
```

型別註記執行時**不檢查**，靠 `mypy` / `pyright` 或編輯器提示抓錯；docstring 慣例見 [軟體工程實務](software-engineering.md)。

## Decorator

decorator 是「接收函式、回傳新函式」的函式；`@deco` 等同 `f = deco(f)`。

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)                         # 保留原函式的 __name__、__doc__
    def wrapper(*args, **kwargs):
        t0 = time.perf_counter()         # 量時間用 perf_counter，不用 time.time
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.perf_counter() - t0:.2f}s")
        return result
    return wrapper

def repeat(times):                       # 帶參數的 decorator：多包一層
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@timer
@repeat(3)                               # 由下往上套：timer(repeat(3)(say_hello))
def say_hello():
    print("Hello!")
```

帶參數 decorator 的執行順序：`repeat(3)` 回傳 `decorator`（閉包記住 `times=3`）→ `decorator(say_hello)` 回傳 `wrapper` → 之後呼叫 `say_hello()` 實際執行的是 `wrapper()`。

### 快取 (Memoization)：用 `functools.cache`

```python
from functools import cache, lru_cache

@cache                                   # 3.9+；無上限快取，等同 lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

@lru_cache(maxsize=128)                  # 有上限，超過丟掉最久沒用的
def load_reference(path):
    ...

fib(80); fib.cache_info()                # hits / misses / currsize
```

| 自己寫 memoize 的坑 | `functools.cache` |
| --- | --- |
| `f(3, 4)` 與 `f(a=3, b=4)` 會存成兩個 key | 一樣會（key 依呼叫方式），但已處理 hash 與 thread-safety |
| 引數必須可 hash（list、DataFrame 不行） | 同樣限制 |

> 快取只適合**純函式**（同輸入必同輸出、無副作用）。讀檔函式若檔案會變，快取會回傳舊結果。

## Context Manager

`with` 保證離開區塊時一定執行清理（關檔、還原狀態、釋放連線），即使中途出錯。

```python
import contextlib, os

@contextlib.contextmanager
def in_dir(path):
    old = os.getcwd()
    os.chdir(path)
    try:
        yield                            # with 區塊在這裡執行
    finally:
        os.chdir(old)                    # 一定會還原

with in_dir("data"):
    print(os.listdir())

with open("a.txt") as fin, open("b.txt", "w") as fout:   # 同時管理多個資源
    fout.write(fin.read())
```

類別版寫法（`__enter__` / `__exit__`）見 [類別](class.md)；檔案操作見 [腳本與 CLI](scripting-and-cli.md)。

## `functools.partial`

```python
from functools import partial

def power(base, exp):
    return base ** exp

square = partial(power, exp=2)
square(5)                                # 25
desc = partial(sorted, reverse=True)
desc([3, 1, 2])                          # [3, 2, 1]
```

平行化時傳給 `Pool.map` 的函式只能收一個參數，`partial` 很好用，見 [平行運算](performance-and-scaling/parallel.md)。
