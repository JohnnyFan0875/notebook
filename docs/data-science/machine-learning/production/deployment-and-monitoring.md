# Deployment and Monitoring

Deploying a model means operationalizing the full prediction workflow, not only the estimator.

## What Should Be Saved

- The preprocessing [pipeline](../workflow/pipeline-basic.md)
- The trained model
- Feature names and expected schema
- Model version and training metadata

## Production Concerns

- Batch vs real-time inference
- Latency and throughput
- Missing or malformed input data
- Reproducibility of the feature [pipeline](../workflow/pipeline-basic.md)

## Monitoring

- Prediction volume
- Input drift
- Target or outcome drift
- Latency and failure rate
- Downstream business metrics

## Retraining Triggers

- Performance degradation
- Significant feature drift
- New business rules or target definitions
- Major changes in upstream data collection

## Practical Rule

If you cannot reproduce the training transformations in production, the model is not truly deployable.

## Related Concepts

- [Model Lifecycle](../workflow/model-lifecycle.md)
- [Pipeline Basics](../workflow/pipeline-basic.md)
- [Generalization](../foundations/generalization.md)
- [Data Leakage](../foundations/data-leakage.md)

[Back to Production](README.md)
