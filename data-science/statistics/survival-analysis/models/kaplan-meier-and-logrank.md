# Kaplan–Meier Estimator and Log-Rank Test

The **Kaplan–Meier (KM)** estimator and **log-rank test** are foundational tools in survival analysis.  
They provide non-parametric methods to **estimate survival probability** over time and **compare survival distributions** between groups — without assuming any specific underlying distribution.

## 1. Kaplan–Meier Estimator

### Concept

The **Kaplan–Meier estimator** calculates the probability of surviving beyond each observed event time.  
It updates survival probabilities stepwise as events occur.

- **Non-parametric** statistic
- Handles **censored data** (when the exact time of event is unknown, e.g., patient lost to follow-up).
- Produces a **step function** survival curve.
- Allows comparison of survival probabilities between groups.

Mathematically, the estimated survival function at time \( t \) is:

$$
\hat{S}(t) = \prod_{t_i \leq t} \left(1 - \frac{d_i}{n_i}\right)
$$

where:

- \(t_i\): the \(i^{th}\) event time
- \(d_i\): number of events at \(t_i\)
- \(n_i\): number of individuals at risk just before \(t_i\)

### Conditional Survival

- The probability of surviving a particular interval, **given that the subject has survived up to the start of that interval**.
- Formula at time \(t_i\):
  $$
  p_i = 1 - \frac{d_i}{n_i}
  $$
- Example interpretation: “If a patient has survived until 3 months, what is the chance they survive past 3 months?”

### Cumulative Survival

- The overall probability of surviving **from time 0 up to a certain time**.
- Computed by multiplying all conditional survival probabilities up to that point:
  $$
  \hat{S}(t) = p_1 \times p_2 \times \cdots \times p_i
  $$
- Example interpretation: “What is the probability a patient survives from the beginning of the study up to 3 months?”

### Stepwise Estimation Example

| Patient | Survival (months) | Event (1=death, 0=censored) |
| :------ | :---------------- | :-------------------------- |
| A       | 2                 | 1                           |
| B       | 3                 | 1                           |
| C       | 6                 | 0                           |
| D       | 7                 | 1                           |
| E       | 10                | 0                           |

At each event time:

| Time | \(n_i\) | \(d_i\) | Conditional Survival | Cumulative Survival |
| ---- | ------- | ------- | -------------------- | ------------------- |
| 2    | 5       | 1       | \(1 - 1/5 = 0.8\)    | 0.8                 |
| 3    | 4       | 1       | \(1 - 1/4 = 0.75\)   | 0.8 × 0.75 = 0.60   |
| 7    | 2       | 1       | \(1 - 1/2 = 0.5\)    | 0.6 × 0.5 = 0.30    |

Thus, by 7 months, the estimated survival probability is **30%**.

- at Time 2
  - 在 2 個月前還活著的病人，有 80% 能活過 2 個月 (此時 individuals at risk 為 5 人，其中 1 個死亡)
  - Cumulative Survival: 從研究一開始到 2 個月，總體的存活機率是 80% (此時 individuals at risk 為 5 人，其中 1 個死亡)
- at Time 3
  - 條件生存率: 在已經存活超過 2 個月的病人當中，仍有 75% 能活過 3 個月（此時 individuals at risk 為 4 人，其中 1 人死亡）。
  - Cumulative Survival: 從研究一開始到 3 個月為止，整體存活機率為 60%（因為 5 個人中有 2 人死亡）。這個結果也可以由前兩段條件生存率相乘得到: 80% (4/5) × 75% (3/4) = 60% (3/5)。
- at Time 6
  - 條件生存率: 在已經存活超過 3 個月的病人當中，有 100% 能活過 6 個月（此時 individuals at risk 為 3 人，其中 0 人死亡，其中 1 人 censored）。
  - Cumulative Survival: 從研究一開始到 6 個月為止，整體存活機率為 60%（因為 5 個人中有 2 人死亡）。這個結果也可以由前兩段條件生存率相乘得到: 80% (4/5) × 75% (3/4) x 100% (3/3) = 60% (3/5)。
  - 超過這個時間點，C 不再列為 risk candidate。

### Interpreting the KM Curve

