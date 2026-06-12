# Clustering

**Clustering** is an **unsupervised** learning task — it finds natural groupings in data without using any labels. Where classification learns from known group memberships, clustering *discovers* group structure from the data itself.

Key point: The core question of cluster analysis: "There are several natural groups in the data. What are the characteristics of each group?" This question is conducted without a standard answer. There is no absolute criterion for whether a clustering result is good or bad - you have to combine mathematical metrics and domain knowledge to judge whether the results are meaningful.

## Three Families of Clustering

| Family | Representative Method | Core Idea | Key Parameter |
| ----------------- | --------------------- | ---------------------------------------------- | --------------------- |
| **Partitional** | K-Means | Assign each point to the nearest centroid | k (number of clusters) |
| **Hierarchical** | Agglomerative HC | Merge closest clusters bottom-up | Linkage method, cut height |
| **Density-based** | DBSCAN | Clusters are dense regions separated by sparse space | ε, min_samples |

## Preprocessing for Clustering

Like PCA, clustering algorithms are **distance-based** and highly sensitive to scale. Always standardize before clustering.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler

iris = load_iris(as_frame=True)
df = iris.frame
df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)

num_cols = ['sepal length (cm)', 'sepal width (cm)',
            'petal length (cm)', 'petal width (cm)']

scaler   = StandardScaler()
X_scaled = scaler.fit_transform(df[num_cols])
```

## K-Means Clustering

K-Means partitions n observations into k clusters by iteratively:
1. Assigning each observation to the **nearest centroid**
2. Recomputing each centroid as the **mean of its assigned observations**
3. Repeating until assignments stop changing

```python
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

# Fit K-Means with k=3 (we know iris has 3 species)
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
labels_km = kmeans.fit_predict(X_scaled)

df['cluster_km'] = labels_km

# Compare clusters to true labels
from sklearn.metrics import adjusted_rand_score, silhouette_score
ari = adjusted_rand_score(iris.target, labels_km)
sil = silhouette_score(X_scaled, labels_km)

print(f"Adjusted Rand Index: {ari:.3f}  (1.0 = perfect match with true labels)")
print(f"Silhouette Score:    {sil:.3f}  (higher = more distinct clusters)")
```

### Choosing k: The Elbow Method

```python
inertias   = []   # within-cluster sum of squares (WCSS)
sil_scores = []
k_range    = range(2, 11)

for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)
    sil_scores.append(silhouette_score(X_scaled, km.labels_))

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Elbow plot
axes[0].plot(k_range, inertias, 'o-', color='steelblue', linewidth=2)
axes[0].set_xlabel('Number of Clusters (k)')
axes[0].set_ylabel('Inertia (WCSS)')
axes[0].set_title('Elbow Method')
axes[0].set_xticks(list(k_range))

# Silhouette score
axes[1].plot(k_range, sil_scores, 'o-', color='tomato', linewidth=2)
axes[1].set_xlabel('Number of Clusters (k)')
axes[1].set_ylabel('Silhouette Score')
axes[1].set_title('Silhouette Score by k')
axes[1].set_xticks(list(k_range))

plt.tight_layout()
plt.show()
```

**Interpreting the elbow and silhouette together:**

| Signal | Recommendation |
| ------------------------------------------- | ---------------------------------------- |
| Clear elbow at k=3 AND silhouette peaks at k=3 | Strong evidence for k=3 |
| Elbow unclear, silhouette peaks at k=2 | Trust silhouette — simpler is better |
| Both curves decrease monotonically | Data may not have clear cluster structure |
| Elbow at 3 but silhouette peaks at 5 | Investigate both; use domain knowledge |

Warning: There is no single "correct" k. The elbow and silhouette give guidance, but the final choice must make sense for your problem. Ask: "Do these k groups have distinct, interpretable profiles?"

### Visualizing K-Means Results

```python
from sklearn.decomposition import PCA

# Project to 2D via PCA for visualization
pca2 = PCA(n_components=2)
X_2d = pca2.fit_transform(X_scaled)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))

palette_km   = {0: '#2196F3', 1: '#4CAF50', 2: '#F44336'}
palette_true = {'setosa': '#4CAF50', 'versicolor': '#2196F3', 'virginica': '#F44336'}

