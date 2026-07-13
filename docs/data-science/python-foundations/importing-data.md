# Python: Importing Data from Common File Formats

Importing data in Python is not one skill but a small family of patterns. The main question is usually:

- Is this plain text or binary?
- Is the structure tabular or nested?
- Do I want a NumPy array, a pandas DataFrame, or a library-specific object?

For most data science workflows:

- use NumPy for numeric arrays
- use pandas for tabular data with labels
- use format-specific libraries when the file is not a plain text table

## Data Sources You Meet Often

A practical mental split:

- flat files: `.txt`, `.csv`, delimiter-separated text
- web-hosted files: datasets accessed by URL
- serialized Python objects: pickle
- statistical data formats: SAS, Stata
- scientific binary formats: HDF5, MATLAB `.mat`
- relational databases: use SQL tools rather than treating them like ordinary files

This note focuses on the file side. Database access is already covered separately in `database-access-sqlalchemy.md`.

## Flat Files

Flat files are still the default exchange format in a lot of data work.

Examples:

- `.csv`
- tab-delimited `.txt`
- custom delimiter text files

They are popular because they are:

- portable
- easy to inspect
- easy to move across tools

But they also have common problems:

- header rows
- mixed types
- comments
- missing values
- inconsistent delimiters

## Importing Files from the Web

Sometimes the file is still a CSV or text file, but it lives behind a URL instead of on disk.

Two common patterns:

- download it to a local file first
- fetch it directly into memory

### Download a Remote File with `urlretrieve()`

```python
from urllib.request import urlretrieve

url = "http://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv"
urlretrieve(url, "winequality-white.csv")
```

This is useful when:

- you want a persistent local copy
- downstream code expects a filename
- the dataset is reused multiple times

### Open a URL Like a File with `urlopen()`

```python
from urllib.request import Request, urlopen

url = "https://www.example.com/data.csv"
request = Request(url)
response = urlopen(request)
raw = response.read()
```

- `urlopen()` accepts URLs instead of filenames
- `.read()` gives the response body as bytes
- this is a lower-level pattern than `requests`, but still useful to know

If your goal is general HTTP work rather than simple download, `requests` is usually more ergonomic.

## HTTP Requests for Import Work

When the data source is on the web, importing often starts as an HTTP `GET` request.

```python
import requests

url = "https://www.example.com/data"
r = requests.get(url)
```

From there, what you do next depends on the response format:

- text / HTML -> use `r.text`
- JSON -> use `r.json()`
- binary content -> use `r.content`

This is where importing data starts to overlap with API usage. For fuller HTTP patterns, see `api-http.md`.

## Importing Numeric Flat Files with NumPy

If the file is mostly numeric and you want an array, `np.loadtxt()` is a simple starting point.

```python
import numpy as np

filename = "mnist.csv"
data = np.loadtxt(filename, delimiter=",")
```

This is best when:

- the file is regular
- most values are numeric
- you do not need column labels

### Customizing `np.loadtxt()`

```python
data = np.loadtxt(
    "MNIST_header.txt",
    delimiter=",",
    skiprows=1,
    usecols=[0, 2],
)
```

Useful arguments:

- `delimiter=`
- `skiprows=`
- `usecols=`
- `dtype=`

If the data contains strings:

```python
data = np.loadtxt("data.csv", delimiter=",", dtype=str)
```

## When `np.loadtxt()` Is Too Strict

`np.loadtxt()` assumes the file is clean and regular. It becomes awkward when:

- rows have missing values
- comments appear in the file
- types vary by column

In those cases, pandas is usually the better default.

## Importing Tabular Data with pandas

For messy or labeled tables, `pd.read_csv()` is the workhorse.

```python
import pandas as pd

df = pd.read_csv("winequality-red.csv")
```

Why pandas is often the default:

- it keeps column names
- it handles mixed dtypes better
- it integrates directly with analysis workflows

After the file loads, the next questions are usually:

- what does each row represent?
- which columns are numeric, categorical, or dates?
- are there obvious missing values or malformed fields?

That means importing is usually followed immediately by a quick inspection pass:

```python
import pandas as pd

df = pd.read_csv("sales.csv")

print(df.head())
print(df.info())
print(df.describe(include="all"))
```

