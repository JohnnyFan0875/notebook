# Python Scripting and CLI

把 notebook 操作改成可重跑腳本需要的工具：entry point、命令列參數、設定檔、檔案讀寫、呼叫外部程式與常用小片段。

## Python Entry Point

The `if __name__ == "__main__"` construct is used to ensure that code only runs when the script is executed directly, and not when it is imported as a module.

### Basic Template

```python
def main():
    print("Hello from main!")

if __name__ == "__main__":
    main()
```

- `__name__` is a built-in variable in Python.
- When a script is run directly, `__name__` is set to `'__main__'`.
- When a script is imported as a module, `__name__` is set to the module's name.

### Why It Matters in Data Science

分析腳本常常一開始只是 notebook 旁邊的小工具，但之後很容易演變成可以被其他模組重用的資料清理、訓練或匯出程式。把執行入口包在 `main()` 裡，能讓程式同時保有：

- 可直接執行
- 可被匯入重用
- 較容易測試

#### Example with Additional Functions

```python
def greet(name):
    return f"Hello, {name}!"

def main():
    name = input("Enter your name: ")
    print(greet(name))

if __name__ == "__main__":
    main()
```

#### Example: Importing as a Module

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

#### Use Case

This pattern is useful when writing:

- Scripts that can be both run standalone and imported
- Unit tests inside the same file
- CLI (command-line interface) tools

### Recommended Pattern

```python
def main():
    ...


if __name__ == "__main__":
    main()
```

這樣做的好處是：真正的邏輯放在函式裡，可測試、可重用；入口條件只負責決定何時執行。

> **Tip**: Always use this pattern when writing Python scripts that might be reused elsewhere as modules.

## Python argparse

```python
import argparse

parser = argparse.ArgumentParser(
    description='Comprehensive argparse demo script',
    formatter_class=argparse.RawDescriptionHelpFormatter
)

# Positional argument
parser.add_argument("filename", help="input file path")

# Optional arguments with types and defaults
parser.add_argument("-p", "--port", type=int, default=5432, help="database port")
parser.add_argument("-m", "--mode", choices=["fast", "slow"], default="fast", help="execution mode")

# Boolean flags
parser.add_argument("-v", "--verbose", action="count", default=0, help="increase verbosity")
parser.add_argument("--quiet", action="store_true", help="suppress output")

# Multiple values
parser.add_argument("--names", nargs="+", help="list of names")

# Boolean option (Python 3.9+ style)
try:
    parser.add_argument("--feature", action=argparse.BooleanOptionalAction, help="enable/disable feature")
except Exception:
    parser.add_argument("--feature", action="store_true", help="enable feature")

# Required option
parser.add_argument("--config", required=True, help="config file path")

# Store constant
parser.add_argument("--debug", action="store_const", const=2, default=0, help="set debug level")

# Append values
parser.add_argument("--tag", action="append", help="add multiple tags")

# Subcommands
subparsers = parser.add_subparsers(dest="command", help="sub-commands")

# Subcommand: add
parser_add = subparsers.add_parser("add", help="add something")
parser_add.add_argument("--ip", help="target IP")

# Subcommand: remove
parser_remove = subparsers.add_parser("remove", help="remove something")
parser_remove.add_argument("--id", type=int, help="item ID")

args = parser.parse_args()

# Example usage of parsed args
print("Filename:", args.filename)
print("Port:", args.port)
print("Mode:", args.mode)
print("Verbosity level:", args.verbose)
print("Quiet mode:", args.quiet)
print("Names:", args.names)
print("Feature enabled:", args.feature)
print("Config file:", args.config)
print("Debug level:", args.debug)
print("Tags:", args.tag)

if args.command == "add":
    print("Subcommand add with IP:", args.ip)
elif args.command == "remove":
    print("Subcommand remove with ID:", args.id)
```

Run examples:

```bash
python script.py data.csv --config settings.yaml -p 3306 -m slow -vv --names Alice Bob --feature --tag alpha --tag beta add --ip 192.168.0.1
python script.py data.csv --config settings.yaml remove --id 42 --quiet
```

