# Python Try-Except

Exception handling in Python is done with the `try-except` block. It helps you catch errors gracefully, log useful debug information, and prevent your program from crashing unexpectedly.

## Basic Structure

```python
try:
    # Code that might raise an exception
    result = 10 / 0
except ZeroDivisionError as e:
    print("Error occurred:", e)
```

## Additional Clauses

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

## Exception Message

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

## Key Points

- Catch **specific exceptions** first (`ValueError`, `FileNotFoundError`, etc.) before using `Exception`.
- Use `traceback` for detailed debugging.
- Always ensure proper cleanup (use `finally` or `with`).
- Avoid **swallowing exceptions** silently—log them instead.
