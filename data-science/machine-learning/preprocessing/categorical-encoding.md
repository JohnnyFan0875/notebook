# Categorical Encoding



Categorical encoding transforms categorical features into numeric representations that machine learning models can use. [scikit-learn](../packages/scikit-learn/README.md) and related libraries provide multiple encoding strategies suitable for different scenarios.

## Example Dataset

```python
import seaborn as sns
import pandas as pd

# Load the Iris dataset
iris = sns.load_dataset("iris").copy()
iris.head()
```

## One-Hot Encoding

One of the most common techniques. Each category is represented as a new binary feature.

```python
from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder(sparse_output=False)
encoded = encoder.fit_transform(iris[['species']])
encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out(['species']))

iris_encoded = pd.concat([iris, encoded_df], axis=1)
```

- Creates a new column for each category.
- Suitable for algorithms that don’t assume order.
- Can increase dimensionality when categories are many (high-cardinality).

## Ordinal Encoding

Assigns integer values to categories. Useful when categories have a natural order.

```python
from sklearn.preprocessing import OrdinalEncoder

encoder = OrdinalEncoder()
iris['species_ordinal'] = encoder.fit_transform(iris[['species']])
```

- Fast and memory efficient.
- Only appropriate when categories are ordered (e.g., small < medium < large).
- Misuse may mislead models into assuming order where none exists.

## Frequency Encoding

Replace each category with its frequency or proportion in the dataset.

```python
freq_map = iris['species'].value_counts(normalize=True)
iris['species_freq'] = iris['species'].map(freq_map)
```

- Keeps feature 1-dimensional.
- Useful for high-cardinality categorical features.
- May capture target leakage if computed improperly (must use only training set).

## Mean Target Encoding

Replace categories with the mean of the target variable within each category.

```python
from sklearn.model_selection import train_test_split

# For illustration, predict whether petal_length > 3.5
iris['target'] = (iris['petal_length'] > 3.5).astype(int)

train, test = train_test_split(iris, test_size=0.3, random_state=42)
mean_target = train.groupby('species')['target'].mean().to_dict()

train['species_mean_target'] = train['species'].map(mean_target)
test['species_mean_target'] = test['species'].map(mean_target)
```

- Powerful for categorical features with predictive power.
- **Risk of [overfitting](../foundations/overfitting-underfitting.md)** if computed on full dataset (must be computed only on training data).
- Can be improved with smoothing (e.g., blending global mean with category mean).

## Hashing Encoding

Encodes categories into a fixed number of hashed bins. Useful for very high-cardinality features.

```python
from sklearn.feature_extraction import FeatureHasher

# Example with synthetic categorical data
import pandas as pd
X = pd.DataFrame({'category': ['a', 'b', 'c', 'a', 'b', 'd']})

hasher = FeatureHasher(n_features=4, input_type='string')
X_hashed = hasher.transform(X['category'])
```

- Constant memory usage.
- No need to store a dictionary of categories.
- Hash collisions possible (two categories mapped to same bin).

## Binary Encoding (via `category_encoders`)

Encodes categories as binary digits. Efficient for medium-cardinality features.

```python
!pip install category_encoders

import category_encoders as ce

encoder = ce.BinaryEncoder(cols=['species'])
iris_binary = encoder.fit_transform(iris[['species']])
```

- More compact than one-hot encoding.
- Reduces dimensionality while retaining some uniqueness.

## Key Considerations

- **One-Hot Encoding** → Safe default for low-cardinality categorical variables.
- **Ordinal Encoding** → Only for ordinal categories.
- **Frequency / Mean Target Encoding** → Powerful but risk leakage; must be computed within training folds.
- **Hashing / Binary Encoding** → Useful for high-cardinality features.
- Always apply encoding **within [cross-validation](../workflow/cross-validation.md) folds** or training set only to avoid leakage.

## Related Concepts

- [Feature Engineering Principles](../foundations/feature-engineering-principles.md)
- [Data Leakage](../foundations/data-leakage.md)
- [Pipeline Basics](../workflow/pipeline-basic.md)
- [Class Imbalance](../evaluation/class-imbalance.md)

[Back to Preprocessing](README.md)
