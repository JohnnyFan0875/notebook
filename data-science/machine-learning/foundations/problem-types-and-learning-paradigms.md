# Problem Types and Learning Paradigms

Machine learning starts with framing the problem correctly.
Before choosing a model, identify what kind of signal you have and what kind of output you need.

## Major Learning Paradigms

- **Supervised learning**: learn from labeled examples.
  - Input: features `X`
  - Output: known target `y`
- **Unsupervised learning**: look for structure without labels.
- **Semi-supervised learning**: use a small amount of labeled data together with more unlabeled data.
- **Self-supervised learning**: create training signals from the data itself.
- **Reinforcement learning**: learn actions from reward signals over time.

## Common Problem Types

- [**Regression**](../supervised-learning/regression/README.md): predict a continuous value such as price, revenue, or duration.
- [**Classification**](../supervised-learning/classification/README.md): predict a category such as spam / not spam or churn / no churn.
- **Ranking**: order items by relevance or priority.
- [**Clustering**](../unsupervised-learning/clustering/README.md): group similar observations without labels.
- [**Dimensionality reduction**](../unsupervised-learning/dimensionality-reduction/README.md): compress features while preserving useful structure.
- **Anomaly detection**: identify unusual or rare patterns.
- **Time series forecasting**: predict future values while preserving time order.

## Why This Matters

- Problem type determines which models are appropriate.
- Problem type influences how data should be split.
- Problem type affects which metrics are meaningful.
- Wrong framing often creates more problems than wrong model selection.

## Quick Examples

- Predict house price: regression
- Predict whether an email is spam: classification
- Group customers by behavior: clustering
- Compress hundreds of correlated variables: dimensionality reduction
- Predict next month's sales: time series forecasting

## Practical Rule

If the prediction target, decision point, or unit of analysis is unclear, do not start tuning models yet.

## Related Concepts

- [Problem Framing](../workflow/problem-framing.md)
- [Supervised Learning](../supervised-learning/README.md)
- [Unsupervised Learning](../unsupervised-learning/README.md)
- [Evaluation Mindset](evaluation-mindset.md)

[Back to Foundations](README.md)
