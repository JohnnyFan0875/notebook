# Imputation

Filling in **`missing values`** in a dataset with substituted values.

## Interview Fast Answer

如果面試官問「怎麼處理 missing data」，最穩的回答通常不是直接報某個函式，而是先講決策順序：

1. 先看缺值比例
2. 再看欄位型態與分布
3. 再問 missingness 本身是否有訊號
4. 最後才選補值方法

一個夠精簡的版本可以說成：

- numerical data 常考慮 mean / median
- categorical data 常考慮 mode 或 `"unknown"`
- 若缺值本身有商業意義，可以加 missingness indicator
- 所有會學到資料資訊的補值規則，都應該只在 training split 或 CV fold 內 fit

- Common strategies:
- **Mean** (for numerical data)
- **Mode** (for categorical data)
- **Constant value** (e.g., `0`, `-999`, `"unknown"`)

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

## Mean vs. Median vs. Fixed Value

補值不是只看哪個函式方便，而是要問缺值本身代表什麼。

例如：

- `age` 缺值，常見會考慮 mean 或 median
- `number_of_purchases_last_year` 缺值，常常其實代表 0
- contact information 缺值，可能值得另外做 missingness indicator

如果欄位分布很偏，mean 可能會被極端值拉走。

例如 `max_donation` 這類 heavy-tailed 欄位，median 往往比 mean 更穩。

### Interview Prompt: Mean vs Median

這也是常見面試追問。

高訊號回答通常是：

- 分布偏斜或有 outliers 時，median 比 mean 更 robust
- 如果缺值其實代表「沒有發生」，fixed value 可能比平均數更合理
- 補值方法不是統計技巧比賽，而是要符合資料生成機制

## Missingness Indicator Can Be a Feature

有時候缺值本身就有訊號。

```python
basetable["no_email"] = basetable["email"].isna().astype(int)
```

這在實務上很常見，尤其是：

- 聯絡資訊缺失
- 財務資訊缺失
- 某個行為欄位只對特定族群有值

Key point: 補值處理不一定只是「把空格補滿」，也可能是把 missingness 本身變成一個 feature。

## Common Interview Traps

- 在 full dataset 上先補值，再切 train/test，這是 leakage
- 忽略 missingness ratio，對高缺值欄位硬補平均數
- 對類別欄位用 mean 這種不合語意的方法
- 把 imputation 和 interpolation 混成同一件事

## Interpolation vs. Imputation

Although both _imputation_ and _interpolation_ involve filling missing data, they differ in purpose and assumption.

- **Imputation** estimates missing values based on other features or statistical distributions (common in clinical or tabular datasets).
- **Interpolation** estimates intermediate values in a **continuous sequence**, such as time-series or spatial data.

For interpolation methods in `pandas`, see:
👉 [Data Modification — Interpolation in Pandas](../../python-foundations/pandas/missing-data.md#interpolation)

> **Tip**: Always check the proportion of missing values before choosing an imputation strategy. For high missingness, consider advanced methods (e.g., [KNN](../supervised-learning/classification/knn.md) imputer, iterative imputer, or multiple imputation).

> **Tip**: 在 time-aware basetable 裡，補值規則也必須能在未來 snapshot 重現，不能偷用未來資料估計 replacement value。

## Related Concepts

- [Data Leakage](../foundations/data-leakage.md)
- [Train-Test Split](train-test-split.md)
- [Pipeline Basics](../workflow/pipeline-basic.md)
- [Feature Engineering Principles](../foundations/feature-engineering-principles.md)
- [Basetable and Time-Aware Feature Engineering](../foundations/basetable-and-time-aware-feature-engineering.md)

[Back to Preprocessing](README.md)