## Configuration Files

Configuration files allow programs to store settings and parameters separately from the source code. This improves flexibility, maintainability, and security (e.g., avoiding hardcoding secrets). Many real-world applications need configuration:

- **Content Management Systems** (WordPress, WikiMedia, Joomla): database credentials
- **Proprietary software**: license keys or registration info
- **Scientific software**: library paths (e.g., BLAS)

For small projects, you might hardcode variables, but this is discouraged — especially if the code is public.

### Common Configuration Formats

#### 1. Python File (`.py`)

Write configs as Python code in a separate file, e.g., `config.py`.

```python
# config.py
import preprocessing

mysql = {
    "host": "localhost",
    "user": "root",
    "passwd": "my secret password",
    "db": "write-math",
}

preprocessing_queue = [
    preprocessing.scale_and_center,
    preprocessing.dot_reduction,
    preprocessing.connect_lines,
]

use_anonymous = True
```

Usage:

```python
import config as cfg
connect(cfg.mysql["host"], cfg.mysql["user"], cfg.mysql["passwd"])
```

- **Pros**: simple, full Python support
- **Cons**: mixes logic/config, not user-friendly

#### 2. JSON (`.json`)

```json
{
  "mysql": {
    "host": "localhost",
    "user": "root",
    "passwd": "my secret password",
    "db": "write-math"
  },
  "other": {
    "preprocessing_queue": [
      "preprocessing.scale_and_center",
      "preprocessing.dot_reduction",
      "preprocessing.connect_lines"
    ],
    "use_anonymous": true
  }
}
```

Read in Python:

```python
import json

with open("config.json") as f:
    data = json.load(f)
```

- **Pros**: standardized, cross-language, structured
- **Cons**: no comments

#### 3. YAML (`.yaml` / `.yml`)

```yaml
mysql:
  host: localhost
  user: root
  passwd: my secret password
  db: write-math

other:
  preprocessing_queue:
    - preprocessing.scale_and_center
    - preprocessing.dot_reduction
    - preprocessing.connect_lines
  use_anonymous: yes
```

Read in Python:

```python
import yaml

with open("config.yml", "r") as f:
    cfg = yaml.safe_load(f)
```

- **Pros**: human-friendly, supports comments
- **Cons**: requires `PyYAML`

#### 4. INI (`.ini`, `.cfg`, `.conf`)

```ini
[mysql]
host=localhost
user=root
passwd=my secret password
db=write-math

[other]
preprocessing_queue=["preprocessing.scale_and_center", "preprocessing.dot_reduction", "preprocessing.connect_lines"]
use_anonymous=yes
```

Using ConfigParser:

```python
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

print(config["mysql"]["host"])
print(config.getboolean("other", "use_anonymous"))
```

- **Pros**: simple, stdlib support
- **Cons**: all values are strings by default

#### 5. XML (`.xml`)

Less common in Python, but supported.

```xml
<config>
  <mysql>
    <host>localhost</host>
    <user>root</user>
    <passwd>my secret password</passwd>
    <db>write-math</db>
  </mysql>
  <other>
    <preprocessing_queue>
      <li>preprocessing.scale_and_center</li>
      <li>preprocessing.dot_reduction</li>
      <li>preprocessing.connect_lines</li>
    </preprocessing_queue>
    <use_anonymous value="true" />
  </other>
</config>
```

Parse with BeautifulSoup:

```python
from bs4 import BeautifulSoup

with open("config.xml") as f:
    soup = BeautifulSoup(f, "xml")

print(soup.mysql.host.text)
```

- **Pros**: structured, mature ecosystem
- **Cons**: verbose, rarely used in Python configs

### File Endings & Conventions

- `.py` → Python config
- `.json` → JSON
- `.yaml` / `.yml` → YAML
- `.ini` / `.cfg` / `.conf` → INI/config files
- `~/.myapprc` → common Linux convention (RC = "run commands")

### Comparison Table

