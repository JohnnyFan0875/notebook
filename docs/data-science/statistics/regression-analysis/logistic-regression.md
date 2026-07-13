# Logistic Regression

Logistic regression is used when the **outcome variable Y is binary** (0 or 1, Yes/No, Pass/Fail). Instead of predicting Y directly, it predicts the **probability** that Y = 1, then maps it through a mathematical transformation to keep probabilities between 0 and 1.

Key point: Why can’t linear regression be used to handle binary outcomes? Linear regression can predict values ​​below 0 or above 1, which is meaningless for probabilities. Logistic regression solves this by predicting log-odds, then converting back to probability via the sigmoid function.

## From Probability to Log-Odds

### The Logit Transformation

\[
\text{logit}(p) = \ln\left(\frac{p}{1-p}\right) = \beta_0 + \beta_1 X_1 + \cdots + \beta_k X_k
\]

| Term | Meaning |
| -------------- | ----------------------------------------------------- |
| $p$ | Probability that Y = 1 |
| $\frac{p}{1-p}$ | Odds — ratio of probability of success to failure |
| $\ln\left(\frac{p}{1-p}\right)$ | Log-odds (logit) — the left-hand side is linear in X |

### Sigmoid Function

\[
p = \frac{1}{1 + e^{-(\beta_0 + \beta_1 X)}}
\]

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

Tip: The sigmoid function squashes any real number into the range (0, 1), making it perfect for probability output. The decision boundary is at p = 0.5, which corresponds to log-odds = 0.

## Interview Fast Answer

如果面試官直接問 logistic regression 和 linear regression 差在哪，最穩的回答通常是：

- linear regression 用來預測連續型 `Y`
- logistic regression 用來建模 binary outcome 的機率
- 它不是直接對 probability 畫直線，而是對 log-odds 建立線性模型

如果想再補一句高訊號的：

- logistic regression 的係數先解讀在 log-odds 空間，再常轉成 odds ratio 講人話

## Logistic Regression as a Generalized Linear Model

The source GLM materials are a good reminder that logistic regression is not an isolated trick. It is a **generalized linear model (GLM)** with:

| Component | Logistic regression choice |
| --------- | -------------------------- |
| Random component | Bernoulli / Binomial outcome |
| Systematic component | Linear predictor $\beta_0 + \beta_1 X_1 + \cdots + \beta_k X_k$ |
| Link function | Logit |

This perspective helps explain why we do **not** model probability directly with a straight line. We model a linear structure in log-odds space, then map it back to probability through the inverse-logit.

## Python Implementation

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
y = data.target  # 0 = malignant, 1 = benign

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

## Interpreting Coefficients: Odds Ratios

Unlike linear regression where β directly tells you the change in Y, logistic regression coefficients work in **log-odds space**. The practical interpretation uses the **odds ratio (OR)**:

\[
\text{OR}_j = e^{\beta_j}
\]

| Odds Ratio | Interpretation |
| ---------- | ---------------------------------------------------- |
| OR = 1 | No association between $X_j$ and outcome |
| OR > 1 | Higher $X_j$ → higher odds of Y = 1 |
| OR < 1 | Higher $X_j$ → lower odds of Y = 1 (protective) |
| OR = 2 | One-unit increase in $X_j$ **doubles** the odds of Y = 1 |

### OR from a 2×2 Contingency Table

When the predictor is binary (e.g., exposed vs unexposed), OR can be calculated directly from a 2×2 table — this is the classical form used in epidemiology and case-control studies:

|  | Outcome = Yes | Outcome = No |
| ------------- | ------------- | ------------ |
| **Exposed** | a | b |
| **Unexposed** | c | d |

\[
\text{OR} = \frac{a/c}{b/d} = \frac{ad}{bc}
\]

The standard error of log(OR) and 95% confidence interval:

\[
SE = \sqrt{\frac{1}{a} + \frac{1}{b} + \frac{1}{c} + \frac{1}{d}}
\]

\[
95\%\,CI = \exp\left( \ln(OR) \pm 1.96 \cdot SE_{\ln(OR)} \right)
\]

Tip: If the 95% CI includes 1, the OR is not statistically significant — the exposure may have no effect on the outcome.

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

Tip: Example interpretation: If OR for "mean radius" = 2.5, then a one-unit increase in mean radius (after scaling) is associated with 2.5× higher odds of the tumor being malignant, holding other variables constant.

## Classification: From Probability to Prediction

By default, most libraries use **0.5** as the decision threshold:

\[
\hat{Y} = \begin{cases} 1 & \text{if } \hat{p} \geq 0.5 \\ 0 & \text{if } \hat{p} < 0.5 \end{cases}
\]

This threshold can be adjusted depending on the relative cost of false positives and false negatives.

### Threshold Tuning Is a Business Decision

`0.5` is only a convention. In practice, you should choose the threshold that matches the decision cost.

