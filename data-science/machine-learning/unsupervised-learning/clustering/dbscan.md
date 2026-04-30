# DBSCAN



DBSCAN stands for **Density-Based Spatial Clustering of Applications with Noise**.
It groups dense regions together and labels sparse points as noise.

## Why It Is Useful

- Does not require specifying the number of clusters in advance
- Can discover irregular cluster shapes
- Naturally identifies outliers

## Key Hyperparameters

- `eps`: neighborhood radius
- `min_samples`: minimum number of nearby points needed to form a dense region

## Strengths

- Good for spatially separated, non-spherical clusters
- Useful when outlier detection matters

## Limitations

- Sensitive to the choice of `eps`
- Struggles when density varies strongly across clusters
- Distance scaling matters

## Example

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", DBSCAN(eps=0.5, min_samples=5))
])

labels = pipeline.fit_predict(X)
```

## Related Concepts

- [Clustering](README.md)
- [Feature Scaling](../../preprocessing/feature-scaling.md)
- [K-Means Clustering](kmeans.md)
- [Gaussian Mixture Models](gaussian-mixture.md)

[Back to Clustering](README.md)
