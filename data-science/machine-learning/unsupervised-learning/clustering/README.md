# Clustering

Clustering groups observations based on similarity when no labeled target is available.

## Topics

- [K-Means Clustering](kmeans.md)
- [Hierarchical Clustering](hierarchical.md)
- [DBSCAN](dbscan.md)
- [Gaussian Mixture Models](gaussian-mixture.md)

## Notes

- K-Means is simple and fast but assumes roughly spherical clusters.
- Hierarchical clustering is useful for exploratory analysis and dendrograms.
- DBSCAN handles noise and irregular shapes.
- Gaussian mixtures provide soft cluster assignments.

## Interpretation Reminders

- A cluster label is only meaningful after you summarize what is inside that cluster.
- Standardization often changes results substantially because distance is scale-sensitive.
- If several methods disagree strongly, the data may not have one clear clustering structure.

## Common Workflows

- Numeric tabular data: standardize first, then compare K-Means, hierarchical clustering, and density-based methods.
- Text data: convert documents into vector representations such as TF-IDF before clustering.
- Image data: cluster pixel values to summarize dominant colors or identify coarse visual regions.

## Choosing Between Common Methods

- Hierarchical clustering is deterministic once you choose a distance metric and linkage rule, so repeated runs on the same data give the same tree.
- K-Means is usually faster on larger datasets, but its result can change across random initializations unless you use multiple starts.
- Hierarchical clustering can work with many distance definitions, while standard K-Means is fundamentally tied to Euclidean-style centroid geometry.

[Back to Unsupervised Learning](../README.md)