```python
from sklearn.metrics import precision_score, recall_score

thresholds = [0.2, 0.4, 0.5, 0.7]

for thr in thresholds:
    y_pred_thr = (y_pred_prob >= thr).astype(int)
    print(
        f"threshold={thr:.1f}  "
        f"precision={precision_score(y_test, y_pred_thr):.3f}  "
        f"recall={recall_score(y_test, y_pred_thr):.3f}"
    )
```

Tip: Lowering the threshold usually increases recall and decreases precision. Raising it does the opposite. This trade-off is often more important than the coefficient table when the model is used for triage or screening.

### Interview Prompt: Precision vs Recall

這也是高頻題。

可以很快回答成：

- precision: 被判成 positive 的裡面，有多少真的 positive
- recall: 所有真的 positive 裡面，抓到了多少
- 要選哪個，取決於 false positive 和 false negative 哪個成本更高

## Model Evaluation

### Confusion Matrix

```python
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Predicted malignant', 'Predicted benign'],
            yticklabels=['Actual malignant', 'Actual benign'])
plt.title('Confusion Matrix')
plt.tight_layout()
plt.show()
```

| Term | Formula | Meaning |
| ----------------------- | ------------------------------ | ------------------------------------------------ |
| **True Positive (TP)** | Actual=1, Predicted=1 | Correctly identified positives |
| **True Negative (TN)** | Actual=0, Predicted=0 | Correctly identified negatives |
| **False Positive (FP)** | Actual=0, Predicted=1 | Predicted positive, actually negative |
| **False Negative (FN)** | Actual=1, Predicted=0 | Predicted negative, actually positive |

### Key Classification Metrics

\[
\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}
\]

\[
\text{Precision} = \frac{TP}{TP + FP} \quad \text{(of predicted positives, how many are correct?)}
\]

\[
\text{Recall (Sensitivity)} = \frac{TP}{TP + FN} \quad \text{(of actual positives, how many did we catch?)}
\]

\[
\text{F1 Score} = 2 \cdot \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}
\]

```python
print(classification_report(y_test, y_pred,
                             target_names=['Malignant', 'Benign']))
```

Warning: Accuracy is misleading for imbalanced classes. If 95% of your data is class 0, a model that always predicts 0 achieves 95% accuracy but is completely useless. Prefer Precision, Recall, F1, or AUC-ROC.

## R Workflow: `glm(..., family = binomial)`

In R, logistic regression is usually fitted with `glm()` rather than `lm()`.

```r
mdl_recency <- glm(
  has_churned ~ time_since_last_purchase,
  data = churn,
  family = binomial
)
```

This is worth contrasting with:

```r
glm(has_churned ~ time_since_last_purchase, data = churn, family = gaussian)
```

The Gaussian version behaves like linear regression and can produce impossible probabilities below 0 or above 1. The binomial family fixes that by modeling log-odds instead.

## R Prediction Scale: Link vs Response

One of the most important practical details in R logistic regression is the prediction scale.

```r
predict(mdl_recency, newdata = explanatory_data)
predict(mdl_recency, newdata = explanatory_data, type = "response")
```

Interpretation:

- default `predict(glm)` for a binomial model returns **log-odds**
- `type = "response"` returns **probabilities**

This distinction matters a lot. If you forget `type = "response"`, you may think you are looking at probabilities when you are actually looking at the linear predictor.

## From Probability to Odds in R

If you already have predicted probabilities, you can convert them into odds and log-odds directly:

```r
prediction_data <- explanatory_data %>%
  mutate(
    has_churned = predict(mdl_recency, explanatory_data, type = "response"),
    odds_ratio = has_churned / (1 - has_churned),
    log_odds_ratio = log(odds_ratio)
  )
```

This is a nice way to connect the three linked scales:

- probability
- odds
- log-odds

Key point: Probability is easiest to communicate, odds are common in interpretation, and log-odds are the scale where the model is actually linear.

## Visualizing Logistic Fits in `ggplot2`

For a quick visual fit in R, `geom_smooth()` can fit the logistic curve directly:

```r
ggplot(churn, aes(time_since_last_purchase, has_churned)) +
  geom_point() +
  geom_smooth(
    method = "glm",
    se = FALSE,
    method.args = list(family = binomial)
  )
```

This is often the fastest way to show why a straight line is inappropriate for a binary response.

## Common Interview Traps

- 把 logistic coefficient 直接當成 probability change 解讀
- 把 `0.5` threshold 當成自然法則，而不是業務決策
- 在 class imbalance 問題裡只報 accuracy
- 只會背 confusion matrix 名詞，卻說不出 precision / recall 背後的成本取捨

### Choosing Between Precision and Recall

