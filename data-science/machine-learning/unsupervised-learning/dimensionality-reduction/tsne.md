# t-SNE



## Overview

- **t-SNE (t-Distributed Stochastic Neighbor Embedding)** is a dimensionality reduction technique designed to visualize high-dimensional data in a lower-dimensional space (commonly 2D or 3D).
- Particularly useful for revealing **clustering structures** or other complex patterns in **non-linear datasets**.
- Unlike [PCA](pca.md), which is linear, t-SNE captures non-linear relationships between data points.
- **Important note:** The axes in t-SNE plots do **not** correspond to specific features of the original dataset. The emphasis is on **relative distances** and local neighborhoods between points.

## Key Characteristics

- Preserves local structure of the data (similar points stay close together).
- Often used in **exploratory data analysis** for biological data (e.g., single-cell RNA-seq), image embeddings, and NLP.
- Computationally more expensive than [PCA](pca.md).
- Requires tuning of hyperparameters (notably `perplexity` and `learning_rate`).

## Example: Visualizing the Iris Dataset with t-SNE

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE

# Load dataset
iris = load_iris()
X = iris.data  # Features
y = iris.target  # Labels

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply t-SNE
tsne = TSNE(n_components=2, random_state=42)
X_tsne = tsne.fit_transform(X_scaled)

# Plot results
plt.figure(figsize=(8, 6))
scatter = plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=y, cmap='viridis', s=50)
plt.title('t-SNE Visualization of Iris Dataset')
plt.xlabel('t-SNE Component 1')
plt.ylabel('t-SNE Component 2')
plt.colorbar(scatter, ticks=[0, 1, 2], label='Iris Species')
plt.show()
```

## Practical Tips

- **Perplexity**: Balances attention between local and global aspects of the data. Common values: 5–50.
- **Learning rate**: Too low → data may clump; too high → scattered noise.
- **Reproducibility**: Set `random_state` for consistent plots.

## Related Concepts

- [Dimensionality Reduction](README.md)
- [PCA](pca.md)
- [Clustering](../clustering/README.md)
- [Feature Scaling](../../preprocessing/feature-scaling.md)

[Back to Dimensionality Reduction](README.md)
