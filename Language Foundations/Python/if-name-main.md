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

> **Tip**: Always use this pattern when writing Python scripts that might be reused elsewhere as modules.

```

```
