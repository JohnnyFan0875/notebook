# Data Splitting and Leakage



[Data leakage](../foundations/data-leakage.md) happens when information from outside the training data influences the model or preprocessing during training.
It makes validation scores look better than reality.

## Correct Order

1. Define the prediction unit and timestamp.
2. Split the data using a strategy that matches the problem.
3. Fit preprocessing only on the training portion.
4. Use validation or [cross-validation](cross-validation.md) for model selection.
5. Evaluate once on the final untouched test set.

## Common Split Strategies

- **Random split**: general default when observations are independent and identically distributed.
- **Stratified split**: [classification](../supervised-learning/classification/README.md) tasks where [class balance](../evaluation/class-imbalance.md) matters.
- **Group split**: when multiple rows belong to the same user, patient, device, or store.
- **Time-based split**: forecasting or any problem with temporal order.

## Common Leakage Patterns

- Scaling, [imputation](../preprocessing/imputation.md), or encoding on the full dataset before splitting
- Feature engineering that uses future data
- Duplicated entities appearing in both train and test
- Target encoding done outside [cross-validation](cross-validation.md) folds
- [Hyperparameter tuning](hyperparameter-tuning.md) evaluated on the final test set repeatedly

## Leakage Prevention

- Use [`Pipeline`](pipeline-basic.md) and `ColumnTransformer`
- Keep a final test set untouched
- Validate feature availability at prediction time
- For grouped data, split by entity rather than by row
- For time data, train on the past and validate on the future

## Mental Model

Ask: "Would I truly know this value at the moment the prediction is made?"
If not, the feature or preprocessing design may be leaking information.

## Related Concepts

- [Data Leakage](../foundations/data-leakage.md)
- [Train-Test Split](../preprocessing/train-test-split.md)
- [Cross-Validation Methods](cross-validation.md)
- [Pipeline Basics](pipeline-basic.md)

[Back to Workflow](README.md)
