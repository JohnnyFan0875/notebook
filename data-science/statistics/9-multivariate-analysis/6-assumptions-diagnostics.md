# 6. Model Assumptions & Diagnostics

Every statistical model rests on assumptions. **Violating assumptions does not always make a model wrong — but it can make its estimates unreliable, its standard errors incorrect, and its predictions biased.** Diagnostics let you detect violations and decide whether to transform the data, use a different model, or simply report the limitation.

> 📌 **為什麼假設診斷常被跳過**：建模很令人興奮，但驗證假設枯燥費時。然而，一個違反核心假設的模型可能產生完全錯誤的結論，而且表面上看起來很好（R² 高、p-value 顯著）。假設診斷是統計嚴謹性的最後一道防線。

---

## 6.1 Linear Regression Assumptions (LINE)

The classical OLS assumptions are often remembered as **LINE**:

| Assumption              | 中文        | What It Means                                           | How to Check                          |
| ----------------------- | ----------- | ------------------------------------------------------- | ------------------------------------- |
| **L**inearity           | 線性關係    | The relationship between X and y is linear             | Residuals vs Fitted plot              |
| **I**ndependence        | 獨立性      | Observations are independent of each other             | Context/design; Durbin-Watson test    |
| **N**ormality           | 常態性      | Residuals are approximately normally distributed       | Q–Q plot, histogram of residuals      |
| **E**qual variance      | 等變異性    | Variance of residuals is constant (homoscedasticity)   | Residuals vs Fitted, Scale-Location   |

Additionally:
- **No multicollinearity**: Predictors are not too highly correlated (check VIF — covered in Section 4)
- **No influential outliers**: No single observation dominates the estimates

> 💡 The most critical assumptions are **linearity** and **equal variance**. Normality is less critical for large samples due to the Central Limit Theorem, and is mainly needed for valid inference (p-values, confidence intervals) in small samples.

---

## 6.2 The Four Diagnostic Plots

These four plots are the standard regression diagnostic suite. Together they check all LINE assumptions.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
import statsmodels.api as sm

housing = fetch_california_housing(as_frame=True)
df = housing.frame.sample(2000, random_state=42)  # sample for speed

feature_cols = ['MedInc', 'HouseAge', 'AveRooms', 'AveOccup']
X = sm.add_constant(df[feature_cols])
y = df['MedHouseVal']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
result = sm.OLS(y_train, X_train).fit()

# Compute diagnostic quantities
fitted   = result.fittedvalues
residuals = result.resid
std_resid = residuals / residuals.std()

# Leverage (hat matrix diagonal)
influence = result.get_influence()
leverage  = influence.hat_matrix_diag
cooks_d   = influence.cooks_distance[0]

fig, axes = plt.subplots(2, 2, figsize=(13, 10))

# Plot 1: Residuals vs Fitted
axes[0,0].scatter(fitted, residuals, alpha=0.3, s=20, color='steelblue')
axes[0,0].axhline(0, color='tomato', linestyle='--', linewidth=1.5)
axes[0,0].set_xlabel('Fitted Values')
axes[0,0].set_ylabel('Residuals')
axes[0,0].set_title('1. Residuals vs Fitted\n(checks linearity + homoscedasticity)')

# Plot 2: Q–Q Plot
stats.probplot(residuals, dist='norm', plot=axes[0,1])
axes[0,1].set_title('2. Q–Q Plot of Residuals\n(checks normality)')

# Plot 3: Scale-Location (sqrt of abs std residuals vs fitted)
axes[1,0].scatter(fitted, np.sqrt(np.abs(std_resid)), alpha=0.3, s=20, color='seagreen')
axes[1,0].set_xlabel('Fitted Values')
axes[1,0].set_ylabel('√|Standardized Residuals|')
axes[1,0].set_title('3. Scale-Location\n(checks homoscedasticity)')

# Plot 4: Cook's Distance
axes[1,1].stem(range(len(cooks_d)), cooks_d,
               linefmt='gray', markerfmt='o', basefmt=' ')
axes[1,1].axhline(4 / len(cooks_d), color='tomato', linestyle='--',
                  label=f"Threshold = 4/n = {4/len(cooks_d):.4f}")
axes[1,1].set_xlabel('Observation Index')
axes[1,1].set_ylabel("Cook's Distance")
axes[1,1].set_title("4. Cook's Distance\n(checks influential observations)")
axes[1,1].legend()

