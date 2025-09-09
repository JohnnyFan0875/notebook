# Imputation

Filling in **`missing values`** in a dataset with substituted values

- Common strategies:
  - **Mean** (for numerical data)
  - **Mode** (for categorical data)
  - **Constant value** (e.g., `-999`)

## Example

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

> **Tip**: Always check the proportion of missing values before choosing an imputation strategy. For high missingness, consider advanced methods (e.g., KNN imputer, iterative imputer).
