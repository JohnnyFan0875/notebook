# String Matching and Fuzzy Matching

String matching is often needed when working with messy or inconsistent text data (e.g., typos, different spellings). Python provides built-in tools (regex, string methods) and specialized libraries like **thefuzz** (formerly fuzzywuzzy) for fuzzy string matching.

## Basic Example with `thefuzz`

```python
from thefuzz import fuzz

# Similarity score between two strings
print(fuzz.WRatio('Reeding', 'Reading'))  # 86
```

- `WRatio` is a weighted measure that combines different similarity metrics.
- Scores range from 0 (no similarity) to 100 (exact match).

Other useful functions:

- `fuzz.ratio()` → Simple Levenshtein distance ratio.
- `fuzz.partial_ratio()` → Useful for substrings.
- `fuzz.token_sort_ratio()` → Ignores word order.
- `fuzz.token_set_ratio()` → Ignores duplicate words.

## Matching Against a List of Choices

```python
from thefuzz import process
import pandas as pd

# Example DataFrame
employees = pd.DataFrame({'Employee': ['Alice', 'Bob', 'Charlie', 'David', 'Eve']})

# Category to match
category = ['Bobo']

matches = process.extract(category[0], employees['Employee'])
print(matches)
# [('Bob', 86, 1), ('Alice', 0, 0), ('Charlie', 0, 2), ('David', 0, 3), ('Eve', 0, 4)]

# Replace near matches with category if above threshold
for match in matches:
    if match[1] >= 80:
        employees.loc[employees['Employee'] == match[0], 'Employee'] = category[0]

print(employees)
```

- `process.extract(query, choices)` → finds closest matches from a list/Series.
- Returns a list of tuples: `(match_string, score, index)`.
- You can set thresholds to decide when to replace or flag values.

## Example with Iris Dataset

Suppose we have typos in the `species` column:

```python
import seaborn as sns
iris = sns.load_dataset("iris").copy()

# Introduce typo
iris.loc[0, 'species'] = 'setossa'  # typo for 'setosa'

# Use fuzzy matching to fix it
matches = process.extract('setosa', iris['species'].unique())
print(matches)
# [('setossa', 92, 0), ('setosa', 100, 1), ...]

# Replace values above threshold
iris['species'] = iris['species'].replace({matches[0][0]: 'setosa'})
```

- Useful for cleaning categorical columns with inconsistent labels.
- Especially relevant in EDA and preprocessing before modeling.

## Tips and Best Practices

- Always normalize text before matching:

  ```python
  text = text.lower().strip()
  ```

  to handle case/whitespace inconsistencies.

- For large datasets, consider **RapidFuzz**, a faster drop-in replacement for `thefuzz`.

- Be careful with aggressive replacements: always review matches before applying.

- Combine fuzzy matching with:

  - `.str.contains()` or regex for rule-based cleaning.
  - Dictionaries of known mappings for frequent errors.

## Key Takeaways

- Use `fuzz.WRatio()` or `fuzz.ratio()` for pairwise similarity.
- Use `process.extract()` to find best matches in a list or Series.
- Apply thresholds to decide when to correct or flag mismatched text.
- Useful in cleaning categorical variables, especially in survey data, user inputs, or datasets with typos.
- Consider **RapidFuzz** for performance in production workflows.
