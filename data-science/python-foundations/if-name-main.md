# Python Entry Point

The `if __name__ == "__main__"` construct is used to ensure that code only runs when the script is executed directly, and not when it is imported as a module.

## Basic Template

```python
def main():
    print("Hello from main!")

if __name__ == "__main__":
    main()
```

- `__name__` is a built-in variable in Python.
- When a script is run directly, `__name__` is set to `'__main__'`.
- When a script is imported as a module, `__name__` is set to the module's name.

## Why It Matters in Data Science

分析腳本常常一開始只是 notebook 旁邊的小工具，但之後很容易演變成可以被其他模組重用的資料清理、訓練或匯出程式。把執行入口包在 `main()` 裡，能讓程式同時保有：

- 可直接執行
- 可被匯入重用
- 較容易測試

### Example with Additional Functions

```python
def greet(name):
    return f"Hello, {name}!"

def main():
    name = input("Enter your name: ")
    print(greet(name))

if __name__ == "__main__":
    main()
```

### Example: Importing as a Module

Assume the above script is saved as greetings.py. If another script imports it:

```python
# another_script.py
import greetings

print(greetings.greet("Alice"))
```

output

```text
Hello, Alice!
```

> Note that the main() function from greetings.py will not be executed when imported — it only runs when greetings.py is the entry point.

### Use Case

This pattern is useful when writing:

- Scripts that can be both run standalone and imported
- Unit tests inside the same file
- CLI (command-line interface) tools

## Recommended Pattern

```python
def main():
    ...


if __name__ == "__main__":
    main()
```

這樣做的好處是：真正的邏輯放在函式裡，可測試、可重用；入口條件只負責決定何時執行。

> **Tip**: Always use this pattern when writing Python scripts that might be reused elsewhere as modules.
