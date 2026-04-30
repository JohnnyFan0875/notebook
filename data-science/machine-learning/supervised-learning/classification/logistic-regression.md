# Logistic Regression



Logistic Regression is a widely used classification algorithm that models the probability of a binary outcome using a logistic (sigmoid) function. Despite its name, it is a **classification** method, not a [regression](../regression/README.md) method. It is interpretable, computationally efficient, and often used as a [baseline](../../evaluation/baselines-and-error-analysis.md) for classification tasks.

## Key Concepts

- **Log-odds linear relationship**: Logistic regression assumes that the log-odds of the target variable are a linear combination of input features.
- **Sigmoid function**: Converts the linear combination into a probability between 0 and 1.
- **[Regularization](../../foundations/regularization.md)**: Helps prevent [overfitting](../../foundations/overfitting-underfitting.md). `C` controls the strength (smaller `C` = stronger regularization).
- **Solvers**: Different optimization algorithms (`liblinear`, `saga`, `lbfgs`) are suitable for different data sizes and [regularization](../../foundations/regularization.md) types.

⚠️ **Critical Notes:**

- Logistic regression requires features to be on a comparable scale → always use scaling (e.g., `StandardScaler`).
- Works best for **linearly separable** problems. Nonlinear relationships may require [feature engineering](../../foundations/feature-engineering-principles.md) or kernel methods.
- Outliers can strongly affect the coefficients.
- For [imbalanced](../../evaluation/class-imbalance.md) datasets, accuracy is not enough → use precision, recall, F1-score, and [ROC-AUC](../../evaluation/roc-auc.md).

## Example: Logistic Regression with Hyperparameter Tuning

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_curve, auc, classification_report, confusion_matrix, RocCurveDisplay

# Generate dataset
X, y = make_classification(n_samples=1000, n_features=20, n_classes=2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize model
log_reg = LogisticRegression()

# Cross-validation
cv_scores = cross_val_score(log_reg, X_train_scaled, y_train, cv=5, scoring='accuracy')

# Hyperparameter tuning
param_grid = {
    'C': [0.01, 0.1, 1, 10, 100],
    'solver': ['liblinear', 'saga'],
    'max_iter': [100, 200, 300],
}

grid_search = GridSearchCV(estimator=log_reg, param_grid=param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train_scaled, y_train)

best_log_reg = grid_search.best_estimator_
best_params = grid_search.best_params_
best_score = grid_search.best_score_

# Predictions
y_pred = best_log_reg.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

classification_rep = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

# ROC curve
fpr, tpr, thresholds = roc_curve(y_test, best_log_reg.predict_proba(X_test_scaled)[:, 1])
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc).plot()
plt.title("ROC Curve")
plt.show()

# Predict new data
new_data = np.random.rand(5, X_train.shape[1])
new_data_scaled = scaler.transform(new_data)
predictions = best_log_reg.predict(new_data_scaled)
```

## Visualizing the Log-Odds Relationship

Logistic regression assumes a linear relationship between features and the **log-odds** of the outcome.

```python
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Load dataset
data = load_iris(as_frame=True)
X = data.data
y = (data.target == 0).astype(int)  # Binary: setosa vs. not-setosa

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

# Probabilities
y_prob = model.predict_proba(X_test)[:, 1]
log_odds = np.log(y_prob / (1 - y_prob))

plt.scatter(X_test['sepal length (cm)'], log_odds)
plt.xlabel('Sepal Length (cm)')
plt.ylabel('Log-Odds')
plt.title('Feature vs Log-Odds')
plt.show()
```

## When to Use Logistic Regression

- Baseline for binary classification problems.
- Useful when interpretability is important (coefficients show feature influence on log-odds).
- Effective for smaller datasets where complex models may overfit.

> Logistic regression is simple yet powerful. Always check assumptions, scale features, and consider [regularization](../../foundations/regularization.md) when applying it in practice.

## Related Concepts

- [Confusion Matrix](../../evaluation/confusion-metrics.md)
- [ROC curve, AUC](../../evaluation/roc-auc.md)
- [Classification Thresholds and Calibration](../../evaluation/classification-thresholds-and-calibration.md)
- [Regularization](../../foundations/regularization.md)

[Back to Classification](README.md)
