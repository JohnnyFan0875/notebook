# Baselines and Error Analysis



Before comparing sophisticated models, build a simple baseline.
After selecting a promising model, study its mistakes.

## Baselines

- **Regression**: mean predictor, median predictor, simple [linear [regression](../supervised-learning/regression/README.md)](../supervised-learning/regression/linear.md)
- **Classification**: majority class, stratified random predictor, simple [logistic regression](../supervised-learning/classification/logistic-regression.md)
- **Time series**: naive forecast, seasonal naive forecast

## Why Baselines Matter

- They tell you whether the problem is genuinely hard.
- They expose [data leakage](../foundations/data-leakage.md) when a complex model looks implausibly good.
- They provide a minimum bar for future models.

## Error Analysis Questions

- Which classes or ranges does the model struggle with?
- Are errors concentrated in specific users, segments, geographies, or time periods?
- Are there systematic false positives or false negatives?
- Do errors correlate with missingness, outliers, or certain feature ranges?

## Useful Slices

- By class
- By customer segment
- By time period
- By geography
- By feature bucket, such as low income vs high income

## Practical Rule

If the aggregate metric looks acceptable but the model fails badly on an important slice, the model is not ready.

## Related Concepts

- [Evaluation Mindset](../foundations/evaluation-mindset.md)
- [Data Leakage](../foundations/data-leakage.md)
- [Model Diagnostics](../interpretability-and-diagnostics/model-diagnostics.md)
- [Model Lifecycle](../workflow/model-lifecycle.md)

[Back to Evaluation](README.md)
