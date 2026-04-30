# Dimensionality Reduction



Dimensionality reduction simplifies high-dimensional data while trying to preserve important structure.

## Why It Matters

- Reduce noise and redundancy
- Speed up downstream models
- Visualize high-dimensional datasets
- Compress features before [clustering](../clustering/README.md) or modeling

## Topics

- [PCA](pca.md): linear projection maximizing variance
- [t-SNE](tsne.md): non-linear embedding for visualization
- [NMF](nmf.md): parts-based factorization for non-negative data

## Notes

- Use PCA when you want a stable linear transformation and explained variance.
- Use t-SNE mainly for visualization, not as a general-purpose [feature engineering](../../foundations/feature-engineering-principles.md) default.
- Use NMF when the data are non-negative and interpretability of latent components matters.

[Back to Unsupervised Learning](../README.md)
