# Pandas: Datetime Handling

Datetime handling is essential for working with time series or date-related data. Pandas provides powerful methods for parsing, extracting, formatting, and performing arithmetic on datetime values.

## Example Dataset

```python
import seaborn as sns
import pandas as pd

# Use the Iris dataset and add a fake datetime column
iris = sns.load_dataset("iris")
iris["measurement_date"] = pd.to_datetime([
    '2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'
] * 30)  # repeat dates for all 150 rows

iris.head()
```

## Convert to Datetime

```python
# Convert an existing string column to datetime
dir_str = pd.Series(['2024-01-01', '2024-05-03', '2024-06-20'])
dir_dt = pd.to_datetime(dir_str, errors='coerce')  # invalid formats become NaT
```

- `errors='coerce'`: forces invalid parsing to `NaT` (Not a Time).
- Ensures consistent datetime dtype.

If date and time are stored in separate string columns, combine them first:

```python
combined = df["date"].str.cat(df["time"], sep=" ")
df["date_and_time"] = pd.to_datetime(combined, errors="coerce")
```

This is a common cleanup step in event logs and transactional datasets.

## Extract Datetime Components

```python
iris['year'] = iris['measurement_date'].dt.year
iris['month'] = iris['measurement_date'].dt.month
iris['day'] = iris['measurement_date'].dt.day
iris['weekday'] = iris['measurement_date'].dt.day_name()
```

- `.dt.year`, `.dt.month`, `.dt.day`: numeric components.
- `.dt.day_name()`: string weekday name.

If the datetime information lives in the index instead of a column, use the index attributes directly:

```python
df = df.set_index("measurement_date")
df.index.month
df.index.day_name()
```

Tip: `.dt` is for datetime-like Series. `DatetimeIndex` uses `.index.month`, `.index.day`, and similar accessors directly.

## Format Datetime to String

```python
iris['date_str'] = iris['measurement_date'].dt.strftime('%d-%m-%Y')
iris['date_str_long'] = iris['measurement_date'].dt.strftime('%B %d, %Y')
```

- `strftime('%d-%m-%Y')`: custom format.
- `%B %d, %Y`: long format with month name.

## Datetime Arithmetic & Filtering

```python
# Calculate days since measurement
today = pd.Timestamp.today()
iris['days_since'] = (today - iris['measurement_date']).dt.days

# Add 30 days
iris['plus_30d'] = iris['measurement_date'] + pd.Timedelta(days=30)

# Filter by date
iris[iris['measurement_date'] > '2024-01-03']
```

- Subtraction between `Timestamp` and datetime column returns `Timedelta`.
- Add or subtract timedeltas for shifting dates.

## Resampling (Time Series)

```python
# Suppose we aggregate petal length by measurement_date
iris.groupby('measurement_date')['petal_length'].mean().resample('D').mean()
```

- `.resample('D')`: resample to daily frequency.
- Supports rules like 'W' (weekly), 'M' (monthly), 'Y' (yearly).

There is an important difference between grouping by calendar components and resampling by true time periods:

```python
df.groupby(df.index.month)["value"].mean()
df["value"].resample("M").mean()
```

- `groupby(df.index.month)` pools all Januaries, all Februaries, and so on across the whole dataset
- `resample("M")` creates one result per actual month in chronological order

Use `groupby(index.month)` for seasonal comparisons.
Use `resample()` when you want a proper time series back.

## Key Takeaways

- Use `pd.to_datetime()` to convert strings to datetime safely.
- `.dt` accessor extracts components and formats dates.
- Perform arithmetic with `Timedelta` for shifts.
- Resampling is useful for time series aggregation.
