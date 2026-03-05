# 5. Cox Proportional Hazards Model

The **Cox proportional hazards model** is the workhorse of survival analysis. It extends the KM/log-rank framework by allowing **multiple covariates** to be incorporated simultaneously, while making minimal distributional assumptions.

> 📌 **為什麼 Cox 模型如此重要**：它是「半參數」模型——不需要假設基線風險的形式（非參數部分），但對共變數效應假設了乘法結構（參數部分）。這種彈性讓它成為生醫、社會科學、商業存活分析的預設模型。

---

## 5.1 The Model

The Cox model specifies how covariates multiplicatively scale the **baseline hazard** h₀(t):

$$h(t \mid \mathbf{x}) = h_0(t) \cdot \exp(\beta_1 x_1 + \beta_2 x_2 + \cdots + \beta_p x_p)$$

Where:
- $h_0(t)$ = baseline hazard function — the hazard when all covariates are zero (never estimated; left unspecified)
- $\exp(\beta_k)$ = **hazard ratio (HR)** for a one-unit increase in $x_k$, holding other covariates constant
- The model is **semi-parametric**: no assumption about the shape of $h_0(t)$, but linearity + log scale for covariates

**The proportional hazards assumption**: The ratio of hazards between any two subjects is **constant over time** — it doesn't depend on t.

$$\frac{h(t \mid \mathbf{x}_1)}{h(t \mid \mathbf{x}_2)} = \exp\left(\boldsymbol{\beta}^T (\mathbf{x}_1 - \mathbf{x}_2)\right) = \text{constant}$$

---

## 5.2 Interpreting the Hazard Ratio (HR)

The **hazard ratio** is the core output of a Cox model:

| HR Value   | Interpretation                                                         |
| ---------- | ---------------------------------------------------------------------- |
| HR = 1.0   | No association — covariate does not affect the hazard                  |
| HR = 2.0   | Twice the instantaneous risk of the event at any given time point      |
| HR = 0.5   | Half the instantaneous risk (protective factor)                        |
| HR = 1.5   | 50% higher risk compared to the reference                              |

> 💡 **HR is not a risk ratio or odds ratio** — it is a ratio of *instantaneous rates*, not cumulative probabilities. A HR of 2.0 does not mean you are twice as likely to experience the event overall; it means at any moment in time where you have survived, your risk rate is twice as high.  
> 風險比（HR）≠ 風險比例（risk ratio）。HR 是瞬時速率之比，不是累積概率之比。

---

## 5.3 Fitting the Cox Model in Python

### R Example

```r
library(survival)
library(survminer)

data(lung)
cox_model <- coxph(Surv(time, status) ~ age + sex + ph.ecog, data = lung)
summary(cox_model)
# coef        → log hazard ratio (β)
# exp(coef)   → hazard ratio (HR)
# p-value     → significance of each covariate
# Concordance → C-index (model discriminative ability)

# Check proportional hazards assumption
cox.zph(cox_model)

# Visualize adjusted survival curves
ggadjustedcurves(cox_model, data = lung, variable = "sex")

# Forest plot of hazard ratios
ggforest(cox_model, data = lung)
```

### Python Example

```python
from lifelines import CoxPHFitter
from lifelines.datasets import load_rossi
import pandas as pd

rossi = load_rossi()

# Select covariates and fit the Cox model
cph = CoxPHFitter()
cph.fit(
    rossi,
    duration_col='week',     # survival time column
    event_col='arrest',      # event indicator column (1=event, 0=censored)
    formula='fin + age + race + wexp + mar + paro + prio'
)

cph.print_summary(decimals=3)
```

**Output (abridged):**

