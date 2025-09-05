# Python Iterators

> Practical patterns for `iter`, `next`, `enumerate`, `zip`, generator functions, `itertools`, and common comprehension idioms.

## Core Ideas

- **Iterable**: an object you can loop over (e.g., `list`, `tuple`, `dict`, `set`, `str`, `range`). Gives an **iterator** when passed to `iter()`.
- **Iterator**: maintains state during iteration and returns the next value when you call `next()`.

```python
nums = [10, 20, 30]
it = iter(nums)      # create an iterator from the iterable
print(next(it))      # 10
print(next(it))      # 20
print(next(it))      # 30
# next(it) now raises StopIteration
```

## enumerate

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

## zip and unzip

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

## range and slicing iterables

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

## map / filter (functional style)

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

## Tips & Gotchas

- Iterators are **consumed**: once you iterate, you can’t reuse without recreating.
- `list(zip(...))` materializes results; if inputs are large, consider iterating directly.
- Prefer comprehensions or generator expressions for readable, memory-friendly pipelines.
- Use `itertools` for advanced iteration patterns instead of writing loops by hand.
