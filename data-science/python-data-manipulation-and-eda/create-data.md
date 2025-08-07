# Creating Data

## Creating and Combining Series

- Creating a Series (1D) with a Custom Index

```python
import pandas as pd

s = pd.Series(
    ['a', 'b', 'c', 'd'],
    index=['1', '2', '3', '4']
)
```

- Loading Data as a Series (or Array) Using NumPy

```python
import numpy as np

s = np.loadtxt(
    "filename.csv",
    delimiter=",",
    skiprows=1,     # Skip the first row (usually the header)
    usecols=[0, 1]  # Load only the first two columns (index 0 and 1)
)
```

## Creating DataFrames

### From Dictionary

```python
import pandas as pd

df = pd.DataFrame(
    {
        "name": ["Bella", "Charlie", "Lucy"],
        "height_cm": [56, 43, 46],
        "weight_kg": [24, 24, 24]
    },
    index=["dog1", "dog2", "dog3"]  # setting custom row labels
)
```

### From List

```python
import pandas as pd

df_list = pd.DataFrame([
    {"name": "Bella", "breed": "Labrador"},
    {"name": "Charlie", "breed": "Poodle",}
])

df_list = pd.DataFrame(
    [
        ["Bella", "Labrador"],
        ["Charlie", "Poodle"]
    ],
    index=[1, 2],
    columns=["name", "breed"]
)
```

### From CSV File

```python
import pandas as pd

df_csv = pd.read_csv(
    "dogs.csv",
    index_col="name",               # use the 'name' column as row index
    parse_dates=["date_of_birth"],  # convert 'date_of_birth' column to datetime
    nrows=5,                        # read only the first 5 rows
    header=0                        # treat the first row as column names
)
```

- Read Large CSV File

```python
import pandas as pd

chunks = []

for chunk in pd.read_csv("csv_file.csv", chunksize=1000):
    chunks.append(chunk)

data = pd.concat(chunks, ignore_index=True)
```

```python
import pandas as pd

for chunk in pd.read_csv("csv_file.csv", chunksize=1000):
    # process each chunk independently
    chunk = chunk[chunk["weight_kg"] > 10]  # filtering
    chunk.to_csv("filtered_output.csv", mode="a", index=False, header=False)
```

### From TXT File

```python
import pandas as pd

df_txt = pd.read_csv("dogs.txt", sep="\t")
```

### From Excel file

```python
import pandas as pd

# method 1
df_excel = pd.read_excel('dogs.xlsx', sheet_name='sheet_name')

# method 2
df_excel = pd.ExcelFile('dogs.xlsx')
df_excel_sheet = data.parse('sheet_name')
df_excel_sheet2 = data.parse(1)
```

### From html

```python
import pandas as pd

df_htmls = pd.read_html(<html>)
df = df_htmls[0]
```

- pd.read_html() reads all table elements from an HTML string, file, or URL.
- **Output**: a list of DataFrames, one for each HTML table found.

### From Pickle Files (`.pkl`, `.pickle`)

- Pickle file is a **Python-specific binary format** for serializing and saving objects (including pandas DataFrames). It is fast and efficient for saving/restoring Python objects. Not human-readable and not cross-language.

```python
import pandas as pd
import pickle

# from pandas dataframe
df = pd.read_pickle("dogs.pkl")

# from any python objects
with open('dogs.pkl', 'rb') as file:
	data = pickle.load(file)
```

### From HDF5 Files (`.h5`)

- HDF5 (Hierarchical Data Format) is designed for storing large, structured, binary data. Supports multiple datasets, compression, and chunking.

#### 1. High-level API using pandas + PyTables (built on h5py internally). Best when dataFrames stored using pandas.to_hdf()

```python
import pandas as pd
df = pd.read_hdf("data.h5", key="mydata")
```

- `key`: name of the dataset stored inside the HDF5 file

#### 2. Low-level API for direct access to HDF5 file structure

```python
import pandas as pd
import pickle

data = h5py.File("data.h5", "r")

for key in data["meta"]:
    print(np.array(data["meta"][key]))
```

- Require importing `h5py` and `numpy` packages
- Doesn’t assume anything is a DataFrame
- Returns **numpy.ndarray**, not pandas.DataFrame

### From SQL

#### 1. Using SQLite (built-in for small databases)

```python
import pandas as pd
import sqlite3

conn = sqlite3.connect("example.db")
df = pd.read_sql("SELECT * FROM dogs", conn)

conn.close()
```

#### 2. Using SQLAlchemy

- Recommended for most databases

```python
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("postgresql://user:password@localhost:5432/mydatabase")
df = pd.read_sql("SELECT * FROM dogs", con=engine)
```

## Setting Index and Column Names Manually

```python
import pandas as pd

df = pd.DataFrame([[56, 24], [43, 24], [46, 24]])

df.index = ["dog1", "dog2", "dog3"]
df.columns = ["height_cm", "weight_kg"]
```
