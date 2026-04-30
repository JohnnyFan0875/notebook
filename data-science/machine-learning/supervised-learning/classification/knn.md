# K-Nearest Neighbors (KNN) Classification Workflow



## Basic Knowledge of KNN

- **K-Nearest Neighbors (KNN)** is a simple, non-parametric, and instance-based learning algorithm.
- **Idea**: To classify a new data point, KNN looks at the _k_ closest labeled data points (neighbors) and assigns the class that is most common among them.
- **Distance metrics**: Common choices include Euclidean, Manhattan, Chebyshev, or cosine distance.
- **Key hyperparameters**:
  - `k` (number of neighbors): Small k → sensitive to noise; Large k → smoother decision boundary.
  - `weights`: `'uniform'` (all neighbors equal) or `'distance'` (closer neighbors have more influence).
- **Advantages**: Easy to understand, no explicit training step, works well for small to medium-sized datasets.
- **Disadvantages**: Computationally expensive for large datasets, sensitive to irrelevant features and [feature scaling](../../preprocessing/feature-scaling.md).

## Overview

This example demonstrates how to build, tune, and evaluate a **K-Nearest Neighbors (KNN)** classifier using [scikit-learn](../../packages/scikit-learn/README.md). It includes:

- Data preprocessing and scaling
- [Train-test split](../../preprocessing/train-test-split.md)
- [Cross-Validation](../../workflow/cross-validation.md)
- [Hyperparameter tuning](../../workflow/hyperparameter-tuning.md) with GridSearchCV
- Evaluation with accuracy, [confusion matrix](../../evaluation/confusion-metrics.md), [ROC curve](../../evaluation/roc-auc.md), and [AUC](../../evaluation/roc-auc.md)
- Making predictions on new data

### Step 1: Import Libraries

```python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_curve, auc
from sklearn.preprocessing import MinMaxScaler
```

### Step 2: Load and Prepare Data

```python
data = load_iris()
X = data.data
y = data.target  # includes classes 0, 1, 2

# Restrict to binary classification (classes 0 and 1)
X = X[y != 2]
y = y[y != 2]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
```

### Step 3: Feature Scaling

```python
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
```

### Step 4: Cross-Validation

```python
knn = KNeighborsClassifier()
cv_scores = cross_val_score(knn, X_train, y_train, cv=5, scoring='accuracy')
print(cv_scores)  # array of accuracy scores from 5 folds
```

### Step 5: Hyperparameter Tuning (Grid Search)

```python
param_grid = {
    'n_neighbors': [3, 5, 7, 9, 11],
    'weights': ['uniform', 'distance'],
    'metric': ['euclidean', 'manhattan', 'chebyshev']
}

grid_search = GridSearchCV(estimator=knn, param_grid=param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

best_knn = grid_search.best_estimator_
best_params = grid_search.best_params_
best_score = grid_search.best_score_
```

### Step 6: Model Evaluation

```python
y_pred = best_knn.predict(X_test)
y_prob = best_knn.predict_proba(X_test)[:, 1]  # probabilities for class 1

classification_rep = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy:.3f}")
```

### Step 7: Visualizations

```python
# Confusion Matrix
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=["Class 0", "Class 1"], yticklabels=["Class 0", "Class 1"])
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# ROC Curve
fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='blue', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='gray', linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve for KNN Classifier')
plt.legend(loc='lower right')
plt.show()
```

### Step 8: Predict on New Data

```python
new_data = np.array([[5.1, 3.5, 1.4, 0.2], [6.7, 3.1, 4.4, 1.4]])
new_data_scaled = scaler.transform(new_data)
new_predictions = best_knn.predict(new_data_scaled)
print(new_predictions)
```

---

### Recommended Notes

- For **multiclass problems**, use **one-vs-rest (OvR)** or **macro-averaged metrics** when computing ROC/[AUC](../../evaluation/roc-auc.md).
- Always scale features for distance-based algorithms like KNN.
- Use [cross-validation](../../workflow/cross-validation.md) to reduce variance in model evaluation.
- GridSearchCV can be computationally expensive; for large datasets, consider **RandomizedSearchCV**.
- Evaluate not only accuracy but also **precision, recall, F1-score**, especially with [imbalanced](../../evaluation/class-imbalance.md) data.

## Related Concepts

- [Feature Scaling](../../preprocessing/feature-scaling.md)
- [Train-Test Split](../../preprocessing/train-test-split.md)
- [Cross-Validation Methods](../../workflow/cross-validation.md)
- [ROC curve, AUC](../../evaluation/roc-auc.md)

[Back to Classification](README.md)
