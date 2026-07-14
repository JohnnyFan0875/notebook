# PCA

**Principal Component Analysis (PCA)**: A dimensionality reduction technique that retains as much variance as possible.
This note focuses on **machine-learning usage**: PCA as feature extraction inside a preprocessing pipeline, especially before visualization, clustering, or downstream estimators. For the fuller multivariate-statistics treatment of loadings, scree logic, and variance interpretation, see [Statistics: Principal Component Analysis](../../../statistics/multivariate-analysis/pca.md).

- Typically starts by **standardizing the data**.
- Assumes that the data has **linear relationships**.
- Each **principal component (PC)** is a linear combination of the original features.
  - **PC1**: direction of maximum variance in the data.
  - **PC2**: direction of the second-highest variance, and so on.
- The principal components are orthogonal to each other, so PCA removes linear correlation in the transformed space.

## Simple Example (Iris Dataset)

```python
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt

# Load dataset
iris = load_iris()
X = iris.data  # Features (sepal length, sepal width, petal length, petal width)
y = iris.target  # Labels (species)
feature_names = iris.feature_names

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply PCA
pca = PCA(n_components=2)  # Reduce to 2 dimensions
X_pca = pca.fit_transform(X_scaled)

# Explained variance ratio
print(pca.explained_variance_ratio_)  # [0.9246, 0.0531]

# Loadings (contribution of each feature to PCs)
loadings = pca.components_
loadings_df = pd.DataFrame(
    loadings,
    columns=feature_names,
    index=[f'PC{i+1}' for i in range(len(loadings))]
)
print(loadings_df)

#      sepal length (cm)  sepal width (cm)  petal length (cm)  petal width (cm)
# PC1           0.521066         -0.269347           0.580413          0.564857
# PC2           0.377418          0.923296           0.024492          0.066942

# Visualization
plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, cmap='viridis')
plt.colorbar(label='Iris Species')
plt.xlabel('First Principal Component')
plt.ylabel('Second Principal Component')
plt.title('PCA of Iris Dataset')
plt.show()
```

### Output Example

- `pca.explained_variance_ratio_`: `[0.9246, 0.0531]` → PC1 explains ~92.5% variance, PC2 explains ~5.3%.
- `loadings_df`: shows how strongly each feature contributes to each principal component (positive or negative correlation).

## Choosing the Number of Components

- You can set a fixed count such as `n_components=2` when visualization is the goal.
- You can also set a variance target such as `n_components=0.9` to keep enough components to explain 90% of the variance.
- Plotting `explained_variance_ratio_` or its cumulative sum helps show where additional components stop adding much information.

## PCA in a Modeling Pipeline

- Fit scaling and PCA only on the training data to avoid leakage.
- In `scikit-learn`, a `Pipeline` is the safest way to combine `StandardScaler`, `PCA`, and a downstream estimator.
- High explained variance does not automatically mean better predictive performance, so always compare validation results.

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("reducer", PCA(n_components=0.9)),
    ("classifier", RandomForestClassifier(random_state=42))
])

pipe.fit(X_train, y_train)
score = pipe.score(X_test, y_test)
retained_variance = pipe["reducer"].explained_variance_ratio_.sum()
```

## Practical Reminders

- PCA is a feature extraction method, not feature selection, because the output variables are new components.
- If two variables are almost duplicates, simple correlation-based pruning may be easier to explain than PCA.
- PCA is often useful before clustering or visualization, but you should still inspect whether the transformed representation helps the downstream task.

## Related Concepts

- [Dimensionality Reduction](README.md)
- [Statistics: Principal Component Analysis](../../../statistics/multivariate-analysis/pca.md)
- [Feature Scaling](../../preprocessing/feature-scaling.md)
- [t-SNE](tsne.md)
- [Clustering](../clustering/README.md)

[Back to Dimensionality Reduction](README.md)
