# Model Lifecycle



A model is part of a larger loop, not a one-time artifact.

## Typical Lifecycle

1. Frame the problem
2. Collect and audit data
3. Split data and define validation
4. Build a [baseline](../evaluation/baselines-and-error-analysis.md)
5. Preprocess and train candidate models
6. Tune and compare models
7. Perform [error analysis](../evaluation/baselines-and-error-analysis.md) and diagnostics
8. Package and deploy the chosen model
9. Monitor predictions, data drift, and outcome drift
10. Retrain or redesign when performance degrades

## What Often Gets Missed

- Baselines
- Error analysis
- Feature availability checks
- Monitoring after deployment
- Clear retraining criteria

## Good Practice

- Version the dataset or extraction logic
- Log parameters and evaluation results
- Save the preprocessing graph together with the model
- Define who owns monitoring and retraining

## Related Concepts

- [Problem Framing](problem-framing.md)
- [Baselines and Error Analysis](../evaluation/baselines-and-error-analysis.md)
- [Deployment and Monitoring](../production/deployment-and-monitoring.md)
- [Generalization](../foundations/generalization.md)

[Back to Workflow](README.md)
