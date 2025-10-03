# Log-Rank Test

The **log-rank test** is a non-parametric statistical test used to compare the survival distributions of two or more groups.  
It is most commonly used alongside Kaplan–Meier survival curves to assess whether there is a statistically significant difference between groups.

---

## Concept

- Tests the **null hypothesis**: There is no difference in survival experience between groups.
- Compares the **observed** number of events in each group at each event time with the **expected** number under the null hypothesis.
- The test statistic follows a chi-square distribution.

---

## Test Statistic

At each event time \( t_j \):

- \( O\_{1j} \): Observed number of events in group 1.
- \( E\_{1j} \): Expected number of events in group 1 under the null hypothesis.
- \( V*{1j} \): Variance of \( O*{1j} \).

The log-rank test statistic is:

$$
\chi^2 = \frac{\left(\sum_j (O_{1j} - E_{1j})\right)^2}{\sum_j V_{1j}}
$$

- For two groups, this follows a chi-square distribution with 1 degree of freedom.
- For more than two groups, degrees of freedom = number of groups − 1.

---

## Example in R

```r
library(survival)

# Example dataset
fit <- survdiff(Surv(time, status) ~ group, data = clinical_data)
fit
```

### Output:

- A chi-square statistic and p-value.
- A significant p-value (e.g., p < 0.05) indicates a difference in survival distributions.

## Example in Python

```python
from lifelines.statistics import logrank_test
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt

# Example data
T1 = [5, 6, 6, 2, 4]   # durations for group 1
E1 = [1, 0, 1, 1, 1]   # event indicators (1=event, 0=censored)

T2 = [6, 3, 7, 10, 8]  # durations for group 2
E2 = [1, 1, 1, 0, 0]

results = logrank_test(T1, T2, event_observed_A=E1, event_observed_B=E2)
results.print_summary()
```

## Interpretation

- **p > 0.05**: No significant difference between survival curves.
- **p < 0.05**: Significant difference between survival distributions.
  - Example: “The log-rank test indicated a significant difference in survival between Drug A and Drug B groups (χ² = 6.5, p = 0.01).”

## Assumptions

1. Independent samples: Subjects in each group are independent.
2. Proportional hazards: The relative risk between groups is constant over time.
   - If this assumption is violated, results may be misleading.
3. Non-informative censoring: Censoring is independent of survival.

## Variants of Log-Rank Test

- Wilcoxon (Breslow) test: Gives more weight to early events.
- Tarone–Ware test: Intermediate weighting between log-rank and Wilcoxon.
- Useful when hazards are not proportional.

## When to Use

- Comparing overall survival (OS) or progression-free survival (PFS) between treatment groups.
- Preliminary analysis before fitting a Cox proportional hazards model.
- Multiple-group comparisons in clinical trials.
