# Data Leakage

Data leakage occurs when information unavailable at prediction time influences model training or evaluation.
It creates overly optimistic performance estimates.

## Why It Is Dangerous

- It makes models look better than they really are.
- It leads to painful failures in production.
- It can happen through preprocessing, splitting, [feature engineering](feature-engineering-principles.md), or repeated tuning on the test set.

## Common Leakage Patterns

- Fitting scalers or [imputers](../preprocessing/imputation.md) on the full dataset before splitting
- Including future information in features
- Letting the same entity appear in both training and test sets
- Tuning against the test set repeatedly during [hyperparameter tuning](../workflow/hyperparameter-tuning.md)
- Using target information inside feature construction

## Conceptual Check

For every feature, ask:

- Would this value truly be known at prediction time?
- Was this transformation fit only on training data?
- Does the validation setup prevent information from crossing folds or time boundaries?

## Where to Read Next

- Workflow-oriented implementation guidance: [workflow/data-splitting-and-leakage.md](../workflow/data-splitting-and-leakage.md)
- Safe preprocessing design: [workflow/pipeline-basic.md](../workflow/pipeline-basic.md)

## Related Concepts

- [Train-Test Split](../preprocessing/train-test-split.md)
- [Cross-Validation Methods](../workflow/cross-validation.md)
- [Pipeline Basics](../workflow/pipeline-basic.md)
- [Feature Engineering Principles](feature-engineering-principles.md)

[Back to Foundations](README.md)
