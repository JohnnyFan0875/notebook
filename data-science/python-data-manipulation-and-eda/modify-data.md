# Modifying Data

| Category                                | Key Methods / Functions                                                                                       |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **1. Updating Data**                    | `.loc[]`, `.iloc[]`, `.at[]`, `.iat[]`, `.replace()`, `.str.replace()`, `.apply()`, `.applymap()`, `.map()`   |
| **2. Adding / Removing Columns & Rows** | `df['col']=...`, `.assign()`, `.insert()`, `.loc[]`, `.drop()`, `.dropna()`                                   |
| **3. Handling Missing Data**            | `.fillna()`, `.dropna()`                                                                                      |
| **4. Data Types & String Operations**   | `.astype()`, `pd.to_datetime()`, `.str.lower()`, `.str.strip()`                                               |
| **5. Row Selection & Filtering**        | `df[cond]`, `.query()`, `.str.contains()`, `np.select()`, `np.where()`                                        |
| **6. Sampling, Duplicates, & Unique**   | `.unique()`, `.nunique()`, `.drop_duplicates()`, `.duplicated()`, `.sample()`, `.groupby().sample()`          |
| **7. Grouping & Aggregation**           | `.groupby()`, `.agg()`, `.transform()`, `.describe()`                                                         |
| **8. Reshaping Data**                   | `.pivot_table()`, `.melt()`, `.unstack()`, `pd.concat()`, `.merge()`, `pd.merge_ordered()`, `pd.merge_asof()` |
| **9. Categorical Data & Encoding**      | `.astype('category')`, `.cat.codes`, `pd.get_dummies()`, `.cat.categories`, `.cat.rename_categories()`        |
| **10. Index & MultiIndex**              | `.set_index()`, `.reset_index()`                                                                              |
| **11. Binning & Categorization**        | `pd.cut()`, `pd.qcut()`                                                                                       |
| **12. Datetime Handling**               | `pd.to_datetime()`, `.dt.year/month/day`, `.dt.day_name()`, `.dt.strftime()`                                  |

## Example Dataset

```python
import pandas as pd
import numpy as np

# Example dataset of dogs
df = pd.DataFrame(
    {
        "name": ["Bella", "Charlie", "Lucy", "Max", "Daisy"],
        "height_cm": [56, 43, 46, 50, np.nan],                # dog's height in cm
        "weight_kg": [24, 24, 24, 30, 20],                    # dog's weight in kg
        "age": [0, 1, np.nan, 5, 2]                           # age in years
    },
    index=["dog1", "dog2", "dog3", "dog4", "dog5"]
)
```

## 1. Updating Data

| Task                     | Method / Function                      |
| ------------------------ | -------------------------------------- |
| Update by label/position | `.loc[]`, `.iloc[]`, `.at[]`, `.iat[]` |
| Replace values           | `.replace()`, `.str.replace()`         |
| Apply function           | `.apply()`, `.applymap()`, `.map()`    |
| Conditional update       | `.loc[condition, col] = ...`           |

- Update by label/position

```python
# Update a specific cell using condition
df.loc[df['name'] == "Bella", "height_cm"] = 60        # if name == "Bella", set height to 60

# Update cell by row/column index
df.iloc[0, 1] = 70                                     # First row, second column
df.iat[1, 2] = 26                                      # Fast scalar update by integer position (dog2 weight_kg -> 26)

# Fast scalar update by label
df.at['dog1', 'age'] = 2                               # dog1 age becomes 2
```

- Replace values

```python
df['name'] = df['name'].replace("Charlie", "Charles")         # Replace exact match
df['name'] = df['name'].str.replace("C", "c")                 # Replace substring in strings

replace_dict = {"Bella": "Bell", "Lucy": "Lucia"}
df['name'] = df['name'].replace(replace_dict)                 # Replace using a dictionary (multiple mappings)
```

- Apply function

```python
# Column-wise transformation
df['height_plus_1'] = df['height_cm'].apply(lambda x: x + 1)               # Add 1 to each height

# Apply function using a predefined function (no lambda)
def to_inches(cm):
    return cm / 2.54 if pd.notna(cm) else np.nan

df['height_inch'] = df['height_cm'].apply(to_inches)

# Element-wise transformation for entire DataFrame
numeric_df = df[['height_cm', 'weight_kg', 'age']]
df_doubled = numeric_df.applymap(lambda x: x * 2)                          # Multiply all numbers by 2

# Transform one Series using map
df['age_label'] = df['age'].map(lambda x: 'puppy' if x < 2 else 'adult')
```

