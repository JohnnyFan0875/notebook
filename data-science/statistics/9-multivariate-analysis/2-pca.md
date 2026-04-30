# 2. Principal Component Analysis (PCA)

**PCA** is a dimension reduction technique that transforms a set of correlated variables into a smaller set of **uncorrelated components**, each capturing as much variance as possible. It is one of the most widely used techniques in multivariate analysis — both as a standalone analysis and as a preprocessing step before clustering or regression.

> 📌 **PCA 的核心思想**：在高維空間中，資料通常不是均勻散佈的——它沿著某些方向分散得多，沿著其他方向幾乎沒有變化。PCA 找到這些「最大變異方向」（主成分），讓你用更少的維度保留最多的資訊。這不是捨棄資料，而是找到資料最本質的結構。

---

## 2.1 Intuition: What PCA Does

Imagine you have 4 highly correlated variables. PCA finds a new coordinate system where:

- **PC1** points in the direction of maximum variance in the data
- **PC2** points in the direction of maximum remaining variance, **orthogonal** (perpendicular) to PC1
- **PC3** captures the next most variance, orthogonal to PC1 and PC2
- ... and so on

The key properties:
- Principal components are **uncorrelated** by construction
- Each successive PC captures less variance than the previous one
- The first few PCs often capture most of the total variance

> 💡 PCA is a **rotation** of the original coordinate axes — no data is added or removed. Every observation can be expressed exactly in the new PC coordinate system; we just choose to keep only the first k components.  
> PCA 是座標系的旋轉，不是資料的丟棄。原始資料可以完整地用主成分表示，我們只是選擇保留最重要的幾個方向。

---

## 2.2 The Math Behind PCA

PCA is based on the **eigendecomposition of the covariance matrix** (or equivalently, the SVD of the centered data matrix).

$$\Sigma = V \Lambda V^T$$

where:
- Σ = covariance matrix of the (standardized) data
- V = matrix of eigenvectors (the principal component directions = **loadings**)
- Λ = diagonal matrix of eigenvalues (= variance captured by each PC)

> ⚠️ **PCA is scale-sensitive.** Variables measured in large units dominate the first components. Always **standardize** (subtract mean, divide by SD) before applying PCA unless all variables are already on the same scale.  
> PCA 對尺度敏感：單位大的變數會主導分析。標準化是必要步驟，不是可選的。

---

## 2.3 Applying PCA with scikit-learn

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# Load data
iris = load_iris(as_frame=True)
df = iris.frame
df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)

num_cols = ['sepal length (cm)', 'sepal width (cm)',
            'petal length (cm)', 'petal width (cm)']

# Step 1: Standardize
scaler  = StandardScaler()
X_scaled = scaler.fit_transform(df[num_cols])

# Step 2: Fit PCA (keep all components first to diagnose)
pca = PCA()
X_pca = pca.fit_transform(X_scaled)

print("Explained variance ratio per component:")
for i, var in enumerate(pca.explained_variance_ratio_):
    print(f"  PC{i+1}: {var:.3f} ({var*100:.1f}%)")
print(f"\nCumulative: {np.cumsum(pca.explained_variance_ratio_).round(3)}")
```

**Expected output:**
```
  PC1: 0.730 (73.0%)
  PC2: 0.229 (22.9%)
  PC3: 0.037 (3.7%)
  PC4: 0.005 (0.5%)

