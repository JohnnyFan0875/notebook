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

## 直覺理解

你可以把 DBSCAN 想成在資料空間中找「夠擁擠」的區域。只要某個點附近在 `eps` 半徑內有足夠多鄰居，它就能成為核心點，並把附近點一路串成一個 cluster；太孤立的點則會被標成 noise。

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

## How to Tune in Practice

- 先做標準化，讓距離尺度有意義。
- 固定 `min_samples` 後，用 k-distance plot 幫助選 `eps`。
- 若不同密度的群同時存在，DBSCAN 常會很掙扎，這時要考慮其他方法。

## Common Pitfalls

- 把被標成 `-1` 的點全當成錯誤資料，其實它們也可能是真實少數型態。
- 沒有標準化就直接跑距離型方法。
- 看到分群結果少就調大 `eps`，最後把原本不同群硬併在一起。

## Related Concepts

- [Clustering](README.md)
- [Feature Scaling](../../preprocessing/feature-scaling.md)
- [K-Means Clustering](kmeans.md)
- [Gaussian Mixture Models](gaussian-mixture.md)

[Back to Clustering](README.md)
