# Problem Framing



Before choosing a model, define the problem in a way that matches the data and the business decision.

## Common ML Problem Types

- **Regression**: predict a continuous value such as price, demand, or risk score.
- **Classification**: predict a category such as churn / no churn or fraud / not fraud.
- **Ranking**: order items such as search results or recommendations.
- **Clustering**: group similar observations without labels.
- **Anomaly detection**: identify unusual observations.
- **Time series forecasting**: predict future values while respecting time order.

## Questions to Clarify Early

- What exactly is the target?
- What is the unit of prediction: user, order, session, product, day?
- When is the prediction made relative to the event being predicted?
- Which errors are more costly: false positives or false negatives?
- What data will be available at prediction time?

## Output Type Guides the Rest

- The problem type affects which models are valid.
- The decision context affects which metric matters.
- The data-generating process affects which split strategy is realistic.

## Common Failure Modes

- Framing a ranking problem as a plain [classification](../supervised-learning/classification/README.md) task
- Using future information that would not exist at prediction time
- Optimizing accuracy when recall or precision is what the business actually needs

## Practical Rule

If the target definition, decision [threshold](../evaluation/classification-thresholds-and-calibration.md), and prediction timestamp are unclear, do not start model tuning yet.

## Related Concepts

- [Problem Types and Learning Paradigms](../foundations/problem-types-and-learning-paradigms.md)
- [Evaluation Mindset](../foundations/evaluation-mindset.md)
- [Supervised Learning](../supervised-learning/README.md)
- [Unsupervised Learning](../unsupervised-learning/README.md)

[Back to Workflow](README.md)
