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