plt.suptitle('OLS Regression Diagnostics', fontsize=14, y=1.01)
plt.tight_layout()
plt.show()
```

---

## 6.3 Reading Each Diagnostic Plot

### Plot 1: Residuals vs Fitted

| Pattern                             | Diagnosis              | Fix                                        |
| ----------------------------------- | ---------------------- | ------------------------------------------ |
| Random scatter around zero          | ✅ Linearity OK        | None needed                                |
| Curved pattern (U or arch)          | ❌ Non-linearity       | Add polynomial term or transform predictor |
| Funnel shape (widening)             | ❌ Heteroscedasticity  | Log/sqrt transform y; use WLS              |
| Systematic bands or groups          | ❌ Unmodeled structure | Add missing variable or interaction        |

### Plot 2: Q–Q Plot

| Pattern                              | Diagnosis              |
| ------------------------------------ | ---------------------- |
| Points on diagonal                   | ✅ Normality OK        |
| Heavy tails (S-curve outward)        | Heavy-tailed residuals |
| Light tails (S-curve inward)         | Light-tailed residuals |
| Curve in one direction               | Skewed residuals       |

> 💡 For large n (>200), minor Q–Q deviations are acceptable — the CLT makes inference robust to mild non-normality. Worry mainly about **severe** departures.

### Plot 3: Scale-Location

If heteroscedasticity is present, the spread of residuals changes with fitted values. The smooth line should be flat.

### Plot 4: Cook's Distance

**Cook's Distance** measures how much all fitted values change if observation i is removed. It combines leverage and residual size.

$$D_i = \frac{\sum_j (\hat{y}_j - \hat{y}_{j(-i)})^2}{(p+1)\hat{\sigma}^2}$$

| Cook's D                 | Interpretation           |
| ------------------------ | ------------------------ |
| < 4/n                    | ✅ Not influential       |
| Between 4/n and 1        | ⚠️ Worth investigating  |
| > 1                      | ❌ Highly influential    |

---

## 6.4 Testing Heteroscedasticity

```python
from statsmodels.stats.diagnostic import het_breuschpagan, het_white

# Breusch-Pagan test: H₀ = homoscedastic
bp_stat, bp_pval, _, _ = het_breuschpagan(result.resid, result.model.exog)
print(f"Breusch-Pagan test:  stat = {bp_stat:.3f},  p = {bp_pval:.4f}")
print("  H₀: Homoscedastic (constant variance)")
print(f"  {'❌ Reject H₀ — heteroscedasticity detected' if bp_pval < 0.05 else '✅ Fail to reject H₀ — no evidence of heteroscedasticity'}")

# White test: more general (also detects non-linear heteroscedasticity)
w_stat, w_pval, _, _ = het_white(result.resid, result.model.exog)
print(f"\nWhite test:  stat = {w_stat:.3f},  p = {w_pval:.4f}")
```

**Remedies for heteroscedasticity:**

| Remedy                              | When to Use                                        |
| ----------------------------------- | -------------------------------------------------- |
| **Log-transform y**                 | Variance grows proportionally with fitted values   |
| **Square root transform**           | Count data with moderate heteroscedasticity        |
| **Weighted Least Squares (WLS)**    | Known variance structure                           |
| **Robust standard errors (HC3)**    | Heteroscedasticity present but don't want to transform |

```python
# Robust standard errors (HC3) — fix inference without transforming
result_robust = sm.OLS(y_train, X_train).fit(cov_type='HC3')
print(result_robust.summary().tables[1])
```

---

## 6.5 Logistic Regression Diagnostics

Logistic regression has different assumptions from OLS. The key checks are:

| Assumption                              | How to Check                               |
| --------------------------------------- | ------------------------------------------ |
| **Linearity of log-odds**               | Box-Tidwell test; component+residual plots |
| **No perfect separation**               | Model convergence warning; all-zero cells  |
| **No severe multicollinearity**         | VIF (same as OLS)                          |
| **Independence of observations**        | Context/design                             |

### Calibration Plot

A **calibration plot** checks whether the model's predicted probabilities match the actual observed proportions. A well-calibrated model's calibration curve should hug the diagonal.

```python
from sklearn.calibration import calibration_curve
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_breast_cancer

cancer = load_breast_cancer(as_frame=True)
X_c, y_c = cancer.data[:, :6], cancer.target
X_tr, X_te, y_tr, y_te = train_test_split(X_c, y_c, test_size=0.3,
                                            random_state=42, stratify=y_c)
scaler = __import__('sklearn.preprocessing', fromlist=['StandardScaler']).StandardScaler()
X_tr_s = scaler.fit_transform(X_tr)
X_te_s = scaler.transform(X_te)

clf = LogisticRegression(random_state=42, max_iter=1000)
clf.fit(X_tr_s, y_tr)
y_prob = clf.predict_proba(X_te_s)[:, 1]

prob_true, prob_pred = calibration_curve(y_te, y_prob, n_bins=8)

plt.figure(figsize=(6, 5))
plt.plot(prob_pred, prob_true, 's-', color='steelblue', linewidth=2, label='Logistic Regression')
plt.plot([0, 1], [0, 1], 'k--', label='Perfect calibration')
plt.xlabel('Mean Predicted Probability')
plt.ylabel('Fraction of Positives')
plt.title('Calibration Plot')
plt.legend()
plt.tight_layout()
plt.show()
```

> 💡 If the calibration curve bows above the diagonal, the model is underconfident (predicted probabilities are too low). If it bows below, the model is overconfident. Calibration matters when you use the predicted probability to make risk-based decisions.

---

## 6.6 PCA and Clustering Diagnostics

### PCA: Cumulative Variance and Component Quality

```python
# Already covered in Section 2 — key checks:
# 1. How much variance do the chosen k components retain?
# 2. Are loadings interpretable (not spread equally across all variables)?
# 3. Does the score plot show meaningful separation?

