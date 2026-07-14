# Generalization

Generalization is the ability of a model to perform well on new, unseen data rather than only on the data it was trained on.

## Why Generalization Matters

- A model with perfect training performance can still fail in practice.
- The real goal of machine learning is not memorization.
- Validation and test performance are proxies for future real-world performance.

## Key Terms

- **Training error**: error on the data used to fit the model
- **Validation error**: error on data used for model selection and tuning
- **Test error**: error on a final untouched dataset used for final evaluation
- **In-sample performance**: performance on seen data
- **Out-of-sample performance**: performance on unseen data

## Typical Patterns

- Low training error and high test error often suggest [overfitting](overfitting-underfitting.md).
- High training error and high test error often suggest [underfitting](overfitting-underfitting.md).
- Similar validation and test performance usually indicate a healthier evaluation process.

## What Affects Generalization

- Model complexity
- Sample size
- Noise in the data
- [Data leakage](data-leakage.md)
- Mismatch between training and deployment distributions
- Feature quality

## Improving Generalization

- Use proper train/validation/test separation
- Use [cross-validation](../workflow/cross-validation.md) where appropriate
- Control model complexity with [regularization](regularization.md) or constraints
- Improve feature quality rather than only increasing model complexity
- Match evaluation design to the real prediction setting

## Interview Fast Answer

如果面試官直接問 generalization 是什麼，一個夠好的短答通常是：

- 模型不只在 training data 上表現好
- 在 unseen data 上也能維持合理表現

再補一句就很完整：

- train metrics 和 validation / test metrics 不應該差太遠
- 過度擬合的模型通常 generalize 不好

## Practical Rule

Always ask whether the validation setup resembles the conditions under which the model will actually be used.

## Related Concepts

- [Overfitting and Underfitting](overfitting-underfitting.md)
- [Data Leakage](data-leakage.md)
- [Cross-Validation Methods](../workflow/cross-validation.md)
- [Sampling and Representativeness](sampling-and-representativeness.md)

[Back to Foundations](README.md)