- **X-axis:** Time (months, days, years)
- **Y-axis:** Estimated survival probability \( \hat{S}(t) \)
- **Steps downward:** Events (e.g., deaths)
- **Tick marks:** Censored cases
- **Flat segments:** Periods with no observed events

The Kaplan–Meier curve does not assume any distribution — it’s purely empirical.

### R Example

```r
library(survival)
library(survminer)

data(lung)
fit <- survfit(Surv(time, status) ~ sex, data = lung)

ggsurvplot(fit,
           data = lung,
           pval = TRUE,
           conf.int = TRUE,
           risk.table = TRUE,
           surv.median.line = "hv",
           xlab = "Time (days)",
           ylab = "Survival probability")
```

### Python Example

```python
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt

durations = [5,6,6,2,4,4,3,2,1,3]
event_observed = [1,0,1,1,1,0,1,0,1,1]

kmf = KaplanMeierFitter()
kmf.fit(durations, event_observed, label="All subjects")

kmf.plot_survival_function()
plt.title("Kaplan–Meier Survival Curve")
plt.xlabel("Time")
plt.ylabel("Survival probability")
plt.show()

# Calculate median survival time
median_survival = kmf.median_survival_time_

# Restricted Mean Survival Time, RMST
tau = max(durations) # Specify an upper limit tau
mean_survival = kmf.mean_survival_time_
```

## 2. Log-Rank Test

### Purpose

The **log-rank test** assesses whether **two or more groups** have statistically different survival experiences.
It compares the _observed_ and _expected_ numbers of events at each time point across groups.
A type of **non-parametric** statistical test

### Hypotheses

- **Null hypothesis (H₀):** All groups have identical survival functions.
- **Alternative (H₁):** At least one group differs.

### Test Statistic

At each event time ( t_j ):

- ( O\_{1j} ): observed events in group 1
- ( E\_{1j} ): expected events in group 1 under ( H_0 )
- ( V*{1j} ): variance of ( O*{1j} )

The log-rank statistic is:

$$
\chi^2 = \frac{\left[ \sum_j (O_{1j} - E_{1j}) \right]^2}{\sum_j V_{1j}}
$$

- Follows a **chi-square distribution** with 1 degree of freedom for two groups.
- For ( k ) groups, degrees of freedom = ( k - 1 ).

### Example in R

```r
fit <- survdiff(Surv(time, status) ~ sex, data = lung)
fit
```

**Output:**
A chi-square statistic and p-value.

- **p < 0.05** → significant difference in survival distributions.

### Example in Python

```python
from lifelines.statistics import logrank_test

T1 = [5,6,6,2,4]
E1 = [1,0,1,1,1]
T2 = [6,3,7,10,8]
E2 = [1,1,1,0,0]

results = logrank_test(T1, T2, event_observed_A=E1, event_observed_B=E2)
results.print_summary()
```

## 3. Assumptions and Variants

| **Condition**                 | **Meaning**                                                            |
| ----------------------------- | ---------------------------------------------------------------------- |
| **Independent samples**       | Subjects between groups are independent.                               |
| **Proportional hazards**      | The relative risk (hazard ratio) between groups is constant over time. |
| **Non-informative censoring** | Censoring is unrelated to true survival probability.                   |

### Variants

- **Wilcoxon (Breslow):** emphasizes early events.
- **Tarone–Ware:** intermediate weighting between log-rank and Wilcoxon.
  Useful when hazard rates cross over time.

## 4. Practical Interpretation

| **Output**                  | **Interpretation**                                      |
| --------------------------- | ------------------------------------------------------- |
| **KM Curve**                | Shows estimated survival probability over time.         |
| **Log-rank p-value < 0.05** | Suggests survival differs significantly between groups. |
| **Median survival time**    | Time when 50% of subjects have experienced the event.   |

**Example statement:**

- Kaplan–Meier analysis showed that patients receiving Drug A had longer median survival (24 vs. 15 months; log-rank p = 0.02).

## 5. Key Takeaways

- **Kaplan–Meier:** estimates survival function non-parametrically.
- **Log-rank test:** statistically compares two or more KM curves.
- Both handle **right-censored** data naturally.
- Together, they form the **first step** in almost every survival analysis workflow before fitting a Cox model.
