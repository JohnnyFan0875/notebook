# Workflow



This section focuses on the end-to-end process of building a machine learning solution.
It is the most important section for avoiding common practical mistakes.

## Core Workflow

1. [Problem Framing](problem-framing.md)
2. [Data Splitting and Leakage](data-splitting-and-leakage.md)
3. [Cross-Validation](cross-validation.md)
4. [Pipeline Basics](pipeline-basic.md)
5. [Hyperparameter Tuning](hyperparameter-tuning.md)
6. [Model Lifecycle](model-lifecycle.md)

## Key Principle

Fit anything that learns from data, including [imputers](../preprocessing/imputation.md), scalers, encoders, and feature selectors, **only on the training portion inside a [pipeline](pipeline-basic.md) or training fold**.

[Back to Machine Learning](../README.md)
