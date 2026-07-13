# Python Functions

This document summarizes key concepts and techniques related to Python functions, from basics to advanced patterns like decorators and context managers.

## Function Basics

### Names and Defaults

```python
def greet(name, message="Hello"):
    return f"{message}, {name}!"

print(greet.__name__)     # 'greet'
print(greet.__defaults__) # ('Hello',)
```

預設值最有用的情境是：

- 某個參數在大多數呼叫中都一樣
- 你想讓常見用法更短
- 你希望保留彈性，但不想逼每個呼叫端都傳同一個值

```python
def round_price(value, digits=2):
    return round(value, digits)
```

這裡的心智模型不是「少打一個參數」而已，而是 API 在明確表達它的預設使用情境。

實務上，default arguments 也會迫使你思考：

- 哪些參數是核心、必填的
- 哪些參數只是常見但可調的設定

### Flexible Arguments

```python
def demo_args(*args):
    print(args)

demo_args('a', 'b', 'c')         # Output: ('a', 'b', 'c')
```

```python
def demo_kwargs(**kwargs):
    print(kwargs)

demo_kwargs(a=[0, 1], b='test')  # Output: {'a': [0, 1], 'b': 'test'}
```

### `*args` and `**kwargs` Mental Model

- `*args` 把額外的位置參數收成 tuple
- `**kwargs` 把額外的關鍵字參數收成 dict

如果這題是 interview prompt，最好順手把「收進來之後變成什麼型別」一起說出來，因為這通常正是面試官想確認的點：

- `*args -> tuple`
- `**kwargs -> dict`

```python
def average(*args):
    return sum(args) / len(args)

print(average(15, 29, 4, 13, 11, 8))  # 13.33
```

```python
def average_kwargs(**kwargs):
    return sum(kwargs.values()) / len(kwargs)

print(average_kwargs(a=15, b=29, c=4))  # 16.0
```

這種介面適合：

- 參數個數不固定
- 要當 wrapper / pass-through function
- 要建立較彈性的 helper API

但它也會降低明確性，所以如果參數結構其實固定，通常還是顯式參數比較好讀。

### Unpacking at Call Time

`*` 和 `**` 不只出現在函式定義，也很常出現在呼叫端做 unpacking。

```python
values = [15, 29, 4, 13, 11, 8]
print(average(*values))
```

```python
payload = {"a": 15, "b": 29, "c": 4}
print(average_kwargs(**payload))
```

這個模式在下面幾種情況特別常見：

- 把 list / tuple 展開成位置參數
- 把 dict 展開成關鍵字參數
- 將一層 wrapper 收到的 `*args, **kwargs` 原封不動往下傳

也可以合併多段資料一起展開：

```python
print(average(*[15, 29], *[4, 13], *[11, 8]))
print(average_kwargs(**{"a": 15, "b": 29}, **{"c": 4, "d": 13}))
```

看到這類寫法時，可以把它想成「先展開，再像普通函式呼叫那樣匹配參數」。

### Interview Fast Answer for Flexible Arguments

如果被問「如何傳可變數量參數給函式」，最穩的回答順序通常是：

1. `*args` 收可變數量的位置參數
2. `**kwargs` 收可變數量的關鍵字參數
3. 呼叫端也可以用 `*` / `**` 做 unpacking

再補一句就很完整：

- 固定結構的函式還是應該優先使用顯式參數，因為可讀性更好

### Return Values

```python
def square(value):
    new_value = value ** 2
    return new_value

print(square(4))  # 16
```

- `return` 會把結果交回呼叫端。
- 如果函式沒有明確 `return`，Python 會回傳 `None`。

面試中這也常和 multiple return values 一起被問。高訊號回答通常是：

- Python 看起來像回傳多個值
- 但底層其實是回傳一個 tuple，再由呼叫端 unpack

### Multiple Return Values

Python 常用 tuple 來表達多重回傳值。

```python
def raise_both(value1, value2):
    return value1 ** 2, value2 ** 2

a, b = raise_both(2, 3)
print(a, b)  # 4 9
```

- 實際上回傳的是 tuple。
- 呼叫端通常會直接 unpack，讓程式更好讀。

### Scope Mental Model

