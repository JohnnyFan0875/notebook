# Two-Way ANOVA

**Two-way ANOVA** extends one-way ANOVA to **two categorical factors** and asks three questions at once:

1. Does factor A affect the outcome?
2. Does factor B affect the outcome?
3. Does the effect of A depend on the level of B?

Key point: The interaction term is the defining feature. Two-way ANOVA is valuable not just because it tests more than one factor, but because it can detect when one factor's effect changes across subgroups.

## When to Use

| Requirement | Example |
| ----------- | ------- |
| Numerical outcome | test score, reaction time, revenue |
| Two categorical factors | treatment and gender, diet and exercise |
| Independent observations | each row is one independent subject |
| Interest in subgroup behavior | treatment may work differently across categories |

## The Three Effects

| Effect | Question |
| ------ | -------- |
| **Main effect A** | Does factor A affect the outcome on average? |
| **Main effect B** | Does factor B affect the outcome on average? |
| **Interaction A × B** | Does the effect of A depend on B? |

## Why Interaction Comes First

If the interaction is significant, the main effects can become misleading because "the average effect" may hide opposite subgroup patterns.

Example:

- treatment helps men a lot
- treatment helps women very little

The average treatment effect might still look moderate, but the scientifically meaningful story is the difference in subgroup response.

Tip: In interpretation order, always read the interaction first, then the main effects only if the interaction is negligible or substantively unimportant.

## Model Formula

\[
Y = \mu + \alpha_i + \beta_j + (\alpha\beta)_{ij} + \varepsilon_{ijk}
\]

Where:

- \(\alpha_i\) = effect of factor A level \(i\)
- \(\beta_j\) = effect of factor B level \(j\)
- \((\alpha\beta)_{ij}\) = interaction between A and B

## Example with Simulated Data

```python
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

rng = np.random.default_rng(42)

rows = []
for treatment in ["Control", "Drug"]:
    for gender in ["Female", "Male"]:
        for _ in range(12):
            base = 70
            treat_eff = 4 if treatment == "Drug" else 0
            gender_eff = 2 if gender == "Male" else 0
            interaction = 5 if (treatment == "Drug" and gender == "Male") else 0
            score = base + treat_eff + gender_eff + interaction + rng.normal(0, 4)
            rows.append({"treatment": treatment, "gender": gender, "score": score})

df = pd.DataFrame(rows)

model = smf.ols("score ~ C(treatment) * C(gender)", data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)
```

## Reading the ANOVA Table

| Row | Meaning |
| --- | ------- |
| `C(treatment)` | main effect of treatment |
| `C(gender)` | main effect of gender |
| `C(treatment):C(gender)` | interaction |
| `Residual` | within-cell variation |

## Interpretation Order

| Situation | What to do |
| --------- | ---------- |
| Interaction significant | focus on simple effects or subgroup comparisons |
| Interaction not significant | interpret main effects more directly |
| Both main effects significant, interaction not | both factors shift the outcome independently |

Warning: A significant interaction means you should not summarize the story with only one overall treatment coefficient or one pooled group difference.

## Visualization: Interaction Plot

```python
import matplotlib.pyplot as plt

cell_means = df.groupby(["treatment", "gender"])["score"].mean().unstack()

cell_means.T.plot(marker="o", figsize=(6, 4))
plt.xlabel("Gender")
plt.ylabel("Mean score")
plt.title("Interaction Plot: Treatment × Gender")
plt.tight_layout()
plt.show()
```

How to read it:

| Pattern | Interpretation |
| ------- | -------------- |
| Roughly parallel lines | little or no interaction |
| Clearly non-parallel lines | interaction likely present |
| Crossing lines | strong interaction, main effects alone can mislead badly |

## Assumptions

| Assumption | Meaning | Check |
| ---------- | ------- | ----- |
| Independence | observations are unrelated | study design |
| Normality within cells | residuals in each factor combination are roughly normal | residual plots, Q-Q plot |
| Homogeneity of variance | cell variances are reasonably similar | Levene's test, residual plots |

Tip: The assumptions apply to the residual structure inside the design cells, not just to the pooled raw outcome.

## Effect Size

Two-way ANOVA is usually reported with **partial eta squared** for each effect.

\[
\eta_p^2 = \frac{SS_{effect}}{SS_{effect} + SS_{error}}
\]

```python
ss_error = anova_table.loc["Residual", "sum_sq"]

for effect in ["C(treatment)", "C(gender)", "C(treatment):C(gender)"]:
    ss_effect = anova_table.loc[effect, "sum_sq"]
    eta_p2 = ss_effect / (ss_effect + ss_error)
    print(f"{effect}: partial eta² = {eta_p2:.4f}")
```

## Follow-up After a Significant Interaction

If the interaction matters, follow-up questions often become:

- compare treatment within each gender
- compare gender within each treatment
- estimate cell means with confidence intervals

In practice, this often means:

1. plotting the interaction
2. running simple-effects tests
3. reporting subgroup mean differences with CIs

## Common Mistakes

| Mistake | Why it's a problem | Better approach |
| ------- | ------------------ | --------------- |
| Ignoring interaction | can hide the real pattern | inspect A × B first |
| Reporting only main effects | can be misleading under interaction | report simple effects |
| Treating factors as interchangeable with covariates | changes model meaning | use ANCOVA when one predictor is continuous |
| Using many subgroup t-tests without structure | inflates Type I error | keep ANOVA hierarchy and planned follow-up |

## Reporting Template

```text
A two-way ANOVA tested the effects of treatment and gender on score.
There was a significant treatment × gender interaction,
F(1, 44) = 6.82, p = .012, partial eta² = .134,
indicating that the treatment effect differed by gender.
Follow-up comparisons showed that the drug improved scores more strongly in men than in women.
```

## Key Takeaways

| Concept | Key point |
| ------- | --------- |
| **Two factors** | Two-way ANOVA studies two grouping variables at the same time |
| **Interaction is central** | It tells whether one factor changes the effect of the other |
| **Interpretation order** | Read interaction before main effects |
| **Partial eta²** | Useful effect size for each ANOVA component |
| **Plots matter** | Interaction plots often reveal the story faster than tables |
