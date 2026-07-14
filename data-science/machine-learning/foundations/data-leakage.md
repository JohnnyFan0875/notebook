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
- Taking the latest status of an entity instead of the status as of the reference date
- Letting the same entity appear in both training and test sets
- Tuning against the test set repeatedly during [hyperparameter tuning](../workflow/hyperparameter-tuning.md)
- Using target information inside feature construction

## Conceptual Check

For every feature, ask:

- Would this value truly be known at prediction time?
- Was this transformation fit only on training data?
- Does the validation setup prevent information from crossing folds or time boundaries?
- Was this feature computed from a timeline-compliant snapshot rather than from the full history?

## Tabular Projects Often Leak Through Basetable Design

在 event-level 或 customer-level 問題裡，leakage 很常不是出在模型，而是出在 basetable 的建法。

典型例子包括：

- 用 target period 內的交易去算「最近一年總金額」
- 直接 join 一張只保留最新狀態的 dimension table
- 用全歷史資料算 category frequency、default rate 或 segment summary

這些做法常常讓 validation 看起來很好，因為模型其實偷看了未來。

## Where to Read Next

- Workflow-oriented implementation guidance: [workflow/data-splitting-and-leakage.md](../workflow/data-splitting-and-leakage.md)
- Safe preprocessing design: [workflow/pipeline-basic.md](../workflow/pipeline-basic.md)
- Time-aware tabular feature design: [basetable-and-time-aware-feature-engineering.md](basetable-and-time-aware-feature-engineering.md)

## Related Concepts

- [Train-Test Split](../preprocessing/train-test-split.md)
- [Cross-Validation Methods](../workflow/cross-validation.md)
- [Pipeline Basics](../workflow/pipeline-basic.md)
- [Feature Engineering Principles](feature-engineering-principles.md)

[Back to Foundations](README.md)
