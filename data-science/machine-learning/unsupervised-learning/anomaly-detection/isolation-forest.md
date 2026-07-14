# Isolation Forest

Isolation Forest is an unsupervised anomaly detection method based on a simple idea: anomalous points are easier to isolate than normal points.

Instead of modeling the dense region directly, it repeatedly partitions the feature space with random splits. Observations that get isolated in fewer splits receive higher anomaly scores.

## Why It Works

If a point lies far from the main cloud of data, random partitions tend to separate it quickly.

| Observation type | Typical path length |
| ---------------- | ------------------- |
| Inlier in dense region | Longer |
| Isolated outlier | Shorter |

Key point: Isolation Forest is not measuring distance in the usual KNN sense. It is measuring how quickly a point becomes isolated under many random recursive partitions.

## Main Hyperparameters

| Hyperparameter | Role | Practical meaning |
| -------------- | ---- | ----------------- |
| `n_estimators` | Number of trees | More trees usually stabilize scores |
| `max_samples` | Subsample size per tree | Controls randomness and runtime |
| `max_features` | Feature subsampling | Can help in wide datasets |
| `contamination` | Thresholding assumption | Fraction flagged as anomalies |

Tip: Tune `contamination` separately from the ranking logic in your mind. A model can rank suspicious points well even when the current binary cutoff is wrong.

## Typical Usage

```python
from pyod.models.iforest import IForest

iforest = IForest(
    n_estimators=200,
    max_samples='auto',
    contamination=0.05,
    random_state=42,
)

iforest.fit(X_train)
scores = iforest.decision_scores_
labels = iforest.labels_
```

## Strengths

- works well for high-dimensional tabular data
- scales better than many exact distance-based methods
- handles multivariate anomalies naturally
- does not require pairwise distance computation between every point

## Limitations

- threshold selection is still a separate problem
- feature scaling and feature quality still matter
- anomaly scores can move when the dataset composition changes
- not ideal when the anomaly pattern is fundamentally sequential or time-dependent

Warning: Isolation Forest can miss anomalies that are not globally isolated in feature space but are only unusual relative to local neighborhoods or temporal context.