- Conditional update

```python
# Increase weight by 5 kg if weight < 25 kg
df.loc[df['weight_kg'] < 25, 'weight_kg'] += 5

# Fill NaN age with 0 only for dogs shorter than 50 cm
df.loc[(df['height_cm'] < 50) & (df['age'].isna()), 'age'] = 0
```

## 2. Adding / Removing Columns and Rows

| Task              | Method / Function                         |
| ----------------- | ----------------------------------------- |
| Add/insert column | `df['col']=...`, `.assign()`, `.insert()` |
| Add row           | `.loc[]` with new index                   |
| Drop column/row   | `.drop()`, `.dropna()`                    |

- Add / Insert column

```python
# Add a new column directly
df['country'] = ["USA", "UK", "Canada", "USA", "UK"]                  # New column with country

# Add column using assign (returns a new DataFrame)
df = df.assign(bmi = df['weight_kg'] / (df['height_cm']/100)**2)      # Calculate BMI

# Insert column at a specific position
df.insert(2, "weight_g", df["weight_kg"]*1000)                        # Insert grams column at index 2

# Create a new column based on calculation of existing columns
df["age_in_months"] = df["age"] * 12
```

- Add row

```python
# Append new row using loc with next integer index
df.loc[df.shape[0]] = ['Rocky', 45, 18, 3, 'USA', 18000, 88.9]  # Fill all columns
```

- Drop column / row

```python
# Drop column
df.drop(columns=['age'], inplace=False)                 # Return new DF without 'age'

# Drop rows by condition
df.drop(df[df['height_cm']>50].index)                   # Drop dogs taller than 50 cm

# Drop rows with missing values in a specific column
df.dropna(subset=['age'])                               # Drop rows where 'age' is NaN
```

## 3. Handling Missing Data

| Task                   | Method / Function |
| ---------------------- | ----------------- |
| Fill missing values    | `.fillna()`       |
| Drop missing rows/cols | `.dropna()`       |

- Fill missing values

```python
# Fill all NaN with 0
df.fillna(0)

# Fill NaN in a single column with the column mean
df['age'].fillna(df['age'].mean())

# Fill using dictionary for multiple columns
df.fillna({'age': df['age'].mean(), 'height_cm': 50})

# Fill with forward fill (previous non-NaN value)
df.fillna(method='ffill')

# Fill with backward fill (next non-NaN value)
df.fillna(method='bfill')
```

- Drop missing rows/cols

```python
# Drop rows with any NaN
df.dropna()

# Drop columns with any NaN
df.dropna(axis=1)

# Drop rows with NaN only in specific columns
df.dropna(subset=['age'])
```

## 4. Data Types & String Operations

| Task                    | Method / Function                  |
| ----------------------- | ---------------------------------- |
| Change dtype            | `.astype()`                        |
| Convert to datetime     | `pd.to_datetime()`                 |
| Clean/transform strings | `.str.strip()`, `.str.lower()`     |
| Select numeric columns  | `.select_dtypes(include="number")` |

- Change dtype

```python
# Convert to float
df['age'] = df['age'].astype(float)

# Convert weight to integer
df['weight_kg'] = df['weight_kg'].astype(int)

# Convert height to string (useful for concatenation)
df['height_cm_str'] = df['height_cm'].astype(str)
```

- Convert to datetime

```python
# Create a new datetime column from a list
df['checkup_date'] = pd.to_datetime(
    ['2025-01-01', '2025-02-01', '2025-03-01', '2025-04-01', '2025-05-01']
)

# Extract date components
df['checkup_month'] = df['checkup_date'].dt.month
df['checkup_weekday'] = df['checkup_date'].dt.day_name()
```

- Clean/transform strings

```python
# Lowercase all names
df['name'] = df['name'].str.lower()

# Remove leading/trailing spaces in names
df['name'] = df['name'].str.strip()

# Replace substring in names
df['name'] = df['name'].str.replace('a', '@', regex=False)  # Replace 'a' with '@'

# Check if names start with 'b'
df['starts_with_b'] = df['name'].str.startswith('b')
```

