# Overfitting and Underfitting



## Overview

When training machine learning models, we aim to achieve good [**generalization**](generalization.md) — strong performance not only on training data but also on unseen test data.

Two common pitfalls are:

- **Overfitting**: Model learns the training data too well, including noise, leading to poor generalization.
- **Underfitting**: Model is too simple to capture the underlying patterns, leading to poor performance on both training and test data.

## Characteristics

### Overfitting

- **Symptoms**:
  - Very low training error
  - Much higher test error
- **Cause**: Model is too complex (captures noise as if it were signal)
- **Bias/Variance tradeoff**: Low bias, high variance

### Underfitting

- **Symptoms**:
  - Both training and test errors are high
  - Training error is close to test error
- **Cause**: Model is too simple (misses important patterns)
- **Bias/Variance tradeoff**: High bias, low variance

## Example: Detecting Overfitting / Underfitting

```python
from sklearn.metrics import mean_squared_error

# Evaluate model on train, test, and cross-validation sets
mse_train = mean_squared_error(y_train, model.predict(X_train))
mse_test = mean_squared_error(y_test, model.predict(X_test))
mse_cv_mean = cv_scores_positive.mean()

if mse_train < mse_test and (mse_test >> mse_cv_mean):
    print("Possible overfitting: model fits training data too well")

if mse_train > mse_test and mse_train > mse_cv_mean:
    print("Possible underfitting: model too simple")

# General patterns:
# - mse_train is usually lower than mse_test
# - mse_test close to mse_cv_mean → good generalization
# - mse_train ≈ mse_test ≈ mse_cv_mean, but all are high → underfitting
```

## Visual Intuition

### Overfitting (too complex model)

- Model passes through almost every training point
- Low training error, high test error

### Underfitting (too simple model)

- Model misses important structure (e.g., linear model on nonlinear data)
- High training and test error

![illustration](https://cdn.prod.website-files.com/614c82ed388d53640613982e/6360ef2568a0381c60b26049_overfitting-and-underfitting-in-machine-learning-1.png)

## Remedies

### Fixing Overfitting

- Simplify the model (reduce parameters, shallower trees, fewer layers)
- Apply [**regularization**](regularization.md) (L1, L2, dropout)
- Collect more training data
- Use [**cross-validation**](../workflow/cross-validation.md) to tune hyperparameters
- Apply **early stopping** in iterative models

### Fixing Underfitting

- Increase model complexity (add features, deeper trees, more layers)
- Reduce regularization strength
- Provide more informative features

## Relation to Bias–Variance Tradeoff

- Overfitting corresponds to **high variance, low bias**
- Underfitting corresponds to **high bias, low variance**
- See also: [Bias–Variance Tradeoff](bias-variance-tradeoff.md)

## Related Concepts

- [Generalization](generalization.md)
- [Regularization](regularization.md)
- [Bias–Variance Tradeoff](bias-variance-tradeoff.md)
- [Cross-Validation Methods](../workflow/cross-validation.md)

[Back to Foundations](README.md)
