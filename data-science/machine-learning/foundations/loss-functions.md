# Loss Functions

A loss function measures how wrong a model's predictions are.
Training usually means choosing model parameters that minimize a loss function.

This note focuses on **machine-learning model choice**: which loss aligns with regression vs classification goals, and how training loss differs from evaluation metrics. For deep-learning implementations in PyTorch and the role of loss in backpropagation, see [Deep Learning: Loss Functions](../../deep-learning/fundamentals/loss-functions.md).

## Why Loss Functions Matter

- They define what the model is trying to optimize.
- Different losses make models behave differently.
- The best evaluation metric is not always the same as the training loss.

## Common Losses

### Regression

- [**MSE**](../evaluation/mse-rmse.md): penalizes large errors more strongly
- [**RMSE**](../evaluation/mse-rmse.md): square root of MSE, easier to interpret in target units
- **MAE**: more robust to outliers than MSE

### Classification

- **Log loss / cross-entropy**: common for probabilistic classifiers
- **Hinge loss**: common in [support vector machines](../supervised-learning/classification/svm.md)
- **0-1 loss**: conceptually simple, but hard to optimize directly

## Choosing a Loss

- Use [MSE](../evaluation/mse-rmse.md) when large errors are especially costly.
- Use MAE when robustness to outliers matters.
- Use log loss when calibrated probabilities are important.
- Use hinge loss when margin-based [classification](../supervised-learning/classification/README.md) is the goal.

## Important Distinction

- **Training loss** is optimized during fitting.
- **Evaluation metric** is used to judge model usefulness.

For example:

- A model may train on log loss
- But be selected based on [ROC-AUC](../evaluation/roc-auc.md) or [F1-score](../evaluation/confusion-metrics.md)
- And still ultimately be judged by business impact

## Practical Rule

Do not assume the model is optimizing the metric you care about unless you verify it.

## Related Concepts

- [MSE, RMSE](../evaluation/mse-rmse.md)
- [ROC curve, AUC](../evaluation/roc-auc.md)
- [Confusion Matrix](../evaluation/confusion-metrics.md)
- [Classification Thresholds and Calibration](../evaluation/classification-thresholds-and-calibration.md)

[Back to Foundations](README.md)