```
<lifelines.CoxPHFitter: fitted with 432 total observations, 114 events>

         coef  exp(coef)  se(coef)  coef lower 95%  coef upper 95%  p
fin    -0.379      0.685     0.191          -0.753          -0.005  0.044 *
age    -0.057      0.944     0.022          -0.100          -0.014  0.009 **
race    0.314      1.369     0.308          -0.290           0.918  0.309
wexp   -0.150      0.861     0.212          -0.566           0.266  0.479
mar    -0.434      0.648     0.382          -1.182           0.315  0.257
paro   -0.085      0.918     0.196          -0.469           0.299  0.665
prio    0.091      1.095     0.029           0.035           0.147  0.002 **
```

### Reading the Output

```python
# Extract and display hazard ratios with confidence intervals
hr_table = cph.summary[['exp(coef)', 'exp(coef) lower 95%', 'exp(coef) upper 95%', 'p']].round(3)
hr_table.columns = ['HR', 'CI Lower', 'CI Upper', 'p-value']
print(hr_table)
```

**Interpretation of key results:**

| Covariate | HR    | Interpretation                                                  |
| --------- | ----- | --------------------------------------------------------------- |
| `fin` (financial aid) | 0.685 | Receiving aid is associated with 31.5% lower risk of rearrest  |
| `age`     | 0.944 | Each additional year of age is associated with 5.6% lower risk |
| `prio`    | 1.095 | Each additional prior conviction increases risk by 9.5%        |

---

## 5.4 Visualizing the Cox Model

### Forest Plot (Hazard Ratios)

```python
cph.plot(hazard_ratios=True)
plt.axvline(1.0, color='gray', linestyle='--', linewidth=1)
plt.title('Hazard Ratios with 95% CI — Cox Model')
plt.tight_layout()
plt.show()
```

### Predicted Survival Curves for Specific Profiles

```python
# Create two hypothetical subject profiles
profiles = pd.DataFrame({
    'fin':  [1, 0],     # with vs. without financial aid
    'age':  [25, 25],
    'race': [1, 1],
    'wexp': [0, 0],
    'mar':  [0, 0],
    'paro': [1, 1],
    'prio': [3, 3]
}, index=['Aid', 'No Aid'])

fig, ax = plt.subplots(figsize=(8, 5))
cph.predict_survival_function(profiles).plot(ax=ax)

ax.set_xlabel('Weeks')
ax.set_ylabel('S(t)')
ax.set_title('Predicted Survival: Aid vs. No Aid\n(age=25, prio=3, all else equal)')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## 5.5 Categorical and Continuous Covariates

### Categorical Variables

Use dummy coding (one-hot encoding) with a reference category. `lifelines` handles this automatically with the `formula` argument using Patsy syntax.

```python
# Explicitly setting reference category with Patsy
cph_cat = CoxPHFitter()
cph_cat.fit(
    rossi,
    duration_col='week',
    event_col='arrest',
    formula='fin + age + C(race, Treatment(reference=0)) + prio'
)
cph_cat.print_summary(decimals=3)
```

### Continuous Variables: Checking Linearity

The Cox model assumes a **log-linear** relationship between continuous covariates and the log-hazard. Use **martingale residuals** to check this.

```python
import matplotlib.pyplot as plt
import numpy as np

# Martingale residuals vs. continuous covariate
residuals = cph.compute_residuals(rossi, kind='martingale')

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

for ax, col in zip(axes, ['age', 'prio']):
    ax.scatter(rossi[col], residuals['martingale'], alpha=0.4, s=20)
    # Add lowess smoother
    from statsmodels.nonparametric.smoothers_lowess import lowess
    smoothed = lowess(residuals['martingale'], rossi[col], frac=0.4)
    ax.plot(smoothed[:, 0], smoothed[:, 1], color='red', linewidth=2)
    ax.axhline(0, color='gray', linestyle='--', linewidth=1)
    ax.set_xlabel(col)
    ax.set_ylabel('Martingale Residual')
    ax.set_title(f'Linearity Check: {col}')
    ax.grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

> 💡 If the LOWESS smoother is roughly flat around zero, the log-linear assumption holds. A curved smoother suggests the variable needs transformation (e.g., log, squared term) or spline modeling.

---

