# Linear Regression



Linear regression is one of the most fundamental supervised learning algorithms used to model the relationship between independent variables (features) and a continuous dependent variable (target).

## 1. Import Required Libraries

```python
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
```

## 2. Generate Sample Data

```python
# Create a regression dataset with 100 samples and 5 features
X, y = make_regression(n_samples=100, n_features=5, noise=0.1, random_state=42)
```

## 3. Train-Test Split

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

## 4. Feature Scaling

```python
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

**Critical Note:**  
Scaling is not strictly required for linear regression, but it is recommended when features have very different ranges, especially if you plan to compare coefficients.

## 5. Initialize and Cross-Validate Model

```python
model = LinearRegression()

# Perform 5-fold cross-validation using negative MSE
cv_scores = cross_val_score(
    model, X_train_scaled, y_train, cv=5, scoring='neg_mean_squared_error'
)
cv_scores = -cv_scores  # Convert to positive MSE
```

## 6. Fit the Model

```python
model.fit(X_train_scaled, y_train)

model_coef = model.coef_
model_intercept = model.intercept_
```

- `model_coef`: the slope (effect size of each feature).
- `model_intercept`: the [baseline](../../evaluation/baselines-and-error-analysis.md) prediction when all features = 0.

## 7. Evaluate Model Performance

```python
y_pred = model.predict(X_test_scaled)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("MSE:", mse)
print("R²:", r2)
```

**Critical Note:**

- **[MSE](../../evaluation/mse-rmse.md) (Mean Squared Error):** Lower is better.
- **R² (Coefficient of Determination):** Closer to 1 means better fit.
- Compare training vs test error to check for **[overfitting](../../foundations/overfitting-underfitting.md)**.

## 8. Predict on New Data

```python
new_data = np.array([[0.1, 0.2, 0.3, 0.4, 0.5]])
new_data_scaled = scaler.transform(new_data)
new_pred = model.predict(new_data_scaled)

print("Prediction for new data:", new_pred)
```

## Example Output

```
MSE: 0.0098
R²: 0.998
Prediction for new data: [12.3456]
```

## Key Takeaways

- Linear regression assumes a **linear relationship** between features and target.
- Always check **residual plots** to validate assumptions.
- Use **[cross-validation](../../workflow/cross-validation.md)** to ensure generalizability.
- [Feature scaling](../../preprocessing/feature-scaling.md) makes coefficients more comparable.
- For non-linear relationships, consider **polynomial regression** or other models.
- Reference: [Kaggle discussion](https://www.kaggle.com/discussions/getting-started/27261).

## Related Concepts

- [MSE, RMSE](../../evaluation/mse-rmse.md)
- [Cross-Validation Methods](../../workflow/cross-validation.md)
- [Feature Scaling](../../preprocessing/feature-scaling.md)
- [Statsmodels: Linear Regression](../../packages/statsmodels/linear-regression.md)

[Back to Regression](README.md)
