# Imputation



Filling in **`missing values`** in a dataset with substituted values.

- Common strategies:

  - **Mean** (for numerical data)
  - **Mode** (for categorical data)
  - **Constant value** (e.g., `-999`)

## Single Imputation

- Replaces each missing value with a single estimated value.
- Methods: mean, median, mode, regression-based substitution, hot-deck imputation.
- **Pros:** Simple to implement, fast.
- **Cons:** Underestimates variability, ignores uncertainty about missing data, may bias results.

**Example:**

```python
from sklearn.impute import SimpleImputer

# Single imputation using mean
imputer = SimpleImputer(strategy='mean')
df[['age']] = imputer.fit_transform(df[['age']])
```

## Multiple Imputation

- Generates several different imputed datasets by replacing missing values with multiple plausible values.
- Each dataset is analyzed separately, and results are pooled for inference.
- Methods: Multiple Imputation by Chained Equations (MICE), Bayesian approaches.
- **Pros:** Accounts for uncertainty, provides valid statistical inference, less bias.
- **Cons:** More complex, computationally intensive.

**Example (using `statsmodels`/`fancyimpute`/`miceforest`):**

```python
# Example with IterativeImputer (approximation of MICE)
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

imputer = IterativeImputer(random_state=0)
imputed_df = imputer.fit_transform(df)
```

## Example: Column-specific Imputation

```python
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer

# Define column-specific imputations
column_transformer = ColumnTransformer(
    transformers=[
        ('age_income', SimpleImputer(strategy='mean'), ['age', 'income']),
        ('gender', SimpleImputer(strategy='most_frequent'), ['gender'])
    ])

# Apply imputation
imputed_df = column_transformer.fit_transform(df)
imputed_df = pd.DataFrame(imputed_df, columns=['age', 'income', 'gender'])
```

## Example: Single Column Imputation

```python
# Note: double brackets are required
df[['col']] = SimpleImputer(strategy='mean').fit_transform(df[['col']])
```

## Interpolation vs. Imputation

Although both _imputation_ and _interpolation_ involve filling missing data, they differ in purpose and assumption.

- **Imputation** estimates missing values based on other features or statistical distributions (common in clinical or tabular datasets).
- **Interpolation** estimates intermediate values in a **continuous sequence**, such as time-series or spatial data.

For interpolation methods in `pandas`, see:  
👉 [Data Modification — Interpolation in Pandas](../../python-foundations/pandas/missing-data.md#interpolation)

> **Tip**: Always check the proportion of missing values before choosing an imputation strategy. For high missingness, consider advanced methods (e.g., [KNN](../supervised-learning/classification/knn.md) imputer, iterative imputer, or multiple imputation).

## Related Concepts

- [Data Leakage](../foundations/data-leakage.md)
- [Train-Test Split](train-test-split.md)
- [Pipeline Basics](../workflow/pipeline-basic.md)
- [Feature Engineering Principles](../foundations/feature-engineering-principles.md)

[Back to Preprocessing](README.md)
