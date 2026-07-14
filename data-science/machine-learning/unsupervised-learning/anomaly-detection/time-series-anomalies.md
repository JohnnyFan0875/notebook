# Time-Series Anomalies

Time-series anomaly detection asks whether an observation is unusual **for that time**, not merely unusual in absolute magnitude.

That distinction matters because ordinary seasonality, trend, and calendar effects can make a perfectly normal value look extreme if you ignore temporal structure.

## Why Raw Thresholds Fail

A large value may be normal:

- on Mondays but not Sundays
- during holiday shopping season but not in February
- during a trending growth phase but not early in the series

Key point: In time series, anomalies should usually be judged against an expected baseline that includes trend, seasonality, and sometimes calendar or domain-specific features.

## A Practical Workflow

1. parse timestamps correctly
2. set a `DatetimeIndex` or equivalent time-aware structure
3. engineer calendar features when useful
4. estimate expected behavior: rolling baseline, seasonal model, decomposition, or forecasting model
5. compute residuals or anomaly scores
6. threshold the residual behavior rather than the raw series alone

```python
import pandas as pd

df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')
df['day_of_week'] = df.index.day_of_week
df['month'] = df.index.month
df['day_of_month'] = df.index.day
```

## Residual-Based Detection

One common strategy is:

\[
\text{observed} = \text{trend} + \text{seasonality} + \text{residual}
\]

Then detect anomalies from the residual component.

This works well because:

- trend absorbs slow change
- seasonality absorbs repeating structure
- residuals isolate what remains unexpectedly different

Tip: A detector run directly on raw time-series values often rediscovers seasonality rather than true anomalies.

## IoT and Sensor Anomalies Need Domain Semantics

In IoT settings, an unusual point is not always the same thing as a meaningful operational anomaly.

A strange value may come from:

- a sensor glitch
- packet loss or delayed transmission
- a device reset
- a real environmental or process change

So anomaly detection in sensor data usually needs two questions, not one:

- is this observation statistically unusual?
- is it operationally meaningful?

Key point: Many "anomalies" in telemetry are data quality events rather than business or engineering incidents.

## Simple Outlier Rules Can Be Useful, But Limited

A first pass might use a mean-and-standard-deviation rule or another simple threshold. That is often fine for triage, especially when you need to quickly inspect one sensor:

```python
temp_mean = data["temperature"].mean()
temp_std = data["temperature"].std()
```

But in a time series, this approach is fragile because:

- the baseline may drift over time
- the variance may change by season or hour
- autocorrelation makes consecutive observations dependent

That is why a global z-score rule is often best treated as a screening tool, not the final anomaly logic.

## Labels Turn Detection into Supervised Alerting

Some operational datasets eventually include a `label` column that marks whether a window is normal or abnormal. Once those labels exist, the problem changes:

- without labels: detect unusual behavior from structure alone
- with labels: learn a classifier that predicts known alert states

This distinction matters because a labeled anomaly dataset is no longer just an outlier-detection problem. It becomes a supervised learning problem with all the usual concerns:

- label quality
- class imbalance
- train / test leakage across time
- whether the label marks root cause, symptom, or only a downstream alarm

## Ensemble Thinking

For difficult time series, practitioners often compare several detectors rather than trusting only one:

- neighborhood-based detector
- isolation-based detector
- residual thresholding rule

Agreement across several methods is often more useful for triage than any single score viewed in isolation.