# K-Means result
for label, color in palette_km.items():
    mask = labels_km == label
    axes[0].scatter(X_2d[mask, 0], X_2d[mask, 1],
                    color=color, alpha=0.6, s=50, label=f'Cluster {label}')
axes[0].set_title(f'K-Means (k=3)\nARI = {ari:.3f}')
axes[0].set_xlabel('PC1')
axes[0].set_ylabel('PC2')
axes[0].legend()

# True labels
for species, color in palette_true.items():
    mask = df['species'] == species
    axes[1].scatter(X_2d[mask, 0], X_2d[mask, 1],
                    color=color, alpha=0.6, s=50, label=species)
axes[1].set_title('True Species Labels')
axes[1].set_xlabel('PC1')
axes[1].set_ylabel('PC2')
axes[1].legend()

plt.tight_layout()
plt.show()
```

Tip: ARI (Adjusted Rand Index) measures how well the clusters match the true labels, correcting for chance. ARI = 1 means perfect agreement; ARI ≈ 0 means no better than random. In real unsupervised problems you won't have true labels — use silhouette score instead.

## Hierarchical Clustering

Hierarchical clustering builds a **tree of nested clusters** (a dendrogram) without requiring a pre-specified k.

```python
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import pdist

# Compute linkage matrix
Z = linkage(X_scaled, method='ward')  # Ward minimizes within-cluster variance

# Plot dendrogram
plt.figure(figsize=(12, 5))
dendrogram(
    Z,
    labels=df['species'].values,
    leaf_rotation=90,
    leaf_font_size=7,
    color_threshold=6,
    above_threshold_color='gray'
)
plt.title('Hierarchical Clustering Dendrogram (Ward Linkage)')
plt.xlabel('Observation')
plt.ylabel('Distance')
plt.tight_layout()
plt.show()
```

**Cut the dendrogram to get cluster assignments:**

```python
# Cut at height to produce k=3 clusters
labels_hc = fcluster(Z, t=3, criterion='maxclust')
df['cluster_hc'] = labels_hc

ari_hc = adjusted_rand_score(iris.target, labels_hc)
sil_hc = silhouette_score(X_scaled, labels_hc)
print(f"HC — ARI: {ari_hc:.3f},  Silhouette: {sil_hc:.3f}")
```

**Linkage methods compared:**

| Linkage | Merges by | Best For | Weakness |
| ----------- | -------------------------------- | -------------------------------------- | --------------------------------- |
| **Ward** | Minimum variance increase | Compact, similarly-sized clusters | Assumes roughly equal-sized groups |
| **Complete** | Maximum distance between clusters | Well-separated, compact clusters | Sensitive to outliers |
| **Average** | Mean distance between clusters | Balanced; good default | Less consistent with visual intuition |
| **Single** | Minimum distance between clusters | Elongated, chain-like clusters | "Chaining" problem |

Tip: Ward linkage is the most commonly recommended starting point for most datasets. It tends to produce compact, clearly separated clusters and often agrees with visual inspection.

## DBSCAN: Density-Based Clustering

DBSCAN identifies **dense regions** of points as clusters, leaving low-density points as **noise (outliers)**. Unlike K-Means, it does not require specifying k and can find non-spherical clusters.

```python
from sklearn.cluster import DBSCAN

dbscan = DBSCAN(eps=0.8, min_samples=5)
labels_db = dbscan.fit_predict(X_scaled)

n_clusters = len(set(labels_db)) - (1 if -1 in labels_db else 0)
n_noise    = (labels_db == -1).sum()

print(f"Clusters found: {n_clusters}")
print(f"Noise points:   {n_noise} ({n_noise/len(labels_db)*100:.1f}%)")

if n_clusters > 1:
    mask = labels_db != -1
    sil_db = silhouette_score(X_scaled[mask], labels_db[mask])
    print(f"Silhouette Score (excluding noise): {sil_db:.3f}")
