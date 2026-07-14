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

### How To Read the Elbow Method

- The elbow plot is only a heuristic, not a proof that one `k` is correct.
- A smooth curve with no obvious bend often means the data does not have one clean cluster count.
- If the elbow is ambiguous, compare with silhouette analysis or a gap statistic style approach.
- Even when the elbow suggests a value, you still need to inspect whether the resulting clusters are interpretable.

## Assumptions & Limitations

- Works best when clusters are roughly spherical and equally sized
- Sensitive to outliers → can distort centroids
- Requires specifying _k_ in advance
- Results may vary with initialization (use `n_init` parameter to run multiple times)

## Practical Tips

- Always scale features before applying K-Means
- Use `random_state` for reproducibility
- If clusters are not well-separated, try other methods (e.g., [DBSCAN](dbscan.md), [Gaussian Mixture](gaussian-mixture.md) Models)

### Why Scaling Matters

- K-Means is distance-based, so variables with larger numeric ranges can dominate the result.
- This issue appears both when units differ, such as centimeters vs. dollars, and when units match but variances differ greatly.
- In practice, standardization is usually the safe default before clustering.

### Python Implementation Notes

- In `scikit-learn`, the main summary statistic is usually `inertia_`, which is the within-cluster sum of squares.
- In `scipy.cluster.vq.kmeans`, the returned `distortion` plays a similar role for elbow-style comparisons.
- A common SciPy workflow is:
  1. standardize observations
  2. estimate centroids with `kmeans(...)`
  3. assign labels with `vq(...)`
- Because centroid initialization is random, it is good practice to run K-Means with multiple starts and compare the best solution rather than trusting one run.

### Common Use Cases

- Customer or user segmentation from behavioral variables
- Color quantization, where pixels are clustered by RGB values to find dominant colors
- Document grouping after converting text into vector features such as TF-IDF

## Customer Segmentation With RFM

One of the most common business uses of K-Means is **customer segmentation** based on behavioral summaries. A classic feature set is **RFM**:

- **Recency**: how recently the customer purchased
- **Frequency**: how often the customer purchased
- **Monetary value**: how much the customer spent

This is useful because customer-level transaction logs are often too granular for direct clustering. RFM compresses repeated purchase behavior into a compact customer profile.

### A Practical RFM Workflow

1. aggregate transaction logs to one row per customer
2. compute recency, frequency, and monetary value
3. inspect skewness and outliers
4. apply a log transform if the positive-valued variables are heavily skewed
5. standardize the transformed features
6. compare several values of `k`
7. profile each cluster in business terms

Warning: the order matters. If you want to use a log transform, do it **before** standardization, because standardization creates negative values and `log(...)` would no longer be valid.

```python
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

snapshot_date = orders['InvoiceDate'].max() + pd.Timedelta(days=1)

rfm = (
    orders.groupby('CustomerID')
    .agg(
        Recency=('InvoiceDate', lambda x: (snapshot_date - x.max()).days),
        Frequency=('InvoiceNo', 'nunique'),
        MonetaryValue=('Sales', 'sum'),
    )
)

rfm_log = np.log(rfm[['Recency', 'Frequency', 'MonetaryValue']])
X = StandardScaler().fit_transform(rfm_log)

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
rfm['Cluster'] = kmeans.fit_predict(X)
```

Tip: if recency contains zeros, use a safer transform such as `np.log1p(...)` after confirming the business meaning of zero.

### Profiling Clusters Matters More Than The Label Number

The cluster IDs themselves are arbitrary. What matters is the profile:

```python
cluster_profile = rfm.groupby('Cluster')[['Recency', 'Frequency', 'MonetaryValue']].mean()
cluster_size = rfm['Cluster'].value_counts().sort_index()
```

Typical interpretation questions:

- which segment is most recent and highest value?
- which segment buys frequently but spends little per order?
- which segment looks inactive or at risk of churn?

### RFM Is Not Always A Clustering Problem

Some teams use RFM without K-Means at all. Instead, they convert each metric into score bands using:

- quantiles or percentiles
- Pareto-style cuts such as 80/20
- custom thresholds based on business knowledge

That approach is often easier to explain operationally, while K-Means is better when you want the grouping to be learned from the joint geometry of the data rather than from hand-written cutoffs.

### Two Useful Ways To Compare Segments

After clustering, two views are especially practical:

- **snake plot**: compare each cluster's average standardized attributes on the same line chart
- **relative importance table**: compare cluster averages against the overall population average

```python
relative_importance = (
    cluster_profile / rfm[['Recency', 'Frequency', 'MonetaryValue']].mean()
    - 1
)
```

If a relative importance value is near `0`, that cluster is close to the population average on that feature. Large positive or negative values make the distinguishing attributes easier to spot.

## Related Concepts

- [Clustering](README.md)
- [Feature Scaling](../../preprocessing/feature-scaling.md)
- [PCA](../dimensionality-reduction/pca.md)
- [Hierarchical Clustering](hierarchical.md)

[Back to Clustering](README.md)
