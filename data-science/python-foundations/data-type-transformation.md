# Data Type Transformation

Transforming data between different formats is a common task in Python programming. This document covers some of the most useful conversions, starting with JSON and dictionaries.

## JSON ↔ Dictionary

Python provides the `json` module for working with JSON data.

### Dictionary → JSON file

```python
import json

sample_dict = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

with open("sample.json", "w") as f_output:
    json.dump(sample_dict, f_output, indent=4)
```

### JSON file → Dictionary

```python
import json

with open("sample.json", "r") as j_sample:
    d_sample = json.loads(j_sample.read())

print(d_sample["name"])  # Alice
```

## Dictionary ↔ JSON string

Sometimes you want to work directly with JSON strings rather than files.

### Dictionary → JSON string

```python
import json

sample_dict = {"fruit": "apple", "quantity": 10}
json_str = json.dumps(sample_dict, indent=2)
print(json_str)
```

### JSON string → Dictionary

```python
import json

json_str = '{"fruit": "apple", "quantity": 10}'
parsed_dict = json.loads(json_str)
print(parsed_dict["fruit"])  # apple
```

## List ↔ Tuple

### List → Tuple

```python
numbers_list = [1, 2, 3]
numbers_tuple = tuple(numbers_list)
```

### Tuple → List

```python
numbers_tuple = (1, 2, 3)
numbers_list = list(numbers_tuple)
```

## String ↔ Datetime

Use the `datetime` module for converting between strings and datetime objects.

### String → Datetime

```python
from datetime import datetime

date_str = "2024-03-15 14:30:00"
dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
print(dt.year)  # 2024
```

### Datetime → String

```python
from datetime import datetime

dt = datetime.now()
formatted_str = dt.strftime("%Y-%m-%d %H:%M:%S")
print(formatted_str)
```

## CSV ↔ Dictionary

Use the `csv` module for structured tabular data.

### CSV file → List of dictionaries

```python
import csv

with open("sample.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    data = [row for row in reader]

print(data)
```

### Dictionary list → CSV file

```python
import csv

data = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25}
]

with open("output.csv", "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerows(data)
```

## Array ↔ DataFrame

### Array → DataFrame

```python
import pandas as pd

data = [
    [1, "Alice", 30],
    [2, "Bob", 25],
]

df = pd.DataFrame(data, columns=["ID", "Name", "Age"])
```

### DataFrame → Array

```python
import pandas as pd
import seaborn as sns

iris = sns.load_dataset("iris")
numeric_df = iris.select_dtypes(include='number')
array = numeric_df.to_numpy()
```

## DataFrame ↔ Other Formats

### DataFrame → Dictionary

```python
import pandas as pd

iris = pd.DataFrame({
    "col": [1, 2, 3]
})

df_dict = iris.to_dict()
print(df_dict)
```

- `.to_dict()` converts the DataFrame into a dictionary.
- Orientations can be specified: `dict`, `list`, `series`, `records`, `split`.

### DataFrame Series → List

```python
col_list = iris['col'].tolist()
print(col_list)
```

- `.tolist()` converts a Series to a Python list.
- Useful when exporting a column to a standard Python structure.

### DataFrame → CSV Output

```python
iris.to_csv("output.csv")
```

- `.to_csv()` exports the DataFrame to a CSV file.
- Options include `index=False`, custom separators, encoding, etc.

## Summary

- **JSON ↔ dict**: `json.dump`, `json.load`, `json.dumps`, `json.loads`
- **List ↔ tuple**: `list()`, `tuple()`
- **String ↔ datetime**: `strftime`, `strptime`
- **CSV ↔ dict/list**: `csv.DictReader`, `csv.DictWriter`
- **Array ↔ DataFrame**: `pd.DataFrame`, `.to_numpy()`
- **DataFrame ↔ dict/list**: `.to_dict()`, `.tolist()`
- **DataFrame → CSV**: `.to_csv()`
