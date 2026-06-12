# Model Diagnostics

Diagnostics help determine whether a model is behaving sensibly, not just scoring well.

## Regression Diagnostics

- Residual plots
- Heteroscedasticity checks
- Influence and leverage analysis
- Error by prediction range

## Classification Diagnostics

- Confusion matrix
- Precision and recall by [threshold](../evaluation/classification-thresholds-and-calibration.md)
- Probability [calibration](../evaluation/classification-thresholds-and-calibration.md)
- Error slices by subgroup

## Data Diagnostics

- Missingness patterns
- Distribution shift between train and test
- Duplicate or near-duplicate rows
- Feature drift over time

## Practical Habit

Whenever a model performs unexpectedly well or unexpectedly poorly, inspect both the data [pipeline](../workflow/pipeline-basic.md) and the error distribution before changing algorithms.

## Related Concepts

- [Baselines and Error Analysis](../evaluation/baselines-and-error-analysis.md)
- [Model Interpretability](model-interpretability.md)
- [Statsmodels Documentation](../packages/statsmodels/README.md)
- [Generalization](../foundations/generalization.md)

[Back to Interpretability and Diagnostics](README.md)
