# Parametric Survival Models

Parametric survival models assume that **event times follow a specific probability distribution**.
Unlike the semi-parametric **Cox proportional hazards model**, which leaves the baseline hazard unspecified, parametric models explicitly define the shape of the hazard function.

This allows smoother survival and hazard estimates, easier extrapolation beyond observed follow-up, and direct computation of mean survival time.

Key point: Parametric survival models are strongest when the assumed hazard shape is informative rather than arbitrary. Their power comes from structure, but that same structure becomes a liability if the chosen distribution is wrong.

## Concept and Rationale

| Feature | Cox Model | Parametric Model |
| --------------- | ------------------------------ | --------------------------------------------- |
| Baseline hazard | Unspecified (non-parametric) | Explicitly modeled by a known distribution |
| Flexibility | Good for moderate sample sizes | Best when data follow a theoretical form |
| Output | Hazard ratios | Survival, hazard, and mean time estimates |
| Use cases | Prognostic factor analysis | Extrapolation, simulation, cost-effectiveness |

## Common Distributions

Parametric models differ by the assumed shape of the hazard over time:

| Distribution | Hazard Shape | Typical Application |
| ---------------- | --------------------------------------- | -------------------------------------- |
| **Exponential** | Constant hazard | Device reliability, simple processes |
| **Weibull** | Increasing or decreasing hazard | Medical survival, reliability testing |
| **Log-normal** | Hazard rises then falls | Biological recovery or latency periods |
| **Log-logistic** | Similar to log-normal but heavier tails | Long-term survival with late events |

Each distribution provides both a **survival function $S(t)$** and a **hazard function $h(t)$**.
Example for the **Weibull model**:

\[
S(t) = \exp\!\left[-\left(\frac{t}{\lambda}\right)^k\right], \qquad
h(t) = \frac{k}{\lambda}\left(\frac{t}{\lambda}\right)^{k-1}
\]

where:

- $ \lambda $: scale parameter
- $ k $: shape parameter
  - $k > 1$: hazard increases over time
  - $k < 1$: hazard decreases over time

## How to Choose a Distribution

In practice, distribution choice is often guided by both subject-matter reasoning and empirical fit:

| If the hazard seems... | Candidate distribution |
| ---------------------- | ---------------------- |
| Roughly constant over time | Exponential |
| Monotone increasing or decreasing | Weibull |
| Rises then falls | Log-normal or log-logistic |
| Heavy-tailed with late events | Log-logistic |

Tip: Do not choose a distribution by convenience alone. Overlay the fitted survival curve against the Kaplan-Meier curve and compare AIC across plausible candidates.

## Model Specification

A parametric model relates the hazard for subject _i_ to covariates $x_i$:

\[
h_i(t) = h_0(t; \theta) \exp(\beta_1 x_{i1} + \beta_2 x_{i2} + \cdots + \beta_p x_{ip})
\]

- $h_0(t; \theta)$: baseline hazard defined by chosen distribution (e.g., Weibull)
- $\beta$: regression coefficients
- $\theta$: parameters of the distribution (e.g., shape, scale)

When the proportional hazards assumption holds, the parametric and Cox models yield similar hazard ratios.

## Example in R

```r
library(survival)
library(flexsurv)

# Weibull model
weibull_model <- flexsurvreg(Surv(time, status) ~ age + treatment,
                             data = clinical_data,
                             dist = "weibull")
summary(weibull_model)

# Exponential model
exp_model <- flexsurvreg(Surv(time, status) ~ treatment,
                         data = clinical_data,
                         dist = "exponential")

# Plot survival function
plot(weibull_model, type = "survival",
     main = "Weibull Survival Curve", xlab = "Time", ylab = "Survival Probability")
```

## Example in Python

```python
from lifelines import WeibullFitter, ExponentialFitter
import matplotlib.pyplot as plt

# Example data
durations = [5, 6, 6, 2, 4, 8, 10]
event_observed = [1, 0, 1, 1, 1, 0, 1]

# Weibull model
wf = WeibullFitter()
wf.fit(durations, event_observed, label="Weibull model")
wf.plot_survival_function()

# Exponential model
ef = ExponentialFitter()
ef.fit(durations, event_observed, label="Exponential model")
ef.plot_survival_function()

plt.title("Parametric Survival Models")
plt.xlabel("Time")
plt.ylabel("Survival probability")
plt.show()
```

## Model Evaluation and Diagnostics

After fitting a parametric model, always check:

**Goodness of fit:**
Compare models using AIC — lower values indicate better fit.

**Graphical assessment:**
Overlay predicted vs. empirical (KM) curves to verify shape consistency.

**Residual analysis:**
Inspect Cox–Snell residuals for randomness.

**Comparison with Cox model:**
If proportional hazards hold, both models should give similar results.

## When Parametric Models Beat Cox

Although Cox is often the default teaching model, parametric models can be better when:

- the scientific problem requires extrapolation beyond observed follow-up
- the sample is modest and a plausible shape assumption can stabilize estimation
- you need interpretable time-based summaries such as mean survival
- simulation, health economics, or reliability work requires a full distribution

## Advantages and Limitations

| Advantages | Limitations |
| ------------------------------------------------ | ------------------------------------------- |
| Smooth, continuous survival and hazard estimates | Requires correct distributional assumption |
| Enables extrapolation beyond observed follow-up | Mis-specified models produce biased results |
| Can estimate mean or median survival directly | Less flexible than non-parametric KM |
| Useful for simulation and economic modeling | May not fit complex hazard patterns |

## When to Use

Parametric survival models are most useful when:

- The **shape of the hazard** is known or can be reasonably assumed.
- You need to **predict beyond observed time** (e.g., long-term follow-up or cost-effectiveness models).
- The **proportional hazards assumption** may not hold, or time-varying hazard is expected.
- You require **closed-form estimates** of mean or restricted mean survival time (RMST).

Warning: A good-looking fitted curve on the observed window does not guarantee good extrapolation beyond that window. Long-horizon projections are only as credible as the distributional assumptions behind them.

## Key Takeaways

- Parametric models assume a specific **distribution of survival times**.
- The **Weibull** model is the most flexible and widely applied.
- **Model fit** must always be evaluated against non-parametric curves.
- These models complement, rather than replace, the **Cox proportional hazards** framework.

Parametric survival analysis offers interpretability and predictive power — especially valuable for extrapolation, simulation, and cost-effectiveness studies in biomedical research.

## Why Use Parametric Models at All?

They become especially attractive when:

- long-horizon extrapolation is required
- a plausible hazard shape is known
- simulation or economic evaluation needs a full distributional model

Tip: Cox is usually safer by default. Parametric models become stronger when their shape assumptions are actually informative.