- Select numeric columns

```python
# Select only numeric columns from DataFrame
numeric_df = df.select_dtypes(include="number")

# Use-case: apply statistical functions only on numeric data
numeric_df.mean(), numeric_df.std()

```

## 5. Row Selection & Filtering

| Task                  | Method / Function         |
| --------------------- | ------------------------- |
| Conditional filtering | `df[cond]`, `.query()`    |
| String filtering      | `.str.contains()`         |
| Advanced conditions   | `np.select()`, `np.where` |

- Conditional filtering

```python
# Select rows where height > 45 cm
df[df['height_cm'] > 45]

# Select rows where weight is between 20 and 25 kg
df[(df['weight_kg'] >= 20) & (df['weight_kg'] <= 25)]

# SQL-like query using .query()
df.query('height_cm > 45 or age < 2')
```

- String filtering

```python
# Names containing 'a' or 'A'
df[df['name'].str.contains('a', case=False)]

# Names starting with 'b'
df[df['name'].str.startswith('b')]

# Names ending with 'y'
df[df['name'].str.endswith('y')]

# Names containing 'a' or 'b'
df[df['name'].str.contains('a|b')]

# Names containing 'a' in the begining
df[df['name'].str.contains('^a')]
```

- Advanced conditions

```python
# Assign size group based on height
choices = ['A', 'B', 'C']
conds = [
    df['height_cm'] < 45,                   # Small dogs
    df['height_cm'].between(45, 50),        # Medium dogs
    df['height_cm'] > 50                    # Large dogs
]
df['size_group'] = np.select(conds, choices, default='Unknown')

# Quick binary classification with np.where
df['is_puppy'] = np.where(df['age'] < 2, True, False)
```

## 6. Sampling, Duplicates, and Unique Values

| Task                | Method / Function                     |
| ------------------- | ------------------------------------- |
| Get unique values   | `.unique()`, `.nunique()`             |
| Handle duplicates   | `.drop_duplicates()`, `.duplicated()` |
| Random sampling     | `.sample()`                           |
| Group-wise sampling | `.groupby().sample()`                 |

- Get unique values

```python
# List unique dog names
df['name'].unique()

# Count unique dog names
df['name'].nunique()
```

- Handle duplicates

```python
# Drop duplicate names (keep the first occurrence)
df.drop_duplicates(subset='name')

# Show all duplicate names (keep=False returns all duplicates)
df[df.duplicated(subset='name', keep=False)]

# Drop duplicates across entire row
df.drop_duplicates()
```

- Random sampling

```python
# Sample 2 random rows (reproducible with random_state)
df.sample(n=2, random_state=42)

# Sample 40% of the rows
df.sample(frac=0.4, random_state=42)
```

- Group-wise sampling

```python
# Sample 1 row per group based on 'name'
df.groupby('name').sample(n=1, random_state=42)

# Sample 50% of rows per group
df.groupby('name').sample(frac=0.5, random_state=42)
```

## 7. Grouping & Aggregation

| Task                        | Method / Function                          |
| --------------------------- | ------------------------------------------ |
| Basic group aggregation     | `.groupby(col)[target].agg(func)`          |
| Multiple aggregations       | `.groupby(col).agg({col: [func1, func2]})` |
| Group transformation        | `.groupby(col)[target].transform(func)`    |
| Descriptive stats per group | `.groupby(col).describe()`                 |

- Basic group aggregation

```python
# Sum weight per dog name
df.groupby('name')['weight_kg'].sum()

# Mean height per name
df.groupby('name')['height_cm'].mean()

# Many groups, many summaries
df.groupby(['name', 'weight_kg'])['height_cm'].mean()
df.groupby(['name', 'weight_kg'])[['height_cm', 'age']].mean()
```

- Multiple aggregations

```python
# Compute mean & max of height, and sum of weight per name
df.groupby('name').agg({
    'height_cm': ['mean', 'max'],
    'weight_kg': 'sum'
})

# Aggregate and rename columns using tuple syntax
df.groupby('name').agg(
    height_mean=('height_cm', 'mean'),
    weight_sum=('weight_kg', 'sum')
)
```

- Group transformation

