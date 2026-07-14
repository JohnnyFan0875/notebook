# Regularization

Regularization is a set of techniques used to control model complexity and improve [generalization](generalization.md).

## Why Regularization Helps

- Complex models can fit noise instead of signal.
- Regularization discourages overly flexible solutions.
- It often reduces variance at the cost of a small increase in bias.

## Common Forms

### L1 Regularization

- Adds a penalty proportional to the absolute value of coefficients
- Encourages sparsity
- Common in [Lasso regression](../supervised-learning/regression/lasso.md)

### L2 Regularization

- Adds a penalty proportional to the squared value of coefficients
- Shrinks coefficients smoothly
- Common in [Ridge regression](../supervised-learning/regression/ridge.md)

### Elastic Net

- Combines L1 and L2 penalties
- Useful when features are correlated and some sparsity is still desired

## Other Regularization Ideas

- Limiting tree depth
- Early stopping
- Dropout in neural networks
- [Feature selection](../preprocessing/feature-selection.md)
- Collecting more training data

## Tradeoff

- Too little regularization can lead to [overfitting](overfitting-underfitting.md).
- Too much regularization can lead to [underfitting](overfitting-underfitting.md).

## Practical Rule

Regularization is not only about penalties in linear models; any method that constrains model flexibility plays a similar role.

## Related Concepts

- [Lasso Regression](../supervised-learning/regression/lasso.md)
- [Ridge Regression](../supervised-learning/regression/ridge.md)
- [Elastic Net Regression](../supervised-learning/regression/elastic-net.md)
- [Bias–Variance Tradeoff](bias-variance-tradeoff.md)

[Back to Foundations](README.md)
