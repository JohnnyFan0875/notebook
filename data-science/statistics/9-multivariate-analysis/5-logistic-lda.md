# 5. Logistic Regression & LDA

When the outcome variable is **categorical** rather than continuous, linear regression is no longer appropriate. This section covers two fundamental methods for multivariate classification: **Logistic Regression** for modeling probabilities of binary outcomes, and **Linear Discriminant Analysis (LDA)** for finding the linear combination of features that best separates multiple classes.

> 📌 **為什麼不能直接用線性迴歸做分類**：線性迴歸可以預測超過 1 或小於 0 的值，這對於機率是無意義的。此外，線性迴歸假設誤差常態分佈，而二元結果（0/1）明顯違反這個假設。邏輯迴歸通過 sigmoid 函數把線性預測值壓縮到 [0, 1] 區間，完美解決這個問題。

---

## 5.1 Logistic Regression

### The Model

Logistic regression models the **log-odds** of the outcome as a linear function of predictors:

$$\log\left(\frac{p}{1-p}\right) = \beta_0 + \beta_1 x_1 + \cdots + \beta_p x_p$$

Solving for p:

$$p = \frac{1}{1 + e^{-(\beta_0 + \beta_1 x_1 + \cdots + \beta_p x_p)}} = \sigma(\mathbf{x}^T \boldsymbol{\beta})$$

where σ is the **sigmoid function**, which maps any real number to (0, 1).

```python
import numpy as np
import matplotlib.pyplot as plt

# Visualize the sigmoid function
z = np.linspace(-6, 6, 300)
sigmoid = 1 / (1 + np.exp(-z))

plt.figure(figsize=(8, 4))
plt.plot(z, sigmoid, color='steelblue', linewidth=2.5)
plt.axhline(0.5, color='tomato', linestyle='--', alpha=0.7, label='Decision boundary (p=0.5)')
plt.axhline(0,   color='gray', linestyle=':', alpha=0.5)
plt.axhline(1,   color='gray', linestyle=':', alpha=0.5)
plt.xlabel('Linear Predictor (log-odds)')
plt.ylabel('Predicted Probability p')
plt.title('Sigmoid Function — Maps Log-Odds to Probability')
plt.legend()
plt.tight_layout()
plt.show()
```

---

### Fitting Logistic Regression

```python
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import statsmodels.api as sm

# Load data: binary classification (malignant vs benign)
cancer = load_breast_cancer(as_frame=True)
df = cancer.frame
feature_cols = cancer.feature_names[:6].tolist()  # use first 6 for interpretability
target_col   = 'target'

X = df[feature_cols]
y = df[target_col]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# Standardize (logistic regression is scale-sensitive for regularized versions)
scaler        = StandardScaler()
X_train_sc    = scaler.fit_transform(X_train)
X_test_sc     = scaler.transform(X_test)

# Fit with statsmodels for full inference output
X_train_sm = sm.add_constant(X_train_sc)
logit_model = sm.Logit(y_train, X_train_sm)
logit_result = logit_model.fit(disp=False)

print(logit_result.summary())
```

---

### Interpreting Coefficients: Log-Odds and Odds Ratios

Logistic regression coefficients are in **log-odds** units, which are hard to interpret directly. Convert to **odds ratios** for communication.

$$\text{Odds Ratio}_j = e^{\beta_j}$$

| Odds Ratio | Interpretation                                        |
| ---------- | ----------------------------------------------------- |
| > 1        | Increasing xⱼ increases the odds of y=1              |
| = 1        | xⱼ has no effect on the odds                         |
| < 1        | Increasing xⱼ decreases the odds of y=1              |
| 2.0        | A 1-unit increase in xⱼ doubles the odds             |
| 0.5        | A 1-unit increase in xⱼ halves the odds              |

```python
# Coefficient table with odds ratios
params = logit_result.params.drop('const')
ci     = logit_result.conf_int().drop('const')

coef_table = pd.DataFrame({
    'Log-Odds':   params,
    'Odds Ratio': np.exp(params),
    'OR CI Low':  np.exp(ci[0]),
    'OR CI High': np.exp(ci[1]),
    'p-value':    logit_result.pvalues.drop('const')
}).round(4)

print(coef_table.sort_values('Odds Ratio', ascending=False).to_string())
```

