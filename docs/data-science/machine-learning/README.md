# Machine Learning

## How to Navigate

- [foundations](foundations/README.md): Core ideas such as bias-variance tradeoff and overfitting.
- [workflow](workflow/README.md): Problem framing, data splitting, leakage, cross-validation, pipelines, and tuning.
- [preprocessing](preprocessing/README.md): Missing values, encoding, scaling, outliers, and feature selection.
- [supervised-learning](supervised-learning/README.md): Classification, regression, and ensemble methods.
- [unsupervised-learning](unsupervised-learning/README.md): Clustering, dimensionality reduction, and association rules.
- [evaluation](evaluation/README.md): Metrics, thresholds, calibration, class imbalance, and error analysis.
- [interpretability-and-diagnostics](interpretability-and-diagnostics/README.md): Feature importance, diagnostics, and model debugging.
- [production](production/README.md): Deployment, monitoring, drift, and retraining considerations.
- [packages](packages/README.md): Package-specific notes such as `[scikit-learn](packages/scikit-learn/README.md)` and `statsmodels`.

## Suggested Learning Order

1. Start with [foundations](foundations/README.md).
2. Read the core [workflow](workflow/README.md) notes, especially data splitting and leakage.
3. Learn [preprocessing](preprocessing/README.md) together with [Pipeline Basics](workflow/pipeline-basic.md).
4. Go into [supervised-learning](supervised-learning/README.md) or [unsupervised-learning](unsupervised-learning/README.md) depending on the problem.
5. Study [evaluation](evaluation/README.md) before trusting any model result.
6. Add [interpretability-and-diagnostics](interpretability-and-diagnostics/README.md) and [production](production/README.md) for real-world practice.

## Naming Conventions

- Feature = predictor variable = independent variable = explanatory variable
- Target = dependent variable = response variable
- Label = observed target for supervised learning
- Hyperparameter = setting chosen before training, such as `alpha`, `max_depth`, or `n_neighbors`

## Important Reminders

- Do not fit scalers, imputers, or encoders on the full dataset before splitting.
- Use a validation strategy that matches the data: random split, stratified split, group split, or time-based split.
- Keep a final test set untouched until model selection is done.
- Always compare against a simple baseline before celebrating a complex model.
