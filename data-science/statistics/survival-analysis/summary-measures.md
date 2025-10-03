# Summary Measures in Survival Analysis

Summary measures provide concise numerical descriptions of survival data.  
They are useful for comparing groups, communicating results, and supporting clinical or epidemiological decision-making.

## 1. Median Survival Time

- The time at which the survival probability drops to **50%**.
- Interpreted as the point where half of the study population has experienced the event.
- More robust than the mean in the presence of censoring.

**Example statement:**

> “The median overall survival for patients treated with Drug A was 18 months, compared to 12 months for Drug B.”

## 2. Mean Survival Time

- The **expected average survival time**, defined as the area under the survival curve:

$$
E[T] = \int_0^\infty S(t) \, dt
$$

- Requires observing survival until the curve reaches zero (all subjects have experienced the event).
- Rarely estimable in practice due to censoring.

## 3. Restricted Mean Survival Time (RMST)

- A practical alternative to mean survival time when follow-up is finite.
- Defined as:

$$
RMST(\tau) = \int_0^\tau S(t) \, dt
$$

- Represents the **average survival time up to a specified time horizon** \( \tau \) (e.g., 3-year or 5-year survival).
- Useful for clinical interpretation and treatment comparison.

**Example statement:**

> “The 5-year RMST was 48.2 months in the treatment group and 44.5 months in the control group, a difference of 3.7 months.”

## 4. Survival Rates at Fixed Time Points

- The estimated probability of surviving beyond a specified time point (e.g., 1-year, 3-year, 5-year survival).
- Commonly reported in clinical studies and registries.

**Example statement:**

> “The 5-year survival rate was 65% for patients with Stage II disease.”

## 5. Hazard Ratios (HR)

- Obtained from Cox models or parametric models.
- Quantify the **relative risk** of event occurrence between groups.

**Interpretation:**

- HR = 1 → no difference.
- HR > 1 → higher risk in the exposed group.
- HR < 1 → lower risk in the exposed group.

## 6. Cumulative Hazard

- Measures accumulated risk of experiencing the event up to time \(t\).
- Related to the survival function:

$$
S(t) = e^{-H(t)}
$$

- Often visualized with **Nelson–Aalen estimator**.

## 7. Life Expectancy Estimates

- Derived from survival curves by extrapolation.
- Provides an estimate of the expected remaining lifetime for a patient cohort.

## 8. Summary in Practice

- **Median survival**: Simple, robust, widely used.
- **RMST**: Preferred when follow-up is limited.
- **Hazard ratios**: Useful for relative comparisons.
- **Fixed-time survival rates**: Clinically interpretable.
- **Cumulative hazard**: Insight into risk accumulation.

### 1. Median Survival Time

- The time point when the survival probability drops to 50%.
- Provides a simple summary of central tendency in survival distribution.

![Image](http://www.finprog.org/images/text/statis12.gif)

### 2. Mean Survival Time

- The **average expected survival time** for individuals in the study population.
- Defined mathematically as the **area under the survival curve**:
  $$
  E[T] = \int_0^\infty S(t) \, dt
  $$
- Provides an overall summary of survival experience across the entire follow-up period.
- Unlike the median survival time (which focuses on the 50% point), the mean incorporates **all observed survival times** and is more sensitive to long-term follow-up and censoring.

#### Mean Survival vs. Restricted Mean Survival Time (RMST)

- In theory, the mean survival time requires the curve to be observed **until it reaches 0** (all individuals have had the event).
- In practice, survival data are censored, and follow-up is finite → the full mean survival time is usually **not estimable**.
- **Restricted Mean Survival Time (RMST)** is therefore used:
  $$
  RMST(\tau) = \int_0^\tau S(t) \, dt
  $$
  where \(\tau\) is a chosen time horizon (e.g., the maximum follow-up or a clinically meaningful cutoff such as 5 years).
- RMST is always well-defined and interpretable as the **average survival up to time \(\tau\)**.
- If follow-up were infinitely long and censoring absent, RMST would converge to the true mean survival time.

![Image](../../../reference/RMST-figure.png)