```python
# Compute standard deviation of weight per name, aligned to original rows
df['weight_std'] = df.groupby('name')['weight_kg'].transform('std')

# Compute normalized weight per group (subtract group mean)
df['weight_norm'] = df['weight_kg'] - df.groupby('name')['weight_kg'].transform('mean')
```

- Descriptive Stats Per Group

```python
# Quick descriptive stats per group
df.groupby('name')['weight_kg'].describe()

# Count rows per group
df.groupby('name').size()
```

## 8. Reshaping Data

| Task             | Method / Function                                   |
| ---------------- | --------------------------------------------------- |
| Pivot table      | `.pivot_table()`                                    |
| Melt (unpivot)   | `.melt()`                                           |
| Unstack index    | `.unstack()`                                        |
| Concatenate      | `pd.concat()`                                       |
| Merge DataFrames | `.merge()`, `pd.merge_ordered()`, `pd.merge_asof()` |

- Pivot table

```python
# Create a pivot table: weight per dog name and age
df.pivot_table(
    index='name',
    values='weight_kg',
    columns='age',
    fill_value=0
)

# Pivot table with multiple aggregation functions
df.pivot_table(
    index='name',
    values=['height_cm','weight_kg'],
    aggfunc={'height_cm':'mean', 'weight_kg':'sum'},
    fill_value=0
)
```

- Melt (unpivot)

```python
# Convert wide to long format
df.melt(
    id_vars=['name'],
    var_name='variable',
    value_name='value'
)

# Example: Only melt numeric columns
df.melt(
    id_vars='name',
    value_vars=['height_cm','weight_kg','age'],
    var_name='measurement',
    value_name='value'
)
```

- Unstack index

```python
# Group by name and age, then unstack to columns
grouped = df.groupby(['name','age'])['weight_kg'].mean()
grouped_unstacked = grouped.unstack(fill_value=0)
```

- Concatenate

```python
# Vertical concatenation (stack rows)
pd.concat([df, df], ignore_index=True)

# Horizontal concatenation (align by index)
pd.concat([df, df[['weight_kg']]], axis=1)

# Concatenate Series objects
series1 = pd.Series(['a','b','c','d'], index=['1','2','3','4'])
series2 = pd.Series(['e','f','g','h'], index=['5','6','7','8'])

pd.concat([series1, series2], ignore_index=True)
```

- Merge DataFrames

```python
# Basic merge on 'name'
df.merge(df, on='name', suffixes=['_L','_R'])

# Ordered merge (useful for time series)
pd.merge_ordered(df, df, on='name')

# As-of merge (useful for nearest time join)
pd.merge_asof(
    df.sort_values('age'),
    df.sort_values('age'),
    on='age',
    suffixes=['_L','_R']
)
```

## 9. Categorical Data & Encoding

| Task                        | Method / Function               |
| --------------------------- | ------------------------------- |
| Convert to categorical type | `.astype('category')`           |
| Label encoding              | `.cat.codes`                    |
| One-hot encoding            | `pd.get_dummies()`              |
| Inspect category info       | `.cat.categories`, `.cat.codes` |

- Convert to categorical type

```python
# Convert name to category dtype
df['name_cat'] = df['name'].astype('category')

# Inspect categories
df['name_cat'].cat.categories
```

- Label encoding

```python
# Numeric codes for each category (0-based)
df['name_code'] = df['name_cat'].cat.codes

# Example: Combine with another column
df['size_label'] = (
    df['height_cm'] > 50
).astype('int')  # Binary categorical from condition
```

- One-hot encoding

```python
# One-hot encode 'name' column into dummy variables
pd.get_dummies(df, columns=['name'])

# Keep only top categories and merge rare ones (example)
df['name_cat'] = df['name_cat'].cat.set_categories(['Bella','Lucy','Max'])
pd.get_dummies(df['name_cat'], dummy_na=True)
```

- Inspect category info

```python
# Reorder categories
df['name_cat'] = df['name_cat'].cat.reorder_categories(
    ['Bella', 'Charlie', 'Lucy', 'Max', 'Daisy'],
    ordered=True
)

# Rename categories
df['name_cat'] = df['name_cat'].cat.rename_categories(
    {'Bella':'Bells', 'Lucy':'Lucia'}
)
```

## 10. Index & MultiIndex

