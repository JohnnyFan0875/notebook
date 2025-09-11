# Voting Ensemble Learning

Voting ensemble methods combine multiple models (base learners) to improve overall predictive performance. There are two main types:

- **VotingClassifier** for classification tasks.
- **VotingRegressor** for regression tasks.

## Voting Classifier

```python
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

# Load dataset
data = load_iris()
X = data.data
y = data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define base models
dt = DecisionTreeClassifier(random_state=42)
svc = SVC(probability=True, random_state=42)
knn = KNeighborsClassifier()

# Voting Classifier
voting_clf = VotingClassifier(
    estimators=[('dt', dt), ('svc', svc), ('knn', knn)],
    voting='hard'  # 'hard' = majority voting, 'soft' = average probabilities
)

# Hyperparameter grid
param_grid = {
    'dt__max_depth': [3, 5, 10, None],
    'svc__C': [0.1, 1, 10],
    'knn__n_neighbors': [3, 5, 7, 9]
}

# Grid search
grid_search = GridSearchCV(
    estimator=voting_clf,
    param_grid=param_grid,
    cv=5,
    n_jobs=-1
)
grid_search.fit(X_train_scaled, y_train)

best_params_ = grid_search.best_params_
best_model = grid_search.best_estimator_
best_score = grid_search.best_score_

# Evaluate on test data
y_pred = best_model.predict(X_test_scaled)
test_accuracy = accuracy_score(y_test, y_pred)

# Cross-validation
cv_scores = cross_val_score(best_model, X_train_scaled, y_train, cv=5)
print(f"Cross-validation Accuracy: {np.mean(cv_scores):.4f} ± {np.std(cv_scores):.4f}")
```

**Critical Notes:**

- Use `voting='soft'` when base models can output class probabilities (better for imbalanced data).
- Make sure hyperparameters in the grid follow the format: `classifier__parameter`.
- Diversity of models (tree, SVM, KNN, etc.) often improves ensemble performance.

## Voting Regressor

```python
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import VotingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

# Generate regression dataset
X, y = make_regression(n_samples=100, n_features=5, noise=0.2, random_state=42)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Feature scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define base regressors
lr = LinearRegression()
dt = DecisionTreeRegressor(random_state=42)
knn = KNeighborsRegressor()

# Voting Regressor
voting_reg = VotingRegressor(estimators=[('lr', lr), ('dt', dt), ('knn', knn)])

# Train
voting_reg.fit(X_train_scaled, y_train)

# Predictions
y_pred = voting_reg.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)

# Cross-validation
cv_scores = cross_val_score(voting_reg, X_train_scaled, y_train, cv=5, scoring='neg_mean_squared_error')
cv_scores = -cv_scores  # convert to positive MSE

print(f"Test MSE: {mse:.4f}")
print(f"Cross-validation MSE: {np.mean(cv_scores):.4f} ± {np.std(cv_scores):.4f}")
```

**Critical Notes:**

- Ridge/Lasso regressors can also be used as base models to handle multicollinearity.
- No `voting='soft'` option in regression; predictions are averaged.
- Consider scaling features, especially when combining distance-based models like KNN with linear models.

## Key Takeaways

- Voting is a simple but effective way to combine multiple learners.
- For classification: choose between **hard** (majority vote) and **soft** (probability averaging).
- For regression: predictions are **averaged** across models.
- Always ensure base learners are diverse for best performance.
