# Gaussian Mixture Models

Gaussian Mixture Models assume the data were generated from a mixture of Gaussian distributions.
Unlike [K-Means](kmeans.md), they provide **soft cluster assignments**.

## Core Idea

- Each cluster is modeled as a Gaussian distribution
- Each point receives probabilities of belonging to each cluster
- Parameters are typically learned with the Expectation-Maximization algorithm

## Why Use GMM

- Clusters can have different shapes and covariance structures
- Probabilistic assignments are useful when cluster membership is uncertain

## Example

```python
from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

gmm = GaussianMixture(n_components=3, covariance_type="full", random_state=42)
gmm.fit(X_scaled)

labels = gmm.predict(X_scaled)
probs = gmm.predict_proba(X_scaled)
```

## Practical Notes

- Standardization is often helpful.
- Compare multiple `n_components` values.
- Use with caution when clusters are not approximately Gaussian.

## Related Concepts

- [Clustering](README.md)
- [Feature Scaling](../../preprocessing/feature-scaling.md)
- [K-Means Clustering](kmeans.md)
- [Model Diagnostics](../../interpretability-and-diagnostics/model-diagnostics.md)

[Back to Clustering](README.md)