| Task                       | Method / Function                |
| -------------------------- | -------------------------------- |
| Set / reset index          | `.set_index()`, `.reset_index()` |
| Create multi-level index   | `.set_index([col1, col2])`       |
| Select rows by tuple index | `.loc[[tuple1, tuple2]]`         |
| Inspect index info         | `.index`, `.names`, `.is_unique` |

- Set / reset index

```python
# Set column as the new index
idx_df = df.set_index('name')
idx_df = df.set_index(['name', 'weight_kg'])

# Reset back to default integer index
reset_df = idx_df.reset_index()

# Inspect index properties
idx_df.index.name        # Name of index
idx_df.index.is_unique   # Check if index values are unique
```

- Create multi-level index

```python
# Create multi-level index using name and age
multi_idx = df.set_index(['name', 'age'])

# Inspect MultiIndex info
multi_idx.index.names        # Names of index levels
multi_idx.index.levels       # Unique values per level
```

- Select rows by tuple index

```python
# Select rows using tuple-based indexing
multi_idx.loc[[("Bella", 0), ("Max", 5)]]

# Slice using pd.IndexSlice for multi-level selection
import pandas as pd
idx = pd.IndexSlice
multi_idx.loc[idx[:, 0:2], :]   # Select all names where age 0 to 2
```

- Inspect index info

```python
# Sort by MultiIndex levels
multi_idx.sort_index(level=['name', 'age'], ascending=[True, False])

# Swap index levels
multi_idx_swapped = multi_idx.swaplevel()

# Reset MultiIndex back to columns
multi_idx.reset_index()
```

## 11. Binning & Categorization

| Task                | Method / Function |
| ------------------- | ----------------- |
| Fixed-width bins    | `pd.cut()`        |
| Quantile-based bins | `pd.qcut()`       |

- Fixed-width bins

```python
# Bin dogs by height (cm) into categories
df['size_cat'] = pd.cut(
    df['height_cm'],
    bins=[0, 45, 50, 55, 100],
    labels=['Small', 'Medium', 'Large', 'Giant']
)

# Inspect resulting categories
df['size_cat'].cat.categories
```

- Quantile-based bins

```python
# Divide dogs into 3 weight quantiles (Light, Medium, Heavy)
df['weight_group'] = pd.qcut(
    df['weight_kg'],
    q=3,
    labels=['Light', 'Medium', 'Heavy']
)

# Check how many dogs fall into each weight bin
df['weight_group'].value_counts()
```

## 12. Datetime Handling

| Task                        | Method / Function                     |
| --------------------------- | ------------------------------------- |
| Convert to datetime         | `pd.to_datetime()`                    |
| Extract datetime components | `.dt.year`, `.dt.month`, `.dt.day`    |
| Format datetime to string   | `.dt.strftime()`                      |
| Day / week operations       | `.dt.day_name()`, `.dt.isocalendar()` |

- Convert to datetime

```python
# Create a datetime column for dog birth dates
df['birth_date'] = pd.to_datetime([
    '2025-01-01', '2024-05-03', '2024-06-20', '2022-07-01', '2021-08-01'
], errors = 'coerce')    # Return NaT (not a time) if conversion failed

# Inspect datetime column dtype
df['birth_date'].dtype
```

- Extract datetime components

```python
df['year'] = df['birth_date'].dt.year           # Extract year
df['month'] = df['birth_date'].dt.month         # Extract month number
df['day'] = df['birth_date'].dt.day             # Extract day of month
df['weekday'] = df['birth_date'].dt.day_name()  # Day of week (string)
```

- Format datetime to string

```python
# Convert datetime to custom string format: DD-MM-YYYY
df['date_str'] = df['birth_date'].dt.strftime('%d-%m-%Y')

# ISO-like format with month name
df['date_str_long'] = df['birth_date'].dt.strftime('%B %d, %Y')
```

- Datetime arithmetic & filtering

```python
# Calculate dog age in days relative to today
df['age_days'] = (pd.Timestamp.today() - df['birth_date']).dt.days

# Add 30 days to each birth date
df['birth_plus_30d'] = df['birth_date'] + pd.Timedelta(days=30)

# Filter dogs born after 2023
df[df['birth_date'] > pd.Timestamp('2023-01-01')]
```
