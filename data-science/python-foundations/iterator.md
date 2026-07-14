# Python Iterators

> Practical patterns for `iter`, `next`, `enumerate`, `zip`, generator functions, `itertools`, and common comprehension idioms.

## Core Ideas

- **Iterable**: an object you can loop over (e.g., `list`, `tuple`, `dict`, `set`, `str`, `range`). Gives an **iterator** when passed to `iter()`.
- **Iterator**: maintains state during iteration and returns the next value when you call `next()`.

## Interview Fast Answer

面試裡如果被問 iterable 和 iterator 的差別，最精簡但不失真的回答可以是：

- iterable 是「可以拿來產生 iterator 的東西」
- iterator 是「真的會一個一個吐值、而且會被消耗的物件」

所以：

- `list` / `tuple` / `dict` / `set` / `str` 通常是 iterable
- `iter(obj)` 回傳的結果才是 iterator

如果你想再多補一句高訊號說法，可以加上：

- iterator 會記住目前走到哪
- `next()` 會推進狀態，耗盡後丟出 `StopIteration`

```python
nums = [10, 20, 30]
it = iter(nums)      # create an iterator from the iterable
print(next(it))      # 10
print(next(it))      # 20
print(next(it))      # 30
# next(it) now raises StopIteration
```

## Iterator Protocol

Python 會把一個物件視為 iterator，前提是它同時定義：

- `__iter__()`：回傳 iterator 物件
- `__next__()`：回傳下一個值，耗盡時丟出 `StopIteration`

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1
```

如果 `__iter__()` 回傳 `self`，代表這個物件本身同時扮演 iterable 與 iterator。這很常見，但也表示它通常是 stateful 且一次性消耗的。

## Enumerate

Attach indexes to items (optionally with a start offset).

```python
avengers = ['hawkeye', 'iron man', 'thor', 'quicksilver']
for idx, name in enumerate(avengers, start=1):
    print(idx, name)
# 1 hawkeye
# 2 iron man
# 3 thor
# 4 quicksilver
```

`enumerate(...)` 本身回傳的不是 list，而是 iterator-like object。這代表它也會被消耗：

```python
e = enumerate(["a", "b", "c"])
print(next(e))   # (0, 'a')
print(list(e))   # [(1, 'b'), (2, 'c')]
print(list(e))   # []
```

`enumerate()` 也是很常見的 interview prompt，因為它可以順手看出你是否知道：

- index 與 value 可以同時拿
- 它回傳的是 lazy object，不是已 materialize 的 list

## Zip and Unzip

Pair multiple iterables elementwise; unzip via splat (`*`).

```python
avengers = ['hawkeye', 'iron man', 'thor', 'quicksilver']
names = ['barton', 'stark', 'odinson', 'maximoff']

pairs = list(zip(avengers, names))
# [('hawkeye','barton'), ('iron man','stark'), ('thor','odinson'), ('quicksilver','maximoff')]

# unzip
heroes, surnames = zip(*pairs)

# build dict quickly
hero2surname = dict(zip(avengers, names))
```

> Note: `zip` stops at the shortest input. Use `itertools.zip_longest` to pad.
> Also note: `zip(...)` is lazy and consumable, just like many other iterators.

面試時如果被問 `zip()`，值得主動講出的兩點通常是：

- 它會依最短 iterable 截斷
- 它常和 unpacking `*` 一起出現做 unzip

## Range and Slicing Iterables

```python
for i in range(3):         # 0,1,2
    ...

letters = list('ABCDE')
print(letters[1:4])        # ['B','C','D']
print(letters[::-1])       # reversed copy
```

## Comprehensions (create new iterables succinctly)

```python
# list
squares = [n*n for n in range(6)]                  # [0,1,4,9,16,25]
# dict
sqd = {n: n*n for n in range(4)}                   # {0:0, 1:1, 2:4, 3:9}
# set (unique)
uniq = {c.lower() for c in 'BaNaNa'}               # {'b','a','n'}
# conditional
evens = [n for n in range(10) if n % 2 == 0]
```

## Generator expressions & functions (lazy iteration)

```python
# generator expression: lazy squares, not stored in memory at once
squares_gen = (n*n for n in range(10))
print(next(squares_gen))   # 0
print(next(squares_gen))   # 1

