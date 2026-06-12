# Autocorrelation in Finance

Autocorrelation measures how strongly a time series is related to its own past values. In finance, it is used to study momentum, mean reversion, and model residuals.

## Interpretation

- Positive autocorrelation suggests persistence.
- Negative autocorrelation suggests reversal.
- The pattern depends on the asset class, time horizon, and return definition.

## Use Cases

- Short-horizon mean-reversion analysis
- Longer-horizon momentum studies
- Residual diagnostics in time-series models

## Python Example

```python
from statsmodels.tsa.stattools import acf

acf_values = acf(returns, nlags=10)
print(acf_values)
```
