# Parametric Survival Models

While the Cox proportional hazards model is the most commonly used method in survival analysis, it relies on the **proportional hazards assumption** and leaves the baseline hazard function unspecified.  
In contrast, **parametric survival models** assume that survival times follow a specific probability distribution.

---

## 1. Common Distributions

- **Exponential model**

  - Assumes a constant hazard over time.
  - Simplest parametric model, rarely realistic in clinical data.

- **Weibull model**

  - Allows hazard to increase or decrease over time.
  - Flexible and widely applied in reliability engineering and medicine.

- **Log-normal model**

  - Assumes log-transformed survival times follow a normal distribution.
  - Useful when hazards first increase, then decrease.

- **Log-logistic model**
  - Similar to log-normal but with heavier tails.

---

## 2. Model Formulation

A parametric survival model specifies the **survival function** \( S(t) \) and **hazard function** \( h(t) \) according to the chosen distribution.

Example: Weibull distribution

- Survival function:
  $$
  S(t) = \exp\left[-\left(\frac{t}{\lambda}\right)^k\right]
  $$
- Hazard function:
  $$
  h(t) = \frac{k}{\lambda} \left(\frac{t}{\lambda}\right)^{k-1}
  $$

Where:

- \( \lambda \) = scale parameter
- \( k \) = shape parameter

---

## 3. Advantages

- Provides **smooth estimates** of survival and hazard functions.
- Allows **extrapolation beyond observed follow-up**, which is not possible with non-parametric methods.
- Can estimate **mean survival time** directly, even when not all events are observed.

---

## 4. Limitations

- Requires correct specification of the distribution.
- Model fit should always be checked (goodness-of-fit tests, graphical checks).
- If the assumed distribution is wrong, results can be biased.

---

## 5. Example in R

```r
library(survival)
library(flexsurv)

# Weibull model
weibull_model <- flexsurvreg(Surv(time, status) ~ age + treatment,
                             data = clinical_data, dist = "weibull")
summary(weibull_model)

# Exponential model
exp_model <- flexsurvreg(Surv(time, status) ~ treatment,
                         data = clinical_data, dist = "exponential")
```

## 6. Example in Python

```python
from lifelines import WeibullFitter, ExponentialFitter
import matplotlib.pyplot as plt

# Example data
durations = [5, 6, 6, 2, 4, 8, 10]
event_observed = [1, 0, 1, 1, 1, 0, 1]

# Weibull
wf = WeibullFitter()
wf.fit(durations, event_observed, label="Weibull model")
wf.plot_survival_function()

# Exponential
ef = ExponentialFitter()
ef.fit(durations, event_observed, label="Exponential model")
ef.plot_survival_function()

plt.title("Parametric Survival Models")
plt.xlabel("Time")
plt.ylabel("Survival probability")
plt.show()
```

## 7. When to Use

- When proportional hazards assumption is violated.
- When long-term extrapolation is needed (e.g., health economics, cost-effectiveness studies).
- When a biologically plausible distribution of survival times can be assumed.
