# ROC curve, AUC

- **ROC curve**: Receiver Operating Characteristic Curve
- **AUC**: Area Under the Curve, ranges between [0, 1]

## Purpose

- Evaluates **binary classification model performance** across thresholds.

## Axes

- **x-axis**: FPR (False Positive Rate)  
  \( FPR = \frac{FP}{TN + FP} = 1 - \text{Specificity} \)
- **y-axis**: TPR (True Positive Rate, Sensitivity)  
  \( TPR = \frac{TP}{TP + FN} \)

## Construction

- Based on different thresholds → get corresponding FPR & TPR → each pair is a point in the ROC curve.

## Evaluation

- **Threshold selection**: Use **Youden index** (TPR − FPR) to find optimal cutoff.
- **Comparing models**: Compare **AUC values**.

## AUC Interpretation

- **AUC = 0.5**: Classifier performs no better than random guessing (diagonal line).
- **AUC > 0.5**: Model has predictive power.
- **AUC = 1.0**: Perfect classifier (no FP or FN).

## References:

- [haosquare ROC curve guide](https://haosquare.com/roc-curve/)
- [Best cutoff point](https://haosquare.com/roc-curve-best-cutoff/)

## Examples:

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve, auc, roc_auc_score
import numpy as np

# Generate dataset
X, y = make_classification(n_samples=1000, n_features=20, n_informative=2, n_classes=2, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predict probabilities
y_prob = model.predict_proba(X_test)[:, 1]

# ROC curve
fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)
roc_auc_score_val = roc_auc_score(y_test, y_prob)

# Find best threshold using Youden index
j_scores = tpr - fpr
best_threshold = thresholds[np.argmax(j_scores)]

print("AUC (via auc):", roc_auc)
print("AUC (via roc_auc_score):", roc_auc_score_val)
print("Best threshold (Youden):", best_threshold)
```

## Key Takeaways

- ROC curve evaluates a model across thresholds instead of at one cutoff.
- AUC summarizes overall discrimination ability.
- **Youden index** helps select the optimal cutoff point.
- Useful when class distribution is imbalanced.
