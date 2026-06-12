# Python `assert`

The `assert` statement in Python is used for **debugging and testing assumptions** in code. It helps ensure that a condition holds true at runtime. If the condition evaluates to `False`, an `AssertionError` is raised.

## Basic Syntax

```python
assert condition, message
```

- **condition** → an expression that should evaluate to `True`
- **message** (optional) → error message shown if the assertion fails

## Examples

### Simple Assertion

```python
x = 5
assert x > 0  # Passes silently since condition is True
```

### Assertion with Message

```python
x = -1
assert x > 0, "x must be positive"
```

Output:

```
AssertionError: x must be positive
```

### Using in Functions

```python
def divide(a, b):
    assert b != 0, "Divider cannot be zero"
    return a / b

print(divide(10, 2))  # 5.0
print(divide(10, 0))  # AssertionError
```

## When to Use

- **Debugging**: to verify assumptions during development
- **Testing**: to validate function inputs or outputs
- **Documentation**: makes expected conditions explicit in code

## When _Not_ to Use

- **Production-critical checks**: Assertions can be globally disabled with the `-O` (optimize) flag when running Python:

  ```bash
  python -O script.py
  ```

  In optimized mode, all `assert` statements are ignored.

- **User input validation**: Use exceptions (`if` + `raise`) instead, since those should not be skipped.

## Best Practices

- Use assertions for conditions that should **always be true** if the program is correct.
- Avoid side effects inside assertions (e.g., modifying variables).
- Provide clear error messages for easier debugging.

## Summary

- `assert` is a lightweight way to check assumptions.
- Raises `AssertionError` when condition fails.
- Good for debugging and testing, but not for handling user errors.
- Can be disabled with the `-O` flag — don’t rely on it for product
