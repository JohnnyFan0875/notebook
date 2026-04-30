# Bias–Variance Tradeoff



## Overview

The **bias–variance tradeoff** describes the balance between a model’s ability to capture patterns in training data and its ability to [generalize](generalization.md) to unseen data.

- **Bias**: Error introduced by overly simplistic assumptions in the model.

  - Difference between expected model prediction and the true value (accuracy).
  - High bias → model is too simple → [**underfitting**](overfitting-underfitting.md).

- **Variance**: Sensitivity of the model to fluctuations in the training set.

  - Measures how much predictions change if trained on different data (precision).
  - High variance → model fits training data too closely → [**overfitting**](overfitting-underfitting.md).

- **Total Error** = Bias² + Variance + Irreducible Error

## Visual Intuition

- **High bias (underfit)**: predictions miss important patterns.
- **High variance (overfit)**: predictions capture noise as if it were signal.
- **Goal**: find a balance where both bias and variance are reasonably low.

![Bias Variance Tradeoff Illustration](https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/Bias_and_variance_contributing_to_total_error.svg/1280px-Bias_and_variance_contributing_to_total_error.svg.png)
![Bias Variance Tradeoff Illustration](https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/images/bias_variance/bullseye.png)

## Strategies to Manage the Tradeoff

- [**Regularization**](regularization.md): prevents overfitting (e.g., L1/L2 penalties).
- [**Cross-validation**](../workflow/cross-validation.md): estimate generalization error and tune complexity.
- **Ensemble methods**: reduce variance without greatly increasing bias.
  - [Bagging](../supervised-learning/ensemble/bagging.md) (e.g., [Random Forest](../supervised-learning/ensemble/random-forest.md))
  - Boosting (e.g., [Gradient Boosting](../supervised-learning/ensemble/gradient-boosting.md))
- **Model complexity adjustment**: e.g., tuning tree depth (`max_depth`).

## Related Concepts

- [Generalization](generalization.md)
- [Regularization](regularization.md)
- [Overfitting and Underfitting](overfitting-underfitting.md)
- [Cross-Validation Methods](../workflow/cross-validation.md)

[Back to Foundations](README.md)