---

### Evaluating Logistic Regression

```python
from sklearn.metrics import (classification_report, confusion_matrix,
                              roc_curve, roc_auc_score, ConfusionMatrixDisplay)

# Predictions
X_test_sm_pred = sm.add_constant(X_test_sc)
y_prob = logit_result.predict(X_test_sm_pred)
y_pred = (y_prob >= 0.5).astype(int)

# Classification report
print(classification_report(y_test, y_pred,
      target_names=cancer.target_names))

# Confusion matrix
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

ConfusionMatrixDisplay.from_predictions(
    y_test, y_pred,
    display_labels=cancer.target_names,
    ax=axes[0], colorbar=False, cmap='Blues')
axes[0].set_title('Confusion Matrix')

# ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_prob)
auc = roc_auc_score(y_test, y_prob)

axes[1].plot(fpr, tpr, color='steelblue', linewidth=2,
             label=f'Logistic Regression (AUC = {auc:.3f})')
axes[1].plot([0, 1], [0, 1], 'k--', alpha=0.5, label='Random Classifier')
axes[1].set_xlabel('False Positive Rate')
axes[1].set_ylabel('True Positive Rate')
axes[1].set_title('ROC Curve')
axes[1].legend()

plt.tight_layout()
plt.show()
```

**Key classification metrics:**

| Metric          | Formula                           | Best When                                       |
| --------------- | --------------------------------- | ----------------------------------------------- |
| **Accuracy**    | (TP + TN) / Total                 | Classes are balanced; all errors equally costly |
| **Precision**   | TP / (TP + FP)                    | False positives are costly (e.g., spam filter)  |
| **Recall**      | TP / (TP + FN)                    | False negatives are costly (e.g., cancer screen)|
| **F1 Score**    | 2 × (Precision × Recall) / (P + R)| Imbalanced classes; need balance of P and R     |
| **AUC-ROC**     | Area under ROC curve              | Threshold-independent; overall discriminability |

> 💡 **AUC interpretation**: AUC = 0.5 means no better than random; AUC = 1.0 means perfect discrimination. AUC can be interpreted as the probability that the model ranks a randomly chosen positive case higher than a randomly chosen negative case.

---

### Threshold Selection

The default threshold of 0.5 is not always optimal. Adjust based on the relative costs of false positives vs false negatives.

```python
# Plot precision-recall tradeoff across thresholds
from sklearn.metrics import precision_recall_curve

precision, recall, thresh = precision_recall_curve(y_test, y_prob)
f1_scores = 2 * precision * recall / (precision + recall + 1e-8)
best_idx  = np.argmax(f1_scores)

plt.figure(figsize=(9, 4))
plt.plot(thresh, precision[:-1], label='Precision', color='steelblue', linewidth=2)
plt.plot(thresh, recall[:-1],    label='Recall',    color='tomato',    linewidth=2)
plt.plot(thresh, f1_scores[:-1], label='F1 Score',  color='seagreen',  linewidth=2)
plt.axvline(thresh[best_idx], color='black', linestyle='--',
            label=f'Best F1 threshold = {thresh[best_idx]:.2f}')
plt.xlabel('Decision Threshold')
plt.ylabel('Score')
plt.title('Precision, Recall, and F1 by Decision Threshold')
plt.legend()
plt.tight_layout()
plt.show()

print(f"Best threshold: {thresh[best_idx]:.3f}  →  F1 = {f1_scores[best_idx]:.3f}")
```

---

## 5.2 Linear Discriminant Analysis (LDA)

LDA finds the **linear combination of features** that maximizes the ratio of between-class variance to within-class variance — the direction that best separates the classes.

> 💡 **LDA vs Logistic Regression**: Both produce linear decision boundaries. LDA is more efficient when the Gaussian assumption holds; logistic regression makes no distributional assumptions and is more robust when it doesn't. In practice, logistic regression is usually preferred for binary classification; LDA shines for **multi-class problems** and as a dimension reduction tool.