| Priority | Optimize | Real-world Example |
| -------------------- | ---------- | ------------------------------------------------ |
| Avoid false positives | Precision | Spam filter (don't want to delete real emails) |
| Avoid false negatives | Recall | Cancer screening (don't want to miss a diagnosis) |
| Balance both | F1 Score | General classification tasks |

## ROC Curve and AUC

The **Receiver Operating Characteristic (ROC) curve** shows the trade-off between Sensitivity (True Positive Rate) and 1 - Specificity (False Positive Rate) across all possible thresholds.

**AUC (Area Under the Curve)** summarizes the ROC curve in a single number:

| AUC | Interpretation |
| ----- | ------------------------------------------ |
| 1.0 | Perfect discrimination |
| 0.9+ | Excellent |
| 0.8–0.9 | Good |
| 0.7–0.8 | Fair |
| 0.6–0.7 | Poor |
| 0.5 | No discrimination (random guessing) |
| < 0.5 | Worse than random — check label encoding |

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

## Calibration: Are the Predicted Probabilities Trustworthy?

A model can rank observations well and still produce poorly calibrated probabilities. If you will act on predicted risk directly, calibration matters.

```python
from sklearn.calibration import calibration_curve

prob_true, prob_pred = calibration_curve(y_test, y_pred_prob, n_bins=8)

plt.figure(figsize=(5, 5))
plt.plot(prob_pred, prob_true, marker='o', color='steelblue', label='Model')
plt.plot([0, 1], [0, 1], '--', color='gray', label='Perfect calibration')
plt.xlabel('Predicted probability')
plt.ylabel('Observed frequency')
plt.title('Calibration Plot')
plt.legend()
plt.tight_layout()
plt.show()
```

Tip: AUC answers "Does the model rank positives above negatives?" Calibration answers "When the model says 0.80, do about 80% actually belong to class 1?" They are different qualities, and good ranking does not guarantee good probability estimates.

Tip: AUC vs Accuracy: AUC measures how well the model ranks observations (separates 1s from 0s regardless of threshold). It is threshold-independent and better suited for imbalanced datasets.

## R Workflow: Confusion Matrix with `yardstick`

If you are evaluating a classification model in R, `yardstick` provides a clean confusion-matrix workflow.

```r
library(yardstick)

confusion <- conf_mat(outcomes)
autoplot(confusion)
summary(confusion, event_level = "second")
```

This is useful because it turns model evaluation into tidy objects instead of making you manually count TP, FP, TN, and FN.

## Model Fit Statistics

Unlike linear regression, logistic regression has no R². Instead:

| Metric | How to Read |
| ------------------- | -------------------------------------------- |
| **Log-likelihood** | More negative = worse fit |
| **AIC** | Lower is better; penalizes model complexity |
| **BIC** | Lower is better; penalizes more than AIC |
| **McFadden's pseudo-R²** | 0.2–0.4 considered excellent for logistic |

```python
print(f"Log-likelihood: {logit_model.llf:.2f}")
print(f"AIC:            {logit_model.aic:.2f}")
print(f"BIC:            {logit_model.bic:.2f}")

# McFadden's pseudo-R²
pseudo_r2 = 1 - (logit_model.llf / logit_model.llnull)
print(f"McFadden R²:    {pseudo_r2:.4f}")
```

## Assumptions

Logistic regression has fewer and different assumptions than linear regression:

| Assumption | How to Check |
| --------------------------------- | ----------------------------------------------- |
| **Binary outcome** (or ordered for ordinal logistic) | Confirm Y ∈ {0, 1} |
| **Independence of observations** | Study design |
| **No multicollinearity** | VIF for predictors |
| **Linearity in log-odds** | Box-Tidwell test; partial regression plots |
| **Large sample size** | Rule of thumb: at least 10–20 events per predictor |
| **No extreme outliers** | Cook's distance; leverage |

Tip: Logistic regression does NOT require: - Normality of residuals - Homoscedasticity - Linear relationship between X and Y (only between X and log-odds)

## Extensions

| Extension | When to Use |
| ----------------------------- | ------------------------------------------------ |
| **Multinomial Logistic** | Outcome has 3+ unordered categories |
| **Ordinal Logistic** | Outcome has 3+ ordered categories (e.g., Low/Medium/High) |
| **Regularized Logistic (L1/L2)** | Many predictors; prevent overfitting |
| **Class weights** | Highly imbalanced outcome (e.g., fraud detection) |

```python
# Regularized logistic regression (sklearn default includes L2)
lr_l2 = LogisticRegression(C=1.0, penalty='l2', random_state=42)
lr_l1 = LogisticRegression(C=1.0, penalty='l1', solver='liblinear', random_state=42)

# Handling class imbalance
lr_balanced = LogisticRegression(class_weight='balanced', random_state=42)
```

## Key Takeaways

| Concept | Key Point |
| ------------------------ | ------------------------------------------------------------------------------- |
| **Use case** | Binary outcome (0/1) — predicts probability, not raw value |
| **Coefficients** | Interpret via odds ratios ($e^\beta$) — not directly as "unit change in Y" |
| **Decision threshold** | Default 0.5 is not always optimal — adjust based on cost of FP vs FN |
| **Evaluation** | Use Precision, Recall, F1, AUC-ROC — not accuracy for imbalanced data |
| **Assumptions** | Fewer than linear regression — no normality or homoscedasticity required |
| **Sample size** | Needs sufficient events per variable — rule of thumb: ≥ 10–20 events per predictor |