# Check reconstruction quality
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris

iris = load_iris()
X    = StandardScaler().fit_transform(iris.data)

pca_k = PCA(n_components=2)
X_reconstructed = pca_k.inverse_transform(pca_k.fit_transform(X))

reconstruction_error = np.mean((X - X_reconstructed) ** 2)
print(f"Mean Squared Reconstruction Error (2 components): {reconstruction_error:.4f}")
print(f"Variance retained: {pca_k.explained_variance_ratio_.sum()*100:.1f}%")
```

### Clustering: Silhouette Analysis

The silhouette score for each observation measures how similar it is to its own cluster vs the nearest other cluster.

$$s_i = \frac{b_i - a_i}{\max(a_i, b_i)}$$

- aᵢ = mean distance to other points in the same cluster
- bᵢ = mean distance to points in the nearest other cluster
- s ranges from −1 (misclassified) to +1 (well-separated)

```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.cm as cm

X_cl = StandardScaler().fit_transform(load_iris().data)

fig, axes = plt.subplots(1, 3, figsize=(14, 5))

for idx, k in enumerate([2, 3, 4]):
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(X_cl)
    sil_vals = silhouette_samples(X_cl, labels)
    avg_sil  = silhouette_score(X_cl, labels)

    ax = axes[idx]
    y_lower = 10
    cmap    = cm.get_cmap('Set2', k)

    for i in range(k):
        ith_sil = np.sort(sil_vals[labels == i])
        size    = ith_sil.shape[0]
        y_upper = y_lower + size
        ax.fill_betweenx(np.arange(y_lower, y_upper), 0, ith_sil,
                         facecolor=cmap(i), alpha=0.7)
        ax.text(-0.05, y_lower + 0.5 * size, str(i))
        y_lower = y_upper + 10

    ax.axvline(avg_sil, color='tomato', linestyle='--',
               label=f'Avg = {avg_sil:.3f}')
    ax.set_xlabel('Silhouette Coefficient')
    ax.set_title(f'k = {k}')
    ax.legend(fontsize=8)

plt.suptitle('Silhouette Analysis — K-Means on Iris', fontsize=13, y=1.02)
plt.tight_layout()
plt.show()
```

**Reading the silhouette plot:**
- Wide, uniform bars → observations are well-assigned to their clusters
- Narrow or negative bars → those observations may belong better to another cluster
- All clusters roughly equal width → balanced, well-separated clusters

---

## 6.7 Complete Diagnostic Checklist

| Model               | Check                     | Tool                                  | Target                              |
| ------------------- | ------------------------- | ------------------------------------- | ----------------------------------- |
| **OLS Regression**  | Linearity                 | Residuals vs Fitted                   | Random scatter around zero           |
|                     | Homoscedasticity          | Scale-Location; Breusch-Pagan test    | Flat smooth line; p > 0.05           |
|                     | Normality                 | Q–Q plot                              | Points on diagonal                   |
|                     | Influential obs           | Cook's Distance                       | No points above 4/n threshold        |
|                     | Multicollinearity         | VIF                                   | All VIF < 10                         |
| **Logistic Regression** | Calibration           | Calibration plot                      | Curve near diagonal                  |
|                     | Discrimination            | ROC / AUC                             | AUC > 0.7 (context-dependent)        |
|                     | Multicollinearity         | VIF                                   | All VIF < 10                         |
| **PCA**             | Variance retained         | Scree + cumulative variance           | ≥ 90–95% with chosen k               |
|                     | Loading interpretability  | Loading bar chart / biplot            | Clear dominant variables per PC      |
| **K-Means**         | Cluster quality           | Silhouette score                      | > 0.5 good; > 0.7 strong            |
|                     | Optimal k                 | Elbow + silhouette                    | Elbow and silhouette agree           |

---

## 6.8 Key Takeaways

| Concept                              | Key Point                                                                           |
| ------------------------------------ | ----------------------------------------------------------------------------------- |
| **Diagnose before concluding**       | A model that fits well but violates assumptions can produce invalid inferences      |
| **Residuals vs Fitted is the first** | This plot catches both non-linearity and heteroscedasticity in one view             |
| **Cook's D identifies influence**    | A single outlier can pull all coefficients — always check for influential points    |
| **Robust SE over transformation**    | If heteroscedasticity is mild, HC3 robust errors fix inference without transforming |
| **Calibration vs discrimination**    | AUC measures ranking ability; calibration checks probability accuracy              |
| **Silhouette confirms cluster quality** | Always validate cluster solutions — don't trust visual inspection alone          |

---