This first pass is important because a successful `read_csv()` call does not guarantee the table is analysis-ready. Columns may still have the wrong dtype, date fields may still be strings, and identifiers may be mixed with measures.

If needed, convert back to a NumPy array:

```python
data_array = df.to_numpy()
```

## Useful `read_csv()` Options

When the file is not perfectly clean, these options matter a lot:

```python
df = pd.read_csv(
    "data.csv",
    sep=",",
    header=0,
    skiprows=2,
    nrows=1000,
)
```

Common options:

- `sep=` for delimiter
- `header=` for which row contains column names
- `skiprows=` to ignore leading junk
- `nrows=` to sample part of a file

If you only need part of a very large file:

```python
df_iter = pd.read_csv("large.csv", chunksize=10000)

for chunk in df_iter:
    ...
```

This pattern avoids loading the whole file into memory at once.

## Loading Many Similar CSV Files

如果一個資料集被拆成多個 CSV 檔，常見做法是先找出檔名，再批次讀入。

```python
import glob
import pandas as pd

csv_files = glob.glob("*.csv")
all_dfs = [pd.read_csv(path) for path in csv_files]
```

這個 pattern 適合：

- 每個檔案 schema 類似
- 想先各自清理，再決定是否 `concat`
- 想避免手動把每個檔名寫死

如果要合併成單一表格：

```python
combined = pd.concat(all_dfs, ignore_index=True)
```

Key point: list comprehension 只是把「重複讀很多檔」壓縮成更短的寫法；真正要先確認的，仍然是這些檔案欄位是否一致。

## Importing JSON from a Local File

JSON is common when data is nested rather than purely tabular.

```python
import json

with open("snakes.json", "r", encoding="utf-8") as json_file:
    json_data = json.load(json_file)
```

The imported object is usually a Python:

- `dict`
- `list`
- nested combination of both

A quick way to inspect it:

```python
for key, value in json_data.items():
    print(key, value)
```

This is often the fastest first step before deciding whether the data should stay nested or be normalized into a DataFrame.

## Line-Delimited JSON and Event Streams

Some datasets are not one big JSON object. Instead, they are newline-delimited JSON records, often called:

- NDJSON
- JSON Lines
- one-JSON-object-per-line event logs

This is common in logs, API exports, and social media archives.

```python
import json

records = []

with open("all_tweets.json", "r", encoding="utf-8") as fh:
    for line in fh:
        line = line.strip()
        if not line:
            continue
        records.append(json.loads(line))
```

Key point: if the file is really NDJSON, think "iterate over records", not "load the whole file as one nested object".

## Flatten Only the Nested Fields You Actually Need

Nested JSON often contains far more structure than you want in the first analysis pass.

A practical pattern is:

1. identify the few nested keys that matter
2. copy them into top-level fields
3. then build a DataFrame

```python
tweet_obj["text"] = tweet_obj["text"]

if "extended_tweet" in tweet_obj:
    tweet_obj["extended_tweet-full_text"] = (
        tweet_obj["extended_tweet"]["full_text"]
    )
```

This keeps the first DataFrame usable without pretending the whole JSON document is flat.

Social-media-style payloads are a good example:

- `tweet["text"]`
- `tweet["extended_tweet"]["full_text"]`
- `tweet["user"]["description"]`
- `tweet["user"]["location"]`
- `tweet["quoted_status"]["extended_tweet"]["full_text"]`

The lesson is broader than Twitter: nested structures often depend on record type, so some paths exist only for certain rows.

## Convert a List of Parsed Records into a DataFrame

After extracting the fields you care about, convert the record list into tabular form:

```python
import pandas as pd

tweets = pd.DataFrame(records)
```

This is usually the handoff point where semi-structured import becomes ordinary pandas cleaning.

## JSON Can Encode Different Levels of Geographic Precision

Another common nested JSON pattern is location data with multiple precision levels.

For example, one record may contain:

- a free-text user location
- a `place` object with a bounding box
- a `coordinates` object with an exact point

These are not interchangeable.

- free-text location is user-entered and messy
- a bounding box gives an area
- coordinates give a point

If you later map or aggregate these records, preserve that distinction instead of collapsing everything into one generic "location" column.

Also remember that geolocation fields are often missing for most records. In social-media-style datasets, the rows with explicit coordinates can be a small and highly selective subset of all observations.