# generator function using yield
def countdown(n):
    while n > 0:
        yield n
        n -= 1

for x in countdown(3):
    print(x)
# 3 2 1
```

如果題目從 iterator 延伸到 generator，一個簡單心智模型是：

- generator 是比較容易寫的 custom iterator
- `yield` 讓函式可以暫停並保留狀態

## Useful itertools

```python
import itertools as it

# chain: iterate through multiple iterables in sequence
for x in it.chain([1,2], ('a','b')):
    pass # [1, 2, 'a', 'b']

# islice: slice an iterator (start, stop, step)
for x in it.islice(range(100), 10, 20, 2):
    pass  # 10,12,14,16,18

# zip_longest: like zip but pads shorter iterables
for a, b in it.zip_longest('abc', [1,2], fillvalue=None):
    pass  # ('a',1), ('b',2), ('c',None)

# product/permutations/combinations
list(it.product('AB', repeat=2))        # [('A','A'), ('A','B'), ('B','A'), ('B','B')]
list(it.permutations([1,2,3], 2))       # (1,2), (1,3), (2,1), ...
list(it.combinations([1,2,3], 2))       # (1,2), (1,3), (2,3)

# groupby: consecutive-grouping by key
animals = ['ant', 'ape', 'bat', 'bear', 'beetle']
for key, group in it.groupby(sorted(animals), key=lambda s: s[0]):
    print(key, list(group))
# a ['ant','ape']
# b ['bat','bear','beetle']
```

## Map / Filter (Functional Style)

```python
nums = [1, 2, 3, 4]
# map: apply function to each element
squared = list(map(lambda x: x*x, nums))            # [1,4,9,16]
# filter: keep elements matching predicate
odds = list(filter(lambda x: x % 2, nums))          # [1,3]
```

## Iterating dictionaries safely

```python
user = {"name": "Alice", "age": 30}
for k, v in user.items():
    print(k, v)
# name Alice
# age 30

# iterate keys or values
for k in user.keys():
    ...
for v in user.values():
    ...
```

## File Objects Are Iterables Too

很多大檔案處理技巧，其實只是善用「檔案物件本身就是 iterable」這件事。

```python
with open("file.txt", "r", encoding="utf-8") as fh:
    for line in fh:
        print(line.rstrip())
```

如果你想更明確看到 iterator 行為，也可以手動呼叫 `iter()` / `next()`：

```python
with open("file.txt", "r", encoding="utf-8") as fh:
    it = iter(fh)
    print(next(it))
    print(next(it))
```

這個模式很重要，因為它提醒你：

- 不一定要一次把整個檔案讀進記憶體
- 很多「逐行處理大檔案」其實就是 iterator consumption
- `for line in fh:` 通常比手動 `readlines()` 更省記憶體

## Custom iterator class

```python
class Countdown:
    def __init__(self, start):
        self.current = start
    def __iter__(self):
        return self
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

for n in Countdown(3):
    print(n)  # 3, 2, 1
```

實務上要特別注意兩件事：

- 如果沒有在結束時 `raise StopIteration`，`for` 迴圈不會正確停止
- 如果 iterator 內部會改動狀態，同一個物件通常不能自然重跑第二次

例如：

```python
counter = Countdown(3)
list(counter)   # [3, 2, 1]
list(counter)   # []
```

這也是為什麼很多情況下，寫 generator function 會比手刻 iterator class 更簡單。

## Tips & Gotchas

- Iterators are **consumed**: once you iterate, you can’t reuse without recreating.
- `list(zip(...))` materializes results; if inputs are large, consider iterating directly.
- Prefer comprehensions or generator expressions for readable, memory-friendly pipelines.
- Use `itertools` for advanced iteration patterns instead of writing loops by hand.

## Interview Heuristics

- 問 iterable vs iterator：先講 `iter()` 和 `next()`
- 問 `enumerate()`：講 index + value 與 lazy consumption
- 問 `zip()`：講 pairwise matching、shortest input、unzip
- 問 generator：講 `yield`、state retention、lazy evaluation
