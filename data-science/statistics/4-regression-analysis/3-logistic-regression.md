# 3. Logistic Regression

Logistic regression is used when the **outcome variable Y is binary** (0 or 1, Yes/No, Pass/Fail). Instead of predicting Y directly, it predicts the **probability** that Y = 1, then maps it through a mathematical transformation to keep probabilities between 0 and 1.

> 📌 **為什麼不能用線性回歸處理二元結果？**  
> Linear regression can predict values below 0 or above 1, which is meaningless for probabilities. Logistic regression solves this by predicting log-odds, then converting back to probability via the sigmoid function.

---

## 3.1 From Probability to Log-Odds

### The Logit Transformation

$$\text{logit}(p) = \ln\left(\frac{p}{1-p}\right) = \beta_0 + \beta_1 X_1 + \cdots + \beta_k X_k$$

| Term           | 中文     | Meaning                                               |
| -------------- | -------- | ----------------------------------------------------- |
| $p$            | 機率     | Probability that Y = 1                                |
| $\frac{p}{1-p}$| 勝算     | Odds — ratio of probability of success to failure     |
| $\ln\left(\frac{p}{1-p}\right)$ | 對數勝算 | Log-odds (logit) — the left-hand side is linear in X |

### Sigmoid Function

$$p = \frac{1}{1 + e^{-(\beta_0 + \beta_1 X)}}$$

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-6, 6, 300)
sigmoid = 1 / (1 + np.exp(-x))

plt.figure(figsize=(7, 4))
plt.plot(x, sigmoid, color='steelblue', linewidth=2)
plt.axhline(0.5, color='red', linestyle='--', alpha=0.7, label='p = 0.5')
plt.axvline(0, color='gray', linestyle='--', alpha=0.5)
plt.xlabel('Log-odds (β₀ + β₁X)')
plt.ylabel('Probability p')
plt.title('Sigmoid Function')
plt.legend()
plt.tight_layout()
plt.show()
```

> 💡 The sigmoid function squashes any real number into the range (0, 1), making it perfect for probability output. The decision boundary is at p = 0.5, which corresponds to log-odds = 0.

---

## 3.2 Python Implementation

```python
import pandas as pd
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (classification_report, confusion_matrix,
                             roc_auc_score, roc_curve)
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data = load_breast_cancer(as_frame=True)
X = data.data[['mean radius', 'mean texture', 'mean perimeter', 'mean area']]
y = data.target  # 1 = malignant, 0 = benign

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features (important for logistic regression)
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

# ── Method 1: scikit-learn ──
lr = LogisticRegression(random_state=42)
lr.fit(X_train_sc, y_train)

y_pred      = lr.predict(X_test_sc)
y_pred_prob = lr.predict_proba(X_test_sc)[:, 1]

# ── Method 2: statsmodels (for statistical inference / p-values) ──
X_train_const = sm.add_constant(X_train_sc)
logit_model   = sm.Logit(y_train, X_train_const).fit()
print(logit_model.summary())
```

---

## 3.3 Interpreting Coefficients: Odds Ratios

Unlike linear regression where β directly tells you the change in Y, logistic regression coefficients work in **log-odds space**. The practical interpretation uses the **odds ratio (OR)**:

$$\text{OR}_j = e^{\beta_j}$$

| Odds Ratio | Interpretation                                       |
| ---------- | ---------------------------------------------------- |
| OR = 1     | No association between $X_j$ and outcome             |
| OR > 1     | Higher $X_j$ → higher odds of Y = 1                 |
| OR < 1     | Higher $X_j$ → lower odds of Y = 1 (protective)     |
| OR = 2     | One-unit increase in $X_j$ **doubles** the odds of Y = 1 |

### OR from a 2×2 Contingency Table

When the predictor is binary (e.g., exposed vs unexposed), OR can be calculated directly from a 2×2 table — this is the classical form used in epidemiology and case-control studies:

|               | Outcome = Yes | Outcome = No |
| ------------- | ------------- | ------------ |
| **Exposed**   | a             | b            |
| **Unexposed** | c             | d            |

$$\text{OR} = \frac{a/c}{b/d} = \frac{ad}{bc}$$

The standard error of log(OR) and 95% confidence interval:

$$SE = \sqrt{\frac{1}{a} + \frac{1}{b} + \frac{1}{c} + \frac{1}{d}}$$

$$95\%\,CI = \exp\left( \ln(OR) \pm 1.96 \cdot SE_{\ln(OR)} \right)$$

> 💡 If the 95% CI **includes 1**, the OR is not statistically significant — the exposure may have no effect on the outcome. 若信賴區間包含 1，表示該關聯在統計上不顯著。

```python
import numpy as np

