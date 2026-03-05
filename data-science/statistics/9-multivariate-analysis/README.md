# Multivariate Analysis

**Multivariate analysis** examines relationships among **three or more variables simultaneously**. Where bivariate analysis asks "are X and Y related?", multivariate analysis asks "how do many variables relate to each other — and to an outcome — all at once?"

> 📌 **核心原則**：多變量分析的價值在於它能捕捉變數之間的*交互*與*共變*結構，而非僅分析兩兩關係。現實世界的問題幾乎都是多變量的：客戶流失取決於數十個因素，基因表達涉及成千上萬個變數。學會在高維資料中找出結構，是現代資料分析的核心能力。

---

## Why This Order?

The sections follow a natural multivariate workflow:

```
Understand correlation structure among all variables
        ↓
Reduce dimensions — find the fewest axes that capture most variance (PCA)
        ↓
Find natural groupings in the data (Clustering)
        ↓
Model a continuous outcome from multiple predictors (Multiple Regression)
        ↓
Model a binary/categorical outcome (Logistic Regression & LDA)
        ↓
Validate, interpret, and diagnose every model
```

This order matters because **dimension reduction often precedes both clustering and regression** in practice: working with raw high-dimensional data amplifies noise, inflates computation, and makes interpretation nearly impossible.

---

## Overview of Topics

| #   | Section                                                                        | Level        | Key Questions Answered                                                        |
| --- | ------------------------------------------------------------------------------ | ------------ | ----------------------------------------------------------------------------- |
| 1   | [**Multivariate EDA**](./1-multivariate-eda.md)                                | Foundation   | How do I explore many variables at once? What patterns exist before modeling? |
| 2   | [**Principal Component Analysis (PCA)**](./2-pca.md)                           | Dimension Reduction | How do I reduce many correlated variables into fewer independent axes? |
| 3   | [**Clustering**](./3-clustering.md)                                             | Unsupervised | How do I find natural groups in the data without labels?                      |
| 4   | [**Multiple Linear Regression**](./4-multiple-regression.md)                   | Supervised   | How do I model a continuous outcome from multiple predictors?                 |
| 5   | [**Logistic Regression & LDA**](./5-logistic-lda.md)                           | Supervised   | How do I classify observations or model a binary outcome?                     |
| 6   | [**Model Assumptions & Diagnostics**](./6-assumptions-diagnostics.md)          | Validation   | How do I check whether my model's assumptions hold?                           |

---

## What's Inside Each Section

### 1. Multivariate EDA

- Correlation matrix and heatmap (extending bivariate to all pairs)
- Pairplot with group coloring
- Parallel coordinates and radar charts for high-dimensional profiles
- Detecting multicollinearity before regression

### 2. Principal Component Analysis (PCA)

The core dimension reduction technique:

| Output            | What It Tells You                                       |
| ----------------- | ------------------------------------------------------- |
| **Eigenvalues**   | How much variance each principal component captures     |
| **Scree plot**    | Visual guide for choosing number of components to keep  |
| **Loadings**      | Which original variables drive each component           |
| **Biplot**        | Observations and variable loadings in the same 2D space |

### 3. Clustering

Two families of clustering methods:

| Method                   | Type         | Key Hyperparameter       | Best For                             |
| ------------------------ | ------------ | ------------------------ | ------------------------------------ |
| **K-Means**              | Partitional  | k (number of clusters)   | Compact, spherical clusters          |
| **Hierarchical**         | Agglomerative| Linkage method, cut height| Nested structure, unknown k         |
| **DBSCAN**               | Density-based| ε, min_samples           | Irregular shapes, noise/outliers     |

### 4. Multiple Linear Regression

Extending simple regression to p predictors:

| Topic                    | Key Concepts                                               |
| ------------------------ | ---------------------------------------------------------- |
| **Coefficient interpretation** | Partial effect: "holding all else constant"          |
| **Multicollinearity**    | VIF, condition number, correlated predictors               |
| **Variable selection**   | Stepwise, LASSO, Ridge                                     |
| **Interaction terms**    | When the effect of X₁ depends on X₂                       |

### 5. Logistic Regression & LDA

| Method                   | Output          | Decision Boundary  | Best For                          |
| ------------------------ | --------------- | ------------------ | --------------------------------- |
| **Logistic Regression**  | Probability     | Linear (in log-odds) | Binary outcome, interpretability |
| **LDA**                  | Class membership | Linear             | Multi-class, Gaussian predictors  |

### 6. Model Assumptions & Diagnostics

Organized by model type:

| Model Type           | Key Assumptions                                         | Diagnostic Tools                     |
| -------------------- | ------------------------------------------------------- | ------------------------------------ |
| **Linear Regression**| Linearity, homoscedasticity, normality, independence    | Residual plots, Q-Q, leverage        |
| **Logistic Regression** | Linearity in log-odds, no perfect separation        | ROC curve, calibration plot          |
| **PCA**              | Linear relationships, scale-sensitivity               | Scree plot, cumulative variance      |
| **K-Means**          | Spherical clusters, similar size                      | Elbow plot, silhouette score         |

---

## Visualization Quick Reference

| Chart                       | Best For                                                    |
| --------------------------- | ----------------------------------------------------------- |
| Correlation heatmap         | Overview of all pairwise relationships                      |
| Pairplot                    | Bivariate distributions for all variable pairs              |
| Parallel coordinates        | Comparing multivariate profiles across groups               |
| PCA biplot                  | Variables and observations in the same reduced space        |
| Scree plot                  | Choosing number of PCA components                           |
| Dendrogram                  | Hierarchical cluster structure                              |
| Silhouette plot             | Assessing cluster quality                                   |
| Residual vs fitted          | Checking regression model assumptions                       |
| ROC curve                   | Evaluating classifier performance                           |

---

## Tools Used in This Module

| Library           | Purpose                                                    |
| ----------------- | ---------------------------------------------------------- |
| `pandas`          | Data manipulation, correlation matrices                    |
| `numpy`           | Linear algebra, matrix operations                          |
| `matplotlib` / `seaborn` | Visualization                                     |
| `sklearn`         | PCA, clustering, regression, classification, metrics       |
| `statsmodels`     | OLS with full statistical summaries, VIF                   |
| `scipy`           | Hierarchical clustering, distance matrices                 |
| `yellowbrick`     | Visual diagnostics for ML models                           |

---

## Key Takeaway

> Multivariate analysis answers: **"What is the structure hidden in many variables simultaneously — and how do they collectively explain an outcome?"**  
> Always start with EDA and correlation structure before building models. Dimension reduction before clustering or regression is usually worth the effort. And always validate assumptions — multivariate models can fail silently.
