# Hierarchical Clustering



## Overview

Hierarchical clustering is an **unsupervised learning method** that groups data points based on similarity or distance, without requiring labeled outputs.

Key characteristics:

- Builds a **tree-like structure** called a **dendrogram** to represent cluster relationships
- Can reveal nested structures within data
- Sensitive to noise and outliers

## Types of Hierarchical Clustering

- **Agglomerative (Bottom-Up) Approach**
  - Start with each data point as its own cluster
  - Iteratively merge the two closest clusters
- **Divisive (Top-Down) Approach**
  - Start with all data points in one single cluster
  - Iteratively split clusters into smaller groups

## Linkage Methods

The **linkage method** determines how distances between clusters are calculated:

- **Single linkage**: Minimum distance between points across clusters
- **Complete linkage**: Maximum distance between points across clusters
- **Average linkage**: Average distance between all pairs of points across clusters
- **Ward’s method**: Minimizes the variance within clusters

![Image](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*7d7DTLiwe0MJEQfPl0PLXw.png)

## Python Example

```python
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

# Generate synthetic data
X, _ = make_blobs(n_samples=100, centers=4, random_state=42)

# Perform hierarchical clustering with complete linkage
linked = linkage(X, method='complete')

# Assign cluster labels (same label = same cluster), height=6
cluster_labels = fcluster(linked, 6, criterion='distance')

# Visualization
plt.figure(figsize=(10, 7))
dendrogram(linked, leaf_rotation=90, leaf_font_size=6)
plt.title('Dendrogram of Hierarchical Clustering')
plt.xlabel('Sample index')
plt.ylabel('Distance')
plt.show()
```

## Advantages

- No need to pre-specify the number of clusters
- Produces a hierarchy that can be cut at different levels for flexible grouping
- Works well for small to medium datasets

## Limitations

- Computationally expensive for large datasets (`O(n^3)` complexity)
- Sensitive to noise and outliers
- Choice of linkage method can significantly affect results

## Practical Tips

- Use **Ward’s linkage** when clusters are expected to be spherical
- Scale features before clustering
- For large datasets, consider **agglomerative clustering with truncated linkage** or alternatives like **[K-Means](kmeans.md) / [DBSCAN](dbscan.md)**

## Related Concepts

- [Clustering](README.md)
- [Feature Scaling](../../preprocessing/feature-scaling.md)
- [K-Means Clustering](kmeans.md)
- [DBSCAN](dbscan.md)

[Back to Clustering](README.md)
