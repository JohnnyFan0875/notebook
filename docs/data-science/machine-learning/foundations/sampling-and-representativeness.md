# Sampling and Representativeness

A model can only learn from the data it sees.
If the data are not representative of the real deployment setting, even a strong model can fail.

## Core Ideas

- **Sampling bias**: the training data are collected in a biased way
- **Selection bias**: some groups are more likely to appear than others
- **Distribution shift**: training and future data come from different distributions

## Why This Matters

- Validation results may not reflect real-world [performance](generalization.md).
- Some groups may be underrepresented.
- Rare but important cases may be missed entirely.

## Common Examples

- Training a fraud model on only reviewed cases
- Training a medical model from one hospital and applying it elsewhere
- Using historical data collected under a different business policy

## Questions to Ask

- Who or what is missing from the data?
- Does the sample reflect the production population?
- Are important edge cases represented?
- Has the data-generating process changed over time?

## Practical Rule

Bad data coverage cannot be fixed purely by a better algorithm.

## Related Concepts

- [Generalization](generalization.md)
- [Evaluation Mindset](evaluation-mindset.md)
- [Model Lifecycle](../workflow/model-lifecycle.md)
- [Deployment and Monitoring](../production/deployment-and-monitoring.md)

[Back to Foundations](README.md)