Cumulative: [0.730 0.958 0.995 1.000]
```

> 💡 Two components already capture 95.8% of total variance for this dataset. The 4-dimensional iris data is effectively 2-dimensional.

---

## 2.4 Scree Plot: Choosing the Number of Components

The **scree plot** shows the variance explained by each component. Look for an "elbow" — the point where additional components add little new information.

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Individual explained variance
axes[0].bar(range(1, len(pca.explained_variance_ratio_) + 1),
            pca.explained_variance_ratio_,
            color='steelblue', edgecolor='white', alpha=0.85)
axes[0].plot(range(1, len(pca.explained_variance_ratio_) + 1),
             pca.explained_variance_ratio_,
             'o-', color='tomato', linewidth=2)
axes[0].set_xlabel('Principal Component')
axes[0].set_ylabel('Explained Variance Ratio')
axes[0].set_title('Scree Plot')
axes[0].set_xticks(range(1, 5))

# Cumulative explained variance
cumvar = np.cumsum(pca.explained_variance_ratio_)
axes[1].plot(range(1, len(cumvar) + 1), cumvar, 'o-',
             color='steelblue', linewidth=2, markersize=8)
axes[1].axhline(0.95, color='tomato', linestyle='--', label='95% threshold')
axes[1].axhline(0.90, color='seagreen', linestyle='--', label='90% threshold')
axes[1].set_xlabel('Number of Components')
axes[1].set_ylabel('Cumulative Explained Variance')
axes[1].set_title('Cumulative Explained Variance')
axes[1].set_xticks(range(1, 5))
axes[1].legend()

plt.tight_layout()
plt.show()
```

**Common rules for choosing k (number of components):**

| Rule                          | Description                                           | Caution                              |
| ----------------------------- | ----------------------------------------------------- | ------------------------------------ |
| **Elbow rule**                | Choose k at the "elbow" in the scree plot             | Subjective when elbow is unclear     |
| **Cumulative variance ≥ 95%** | Keep enough components to explain 95% of variance     | May keep too many for noisy data     |
| **Eigenvalue > 1 (Kaiser)**   | Keep PCs with eigenvalue > 1 (for standardized data)  | Can be overly liberal                |
| **Domain-driven**             | Choose k based on how many dimensions make sense      | Most reliable when context is clear  |

---

## 2.5 PCA Score Plot (2D Projection)

Project the data onto the first two principal components and visualize the result — this is the most common use of PCA.

```python
# Re-fit with 2 components
pca2 = PCA(n_components=2)
X_2d = pca2.fit_transform(X_scaled)

pca_df = pd.DataFrame(X_2d, columns=['PC1', 'PC2'])
pca_df['species'] = df['species'].values

plt.figure(figsize=(8, 6))
colors = {'setosa': '#4CAF50', 'versicolor': '#2196F3', 'virginica': '#F44336'}

for species, group in pca_df.groupby('species'):
    plt.scatter(group['PC1'], group['PC2'],
                label=species, color=colors[species], alpha=0.7, s=60)

plt.xlabel(f"PC1 ({pca2.explained_variance_ratio_[0]*100:.1f}% variance)")
plt.ylabel(f"PC2 ({pca2.explained_variance_ratio_[1]*100:.1f}% variance)")
plt.title('PCA Score Plot — Iris Dataset')
plt.legend(title='Species')
plt.tight_layout()
plt.show()
```

> 💡 Always label axes with the percentage of variance explained. This tells the viewer how much information the 2D projection actually retains — critical for interpreting how meaningful the separation is.

---

## 2.6 Loadings: What Does Each Component Mean?

**Loadings** are the weights (eigenvectors) that define each principal component as a linear combination of the original variables. They tell you which variables drive each component.

```python
loadings = pd.DataFrame(
    pca2.components_.T,
    columns=['PC1', 'PC2'],
    index=num_cols
)
print("PCA Loadings:")
print(loadings.round(3))
```

**Visualizing loadings:**

```python
fig, ax = plt.subplots(figsize=(7, 5))
loadings.plot(kind='bar', ax=ax, color=['steelblue', 'tomato'],
              edgecolor='white', alpha=0.85)
ax.axhline(0, color='black', linewidth=0.8)
ax.set_title('PCA Loadings — PC1 and PC2')
ax.set_ylabel('Loading Weight')
ax.set_xlabel('Original Variable')
ax.set_xticklabels(ax.get_xticklabels(), rotation=25, ha='right')
plt.tight_layout()
plt.show()
```

**Interpreting loadings:**