| Format | Human-Friendly | Comments | Libraries Needed             | Typical Use             |
| ------ | -------------- | -------- | ---------------------------- | ----------------------- |
| Python | ✔️             | ✔️       | None                         | Small scripts, dev-only |
| JSON   | ➖             | ❌       | None                         | Web apps, APIs          |
| YAML   | ✔️             | ✔️       | `PyYAML`                     | Configs, CI/CD          |
| INI    | ✔️             | Limited  | None                         | Legacy, simple configs  |
| XML    | ➖             | ✔️       | `BeautifulSoup`, `xml.etree` | Legacy enterprise       |

### Resources

- [Martin Thoma](https://martin-thoma.com/configuration-files-in-python/)

## Python File I/O and Modes

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

### File Modes

The `mode` parameter defines how the file is opened. Below is a summary:

| Mode | Read | Write | Create | Truncate (Clear) | Cursor Start | Cursor End |
| ---- | ---- | ----- | ------ | ---------------- | ------------ | ---------- |
| `r`  | ✔    |       |        |                  | ✔            |            |
| `r+` | ✔    | ✔     |        |                  | ✔            |            |
| `w`  |      | ✔     | ✔      | ✔                | ✔            |            |
| `w+` | ✔    | ✔     | ✔      | ✔                | ✔            |            |
| `a`  |      | ✔     | ✔      |                  |              | ✔          |
| `a+` | ✔    | ✔     | ✔      |                  |              | ✔          |

#### Key Concepts

- **Truncate**: When a file is opened in `w` or `w+` mode, the file is cleared (truncated) before writing new content. This means existing data is lost.
- **Cursor Start vs End**: The cursor (or file pointer) indicates where reading/writing begins.

  - Modes like `r`, `r+`, `w`, `w+` place the cursor at the **start** of the file.
  - Modes like `a`, `a+` place the cursor at the **end** of the file.

### Decision Tree for File Modes

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

### Examples

#### 1. Reading a File (`r`)

```python
with open("example.txt", "r") as f:
    content = f.read()
    print(content)
```

#### 2. Writing to a File (`w`) – Truncate

```python
with open("example.txt", "w") as f:
    f.write("This will overwrite existing content.")
```

#### 3. Appending to a File (`a`) – Cursor at End

```python
with open("example.txt", "a") as f:
    f.write("\nThis will be added at the end.")
```

#### 4. Read and Write (`r+`) – Cursor at Start

```python
with open("example.txt", "r+", encoding="utf-8") as f:
    data = f.read()
    f.seek(0)  # Move cursor back to the beginning
    f.write("Prepended text.\n" + data)
```

- **`seek(0)`**: Moves the cursor back to the beginning of the file, which is useful if you want to re-read after writing.

#### 5. Write and Read (`w+`) – Truncate then Write

```python
with open("example.txt", "w+", encoding="utf-8") as f:
    f.write("New content.")
    f.seek(0)           # Reset cursor to re-read from start
    print(f.read())     # will show "New content."
```

#### 6. Append and Read (`a+`) – Cursor at End

```python
with open("example.txt", "a+", encoding="utf-8") as f:
    f.write("\nAppended line.")
    f.seek(0)  # Reset cursor to beginning for reading
    print(f.read())
```

### Key Points

- Always close files, or better, use `with`.
- **Truncate** (`w`, `w+`) clears the file before writing.
- Be aware of the **cursor position**: reading moves the cursor, affecting subsequent writes.
- Use **`seek(0)`** to reset the cursor for re-reading after writing.
- `a`, `a+` always append at the end of the file.
- `r`, `r+` require the file to exist.

## Python `subprocess` Module

The `subprocess` module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes. It is the preferred way to run external commands in Python.

### 1. Basic Usage

#### Run a simple shell command

```python
import subprocess

# Executes a command and waits for it to complete
subprocess.run(["ls", "-l"])
```

#### With `shell=True` (string command)

```python
subprocess.run("ls -l", shell=True)
```

> 🔸 Use `shell=True` with caution due to security implications when using untrusted input.

### 2. Capturing Output

```python
result = subprocess.run(["echo", "hello"], capture_output=True, text=True)
print(result.stdout)  # prints 'hello\n'
```

#### With older Python versions

```python
result = subprocess.run(["echo", "hello"], stdout=subprocess.PIPE)
print(result.stdout.decode())
```

### 3. Getting the Return Code

- Exit status of the command (int)
- Check if command succeeded

```python
completed = subprocess.run(["ls", "nonexistent"], capture_output=True)
print(completed.returncode)  # Non-zero indicates failure
```

### 4. Redirecting stdout/stderr

```python
with open("output.txt", "w") as f:
    subprocess.run(["ls", "-l"], stdout=f)
```

#### Redirect stderr to stdout

```python
subprocess.run(["ls", "nonexistent"], stderr=subprocess.STDOUT)
```

### 5. Using `Popen` for Advanced Control

```python
from subprocess import Popen, PIPE

process = Popen(["grep", "foo"], stdin=PIPE, stdout=PIPE, text=True)
stdout, stderr = process.communicate(input="foo\nbar\nbaz")
print(stdout)  # prints 'foo\n'
```

### 6. Common Parameters

| Parameter         | Description                                  |
| ----------------- | -------------------------------------------- |
| `args`            | List or string of command and arguments      |
| `shell`           | Run through the shell (e.g., `/bin/sh`)      |
| `capture_output`  | Shortcut for capturing stdout and stderr     |
| `stdout`/`stderr` | Redirect output streams                      |
| `cwd`             | Set the working directory for the subprocess |
| `env`             | Pass custom environment variables            |
| `timeout`         | Time to wait before killing process          |
| `check`           | Raise error if returncode != 0               |

### 7. Raise Exception on Failure

```python
subprocess.run(["false"], check=True)  # Raises CalledProcessError
```

### 8. Security Notes

- Avoid `shell=True` when passing untrusted input.
- Prefer `list` over `str` for `args`.
- Validate all inputs when building dynamic command lines.

### 9. Use Cases

- Run shell scripts or CLI tools (e.g., `ffmpeg`, `bcftools`, `aws cli`)
- Automate data preprocessing pipelines
- Chain multiple commands using pipes (`Popen`)
- Invoke bioinformatics tools from within Python workflows

## Python Snippets

This file collects small but useful Python snippets for common tasks, including file handling, encoding, and module imports. These are practical utilities that can save time in everyday coding.

### Get Script Path

Retrieve the absolute directory path of the currently running script.

```python
import os

script_path = os.path.dirname(os.path.abspath(__file__))
print(script_path)
```

### Find Files with `glob`

Use the `glob` module for file pattern matching.

```python
import glob

# Find all files under <file_path> containing <keyword>
selected_files = glob.glob("<file_path>/**/*<keyword>*", recursive=True)
for f in selected_files:
    print(f)
```

- `*` matches any characters within a filename.
- `**` (with `recursive=True`) matches files in all subdirectories.

### Redirect stdout to UTF-8

Ensure proper encoding for standard output.

```python
import sys, codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
print("Hello, 世界")
```

This snippet forces stdout to UTF-8, so printing Unicode like "世界" won’t cause encoding errors

### Add Path for Module Imports

Add an external directory to Python’s module search path.

```python
import sys

sys.path.append("/path/to/module")

import my_module  # from /path/to/module
```

### Check Python Version

```python
import sys
print(sys.version)
print(sys.version_info)
```

### Measure Execution Time

```python
import time

start = time.time()
# your code
end = time.time()
print(f"Execution time: {end - start:.2f} seconds")
```

Or use `timeit` for micro-benchmarks:

```python
import timeit
print(timeit.timeit("sum(range(1000))", number=10000))
```

### List Installed Packages

```python
import pkg_resources

installed_packages = [d.project_name for d in pkg_resources.working_set]
print(installed_packages)
```

### Pretty Print Data Structures

```python
from pprint import pprint

data = {"name": "Alice", "age": 30, "hobbies": ["reading", "cycling"]}
pprint(data)
```

### Get Current Working Directory

```python
import os

print(os.getcwd())
```

### Environment Variables

```python
import os

print(os.getenv("HOME"))
os.environ["MY_ENV_VAR"] = "123"
```
