# Evaluation Mindset

Good evaluation is about more than choosing a metric.
It is about making sure the validation process reflects the real decision you care about.

## Key Principles

- Match the metric to the business or scientific objective.
- Match the split strategy to the deployment setting.
- Compare against a simple baseline.
- Inspect failure modes, not only average performance.

## Common Mistakes

- Optimizing accuracy on an [imbalanced classification problem](../evaluation/class-imbalance.md)
- Using a random split for grouped or time-dependent data
- Picking a model based only on one summary score
- Looking at the test set repeatedly during tuning

## Better Questions

- What kind of mistakes are most costly?
- Which subgroups matter most?
- Is [threshold selection](../evaluation/classification-thresholds-and-calibration.md) part of the decision process?
- Does offline performance relate to the real-world outcome?

## Practical Rule

Evaluation should be designed before model comparison, not after.

See also:

- [Baselines and Error Analysis](../evaluation/baselines-and-error-analysis.md)
- [Classification Thresholds and Calibration](../evaluation/classification-thresholds-and-calibration.md)
- [Data Splitting and Leakage](../workflow/data-splitting-and-leakage.md)

## Related Concepts

- [Generalization](generalization.md)
- [Class Imbalance](../evaluation/class-imbalance.md)
- [Baselines and Error Analysis](../evaluation/baselines-and-error-analysis.md)
- [Problem Framing](../workflow/problem-framing.md)

[Back to Foundations](README.md)