函式相關錯誤很多不是邏輯錯，而是 scope 沒想清楚。

```python
x = 10

def show_local(value):
    x = value ** 2
    return x

print(show_local(3))  # 9
print(x)              # 10
```

- function 裡建立的名稱，預設只活在 local scope。
- function 外的名稱屬於 global scope。
- 此外還有 built-in scope，例如 `len`、`sum`。

可以用簡化版 LEGB 心智模型來記：

- `L`: local
- `E`: enclosing
- `G`: global
- `B`: built-in

### `global` vs `nonlocal`

如果只是「讀取」外層變數，通常不用特別宣告；真正容易混淆的是「重新賦值」時 Python 會把名稱視為新的 local variable。

```python
x = 7

def change_local_only():
    x = 42
    return x

print(change_local_only())  # 42
print(x)                    # 7
```

如果你真的要修改 module scope 的名稱，才使用 `global`：

```python
x = 7

def change_global():
    global x
    x = 42

change_global()
print(x)  # 42
```

如果你要修改的是外層函式中的名稱，而不是全域名稱，就用 `nonlocal`：

```python
def outer():
    x = 10

    def inner():
        nonlocal x
        x = 200

    inner()
    return x

print(outer())  # 200
```

- `global` 連到 module scope。
- `nonlocal` 連到最近一層 enclosing function scope。
- 實務上優先避免共享可變狀態，只有在 closure 或狀態型 helper 很自然時才考慮 `nonlocal`。

### Closures Depend on Scope

closure 本質上就是內部函式記住外層作用域中的值。

```python
def raise_val(n):
    def inner(x):
        return x ** n
    return inner

square = raise_val(2)
print(square(5))  # 25
```

- `inner()` 離開 `raise_val()` 後仍能記住 `n`。
- 這也是為什麼 decorators、factory functions 和 partial-like patterns 常依賴 closure。

### Closures Keep Referenced Values Alive

closure 不只是語法技巧，它真的會把需要的外層值附著在回傳函式上。

```python
def make_printer(value):
    def printer():
        print(value)
    return printer

show = make_printer(25)
show()  # 25
```

即使原本建立 `value` 的外層函式早就結束，`show()` 還是能印出 `25`，因為 closure 已經保存了它需要的參照。

如果想觀察 Python 怎麼保存這些值，可以看 `__closure__`：

```python
def parent(arg_1, arg_2):
    value = 22
    my_dict = {"chocolate": "yummy"}

    def child():
        return arg_1 + arg_2, value, my_dict["chocolate"]

    return child

fn = parent(3, 4)
print([cell.cell_contents for cell in fn.__closure__])
# [3, 4, 22, {'chocolate': 'yummy'}]
```

- `__closure__` 讓你看到 closure 捕捉到哪些值。
- 平常不需要依賴這個屬性寫業務邏輯，但它很適合拿來理解 decorators、factory functions 與 late binding 問題。

### Lambda Functions

Anonymous functions defined with `lambda`.

```python
square = lambda x: x ** 2
print(square(4))  # 16
```

## Higher-order Functions

### map

```python
lists = ['a','b','c']
result = list(map(lambda item: item + '!!!', lists))
# ['a!!!','b!!!','c!!!']
```

### filter

```python
lists = ['a','ab','abc']
result = list(filter(lambda x: len(x) > 1, lists))
# ['ab','abc']
```

### reduce

```python
from functools import reduce

lists = ['a','b','c']
result = reduce(lambda item1, item2: item1 + item2, lists)
# 'abc'
```

### sorted

```python
numbers = [3,1,4,1,5,9,2,6,5,3,5]
numbers_sort = sorted(numbers, key=lambda x: -x) # Sorts the list in descending order

li = [(0,3),(1,2),(3,0)]
li_sort_0 = sorted(li)  # [(0,3), (1,2), (3,0)]
li_sort_1 = sorted(li, key=lambda e: e[1]) # [(3,0), (1,2), (0,3)]
```

Sort by index:

```python
s = [2,3,1]
s_index = sorted(range(len(s)), key=lambda k: s[k])
# [2,0,1]
```

## Docstrings and Introspection

### Docstrings

