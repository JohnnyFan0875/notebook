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

## Ensemble Thinking

For difficult time series, practitioners often compare several detectors rather than trusting only one:

- neighborhood-based detector
- isolation-based detector
- residual thresholding rule

Agreement across several methods is often more useful for triage than any single score viewed in isolation.