# Example 2×2 table: a=30, b=10, c=20, d=40
a, b, c, d = 30, 10, 20, 40

or_value = (a * d) / (b * c)
se       = np.sqrt(1/a + 1/b + 1/c + 1/d)
log_or   = np.log(or_value)

ci_lower = np.exp(log_or - 1.96 * se)
ci_upper = np.exp(log_or + 1.96 * se)

print(f"Odds Ratio: {or_value:.3f}")
print(f"95% CI:     ({ci_lower:.3f}, {ci_upper:.3f})")
```

### OR from Logistic Regression (Continuous Predictors)

```python
# Compute odds ratios and 95% CIs from statsmodels output
params = logit_model.params
conf   = logit_model.conf_int()

odds_ratios = pd.DataFrame({
    'OR':     np.exp(params),
    'Lower':  np.exp(conf[0]),
    'Upper':  np.exp(conf[1]),
    'p-value': logit_model.pvalues
}).drop('const').round(3)

print(odds_ratios)
```

> 💡 **Example interpretation**: If OR for "mean radius" = 2.5, then a one-unit increase in mean radius (after scaling) is associated with 2.5× higher odds of the tumor being malignant, holding other variables constant.

---

## 3.4 Classification: From Probability to Prediction

By default, most libraries use **0.5** as the decision threshold:

$$\hat{Y} = \begin{cases} 1 & \text{if } \hat{p} \geq 0.5 \\ 0 & \text{if } \hat{p} < 0.5 \end{cases}$$

This threshold can be adjusted depending on the cost of false positives vs false negatives (see Section 3.6).

---

## 3.5 Model Evaluation

### Confusion Matrix

```python
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Predicted 0', 'Predicted 1'],
            yticklabels=['Actual 0', 'Actual 1'])
plt.title('Confusion Matrix')
plt.tight_layout()
plt.show()
```

| Term                    | 中文         | Formula                        | Meaning                                          |
| ----------------------- | ------------ | ------------------------------ | ------------------------------------------------ |
| **True Positive (TP)**  | 真陽性       | Actual=1, Predicted=1          | Correctly identified positives                   |
| **True Negative (TN)**  | 真陰性       | Actual=0, Predicted=0          | Correctly identified negatives                   |
| **False Positive (FP)** | 假陽性 (Type I error) | Actual=0, Predicted=1 | Predicted positive, actually negative            |
| **False Negative (FN)** | 假陰性 (Type II error) | Actual=1, Predicted=0 | Predicted negative, actually positive            |

### Key Classification Metrics

$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$

$$\text{Precision} = \frac{TP}{TP + FP} \quad \text{(of predicted positives, how many are correct?)}$$

$$\text{Recall (Sensitivity)} = \frac{TP}{TP + FN} \quad \text{(of actual positives, how many did we catch?)}$$

$$\text{F1 Score} = 2 \cdot \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

```python
print(classification_report(y_test, y_pred,
                             target_names=['Benign', 'Malignant']))
```

> ⚠️ **Accuracy is misleading for imbalanced classes.** If 95% of your data is class 0, a model that always predicts 0 achieves 95% accuracy but is completely useless. Prefer Precision, Recall, F1, or AUC-ROC.

### Choosing Between Precision and Recall

| Priority             | Optimize   | Real-world Example                               |
| -------------------- | ---------- | ------------------------------------------------ |
| Avoid false positives | Precision | Spam filter (don't want to delete real emails)   |
| Avoid false negatives | Recall    | Cancer screening (don't want to miss a diagnosis)|
| Balance both         | F1 Score  | General classification tasks                     |

---

## 3.6 ROC Curve and AUC

The **Receiver Operating Characteristic (ROC) curve** shows the trade-off between Sensitivity (True Positive Rate) and 1 - Specificity (False Positive Rate) across all possible thresholds.

**AUC (Area Under the Curve)** summarizes the ROC curve in a single number:

| AUC   | Interpretation                             |
| ----- | ------------------------------------------ |
| 1.0   | Perfect discrimination                     |
| 0.9+  | Excellent                                  |
| 0.8–0.9 | Good                                     |
| 0.7–0.8 | Fair                                     |
| 0.6–0.7 | Poor                                     |
| 0.5   | No discrimination (random guessing)        |
| < 0.5 | Worse than random — check label encoding   |

```python
fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)
auc_score = roc_auc_score(y_test, y_pred_prob)

