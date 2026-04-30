# Feature Scaling



Feature scaling is the process of transforming features so they are on comparable scales, which prevents models from giving undue importance to variables with larger ranges. It is an essential step in machine learning [pipelines](../workflow/pipeline-basic.md), especially for algorithms that rely on distance metrics or assume normally distributed data.

⚠️ **Critical Note:** Scaling must always be fit on the **training set only**, and then the same parameters (mean, std, min, max, etc.) should be applied to the test set to avoid [data leakage](../foundations/data-leakage.md).

## Standardization (Z-score scaling)

- Transforms features to have **mean = 0** and **standard deviation = 1**.
- Formula: `(x - mean) / std`.
- Effective when features are approximately Gaussian.
- Commonly used in **[linear regression](../supervised-learning/regression/linear.md)**, **[logistic regression](../supervised-learning/classification/logistic-regression.md)**, **[SVM](../supervised-learning/classification/svm.md)**, and **[PCA](../unsupervised-learning/dimensionality-reduction/pca.md)**.

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

### With Pipelines

```python
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
import numpy as np

steps = [("scaler", StandardScaler()), ("knn", KNeighborsClassifier())]
pipeline = Pipeline(steps)

parameters = {"knn__n_neighbors": np.arange(1, 50)}

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
cv = GridSearchCV(pipeline, param_grid=parameters)
cv.fit(X_train, y_train)
y_pred = cv.predict(X_test)
```

## Normalization (Min-Max scaling)

- Scales features to a given range, typically **[0, 1]**.
- Preserves relative distances but **sensitive to outliers**.
- Suitable for algorithms that don’t assume normality, such as **[KNN](../supervised-learning/classification/knn.md), neural networks**.

```python
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

df = pd.DataFrame({'Age': [25, 30, 35, 40, 45]})

scaler = MinMaxScaler()
normalized_data = scaler.fit_transform(df)
```

## MaxAbs Scaling

- Scales each feature by its **maximum absolute value**.
- Maps data into range [-1, 1].
- Good for **sparse data** since it does not destroy sparsity.

```python
from sklearn.preprocessing import MaxAbsScaler

scaler = MaxAbsScaler()
X_scaled = scaler.fit_transform(X)
```

## Robust Scaling

- Uses **median** and **IQR (interquartile range)** instead of mean and variance.
- More robust to **outliers**.

```python
from sklearn.preprocessing import RobustScaler

scaler = RobustScaler()
X_scaled = scaler.fit_transform(X)
```

## Normalizer (Row-wise scaling)

- Scales each **sample (row)** to unit norm (L1, L2, or max).
- Often used in **text [classification](../supervised-learning/classification/README.md)** or algorithms relying on cosine similarity.

```python
from sklearn.preprocessing import Normalizer

scaler = Normalizer(norm='l2')  # options: 'l1', 'l2', 'max'
X_scaled = scaler.fit_transform(X)
```

## Log Transformations

- Applied to **skewed data** to reduce the influence of extreme values.
- Makes distributions more symmetric.
- Example: income, count data, gene expression.

```python
import numpy as np
from sklearn.preprocessing import FunctionTransformer

log_transformer = FunctionTransformer(np.log1p, validate=True)
X_log = log_transformer.fit_transform(X)
```

## Notes & Best Practices

- **StandardScaler**: default choice for most algorithms (linear, [SVM](../supervised-learning/classification/svm.md), [PCA](../unsupervised-learning/dimensionality-reduction/pca.md)).
- **MinMaxScaler**: when features need to be in a bounded range ([KNN](../supervised-learning/classification/knn.md), neural nets).
- **RobustScaler**: when outliers are present.
- **Normalizer**: when row-wise normalization is needed (text, cosine similarity).
- **MaxAbsScaler**: when working with sparse data.
- **Log transform**: when distributions are highly skewed.

> Choose scaling technique based on **data distribution**, **model assumptions**, and **presence of outliers**.

## Related Concepts

- [K-Nearest Neighbors (KNN)](../supervised-learning/classification/knn.md)
- [Support Vector Machine (SVM)](../supervised-learning/classification/svm.md)
- [PCA](../unsupervised-learning/dimensionality-reduction/pca.md)
- [Pipeline Basics](../workflow/pipeline-basic.md)

[Back to Preprocessing](README.md)
