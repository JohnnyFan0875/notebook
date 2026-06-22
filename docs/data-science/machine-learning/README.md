# Machine Learning

這個章節以「從問題到部署」的完整工作流來整理機器學習，而不是單純羅列模型。若你只記演算法名稱，卻沒有先建立 workflow、evaluation 與 data leakage 的觀念，實務上很容易得出看似漂亮但不可用的結果。

## How to Navigate

- [foundations](foundations/README.md): Core ideas such as bias-variance tradeoff and overfitting.
- [workflow](workflow/README.md): Problem framing, data splitting, leakage, cross-validation, pipelines, and tuning.
- [preprocessing](preprocessing/README.md): Missing values, encoding, scaling, outliers, and feature selection.
- [supervised-learning](supervised-learning/README.md): Classification, regression, and ensemble methods.
- [unsupervised-learning](unsupervised-learning/README.md): Clustering, dimensionality reduction, and association rules.
- [recommender-systems](recommender-systems/README.md): Recommendation logic, collaborative filtering, ALS, and implicit feedback.
- [evaluation](evaluation/README.md): Metrics, thresholds, calibration, class imbalance, and error analysis.
- [interpretability-and-diagnostics](interpretability-and-diagnostics/README.md): Feature importance, diagnostics, and model debugging.
- [production](production/README.md): Deployment, monitoring, drift, and retraining considerations.
- [packages](packages/README.md): Package-specific notes such as `[scikit-learn](packages/scikit-learn/README.md)` and `statsmodels`.

## Suggested Learning Order

1. Start with [foundations](foundations/README.md).
2. Read the core [workflow](workflow/README.md) notes, especially data splitting and leakage.
3. Learn [preprocessing](preprocessing/README.md) together with [Pipeline Basics](workflow/pipeline-basic.md).
4. Go into [supervised-learning](supervised-learning/README.md), [unsupervised-learning](unsupervised-learning/README.md), or [recommender-systems](recommender-systems/README.md) depending on the problem.
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

## A Practical Path

If you are new to this section, read `foundations -> workflow -> preprocessing -> supervised or unsupervised -> evaluation -> interpretability -> production`. That order mirrors how real projects mature.