| Loading Magnitude | Interpretation                                      |
| ----------------- | --------------------------------------------------- |
| Close to ±1       | This variable is strongly aligned with the component|
| Near 0            | This variable contributes little to the component   |
| Same sign         | Variables move together along this component        |
| Opposite sign     | Variables move in opposite directions               |

> 💡 **Naming components**: If PC1 has high positive loadings on all four iris measurements, it represents "overall flower size." If PC2 has high positive loading on sepal width and high negative loading on petal dimensions, it represents "sepal-vs-petal shape contrast." Meaningful names make PCA results interpretable to non-statisticians.

---

## 2.7 Biplot: Observations and Variables Together

A **biplot** overlays the PCA scores (observations) and the loading vectors (variables) in the same 2D space. It shows both *how observations are distributed* and *which variables are responsible* for the separation.

```python
fig, ax = plt.subplots(figsize=(9, 7))

# Plot observations
for species, group in pca_df.groupby('species'):
    ax.scatter(group['PC1'], group['PC2'],
               label=species, color=colors[species], alpha=0.5, s=50)

# Plot loading arrows
scale = 3.0  # scale factor for visibility
for i, var in enumerate(num_cols):
    ax.annotate('',
        xy=(pca2.components_[0, i] * scale,
            pca2.components_[1, i] * scale),
        xytext=(0, 0),
        arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
    ax.text(pca2.components_[0, i] * scale * 1.12,
            pca2.components_[1, i] * scale * 1.12,
            var, fontsize=9, ha='center')

ax.axhline(0, color='gray', linestyle='--', alpha=0.4)
ax.axvline(0, color='gray', linestyle='--', alpha=0.4)
ax.set_xlabel(f"PC1 ({pca2.explained_variance_ratio_[0]*100:.1f}%)")
ax.set_ylabel(f"PC2 ({pca2.explained_variance_ratio_[1]*100:.1f}%)")
ax.set_title('PCA Biplot — Iris Dataset')
ax.legend(title='Species')
plt.tight_layout()
plt.show()
```

**Reading the biplot:**
- Arrows pointing in the same direction → those variables are highly correlated
- Arrows pointing in opposite directions → those variables are negatively correlated
- Long arrows → variable has strong influence in this 2D space
- Short arrows → variable is not well represented by the first two components

---

## 2.8 PCA as Preprocessing

PCA components can be used as inputs to downstream models — particularly useful when you have many correlated features.

```python
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Keep 2 components for downstream use
pca_pre = PCA(n_components=2)
X_reduced = pca_pre.fit_transform(X_scaled)

# X_reduced can now be fed into clustering, regression, or classification
print(f"Original shape: {X_scaled.shape}")
print(f"Reduced shape:  {X_reduced.shape}")
print(f"Variance retained: {pca_pre.explained_variance_ratio_.sum()*100:.1f}%")
```

> ⚠️ **Fit PCA on training data only.** If you have a train/test split, fit the scaler and PCA on training data, then use `transform()` (not `fit_transform()`) on the test set. Otherwise you leak test set information into the transformation.  
> PCA 和 StandardScaler 都只能在訓練資料上 fit，測試資料只能用 transform。這是防止資料洩漏的基本原則。

---

## 2.9 Key Takeaways

| Concept                          | Key Point                                                                         |
| -------------------------------- | --------------------------------------------------------------------------------- |
| **Always standardize first**     | PCA is scale-sensitive — skip standardization only if all variables share units   |
| **Scree plot guides k**          | Use cumulative variance ≥ 95% as a starting point; validate with domain knowledge|
| **Loadings reveal meaning**      | Name each component based on which variables load most strongly                   |
| **Biplot combines both views**   | Shows observations and variable contributions in the same reduced space           |
| **PCA captures linear structure** | Non-linear relationships won't be captured — consider kernel PCA or UMAP        |
| **Fit only on training data**    | Never fit-transform on the test set — transform only                             |

---