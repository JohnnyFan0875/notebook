# Core Concepts

This note defines anomaly-detection concepts such as outliers, novelty, contamination, and thresholding. If you are looking for experiment-design terminology or survival-analysis censoring, those topics live in [Core Concepts & Terminology](../../../statistics/experimental-design/core-concepts.md) and [Core Concepts & Censoring](../../../statistics/survival-analysis/core-concepts.md).

An anomaly is an observation that looks unusually different from the bulk of the data under the representation and assumptions you are using.

Key point: "Unusual" is never purely objective. It depends on what features are included, what scale they are on, what time context exists, and what kind of abnormality matters in the problem domain.

## Outliers vs. Anomalies vs. Novelty

These terms are related but not interchangeable:

| Term | Typical Meaning | Common Use |
| ---- | --------------- | ---------- |
| **Outlier** | A data point unusually far from the rest | Statistical summaries, preprocessing |
| **Anomaly** | A suspicious or abnormal observation | Monitoring, fraud, fault detection |
| **Novelty** | A new pattern not seen in clean training data | Deployment-time detection |

Tip: Outlier detection often assumes training data may already contain anomalies. Novelty detection usually assumes the training data is mostly clean and asks whether future data departs from that baseline.

## Common Types of Anomalies

| Type | Meaning | Example |
| ---- | ------- | ------- |
| **Point anomaly** | One observation is individually unusual | A transaction 100x larger than typical |
| **Contextual anomaly** | Unusual only in a particular context | High electricity usage at 3 a.m. |
| **Collective anomaly** | A pattern across multiple observations is unusual | A burst of failed logins over 10 minutes |
| **Multivariate anomaly** | Individual features look ordinary, but the combination is unusual | A child's height is ordinary, weight is ordinary, but the pair is implausible together |

Key point: Multivariate anomalies are one reason simple univariate rules are often insufficient. A point can look normal in every single column and still be abnormal in the joint feature space.

## A Practical Workflow

Anomaly detection usually follows this pattern:

1. clarify whether the goal is cleaning, alerting, triage, or automated blocking
2. define the unit of analysis: event, user, device, day, or time window
3. choose features that express normal behavior
4. scale and preprocess carefully
5. fit a detector that matches the structure of the data
6. inspect anomaly scores before locking in a threshold
7. evaluate with domain feedback, labels, or downstream utility

## Thresholds and Contamination

Most unsupervised anomaly detectors do not begin with a natural yes/no boundary. They produce a ranking or score, then require a threshold.

One common parameter is **contamination**:

- it specifies the fraction of observations you are willing to flag as anomalous
- it converts raw scores into binary labels
- it should be treated as a modeling assumption, not a discovered fact

Warning: If contamination is badly misspecified, the model may still produce sensible rankings but misleading binary flags.

When labels are available, evaluate two separate questions:

1. does the model rank true anomalies near the top?
2. does the chosen decision threshold produce an acceptable precision-recall tradeoff?

Tip: A weak binary result does not always mean the detector is bad. Sometimes the ranking is useful, but the cutoff is poorly chosen.

## Scaling and Feature Choice

Distance- and isolation-based methods are strongly affected by representation.

Important checks:

- are numeric features on comparable scales?
- are rare categorical values encoded appropriately?
- are calendar effects or time windows missing?
- does one noisy feature dominate all others?

Tip: Good anomaly detection is often more about feature design and thresholding discipline than about finding a fancier algorithm.
