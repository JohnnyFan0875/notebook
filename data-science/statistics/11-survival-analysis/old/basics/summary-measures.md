# Summary Measures in Survival Analysis

**Summary measures** provide concise numerical descriptions of time-to-event data.  
They help quantify overall survival experience, compare treatment groups, and communicate results effectively in biomedical and epidemiological studies.

## 1. Median Survival Time

- **Definition**: The time at which the estimated survival probability drops to 0.5.  
  It represents the point where half of the subjects have experienced the event.

- **Advantages**:
  - Simple and robust even with censored data.
  - Does not assume any distribution for survival times.

**Example interpretation:**

- “The median overall survival was 18 months in the treatment group and 12 months in the control group.”

![Image](http://www.finprog.org/images/text/statis12.gif)

## 2. Mean and Restricted Mean Survival Time (RMST)

- **Mean survival time** is the expected value of survival time:

  $$
  E[T] = \int_0^{\infty} S(t) \, dt
  $$

  However, it requires observing the entire survival curve until all subjects experience the event — rarely achievable in censored data.

- **Restricted Mean Survival Time (RMST)** provides a practical alternative:

  $$
  RMST(\tau) = \int_0^{\tau} S(t) \, dt
  $$

  where \( \tau \) is a fixed follow-up horizon (e.g., 3 years or 5 years).

  ![Image](../../../reference/RMST-figure.png)

- **Interpretation**:  
  The average survival time **up to** time \( \tau \).  
  Differences in RMST between groups represent **average survival gain or loss** within that time frame.

**Example:**

> “The 5-year RMST was 48.2 months in the treatment group vs. 44.5 months in the control group (Δ = 3.7 months).”

## 3. Survival Probabilities at Fixed Time Points

- Estimate the probability of surviving beyond a specified time (e.g., 1-year, 3-year, or 5-year survival rate).
- Obtained directly from Kaplan–Meier or parametric models.

**Example:**

> “The 3-year survival rate was 72% for patients with Stage II disease.”

## 4. Hazard Ratio (HR)

- Obtained from **Cox** or **parametric** survival models.
- Represents the **relative risk** of experiencing the event between two groups or per unit increase in a covariate.

$$
HR = e^{\beta}
$$

**Interpretation:**

- HR = 1 → no difference between groups
- HR > 1 → higher hazard (worse survival)
- HR < 1 → lower hazard (better survival)

**Example:**

> “Treatment A reduced the risk of death by 40% (HR = 0.60, 95% CI 0.45–0.80, p = 0.002).”

## 5. Cumulative Hazard

- Measures the **total risk accumulated** up to a specific time:
  $$
  H(t) = -\ln S(t)
  $$
- Provides a monotonic measure of risk over time.
- Often visualized using the **Nelson–Aalen estimator** or in **log-minus-log plots** to assess proportional hazards.

## 6. Life Expectancy and Derived Measures

- Estimated from extrapolated survival curves.
- Useful for expressing expected remaining lifetime or survival gain under treatment.

## Key Takeaways

| Measure                 | Interpretation                                  | Typical Use                                               |
| ----------------------- | ----------------------------------------------- | --------------------------------------------------------- |
| **Median survival**     | Time when 50% of subjects have had the event    | Simple, robust summary                                    |
| **RMST**                | Average survival up to a fixed time horizon     | Alternative to median; interpretable in limited follow-up |
| **Fixed-time survival** | Probability of surviving beyond a specific time | Clinical comparison                                       |
| **Hazard ratio**        | Relative risk between groups                    | Regression-based inference                                |
| **Cumulative hazard**   | Accumulated risk over time                      | Diagnostic or visualization metric                        |

> **In summary:**
>
> - Median survival and RMST summarize the _absolute_ survival experience, while hazard ratios describe _relative_ risk.
> - Together, they provide a complete quantitative summary of survival outcomes.
