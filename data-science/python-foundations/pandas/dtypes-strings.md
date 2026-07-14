# Pandas: Data Types & String Operations

Data type conversion and string manipulation are key steps in preparing data for analysis. Pandas provides flexible tools for converting between types and cleaning text data.

## Example Dataset

```python
import seaborn as sns
import pandas as pd

# Load iris dataset
iris = sns.load_dataset("iris").copy()

# Add a categorical/string column
iris["species_str"] = iris["species"].astype(str)

iris.head()
```

## Change Dtype

```python
# Convert to float
iris['sepal_length'] = iris['sepal_length'].astype(float)

# Convert to integer
iris['sepal_width'] = iris['sepal_width'].astype(int)

# Convert to string (useful for concatenation)
iris['petal_length_str'] = iris['petal_length'].astype(str)

# Convert to category
iris['species_cat'] = iris['species'].astype('category')
```

- `astype()` is used for conversion between numeric, string, datetime, or category dtypes.
- Converting to `category` reduces memory and is efficient for repeated labels.

## Convert to Datetime

```python
# Create a new datetime column
iris['measure_date'] = pd.to_datetime(
    ['2024-01-01', '2024-01-02', '2024-01-03'] * 50
)

# Extract date components
iris['year'] = iris['measure_date'].dt.year
iris['month'] = iris['measure_date'].dt.month
iris['weekday'] = iris['measure_date'].dt.day_name()
```

## Clean & Transform Strings

```python
# Lowercase all species names
iris['species_str'] = iris['species_str'].str.lower()

# Remove leading/trailing spaces
iris['species_str'] = iris['species_str'].str.strip()

# Replace substring
iris['species_str'] = iris['species_str'].str.replace('setosa', 'SET', regex=False)

# String length
iris['name_length'] = iris['species_str'].str.len()

# Check if string contains pattern
iris['has_virginica'] = iris['species_str'].str.contains('virginica')
```

Case-insensitive matching is often useful for user-generated text:

```python
iris["has_virginica"] = iris["species_str"].str.contains(
    "virginica",
    case=False,
    na=False,
)
```

- `case=False` avoids missing matches due to capitalization.
- `na=False` turns missing text into `False` instead of propagating nulls into the boolean mask.

## Search Across Multiple Text Fields

Semi-structured text data often spreads meaningful content across several columns, such as:

- original text
- expanded full text
- quoted text
- retweeted text

In those cases, one column-level `.str.contains()` is not enough.

```python
apple = tweets["text"].str.contains("apple", case=False, na=False)

for column in [
    "extended_tweet-full_text",
    "retweeted_status-text",
    "retweeted_status-extended_tweet-full_text",
]:
    apple = apple | tweets[column].str.contains(
        "apple",
        case=False,
        na=False,
    )
```

This pattern is useful whenever the same concept may appear in several alternate fields.

Key point: if the text schema varies by record type, build the boolean mask from all relevant fields first, then count or filter.

## Select Numeric Columns

```python
# Select only numeric columns
numeric_df = iris.select_dtypes(include="number")

# Apply statistical functions
numeric_df.mean(), numeric_df.std()
```

## Key Takeaways

- Use `.astype()` to convert between numeric, string, and categorical types.
- `pd.to_datetime()` enables safe conversion to datetime.
- String operations are accessed via `.str` accessor.
- `select_dtypes()` allows focusing on numeric vs. non-numeric subsets.
