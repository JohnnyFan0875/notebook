# Interpretation of Survival Analysis Results

Interpreting survival analysis results requires understanding both **statistical meaning** (e.g., hazard ratios, survival probabilities) and **clinical or biological context**.
This section summarizes how to interpret key outputs from Kaplan–Meier curves, Cox models, and related analyses — and how to communicate findings clearly.

Key point: Three levels of result interpretation: first descriptive (KM curve), then comparative (log-rank test), and finally modeling (Cox HR). The three levels complement each other and are indispensable. Statistical significance must be paired with clinical/biological plausibility to be meaningful.

## A Good Interpretation Sequence

Survival results are easiest to read when you move in the same order the analysis was built:

1. **describe the curve**: what does the time pattern look like?
2. **compare groups**: are the survival experiences meaningfully different?
3. **model covariates**: after adjustment, what factors shift the hazard?

This order matters because model-based summaries are safer when you already understand the raw survival pattern.

## Kaplan–Meier Survival Curves

### Interpretation

- The curve estimates the probability that a subject **survives longer than time $t$**.
  - Example: “At 12 months, the survival probability was 70%.”
- Steeper drops indicate higher event rates.
- Parallel or overlapping curves suggest similar outcomes between groups.

### Comparing Groups

- Visual comparison supported by **log-rank test**.
- p < 0.05 → significant difference in survival distributions.

## Median and Mean Survival

| Measure | Meaning | Comment |
| ---------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------- |
| **Median survival time** | Time when survival probability = 0.5 | Most reported; robust to censoring. |
| **Mean survival time** | Area under survival curve $E[T] = \int_0^\infty S(t)\,dt$ | Rarely estimable due to incomplete follow-up. |
| **Restricted Mean Survival Time (RMST)** | Average survival up to a fixed time $\tau$: $RMST(\tau) = \int_0^\tau S(t)\,dt$ | Useful for truncated or finite follow-up studies. |

Example:

“The median survival was 18 months for the treatment group and 12 months for the control group.”

## Hazard Ratios (Cox Model)

### Concept

The **hazard ratio (HR)** quantifies the relative risk of an event between two groups or per unit change in a covariate.

\[
HR = e^{\beta}
\]

| HR Value | Interpretation |
| -------- | -------------------------------- |
| HR = 1 | No difference in risk |
| HR > 1 | Higher hazard → shorter survival |
| HR < 1 | Lower hazard → longer survival |

Example statements:

- “Patients with mutation X had a **1.8-fold higher hazard of death** (HR = 1.8, 95% CI: 1.2–2.7, p = 0.004).”
- “Treatment A reduced the hazard of disease progression by 35% (HR = 0.65, 95% CI: 0.50–0.85).”

## Confidence Intervals and p-values

- **95% CI (Confidence Interval)**
  - If the CI **excludes 1.0** (for HRs), the effect is statistically significant.
  - Narrower CIs indicate greater precision.
- **p-value**
  - Tests whether the effect could be due to chance.
  - p < 0.05 is conventionally significant, but interpretation should consider effect size and CI width.

Always pair statistical significance with biological plausibility and effect magnitude.

## Absolute Difference vs Relative Difference

One of the most common interpretation mistakes is to report only the hazard ratio.

| Summary Type | Example question |
| ------------ | ---------------- |
| **Absolute** | How many more months of event-free time does one group have? |
| **Relative** | How much higher or lower is the instantaneous event rate? |

Tip: Median survival, fixed-time survival probability, and RMST help express absolute benefit. Hazard ratios express relative rate differences. Strong reporting usually includes both.

## Checking Assumptions

### For Cox Proportional Hazards Model:

- **Proportional hazards assumption**
  - Tested via **Schoenfeld residuals** or log-minus-log plots.
  - If violated, consider time-dependent covariates or stratified Cox models.
- **Linearity** of continuous covariates
  - Checked using **Martingale residuals** or splines.

Violating these assumptions can bias hazard ratio estimates.

## Clinical and Biological Relevance

Statistical significance does not guarantee **clinical importance**.

When interpreting results:

- Assess whether the observed survival difference translates into **meaningful patient benefit**.
- Consider **sample size** and **number at risk** at each time point.
- Evaluate **consistency** across subgroups and external cohorts.

Example:

“Although the hazard ratio was statistically significant, the absolute survival difference at 3 years was only 4%, which may have limited clinical impact.”

## Common Pitfalls

| Pitfall | Explanation |
| ---------------------------------- | ---------------------------------------------------------------------------------------- |
| **Overinterpreting censored data** | Censoring ≠ event-free survival; censored subjects may still experience the event later. |
| **Small numbers at risk** | Leads to unstable survival estimates in the tail of the curve. |
| **Ignoring assumption violations** | Produces misleading hazard ratios. |
| **Multiple testing** | Adjust p-values (e.g., FDR) in multi-gene or multi-variable analyses. |

## Example Summary Statement

- Kaplan–Meier analysis revealed that patients receiving Drug A had significantly longer survival than those receiving Drug B (median 24 vs. 15 months; log-rank p = 0.02).
- Cox proportional hazards modeling confirmed the result (HR = 0.60, 95% CI: 0.42–0.86), with no violation of the proportional hazards assumption (p = 0.72, Schoenfeld test).
- These findings indicate that Drug A confers a clinically meaningful survival advantage.

## A Reporting Template You Can Reuse

When writing up results, this structure is often clear and complete:

1. report the observed survival pattern or median survival
2. state the group comparison result with a log-rank p-value if relevant
3. report the Cox estimate as HR with 95% CI
4. mention whether major assumptions were checked
5. close with the practical or clinical meaning of the effect

## Key Takeaways

- Interpret survival results at **three levels**: descriptive (KM), comparative (log-rank), and model-based (Cox).
- Evaluate both **statistical** and **clinical** significance.
- Always check model assumptions before drawing conclusions.
- Summarize findings with clear, quantitative statements (HR, CI, p-value, and clinical context).

Effective interpretation bridges statistical rigor and biological insight — turning numbers into meaningful conclusions.

## Translate Back to Time Questions

Interpretation improves when you ask:

- what is the typical event-free time?
- how much longer does one group remain event-free by a relevant horizon?
- is the main story about timing, instantaneous risk, or cumulative probability?

Tip: Hazard ratios are rarely the whole story. Time-based summaries usually make the results more concrete.