```python
def add(a, b):
    """Return the sum of a and b."""
    return a + b

print(add.__doc__) # "Return the sum of a and b."
```

Use the `inspect` module

```python
import inspect
print(inspect.getdoc(add))  # "Return the sum of a and b."
```

- \_\_doc\_\_ → gets the raw docstring as written.
- inspect.getdoc() → cleans indentation and strips whitespace (better for multi-line docstrings).

## Decorators

### Simple Decorator

```python
def double_args(func):
    def wrapper(a, b):
        return func(a * 2, b * 2)
    return wrapper

@double_args
def multiply(a, b):
    return a * b

print(multiply(1, 5))  # 20
```

### Decorator with Arguments

```python
def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def say_hello():
    print("Hello!")

say_hello()
```

- @repeat(3) → calls repeat(3).
- repeat(3) returns decorator with times = 3 stored in its closure.
- decorator(say_hello) runs, and returns wrapper. Now say_hello = wrapper.
- Calling say_hello() actually calls wrapper().
- Since say_hello() has no arguments → \*args and \*\*kwargs are empty.
- Inside wrapper: for \_ in range(times): → times = 3 → loop runs 3 times.
- Each iteration calls func(\*args, \*\*kwargs), where func = the original say_hello.
- The original say_hello executes → prints "Hello!".
- Loop runs 3 times → "Hello!" is printed 3 times.

### Preserving Metadata with `wraps`

`functools.wraps` is a decorator that preserves a function’s metadata (name, docstring, annotations, etc.) when it is wrapped by another function, such as in custom decorators.

```python
from functools import wraps
import time

def timer(func):
    """A decorator that prints how long a function took to run."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        t_start = time.time()
        result = func(*args, **kwargs)
        t_total = time.time() - t_start
        print(f"{func.__name__} took {t_total:.2f}s")
        return result
    return wrapper

@timer
def sleep_n_seconds(n=5):
    """Pause processing for n seconds."""
    time.sleep(n)

sleep_n_seconds(2)
```

### Memoization Example

```python
def memoize(func):
    cache = {}
    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    wrapper.cache = cache
    return wrapper

@memoize
def slow_function(a, b):
    import time
    time.sleep(2)
    return a + b

slow_function(3, 4)
print(slow_function.cache)
# {((3, 4), ()): 7}

slow_function(a=3, b=4)
print(slow_function.cache)
# {
#   ((3, 4), ()): 7,
#   ((), (('a', 3), ('b', 4))): 7
# }
```

- memoize is called one time when Python executes the def slow_function statement. so `cache` would store the information at each run

### Type Checking with Decorators

```python
def returns(return_type):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            assert isinstance(result, return_type), f"Expected {return_type}, got {type(result)}"
            return result
        return wrapper
    return decorator

@returns(dict)
def foo(value):
    return value
```

## Context Managers

Create custom context managers using `@contextlib.contextmanager`.

```python
import contextlib, os

@contextlib.contextmanager
def in_dir(path):
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)

with in_dir('/tmp'):
    print(os.listdir())
```

## Additional Useful Function Techniques

### Function Annotations (Type Hints)

```python
def greet(name: str, age: int) -> str:
    return f"Hello {name}, you are {age} years old."
```

### Partial Functions

```python
from functools import partial

def power(base, exp):
    return base ** exp

square = partial(power, exp=2)
print(square(5))  # 25
```

### Closures

```python
def make_multiplier(n):
    def multiplier(x):
        return x * n
    return multiplier

double = make_multiplier(2)
print(double(10))  # 20
```

## Summary

- **Basics**: args, kwargs, defaults, lambdas
- **Functional tools**: map, filter, reduce, sorted
- **Docstrings**: `__doc__`, `inspect`
- **Decorators**: simple, parameterized, memoization, type checking
- **Context managers**: using `@contextlib.contextmanager`
- **Advanced patterns**: closures, partial functions, annotations

## Common Interview Traps

- `*args` 不是 list，而是 tuple
- `**kwargs` 不是特別語法糖物件，而是普通 dict
- `return a, b` 本質上是回傳 tuple
- mutable default argument 是另一個經典坑，但它和 `*args/**kwargs` 是不同問題
