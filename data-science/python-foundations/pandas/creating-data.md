# Pandas: Creating Data

Creating DataFrames and Series is often the first step of any analysis. Pandas provides multiple methods to create data from scratch or load it from files and databases.

## Example Dataset

```python
import seaborn as sns
import pandas as pd

# Load iris dataset as example
iris = sns.load_dataset("iris").copy()

iris.head()
```

## Creating and Combining Series

- Creating a Series with a custom index

```python
s = pd.Series(['a', 'b', 'c', 'd'], index=['1', '2', '3', '4'])
```

- Creating from NumPy

```python
import numpy as np

s = pd.Series(np.array([10, 20, 30]), index=['A', 'B', 'C'])
```

## Creating DataFrames

### From Dictionary

```python
df_dict = pd.DataFrame({
    "species": ["setosa", "versicolor", "virginica"],
    "avg_length": [5.0, 5.9, 6.5]
})
```

### From List

```python
df_list = pd.DataFrame([
    ["setosa", 5.0],
    ["versicolor", 5.9]
], columns=["species", "avg_length"])
```

### From CSV File

```python
df_csv = pd.read_csv(
    "iris.csv",
    index_col=0,             # use first column as index
    parse_dates=None,        # can specify datetime columns
    nrows=5,                 # read only first 5 rows
    header=0                 # first row as column names
)
```

- Reading large CSV in chunks:

```python
chunks = []
for chunk in pd.read_csv("iris.csv", chunksize=50):
    chunks.append(chunk)
iris_chunked = pd.concat(chunks, ignore_index=True)
```

### From TXT File

```python
df_txt = pd.read_csv("iris.txt", sep="\t")
```

### From Excel File

```python
# Method 1
df_excel = pd.read_excel('iris.xlsx', sheet_name='Sheet1')

# Method 2
excel_file = pd.ExcelFile('iris.xlsx')
df_excel_sheet = excel_file.parse('Sheet1')
```

如果活頁簿有多個工作表，`ExcelFile` 很適合先檢查再逐張讀：

```python
workbook = pd.ExcelFile("fruit_tabs.xlsx")
print(workbook.sheet_names)
# ['price', 'color']

price_df = workbook.parse("price")
color_df = workbook.parse("color")
```

這個流程特別適合：

- 不確定 workbook 裡有哪些 sheet
- 不想一次把所有工作表都讀進來
- 不同工作表稍後還要 merge / compare

如果你已經知道目標工作表名稱，`read_excel(..., sheet_name=...)` 會比較短；如果你需要先探索 workbook 結構，`ExcelFile(...).sheet_names` 會更自然。

### From HTML

```python
df_htmls = pd.read_html("https://en.wikipedia.org/wiki/Iris_flower_data_set")
df = df_htmls[0]  # pick first table
```

- `pd.read_html()` reads all table elements from a webpage or HTML file.

### From Pickle

```python
df_pickle = pd.read_pickle("iris.pkl")
```

### From HDF5

```python
df_hdf = pd.read_hdf("iris.h5", key="mydata")
```

### From SQL

```python
import sqlite3
conn = sqlite3.connect("iris.db")
df_sql = pd.read_sql("SELECT * FROM iris", conn)
conn.close()
```

With SQLAlchemy:

```python
from sqlalchemy import create_engine
engine = create_engine("sqlite:///iris.db")
df_sql = pd.read_sql("SELECT * FROM iris", engine)
```

## Setting Index and Column Names

```python
df = pd.DataFrame([[5.1, 3.5], [4.9, 3.0], [4.7, 3.2]])
df.index = ["row1", "row2", "row3"]
df.columns = ["sepal_length", "sepal_width"]
```

## Key Takeaways

- DataFrames can be created from dictionaries, lists, or arrays.
- Use `read_csv`, `read_excel`, `read_html`, `read_pickle`, `read_hdf`, and `read_sql` for file/database input.
- For large CSVs, chunked reading is efficient.
- Index and column names ca
