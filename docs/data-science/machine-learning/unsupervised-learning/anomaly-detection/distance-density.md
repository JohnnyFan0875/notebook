# Distance- and Density-Based Methods

Distance- and density-based anomaly detectors treat unusual observations as points that are far from their neighbors, live in sparse regions, or both.

These methods are often intuitive, but they are also highly sensitive to feature scaling and distance choice.

## KNN-Based Outlier Detection

KNN-style anomaly detection uses neighbor distances to assign anomaly scores. A point that is far from its nearest neighbors looks more suspicious.

Typical idea:

1. choose a distance metric
2. find the `k` nearest neighbors of each point
3. use neighbor distance as an anomaly score

```python
from pyod.models.knn import KNN

knn = KNN(n_neighbors=20, contamination=0.01, n_jobs=-1)
knn.fit(X)

probs = knn.predict_proba(X)
is_outlier = probs[:, 1] > 0.55
```

Key point: KNN methods are simple because the anomaly score comes directly from neighborhood structure rather than a more elaborate model.

## Choosing `k`

`k` controls how local the detector is:

| `k` choice | Tends to emphasize |
| ---------- | ------------------ |
| Smaller `k` | Very local structure, sharper sensitivity |
| Larger `k` | Broader neighborhoods, smoother scoring |

If `k` is too small, the detector becomes unstable. If `k` is too large, local anomalies may get washed out.

## Distance Metrics Matter

Common choices:

- Euclidean distance: default for many continuous settings
- Manhattan distance: often more robust when dimensions are sparse or axis-aligned
- Minkowski distance: general family containing both Euclidean and Manhattan

Warning: Distances are meaningless when one feature dominates the scale. Standardize or otherwise normalize before trusting neighbor-based anomaly scores.

## Local Density Methods

KNN is not the only neighborhood approach. Methods such as **Local Outlier Factor (LOF)** compare a point's density to the densities of its neighbors.

This can help when:

- the dataset has clusters of different densities
- global isolation is not the main issue
- a point is normal globally but strange locally

Tip: LOF is often a better fit than raw KNN distance when the data has heterogeneous neighborhoods.

### How To Read LOF

LOF is a ratio-style score:

- `LOF ≈ 1`: local density is similar to neighbors
- `LOF > 1`: point is sparser than its neighborhood
- larger LOF values: increasingly suspicious local anomalies

Key point: LOF is mainly useful when you care about **local** anomalies rather than only globally isolated points.

### Global vs. Local Anomalies

This distinction helps explain why methods disagree:

| Type | Meaning | Often detected well by |
| ---- | ------- | ---------------------- |
| **Global anomaly** | Far from the dataset as a whole | KNN distance, Isolation Forest |
| **Local anomaly** | Looks odd relative to nearby points, even if not globally extreme | LOF |

Tip: If KNN distance misses something that clearly looks suspicious inside a dense subgroup, try a local-density method before assuming the data has no anomaly signal.

### Mixed Data and Gower Distance

Euclidean-style distances assume numeric features on a common scale. That breaks down when a dataset mixes:

- continuous variables
- ordinal values
- binary flags
- nominal categories

In these settings, **Gower distance** is often a better choice because it can combine numeric and categorical features into one dissimilarity measure.

```r
library(cluster)

sat_dist <- daisy(sat[, -1], metric = "gower")
sat_lof  <- lof(sat_dist, k = 10)
```

Warning: If you force mixed-type data into a purely numeric Euclidean distance without thinking carefully, the anomaly score may mostly reflect encoding artifacts instead of real abnormality.

## Strengths and Weaknesses

| Strength | Weakness |
| -------- | -------- |
| Intuitive scoring logic | Sensitive to scaling |
| Good for local anomalies | Runtime can grow quickly with dataset size |
| Flexible metric choices | Choice of `k` can be unstable |
| Can expose multivariate oddities | High-dimensional distance can degrade badly |
