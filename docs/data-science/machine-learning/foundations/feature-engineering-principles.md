# Feature Engineering Principles

Feature engineering is the process of turning raw data into informative inputs for a model.

## Why It Matters

- Better features often improve performance more than switching algorithms.
- Features determine what information the model can actually use.
- Poor feature design can introduce [leakage](data-leakage.md), noise, or instability.

## Common Principles

- Make features reflect information available at prediction time.
- Prefer meaningful domain-driven transformations over arbitrary complexity.
- Respect the structure of the data: numeric, categorical, text, temporal, grouped.
- Keep transformations reproducible and consistent between training and inference.

## Common Examples

- Log-transforming skewed numeric variables
- Extracting day-of-week or month from timestamps
- Creating interaction features
- Aggregating behavior over a past time window

## Risks

- [Data leakage](data-leakage.md)
- Overly sparse or noisy features
- Unstable encodings for high-cardinality categories
- Features that depend on business rules that later change

## Practical Rule

Ask whether the feature is informative, available at prediction time, and stable enough to maintain.

## Related Concepts

- [Data Leakage](data-leakage.md)
- [Feature Selection](../preprocessing/feature-selection.md)
- [Categorical Encoding](../preprocessing/categorical-encoding.md)
- [Pipeline Basics](../workflow/pipeline-basic.md)

[Back to Foundations](README.md)