plt.figure(figsize=(6, 5))
plt.plot(fpr, tpr, color='steelblue', linewidth=2,
         label=f'ROC Curve (AUC = {auc_score:.3f})')
plt.plot([0, 1], [0, 1], color='red', linestyle='--', label='Random Classifier')
plt.xlabel('False Positive Rate (1 - Specificity)')
plt.ylabel('True Positive Rate (Sensitivity)')
plt.title('ROC Curve')
plt.legend()
plt.tight_layout()
plt.show()
```

> 💡 **AUC vs Accuracy**: AUC measures how well the model **ranks** observations (separates 1s from 0s regardless of threshold). It is threshold-independent and better suited for imbalanced datasets.

---

## 3.7 Model Fit Statistics

Unlike linear regression, logistic regression has no R². Instead:

| Metric              | 中文           | How to Read                                  |
| ------------------- | -------------- | -------------------------------------------- |
| **Log-likelihood**  | 對數概似       | More negative = worse fit                    |
| **AIC**             | 赤池信息準則   | Lower is better; penalizes model complexity  |
| **BIC**             | 貝氏信息準則   | Lower is better; penalizes more than AIC     |
| **McFadden's pseudo-R²** | 偽R²    | 0.2–0.4 considered excellent for logistic    |

```python
print(f"Log-likelihood: {logit_model.llf:.2f}")
print(f"AIC:            {logit_model.aic:.2f}")
print(f"BIC:            {logit_model.bic:.2f}")

# McFadden's pseudo-R²
pseudo_r2 = 1 - (logit_model.llf / logit_model.llnull)
print(f"McFadden R²:    {pseudo_r2:.4f}")
```

---

## 3.8 Assumptions

Logistic regression has fewer and different assumptions than linear regression:

| # | Assumption                        | How to Check                                    |
| - | --------------------------------- | ----------------------------------------------- |
| 1 | **Binary outcome** (or ordered for ordinal logistic) | Confirm Y ∈ {0, 1}              |
| 2 | **Independence of observations**  | Study design                                    |
| 3 | **No multicollinearity**          | VIF for predictors                              |
| 4 | **Linearity in log-odds**         | Box-Tidwell test; partial regression plots      |
| 5 | **Large sample size**             | Rule of thumb: at least 10–20 events per predictor |
| 6 | **No extreme outliers**           | Cook's distance; leverage                       |

> 💡 Logistic regression does **NOT** require:
> - Normality of residuals
> - Homoscedasticity
> - Linear relationship between X and Y (only between X and log-odds)

---

## 3.9 Extensions

| Extension                     | When to Use                                      |
| ----------------------------- | ------------------------------------------------ |
| **Multinomial Logistic**      | Outcome has 3+ unordered categories              |
| **Ordinal Logistic**          | Outcome has 3+ ordered categories (e.g., Low/Medium/High) |
| **Regularized Logistic (L1/L2)** | Many predictors; prevent overfitting          |
| **Class weights**             | Highly imbalanced outcome (e.g., fraud detection)|

```python
# Regularized logistic regression (sklearn default includes L2)
lr_l2 = LogisticRegression(C=1.0, penalty='l2', random_state=42)
lr_l1 = LogisticRegression(C=1.0, penalty='l1', solver='liblinear', random_state=42)

# Handling class imbalance
lr_balanced = LogisticRegression(class_weight='balanced', random_state=42)
```

---

## 3.10 Key Takeaways

| Concept                  | Key Point                                                                       |
| ------------------------ | ------------------------------------------------------------------------------- |
| **Use case**             | Binary outcome (0/1) — predicts probability, not raw value                      |
| **Coefficients**         | Interpret via odds ratios ($e^\beta$) — not directly as "unit change in Y"     |
| **Decision threshold**   | Default 0.5 is not always optimal — adjust based on cost of FP vs FN            |
| **Evaluation**           | Use Precision, Recall, F1, AUC-ROC — not accuracy for imbalanced data          |
| **Assumptions**          | Fewer than linear regression — no normality or homoscedasticity required        |
| **Sample size**          | Needs sufficient events per variable — rule of thumb: ≥ 10–20 events per predictor |

---
