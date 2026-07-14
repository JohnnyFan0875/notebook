# Ensemble Methods

Ensemble methods combine multiple learners to improve stability, accuracy, or both.

## Topics

- [Bagging](bagging.md)
- [Random Forest](random-forest.md)
- [AdaBoost](adaboost.md)
- [Gradient Boosting](gradient-boosting.md)
- [XGBoost](xgboost.md)
- [Voting](voting.md)
- [Stacking](stacking.md)

## Notes

- Bagging reduces variance.
- Boosting focuses on sequentially improving weak learners.
- Voting and stacking combine diverse models in different ways.

## Practical Reminders

- Ensembles often improve scores, but they also increase complexity in interpretation and deployment.
- If the base workflow is leaking or unstable, an ensemble will usually hide the problem rather than fix it.
- Pair ensemble use with [error analysis](../../evaluation/baselines-and-error-analysis.md) and [diagnostics](../../interpretability-and-diagnostics/model-diagnostics.md).

[Back to Supervised Learning](../README.md)
