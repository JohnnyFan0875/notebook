# MSE, RMSE

- **Mean Squared Error (MSE):**  
  Measures the average of the squared differences between actual values \(y*i\) and predicted values \(\hat{y}\_i\).  
  \[
  MSE = \frac{1}{n} \sum*{i=1}^{n} (y_i - \hat{y}\_i)^2
  \]

  - Penalizes larger errors more heavily (because of squaring).
  - More sensitive to **outliers**.

- **Root Mean Squared Error (RMSE):**  
  The square root of MSE.  
  \[
  RMSE = \sqrt{MSE}
  \]
  - Same unit as the dependent variable (target).
  - Easier to interpret in the original scale of the data.
  - Smaller RMSE = better model fit.

## Example in Python

```python
import numpy as np
from sklearn.metrics import mean_squared_error

# Example data
y_true = np.array([3, -0.5, 2, 7])
y_pred = np.array([2.5, 0.0, 2, 8])

# Compute MSE
mse = mean_squared_error(y_true, y_pred)

# Compute RMSE
rmse = np.sqrt(mse)

print("MSE:", mse)
print("RMSE:", rmse)
```

**Output:**

```
MSE: 0.375
RMSE: 0.6123724356957945
```

## Critical Notes

- MSE penalizes large errors more severely than small ones → can exaggerate the effect of **outliers**.
- RMSE is more interpretable than MSE since it is in the **same unit as the target variable**.
- When comparing models, lower MSE and RMSE values indicate better fit.
- For imbalanced or skewed data, also consider metrics like **MAE (Mean Absolute Error)**.