Key point: geographic JSON is often both nested and biased. Treat "has location" as a sampling filter, not just a convenience field.

## Importing JSON from an API

If the server already returns JSON, `requests` can parse it directly.

```python
import requests

url = "http://www.omdbapi.com/?t=hackers"
r = requests.get(url)
json_data = r.json()

for key, value in json_data.items():
    print(key, value)
```

Useful mental model:

- `r.text` gives raw text
- `r.json()` decodes JSON into Python objects

If you are manually reading query strings like `?t=hackers`, that is a sign you may want to switch to `params=` in real code for better readability and safer encoding.

## Importing HTML for Quick Parsing

Sometimes the source is not a downloadable file or JSON API, but an HTML page you need to inspect or parse.

```python
import requests
from bs4 import BeautifulSoup

url = "https://www.crummy.com/software/BeautifulSoup/"
r = requests.get(url)
html_doc = r.text
soup = BeautifulSoup(html_doc)
```

This gives you parsed HTML you can inspect or query.

For example:

```python
print(soup.prettify())
```

This is useful for:

- exploratory inspection of page structure
- quick-turnaround scraping
- confirming whether the data is embedded in HTML or loaded later by JavaScript

For a fuller note on selectors, extraction, and crawlers, see `web-scraping.md`.

## Pickle Files

Pickle stores serialized Python objects.

```python
import pickle

with open("pickled_fruit.pkl", "rb") as file:
    data = pickle.load(file)
```

Use pickle when:

- the producer and consumer are both Python
- you want to preserve Python object structure

Be careful:

- pickle is Python-specific
- pickle is not a good interchange format across languages
- never unpickle untrusted data

## SAS Files

SAS data files often appear in enterprise or public-sector datasets.

```python
import pandas as pd
from sas7bdat import SAS7BDAT

with SAS7BDAT("urbanpop.sas7bdat") as file:
    df_sas = file.to_data_frame()
```

This gives you a pandas DataFrame, which is usually the format you want downstream.

## Stata Files

Pandas supports Stata directly.

```python
import pandas as pd

df = pd.read_stata("urbanpop.dta")
```

This is one of the cases where pandas hides the format complexity nicely.

## HDF5 Files

HDF5 is common in scientific computing because it can store large structured binary datasets efficiently.

```python
import h5py

filename = "H-H1_LOSC_4_V1-815411200-4096.hdf5"
file = h5py.File(filename, "r")
```

A useful mental model:

- HDF5 behaves more like a hierarchy of groups and datasets
- it is not just "read table into DataFrame"

Typical next step is to inspect keys and datasets before extracting arrays.

## MATLAB `.mat` Files

MATLAB files are common in older research and signal-processing workflows.

```python
import scipy.io

mat = scipy.io.loadmat("albeck_gene_expression.mat")
```

What you get back is usually a dictionary-like object containing arrays and metadata.

This is often a conversion step:

1. load the `.mat`
2. inspect keys
3. pull out the arrays you actually need

## Choosing the Right Import Tool

A quick rule of thumb:

- numeric plain text -> `np.loadtxt()`
- messy or labeled table -> `pd.read_csv()`
- Python object snapshot -> `pickle.load()`
- SAS/Stata -> pandas or format-specific reader
- HDF5 / `.mat` -> scientific library first, then convert as needed

## Practical Workflow

When opening an unfamiliar file:

1. identify the format from the extension and context
2. decide whether you want arrays or DataFrames
3. import a small sample first if the file is large
4. check dtypes, shape, missing values, and headers immediately
5. only then continue with cleaning or analysis

This avoids spending time debugging downstream issues that were actually caused by a bad import decision.

## Common Failure Modes

- using NumPy for mixed-type tables that really want pandas
- forgetting to skip metadata rows or comments
- assuming a delimiter instead of checking it
- loading a huge file fully when chunked reading would be safer
- treating format-specific binary files like plain text

## Key Takeaways

- Choose the import function based on the file format and the target in-memory structure.
- `np.loadtxt()` is great for clean numeric text, but pandas is safer for real-world tables.
- `pd.read_csv()` is the default workhorse for tabular text data.
- Binary and scientific formats usually need their own library before conversion to arrays or DataFrames.
- Import is part of data quality work; verify the result immediately instead of assuming it loaded correctly.