```python
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.datasets import load_iris

# Iris: 3 classes — LDA reduces to at most min(p, K-1) = 2 dimensions
iris = load_iris(as_frame=True)
X_iris = iris.data
y_iris = iris.target

lda = LinearDiscriminantAnalysis()
X_lda = lda.fit_transform(X_iris, y_iris)

print(f"Explained variance ratio by discriminant: {lda.explained_variance_ratio_.round(3)}")
```

### LDA Score Plot

```python
iris_df = iris.frame
iris_df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)

lda_df = pd.DataFrame(X_lda, columns=['LD1', 'LD2'])
lda_df['species'] = iris_df['species'].values

colors = {'setosa': '#4CAF50', 'versicolor': '#2196F3', 'virginica': '#F44336'}

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# LDA projection
for species, group in lda_df.groupby('species'):
    axes[0].scatter(group['LD1'], group['LD2'],
                    label=species, color=colors[species], alpha=0.7, s=60)

axes[0].set_xlabel(f"LD1 ({lda.explained_variance_ratio_[0]*100:.1f}% variance)")
axes[0].set_ylabel(f"LD2 ({lda.explained_variance_ratio_[1]*100:.1f}% variance)")
axes[0].set_title('LDA Score Plot — Iris (maximizing class separation)')
axes[0].legend()

# LD1 alone as a 1D density plot
for species, group in lda_df.groupby('species'):
    axes[1].hist(group['LD1'], bins=20, alpha=0.5,
                 color=colors[species], label=species, density=True)
axes[1].set_xlabel('LD1')
axes[1].set_ylabel('Density')
axes[1].set_title('LD1 Distribution by Species')
axes[1].legend()

plt.tight_layout()
plt.show()
```

---

### LDA vs PCA: Key Differences

| Dimension               | PCA                                     | LDA                                       |
| ----------------------- | --------------------------------------- | ----------------------------------------- |
| **Goal**                | Maximize total variance                 | Maximize between-class / within-class variance |
| **Uses class labels?**  | ❌ Unsupervised                         | ✅ Supervised                             |
| **Output**              | Principal components                    | Linear discriminants                      |
| **Max components**      | min(n−1, p)                             | **min(p, K−1)** where K = number of classes |
| **Best for**            | Dimension reduction, noise removal      | Classification, class visualization        |
| **Gaussian assumption** | Not required                            | Assumes equal covariance within classes   |

```python
# Direct classification with LDA
from sklearn.model_selection import cross_val_score

cv_scores = cross_val_score(lda, X_iris, y_iris, cv=5, scoring='accuracy')
print(f"LDA 5-fold CV Accuracy: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
```

---

## 5.3 Logistic vs Linear Regression vs LDA — Decision Guide

| Scenario                                    | Best Method                        |
| ------------------------------------------- | ---------------------------------- |
| Binary outcome, need probabilities          | **Logistic Regression**            |
| Multi-class outcome, Gaussian predictors    | **LDA**                            |
| Continuous outcome, multiple predictors     | **Multiple Linear Regression**     |
| Need dimension reduction + classification   | **LDA** (supervised)               |
| Imbalanced classes, no distributional assumptions | **Logistic Regression**       |
| Many correlated predictors, classification  | **Logistic Regression + LASSO**    |

---

## 5.4 Key Takeaways

| Concept                              | Key Point                                                                           |
| ------------------------------------ | ----------------------------------------------------------------------------------- |
| **Logistic regression models P(y=1)**| Output is a probability via sigmoid — never outside [0, 1]                        |
| **Coefficients are log-odds**        | Exponentiate to get odds ratios for intuitive interpretation                        |
| **AUC is threshold-free**            | Evaluate at AUC before committing to a threshold                                    |
| **Threshold = business decision**    | Set threshold based on relative costs of FP vs FN, not always 0.5                 |
| **LDA = supervised dimension reduction** | At most K−1 discriminant dimensions; visualizes class separation                |
| **LDA vs PCA**                       | PCA ignores class labels; LDA uses them — prefer LDA when labels exist            |

---

**← Previous:** [Multiple Linear Regression](./4-multiple-regression.md)  
**Next:** [Model Assumptions & Diagnostics →](./6-assumptions-diagnostics.md)