## 5.6 Time-Dependent Covariates

Standard Cox models assume covariates are fixed at baseline. When a covariate changes over time (e.g., a patient's lab values, employment status), it must be modeled as **time-dependent**.

```python
from lifelines.utils import to_long_format, add_covariate_to_timeline

# Time-dependent covariates require "long format" with (start, stop, event) per row
# Each subject may have multiple rows representing intervals of covariate values

# Example: measuring cholesterol at different time points
base = pd.DataFrame({
    'id':       [1, 2, 3],
    'start':    [0, 0, 0],
    'stop':     [10, 8, 15],
    'event':    [1, 0, 1],
    'age':      [50, 45, 60],
})

# In long format, start/stop defines each interval
cph_td = CoxPHFitter()
cph_td.fit(
    base,
    duration_col='stop',
    event_col='event',
    entry_col='start',    # left-truncation / start of risk interval
    formula='age'
)
```

> ⚠️ **Immortal time bias**: If a time-dependent covariate is coded incorrectly (e.g., a treatment received at week 10 is incorrectly attributed to the period before week 10), the model gives biased estimates. Always use (start, stop) intervals and ensure covariate values only apply to the correct time intervals.  
> 不死時間偏差（immortal time bias）是時間依賴共變數中最常見的錯誤之一，會使保護性因子看起來效果被高估。

---

## 5.7 Stratified Cox Model

When a covariate violates the proportional hazards assumption (Section 6), one solution is to **stratify** on it. This allows each stratum to have its own baseline hazard while sharing the same covariate coefficients.

```python
# Stratify on race (allows different baseline hazards by race)
cph_strat = CoxPHFitter()
cph_strat.fit(
    rossi,
    duration_col='week',
    event_col='arrest',
    formula='fin + age + wexp + mar + paro + prio',
    strata=['race']      # race gets its own baseline hazard
)

cph_strat.print_summary(decimals=3)
print(f"\nNote: 'race' is now a stratification variable — no HR is estimated for it.")
```

> 💡 Stratification removes the stratifying variable from the model as a covariate — you **cannot estimate its HR** anymore. Use stratification when you need to control for a covariate's confounding effect but don't need to estimate its association.  
> 分層後的變數不再有 HR 輸出。只有在不需要估計該變數效應、只需要控制其混淆的情況下才使用分層策略。

---

## 5.8 Model Extensions

Beyond the standard Cox model, several extensions handle more complex settings:

| Extension | Purpose |
|---|---|
| **Penalized Cox (LASSO / Ridge)** | Handle high-dimensional covariates (e.g., genomics); LASSO performs variable selection by shrinking coefficients to zero, Ridge shrinks without elimination |
| **Multistate Cox models** | Model transitions between multiple states (e.g., healthy → disease → death) |
| **Competing risks (Fine-Gray)** | Model cause-specific events when multiple event types are possible |
| **Frailty models** | Account for unobserved heterogeneity or clustered data (random effects for Cox) |

---

## 5.9 Key Takeaways

| Concept                      | Key Point                                                                     |
| ---------------------------- | ----------------------------------------------------------------------------- |
| **Semi-parametric**          | Baseline hazard is unspecified; only covariate effects are estimated          |
| **Hazard ratio (HR)**        | exp(β); HR > 1 increases risk, HR < 1 is protective                          |
| **HR is not a risk ratio**   | It is a ratio of instantaneous rates; interpretation requires care            |
| **Proportional hazards**     | The key assumption: HR is constant over time — must be checked (Section 6)   |
| **Martingale residuals**     | Diagnose non-linearity in continuous covariates                               |
| **Time-dependent covariates**| Use (start, stop) long format; beware immortal time bias                     |
| **Stratified Cox**           | Controls for PH violations without estimating the stratifying variable's HR   |

---

**← Previous:** [Log-Rank Test](./4-log-rank-test.md)  
**Next:** [Model Diagnostics & Violations →](./6-diagnostics.md)
