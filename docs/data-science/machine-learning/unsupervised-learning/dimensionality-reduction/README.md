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

## Feature Selection vs. Feature Extraction

- **Feature selection** keeps a subset of the original variables and drops the rest.
- **Feature extraction** creates new variables by combining or transforming the originals.
- Correlation filtering, tree-based importance thresholds, and RFE are selection approaches.
- PCA is an extraction approach because the principal components are new linear combinations of the original features.

## Practical Workflow

- Start by asking whether you need interpretability of original variables or just a lower-dimensional representation.
- Remove obviously redundant features first when strong pairwise correlation is creating noise.
- Then compare feature selection and feature extraction approaches in a validation pipeline instead of assuming lower dimension always improves the model.

## Unsupervised vs. Supervised Selection

- **Unsupervised feature selection** uses only the predictors, without looking at the target.
- Common examples include missing-value filters, low-variance filters, and correlation filters.
- **Supervised feature selection** uses information about how predictors relate to the target variable.
- Supervised selection can be very effective, but it must be fit inside the training workflow to avoid leakage into validation or test data.

[Back to Unsupervised Learning](../README.md)
