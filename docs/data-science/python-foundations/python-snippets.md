# Python Snippets

This file collects small but useful Python snippets for common tasks, including file handling, encoding, and module imports. These are practical utilities that can save time in everyday coding.

## Get Script Path

Retrieve the absolute directory path of the currently running script.

```python
import os

script_path = os.path.dirname(os.path.abspath(__file__))
print(script_path)
```

## Find Files with `glob`

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

## Redirect stdout to UTF-8

Ensure proper encoding for standard output.

```python
import sys, codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
print("Hello, 世界")
```

This snippet forces stdout to UTF-8, so printing Unicode like "世界" won’t cause encoding errors

## Add Path for Module Imports

Add an external directory to Python’s module search path.

```python
import sys

sys.path.append("/path/to/module")

import my_module  # from /path/to/module
```

## Check Python Version

```python
import sys
print(sys.version)
print(sys.version_info)
```

## Measure Execution Time

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

## List Installed Packages

```python
import pkg_resources

installed_packages = [d.project_name for d in pkg_resources.working_set]
print(installed_packages)
```

## Pretty Print Data Structures

```python
from pprint import pprint

data = {"name": "Alice", "age": 30, "hobbies": ["reading", "cycling"]}
pprint(data)
```

## Get Current Working Directory

```python
import os

print(os.getcwd())
```

## Environment Variables

```python
import os

print(os.getenv("HOME"))
os.environ["MY_ENV_VAR"] = "123"
```
