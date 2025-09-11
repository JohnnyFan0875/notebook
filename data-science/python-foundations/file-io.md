# Python File I/O and Modes

Working with files is a fundamental skill in Python. The built-in `open()` function is used to open files in different modes for reading, writing, or appending.

```python
file = open("filename.txt", mode="r")
# do something with file
file.close()
```

It is recommended to use `with` to handle files, as it ensures proper closing:

```python
with open("filename.txt", "r") as f:
    data = f.read()
```

## File Modes

The `mode` parameter defines how the file is opened. Below is a summary:

| Mode | Read | Write | Create | Truncate (Clear) | Cursor Start | Cursor End |
| ---- | ---- | ----- | ------ | ---------------- | ------------ | ---------- |
| `r`  | ✔    |       |        |                  | ✔            |            |
| `r+` | ✔    | ✔     |        |                  | ✔            |            |
| `w`  |      | ✔     | ✔      | ✔                | ✔            |            |
| `w+` | ✔    | ✔     | ✔      | ✔                | ✔            |            |
| `a`  |      | ✔     | ✔      |                  |              | ✔          |
| `a+` | ✔    | ✔     | ✔      |                  |              | ✔          |

### Key Concepts

- **Truncate**: When a file is opened in `w` or `w+` mode, the file is cleared (truncated) before writing new content. This means existing data is lost.
- **Cursor Start vs End**: The cursor (or file pointer) indicates where reading/writing begins.

  - Modes like `r`, `r+`, `w`, `w+` place the cursor at the **start** of the file.
  - Modes like `a`, `a+` place the cursor at the **end** of the file.

## Decision Tree for File Modes

The decision process for choosing the right mode can be represented as:

- **Reading only** → `r`
- **Writing only**

  - Truncate file? → `w`
  - Append to end? → `a`

- **Reading and writing**

  - Truncate file? → `w+`
  - Do not truncate:

    - Start at beginning → `r+`
    - Start at end → `a+`

## Examples

### 1. Reading a File (`r`)

```python
with open("example.txt", "r") as f:
    content = f.read()
    print(content)
```

### 2. Writing to a File (`w`) – Truncate

```python
with open("example.txt", "w") as f:
    f.write("This will overwrite existing content.")
```

### 3. Appending to a File (`a`) – Cursor at End

```python
with open("example.txt", "a") as f:
    f.write("\nThis will be added at the end.")
```

### 4. Read and Write (`r+`) – Cursor at Start

```python
with open("example.txt", "r+", encoding="utf-8") as f:
    data = f.read()
    f.seek(0)  # Move cursor back to the beginning
    f.write("Prepended text.\n" + data)
```

- **`seek(0)`**: Moves the cursor back to the beginning of the file, which is useful if you want to re-read after writing.

### 5. Write and Read (`w+`) – Truncate then Write

```python
with open("example.txt", "w+", encoding="utf-8") as f:
    f.write("New content.")
    f.seek(0)           # Reset cursor to re-read from start
    print(f.read())     # will show "New content."
```

### 6. Append and Read (`a+`) – Cursor at End

```python
with open("example.txt", "a+", encoding="utf-8") as f:
    f.write("\nAppended line.")
    f.seek(0)  # Reset cursor to beginning for reading
    print(f.read())
```

## Key Points

- Always close files, or better, use `with`.
- **Truncate** (`w`, `w+`) clears the file before writing.
- Be aware of the **cursor position**: reading moves the cursor, affecting subsequent writes.
- Use **`seek(0)`** to reset the cursor for re-reading after writing.
- `a`, `a+` always append at the end of the file.
- `r`, `r+` require the file to exist.