```

**Tuning DBSCAN's two key parameters:**

| Parameter | Effect of Increasing | Effect of Decreasing |
| -------------- | ------------------------------- | -------------------------------------- |
| **ε (eps)** | Fewer, larger clusters | More clusters, more noise points |
| **min_samples** | Fewer, larger clusters; more noise | Smaller clusters identified |

```python
# k-distance plot to find a good ε
from sklearn.neighbors import NearestNeighbors

nbrs = NearestNeighbors(n_neighbors=5).fit(X_scaled)
distances, _ = nbrs.kneighbors(X_scaled)
distances_sorted = np.sort(distances[:, -1])

plt.figure(figsize=(8, 4))
plt.plot(distances_sorted, color='steelblue', linewidth=2)
plt.axhline(0.8, color='tomato', linestyle='--', label='Chosen ε = 0.8')
plt.xlabel('Points (sorted by distance to 5th nearest neighbor)')
plt.ylabel('5-NN Distance')
plt.title('k-Distance Plot for ε Selection')
plt.legend()
plt.tight_layout()
plt.show()
```

Tip: In the k-distance plot, look for the "knee" — the point where the curve starts bending sharply upward. The distance at the knee is a good candidate for ε.

## Comparing the Three Methods

```python
from sklearn.metrics import adjusted_rand_score, silhouette_score

results = pd.DataFrame({
    'Method':    ['K-Means (k=3)', 'Hierarchical (Ward, k=3)', 'DBSCAN (ε=0.8)'],
    'ARI':       [adjusted_rand_score(iris.target, labels_km),
                  adjusted_rand_score(iris.target, labels_hc),
                  adjusted_rand_score(iris.target, labels_db)],
    'Silhouette':[silhouette_score(X_scaled, labels_km),
                  silhouette_score(X_scaled, labels_hc),
                  silhouette_score(X_scaled[labels_db != -1], labels_db[labels_db != -1])
                  if (labels_db != -1).sum() > 0 else np.nan]
}).round(3)

print(results.to_string(index=False))
```

**When to use which method:**

| Scenario | Best Method |
| ----------------------------------------- | ------------------------ |
| Know approximate k; clusters are compact | **K-Means** |
| Unknown k; want to explore hierarchy | **Hierarchical (Ward)** |
| Non-spherical clusters; outliers present | **DBSCAN** |
| Very large dataset (>100k obs) | **K-Means** (fastest) |
| Need nested cluster structure | **Hierarchical** |

## Cluster Profiling

Finding clusters is only half the job. You must also **describe what makes each cluster distinctive**.

```python
df['cluster_km'] = labels_km

# Cluster means for each variable
profile = df.groupby('cluster_km')[num_cols].mean().round(3)
print("Cluster Profiles (means):")
print(profile)

# Heatmap of normalized cluster profiles
profile_norm = (profile - profile.mean()) / profile.std()

plt.figure(figsize=(8, 4))
sns.heatmap(profile_norm, annot=True, fmt='.2f',
            cmap='RdBu_r', center=0, linewidths=0.5)
plt.title('Cluster Profile Heatmap (Standardized)')
plt.ylabel('Cluster')
plt.tight_layout()
plt.show()
```

Tip: Always profile your clusters by computing mean (or median for skewed variables) of each feature per cluster. This is what transforms a label like "Cluster 2" into a meaningful description like "large flowers with long petals."

## Key Takeaways

| Concept | Key Point |
| ------------------------------------ | --------------------------------------------------------------------------------- |
| **Standardize before clustering** | Distance-based methods are scale-sensitive — this step is not optional |
| **Elbow + silhouette for k** | Use both to choose k; the "best" k must also make business/domain sense |
| **Ward linkage is the safe default** | For hierarchical clustering, Ward usually gives the most interpretable results |
| **DBSCAN finds noise** | Points labeled −1 are genuine outliers, not forced into a cluster |
| **ARI needs true labels** | In real unsupervised problems, use silhouette score instead |
| **Always profile clusters** | Cluster labels are meaningless without describing what characterizes each group |

## Clusters Are Hypotheses About Structure

A clustering result is not automatically evidence that natural groups truly exist in the world.

Good follow-up checks:

- stability under resampling
- sensitivity to scaling / preprocessing
- interpretability in domain language

Tip: Clustering is exploratory until validated.
