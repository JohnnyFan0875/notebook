# Hyperparameter Tuning

Hyperparameter tuning is the process of finding the **optimal set of hyperparameters** that leads to the best model performance. Unlike model parameters (learned during training), hyperparameters are set before training and control aspects such as regularization strength, learning rate, or tree depth.

⚠️ **Critical Note:** Always perform hyperparameter tuning on the **training set only** (with cross-validation). The final evaluation must be done on a separate **test set** to avoid overfitting.

## Grid Search

- **Exhaustive search**: tries every possible combination of hyperparameters in the search space.
- Simple but computationally expensive.
- Works well for **small search spaces**.

```python
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error

# Example dataset
df = pd.read_csv('dataset.csv')
X = df[['col1','col2']]
y = df['col3']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = Lasso()

param_grid = {
    'alpha': [0.1, 0.5, 1, 10, 100],    # Regularization strength
    'max_iter': [1000, 2000, 3000],     # Iterations
    'tol': [1e-4, 1e-3, 1e-2]           # Stopping tolerance
}

grid_search = GridSearchCV(model, param_grid, cv=5, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

print("Best params:", grid_search.best_params_)
print("Best CV score:", grid_search.best_score_)

y_pred = grid_search.best_estimator_.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print("Test MSE:", mse)
```

## Random Search

- Samples hyperparameter combinations **randomly** from distributions or sets.
- More efficient for **large search spaces**.
- Not guaranteed to test every combination but often finds good results faster.

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform

param_dist = {
    'alpha': uniform(0.1, 100),  # sample values between 0.1 and 100
    'max_iter': [1000, 2000, 3000],
    'tol': [1e-4, 1e-3, 1e-2]
}

random_search = RandomizedSearchCV(
    estimator=model,
    param_distributions=param_dist,
    n_iter=50,      # number of random combinations
    cv=5,
    random_state=42,
    n_jobs=-1,
    verbose=2
)

random_search.fit(X_train, y_train)
print("Best params:", random_search.best_params_)

y_pred = random_search.best_estimator_.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print("Test MSE:", mse)
```

## Bayesian Optimization

- Builds a **probabilistic model** of the objective function.
- Selects hyperparameters intelligently, balancing exploration vs. exploitation.
- More **sample-efficient** than random/grid search.
- Popular libraries: **Optuna**, **Hyperopt**, **scikit-optimize (skopt)**.

```python
import optuna
from sklearn.model_selection import cross_val_score

def objective(trial):
    alpha = trial.suggest_loguniform('alpha', 1e-3, 100)
    tol = trial.suggest_categorical('tol', [1e-4, 1e-3, 1e-2])
    model = Lasso(alpha=alpha, tol=tol)
    score = cross_val_score(model, X_train, y_train, cv=5, scoring='neg_mean_squared_error')
    return -score.mean()

study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=50)

print("Best params:", study.best_params)
```

## Gradient-based Optimization

- Adjusts hyperparameters iteratively using gradient information.
- Used mainly in **deep learning** (e.g., learning rate schedules).
- Less common in scikit-learn but integral in frameworks like TensorFlow/PyTorch.

## Evolutionary / Population-based Methods

- Inspired by **genetic algorithms**.
- Maintain a population of hyperparameters and evolve them over generations.
- Suitable for **large, complex search spaces** (e.g., reinforcement learning).
- Tools: **Population Based Training (PBT)** in Ray Tune, DEAP (genetic algorithms in Python).

## 🔑 Notes & Best Practices

- **Grid Search**: good for small spaces, baseline comparisons.
- **Random Search**: efficient for large spaces, often better than grid search.
- **Bayesian Optimization**: more intelligent search, fewer evaluations.
- **Evolutionary methods**: useful for non-smooth or very large search spaces.
- Always evaluate tuned models on a **held-out test set**.
- Beware of **overfitting to cross-validation** when search spaces are very large.

> In practice: Start with **Random Search**, refine with **Bayesian Optimization** (Optuna/Hyperopt), and consider advanced methods for deep learning or RL.
