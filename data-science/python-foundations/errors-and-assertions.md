# Python Errors and Assertions

`try-except` 處理預期中的執行期錯誤，`assert` 檢查不該發生的內部假設；兩者用途不同，不要互相取代。

## Python Try-Except

Exception handling in Python is done with the `try-except` block. It helps you catch errors gracefully, log useful debug information, and prevent your program from crashing unexpectedly.

### Basic Structure

```python
try:
    # Code that might raise an exception
    result = 10 / 0
except ZeroDivisionError as e:
    print("Error occurred:", e)
```

### Additional Clauses

- **`try-except-else`**: The `else` block runs only if no exception occurs.
- **`try-except-finally`**: The `finally` block runs whether an exception occurred or not (commonly used for cleanup).

```python
try:
    f = open("example.txt", "r")
    data = f.read()
except FileNotFoundError:
    print("File not found!")
else:
    print("Read success.")
finally:
    if 'f' in locals():
        f.close()
```

### Exception Message

You can capture detailed exception information (type, message, call stack, etc.) using the `traceback` and `sys` modules.

```python
def exception_calling(err):
    import traceback, sys
    err_type = err.__class__.__name__    # Error class name
    info = err.args[0]                   # Error details
    detains = traceback.format_exc()     # Full traceback string

    n1, n2, n3 = sys.exc_info()                   # Current exception info
    lastCallStack = traceback.extract_tb(n3)[-1]  # Most recent call stack
    fn = lastCallStack[0]                         # Filename where error occurred
    lineNum = lastCallStack[1]                    # Line number of the error
    funcName = lastCallStack[2]                   # Function name

    errMesg = (
        f"FileName: {fn}, lineNum: {lineNum}, Fun: {funcName}, "
        f"reason: {info}, trace:\n {traceback.format_exc()}"
    )
    print(errMesg)

try:
    print(1/0)
except Exception as err:
    exception_calling(err)
```

**Output Example:**

```
FileName: <stdin>, lineNum: 22, Fun: <module>, reason: division by zero, trace:
 Traceback (most recent call last):
  File "<stdin>", line 22, in <module>
ZeroDivisionError: division by zero
```

### Key Points

- Catch **specific exceptions** first (`ValueError`, `FileNotFoundError`, etc.) before using `Exception`.
- Use `traceback` for detailed debugging.
- Always ensure proper cleanup (use `finally` or `with`).
- Avoid **swallowing exceptions** silently—log them instead.

### `raise` vs `try-except`

這兩者常一起出現，但責任不同。

`try-except` 的用途通常是：

- 在可以恢復的地方處理錯誤
- 轉成較友善的 fallback 行為
- 補上記錄、清理、重試等流程

`raise` 的用途通常是：

- 主動宣告輸入或狀態不合法
- 在不應繼續執行時中止流程
- 把錯誤往上層呼叫端交回去決定怎麼處理

例如：

```python
def average(values):
    if not isinstance(values, (list, set, tuple)):
        raise TypeError("average() expects a list, set, or tuple.")
    return sum(values) / len(values)
```

這裡 `raise` 比 `try-except` 更合適，因為：

- 問題不是執行時偶發故障
- 而是呼叫端提供了不符合 contract 的輸入

一個簡化判斷方式是：

- 如果你能在這一層合理恢復，就考慮 `try-except`
- 如果這一層不應該默默繼續，就明確 `raise`

### Raise Specific Exceptions

比起裸 `raise Exception(...)`，通常更應該選擇語意明確的 exception type。

常見例子：

- `TypeError`: 型別不符合預期
- `ValueError`: 型別對，但值不合理
- `KeyError`: 缺少必要 key
- `FileNotFoundError`: 檔案不存在

```python
def set_discount(rate):
    if not 0 <= rate <= 1:
        raise ValueError("rate must be between 0 and 1")
```

這樣上層呼叫端比較容易：

- 精準捕捉特定錯誤
- 根據錯誤類型做不同處理
- 從 traceback 更快理解問題性質

## Python `assert`

The `assert` statement in Python is used for debugging and testing assumptions in code. It is most useful when a condition should always be true if the program is correct. If the condition evaluates to `False`, Python raises an `AssertionError`.

### Basic Syntax

```python
assert condition, message
```

- **condition** → an expression that should evaluate to `True`
- **message** (optional) → error message shown if the assertion fails

### Examples

#### Simple Assertion

```python
x = 5
assert x > 0  # Passes silently since condition is True
```

#### Assertion with Message

```python
x = -1
assert x > 0, "x must be positive"
```

Output:

```
AssertionError: x must be positive
```

#### Using in Functions

```python
def divide(a, b):
    assert b != 0, "Divider cannot be zero"
    return a / b

print(divide(10, 2))  # 5.0
print(divide(10, 0))  # AssertionError
```

### When to Use

- **Debugging**: to verify assumptions during development
- **Testing**: to validate function inputs or outputs
- **Documentation**: makes expected conditions explicit in code

### A Good Mental Model

Use `assert` for programmer errors, not user errors. In other words:

- "This internal helper should only ever receive a sorted list" -> `assert`
- "The user may forget to upload a file" -> normal exception handling

### When _Not_ to Use

- **Production-critical checks**: Assertions can be globally disabled with the `-O` (optimize) flag when running Python:

  ```bash
  python -O script.py
  ```

  In optimized mode, all `assert` statements are ignored.

- **User input validation**: Use exceptions (`if` + `raise`) instead, since those should not be skipped.

### Common Pitfalls

- Using `assert` to validate external data or API input
- Putting side effects inside assertions
- Forgetting that `python -O` disables assertions

### Best Practices

- Use assertions for conditions that should **always be true** if the program is correct.
- Avoid side effects inside assertions (e.g., modifying variables).
- Provide clear error messages for easier debugging.

### Summary

- `assert` is a lightweight way to check assumptions.
- Raises `AssertionError` when condition fails.
- Good for debugging and testing, but not for handling user errors.
- Can be disabled with the `-O` flag, so do not rely on it for production-critical validation.
