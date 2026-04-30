# Decision Tree (Classification)



Decision Trees are versatile supervised learning algorithms commonly used for **classification** tasks. In [scikit-learn](../../packages/scikit-learn/README.md), this is implemented as:

- `DecisionTreeClassifier`

They recursively split the data based on feature values, creating a tree-like model that is easy to interpret but prone to [overfitting](../../foundations/overfitting-underfitting.md) if not pruned or regularized.

## Key Parameters

- **`max_depth`**: Maximum depth of the tree. Limits complexity to avoid [overfitting](../../foundations/overfitting-underfitting.md).
- **`min_samples_split`**: Minimum samples required to split an internal node.
- **`min_samples_leaf`**: Minimum samples required to be at a leaf node.
- **`criterion`**: Metric to evaluate split quality (`gini`, `entropy` for classification).
- **`max_features`**: Number of features to consider when looking for the best split.

## Example: Breast Cancer Classification

```python
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_curve, auc

# Load dataset
data = load_breast_cancer()
X = data.data
y = data.target

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize classifier
dt_classifier = DecisionTreeClassifier(random_state=42)

# Cross-validation
cv_scores = cross_val_score(dt_classifier, X_train, y_train, cv=5)

# Hyperparameter tuning
param_grid = {
    'max_depth': [3, 5, 10, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(estimator=dt_classifier, param_grid=param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Best model
best_model = grid_search.best_estimator_
best_params = grid_search.best_params_
best_score = grid_search.best_score_

# Predictions
y_pred = best_model.predict(X_test)
y_pred_prob = best_model.predict_proba(X_test)[:, 1]

# Evaluation
accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

fpr, tpr, thresholds = roc_curve(y_test, y_pred_prob)
roc_auc = auc(fpr, tpr)

# Predict unseen data
unseen_data = X_test[0].reshape(1, -1)
unseen_prediction = best_model.predict(unseen_data)

# Plot decision tree
plt.figure(figsize=(15, 10))
plot_tree(
    best_model,
    filled=True,
    feature_names=list(data.feature_names),
    class_names=list(data.target_names),
    rounded=True,
    fontsize=12
)
plt.title('Decision Tree for Breast Cancer Classification', fontsize=16)
plt.show()
```

## Critical Notes

- **[Overfitting](../../foundations/overfitting-underfitting.md)**: Decision trees can perfectly fit training data if not controlled. Use parameters like `max_depth` and `min_samples_leaf`.
- **Interpretability**: Trees are easy to visualize and explain, making them useful for interpretability.
- **Unstable splits**: Small changes in data can lead to very different trees. Ensemble methods ([Random Forest](../ensemble/random-forest.md), [Gradient Boosting](../ensemble/gradient-boosting.md)) are often preferred.
- **Feature importance**: Trees provide a natural way to rank features by importance.

## Related Concepts

- [Confusion Matrix](../../evaluation/confusion-metrics.md)
- [Cross-Validation Methods](../../workflow/cross-validation.md)
- [Hyperparameter Tuning](../../workflow/hyperparameter-tuning.md)
- [Random Forest](../ensemble/random-forest.md)

[Back to Classification](README.md)
