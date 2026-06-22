# Anomaly Detection

Anomaly detection looks for observations that deviate meaningfully from the prevailing pattern of the data. Unlike ordinary outlier cleaning, the goal is often to **surface rare but important cases** rather than automatically remove them.

## Topics

- [Core Concepts](core-concepts.md)
- [Isolation Forest](isolation-forest.md)
- [Distance- and Density-Based Methods](distance-density.md)
- [Time-Series Anomalies](time-series-anomalies.md)

## Notes

- Anomalies can be point anomalies, contextual anomalies, or collective anomalies.
- Many anomaly detectors output a **score** first and a binary flag only after a threshold is chosen.
- The same rare point may be informative in fraud detection but harmful noise in data preprocessing. Context decides the right response.

## Interpretation Reminders

- A model can be good at ranking suspicious cases even when the final threshold is still uncertain.
- `contamination` is a decision setting, not a discovered truth about the world.
- Distance-based methods are sensitive to scaling; standardization is often mandatory.
- For time series, anomalies should usually be judged against trend, seasonality, and calendar structure rather than raw values alone.

[Back to Unsupervised Learning](../README.md)
