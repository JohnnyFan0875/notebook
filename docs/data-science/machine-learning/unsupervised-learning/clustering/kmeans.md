# K-Means Clustering

## Overview

K-Means is one of the most widely used **unsupervised clustering algorithms**.
It partitions data into _k_ clusters, where each data point belongs to the cluster with the nearest centroid.

- **Centroid**: The mean position of all the points within a cluster.
  - Closer centroids → similar clusters
  - Large differences in cluster sizes → may indicate that data does not naturally divide into equal-sized groups

## Key Concepts

### Cluster Quality

- **Intra-cluster variance**: ideally small → data points should be close to their centroid
- **Inter-cluster distance**: ideally large → clusters should be well-separated
- **Silhouette Score**
  - Measures how similar each point is to its own cluster compared to other clusters
  - Range: `[-1, 1]` (higher is better)
  - Requires `n_clusters > 1`
- **Inertia**
  - Sum of squared distances of points to their closest centroid
  - Lower value → better compactness
  - Commonly used in the **elbow method** to determine the optimal number of clusters

## Python Example

```python
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import silhouette_score

# Generate synthetic data: 3 clusters, 2 features
X, y = make_blobs(n_samples=300, centers=3, n_features=2, random_state=42)

# Train KMeans (assuming we know k=3)
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(X)

# Alternative: with scaling
scaler = StandardScaler()
pipeline = make_pipeline(scaler, KMeans(n_clusters=3))
pipeline.fit(X)

# Predict new data
new_data = np.array([[5, 3], [-3, -4], [2, -6]])
new_labels = kmeans.predict(new_data)

# Cluster attributes
centroids = kmeans.cluster_centers_     # coordinates of centroids (shape: k x n_features)
labels = kmeans.labels_                 # cluster assignment for each sample
inertia_values = kmeans.inertia_        # total within-cluster sum of squares
sil_score = silhouette_score(X, labels)
```

## Choosing the Number of Clusters

- **Elbow Method**: Plot inertia vs. number of clusters → look for the “elbow” point
- **Silhouette Analysis**: Compare average silhouette score across different _k_
- **Domain Knowledge**: Sometimes business or biological context defines the meaningful number of groups

## Assumptions & Limitations

- Works best when clusters are roughly spherical and equally sized
- Sensitive to outliers → can distort centroids
- Requires specifying _k_ in advance
- Results may vary with initialization (use `n_init` parameter to run multiple times)

## Practical Tips

- Always scale features before applying K-Means
- Use `random_state` for reproducibility
- If clusters are not well-separated, try other methods (e.g., [DBSCAN](dbscan.md), [Gaussian Mixture](gaussian-mixture.md) Models)

## Related Concepts

- [Clustering](README.md)
- [Feature Scaling](../../preprocessing/feature-scaling.md)
- [PCA](../dimensionality-reduction/pca.md)
- [Hierarchical Clustering](hierarchical.md)

[Back to Clustering](README.md)
