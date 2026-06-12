# Model Interpretability

Interpretability is about understanding how a model uses information.
The right tool depends on the model and the question you are asking.

## Common Approaches

- **Coefficients**: useful for linear and [logistic regression](../supervised-learning/classification/logistic-regression.md), but interpretation depends on scaling, collinearity, and feature coding.
- **Feature importance**: common for tree-based models, but importance can be unstable or biased toward high-cardinality features.
- **Permutation importance**: model-agnostic and often a better default than impurity-based importance.
- **Partial dependence / ICE**: show how predictions change as a feature changes.
- **SHAP**: local and global explanations for complex models.

## Important Cautions

- Correlated features can distort importances.
- A feature being important does not mean it is causal.
- Explanations of a single prediction do not automatically summarize the whole model.

## Practical Advice

- Start with simple model behavior checks.
- Use permutation importance for a more robust first pass.
- Pair explanations with slice-based evaluation and domain knowledge.

## Related Concepts

- [Model Diagnostics](model-diagnostics.md)
- [Feature Selection](../preprocessing/feature-selection.md)
- [Random Forest](../supervised-learning/ensemble/random-forest.md)
- [Statsmodels Documentation](../packages/statsmodels/README.md)

[Back to Interpretability and Diagnostics](README.md)
