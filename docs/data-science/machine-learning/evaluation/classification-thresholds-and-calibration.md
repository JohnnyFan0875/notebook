# Classification Thresholds and Calibration

Many classifiers produce a probability or score before they produce a class label.
Turning that score into an action requires a threshold.

## Default Threshold Is Not Always Correct

- In binary [classification](../supervised-learning/classification/README.md), `0.5` is only a default.
- If false negatives are costly, you may lower the threshold.
- If false positives are costly, you may raise the threshold.

## Threshold Selection Depends On

- Business cost of each error type
- [Class imbalance](class-imbalance.md)
- Capacity constraints, such as how many cases can be reviewed manually
- Desired precision or recall target

## Common Tools

- Precision-recall curve
- [ROC curve](roc-auc.md)
- [Confusion matrix](confusion-metrics.md) at multiple thresholds
- Cost-based decision table

## Calibration

Calibration asks whether predicted probabilities match observed frequencies.

- A well-calibrated model predicting `0.8` should be correct about 80% of the time for those cases.
- Some models rank well but are poorly calibrated.
- Calibration matters for risk scoring, triage, pricing, and resource allocation.

## Calibration Methods

- Platt scaling
- Isotonic [regression](../supervised-learning/regression/README.md)

## Practical Advice

- Separate ranking quality from probability quality.
- Tune the threshold on validation data, not the final test set.
- If downstream actions depend on the probability itself, check calibration explicitly.

## Related Concepts

- [ROC curve, AUC](roc-auc.md)
- [Confusion Matrix](confusion-metrics.md)
- [Class Imbalance](class-imbalance.md)
- [Logistic Regression](../supervised-learning/classification/logistic-regression.md)

[Back to Evaluation](README.md)
