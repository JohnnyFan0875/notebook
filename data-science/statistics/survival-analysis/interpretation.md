# Interpretation of Survival Analysis Results

Interpreting results from survival analysis requires understanding both the **statistical estimates** (survival probabilities, hazard ratios) and the **clinical or biological context**.  
This section provides guidance on how to interpret common outputs from Kaplan–Meier, Cox models, and related methods.

## 1. Survival Curves (Kaplan–Meier)

- **Y-axis**: Estimated survival probability $ \hat{S}(t) $.
- **X-axis**: Time from study entry or treatment initiation.
- **Steps downward**: Occur at each event time.
- **Tick marks**: Represent censored observations.

**Interpretation:**

- “At 12 months, the probability of survival is 70%.”
- Differences between groups can be compared visually and tested with the **log-rank test**.

## 2. Median and Mean Survival

- **Median survival time**: The time at which survival probability = 0.5 (50% of participants have experienced the event).
  - Example: “The median survival for treated patients was 18 months.”
- **Mean survival time**: The area under the survival curve.
  - Often replaced with **Restricted Mean Survival Time (RMST)** when follow-up is incomplete.

## 3. Hazard Ratios (Cox Model)

- **Hazard Ratio (HR)** quantifies the relative risk between groups or per unit change in covariate.

**Interpretation:**

- HR = 1 → No difference in hazard.
- HR > 1 → Higher hazard (shorter survival).
- HR < 1 → Lower hazard (longer survival).

**Example statements:**

- “Patients with mutation X had a 1.8-fold higher risk of death compared to wild-type (HR = 1.8, 95% CI: 1.2–2.7, p = 0.004).”
- “Treatment A reduced the hazard of disease progression by 35% (HR = 0.65, 95% CI: 0.50–0.85).”

## 4. Confidence Intervals and p-values

- **95% CI**: If it excludes 1.0 (for HR) or does not cross the reference value, the effect is statistically significant.
- **p-value**: Tests whether the observed effect is likely due to chance.
  - p < 0.05 is often considered significant, but interpretation should also consider effect size and CI.

## 5. Checking Assumptions

- Cox model assumes **proportional hazards**:
  - Verified with Schoenfeld residuals or log-minus-log plots.
  - If violated, consider time-dependent covariates or stratified models.
- Non-linear effects can be checked with Martingale residuals.

## 6. Clinical and Biological Relevance

- Statistical significance ≠ clinical importance.
- Always contextualize:
  - Does the survival difference translate to meaningful patient benefit?
  - Are sample sizes adequate?
  - Are results consistent across subgroups?

## 7. Common Pitfalls

- **Overinterpretation of censored data**: Censoring ≠ event-free survival.
- **Small numbers at risk** late in follow-up → wide confidence intervals.
- **Ignoring assumption violations** can bias results.
- **Multiple testing**: Adjust p-values or use false discovery rate in genomic studies.

## Example Interpretation in Practice

> Kaplan–Meier analysis showed that patients receiving Drug A had a significantly longer median survival (24 months) compared to those receiving Drug B (15 months, log-rank p = 0.02).  
> Cox proportional hazards modeling confirmed this association, with Drug A reducing the hazard of death by 40% (HR = 0.60, 95% CI: 0.42–0.86).  
> The proportional hazards assumption was satisfied (p = 0.72 from Schoenfeld test).  
> These findings suggest Drug A confers a clinically meaningful survival benefit.

## References

- Kleinbaum DG, Klein M. _Survival Analysis: A Self-Learning Text_. Springer, 2012.
- Therneau TM, Grambsch PM. _Modeling Survival Data: Extending the Cox Model_. Springer, 2000.
