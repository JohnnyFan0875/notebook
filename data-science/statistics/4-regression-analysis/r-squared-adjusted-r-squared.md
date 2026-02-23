### **1. R-squared (R²)**

- **Definition**: R-squared represents the proportion of the variance in the dependent variable (\(y\)) that is explained by the independent variable(s) (\(X\)) in a regression model. It provides an indication of how well the model fits the data.

\[
R^2 = 1 - \frac{SSR}{SST}
\]

**Where:**

- \(SSR\) = Sum of Squared Residuals = \(\sum (y_i - \hat{y}\_i)^2\)
- \(SST\) = Total Sum of Squares = \(\sum (y_i - \bar{y})^2\)

**Limitations of R²:**

- **Increases with more predictors**: Adding more independent variables (even irrelevant ones) will always **increase or maintain** \(R^2\).
- **Does not account for model complexity**: No penalty for unnecessary predictors, which can lead to **overfitting**.

### **2. Adjusted R-squared**

- **Definition**: Adjusted R-squared modifies the \(R^2\) value to account for the number of predictors. It penalizes the inclusion of irrelevant variables and helps prevent overfitting.

\[
R^2\_{\text{adj}} = 1 - \left(1 - R^2\right) \cdot \frac{n-1}{n-p-1}
\]

**Where:**

- \(R^2\): regular R-squared
- \(n\): number of observations
- \(p\): number of predictors

**Interpretation:**

- \(R^2\_{\text{adj}}\) increases only if new predictors improve the model more than expected by chance.
- It decreases when unnecessary predictors are added.

**Range:**

- Adjusted R² can be **negative** if the model is worse than a baseline model (predicting the mean).
- Unlike R², which is bounded between 0 and 1, adjusted R² can fall below 0.

### **Key Differences Between R-squared and Adjusted R-squared**

1. **Effect of Adding Predictors**

   - **R²**: Always increases (or stays the same).
   - **Adjusted R²**: Can increase or decrease depending on predictor usefulness.

2. **Model Complexity**

   - **R²**: Does not account for complexity.
   - **Adjusted R²**: Penalizes excessive predictors; accounts for both \(n\) and \(p\).

3. **Interpretation of Performance**
   - **R²**: Higher values indicate better fit but may mislead when comparing models with different predictor counts.
   - **Adjusted R²**: More reliable for comparing models of different complexities.

### **When to Use Adjusted R-squared vs R-squared**

- **Use R²** when:

  - Only one or a few predictors are present.
  - You want a quick measure of overall fit.

- **Use Adjusted R²** when:
  - Comparing models with different numbers of predictors.
  - Building models with many predictors (to avoid overfitting).
  - You want a fairer measure of model quality.

### **Example**

Suppose we compare two models:

1. **Model 1**: Simple regression with 1 predictor.

   - \(R^2 = 0.80\)
   - \(R^2\_{\text{adj}} = 0.79\)

2. **Model 2**: Regression with 10 predictors.
   - \(R^2 = 0.85\)
   - \(R^2\_{\text{adj}} = 0.75\)

**Interpretation:**

- \(R^2\) suggests Model 2 is better (0.85 vs 0.80).
- \(R^2\_{\text{adj}}\) shows Model 2 is worse after penalizing complexity (0.75 vs 0.79).
- Therefore, **Model 1** is more efficient and generalizable.

### **Conclusion**

- **R²**: Measures variance explained by the model but can be misleading with many predictors.
- **Adjusted R²**: Penalizes unnecessary predictors, providing a more reliable metric for model comparison in multiple regression.
