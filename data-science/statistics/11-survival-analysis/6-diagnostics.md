# 6. Model Diagnostics & Violations

Fitting a Cox model is not the final step. Like any regression model, it rests on assumptions that must be **checked empirically**. The most critical assumption is proportional hazards — but linearity, influential observations, and overall fit also need attention.

> 📌 **診斷不是選項，是義務**：忽略假設檢查就發表 Cox 模型的結果，就像不看殘差圖就發表線性迴歸一樣。比例風險假設若被違反但沒被偵測到，所有的 HR 估計和 p 值都會失去意義。

---

## 6.1 The Proportional Hazards (PH) Assumption

The Cox model assumes that **the ratio of hazards between any two subjects is constant over time**:

$$\frac{h_i(t)}{h_j(t)} = \exp\left(\boldsymbol{\beta}^T (\mathbf{x}_i - \mathbf{x}_j)\right) = \text{constant (does not depend on } t\text{)}$$

**When the PH assumption is violated:**
- Estimated HRs are averages over time and may not represent any specific time period well
- Confidence intervals are too narrow → inflated Type I error
- Substantive conclusions can be completely wrong

---

## 6.2 Visual Check: Log-Log Plot

Plot $\log(-\log \hat{S}(t))$ vs. $\log(t)$ for each group. Under proportional hazards, the curves should be **parallel** (constant vertical distance = constant log hazard ratio).

$$\log(-\log S(t)) = \log H(t) = \log H_0(t) + \boldsymbol{\beta}^T \mathbf{x}$$

```python
from lifelines import KaplanMeierFitter
from lifelines.datasets import load_rossi
import matplotlib.pyplot as plt
import numpy as np

rossi = load_rossi()
T = rossi['week']
E = rossi['arrest']

fig, ax = plt.subplots(figsize=(8, 5))

for group, color, label in [(1, '#3B82F6', 'Received Aid'), (0, '#EF4444', 'No Aid')]:
    mask = rossi['fin'] == group
    kmf = KaplanMeierFitter()
    kmf.fit(T[mask], E[mask], label=label)

    # Extract survival estimates, avoiding S=0 or S=1 (log undefined)
    sf = kmf.survival_function_.copy()
    sf = sf[(sf.iloc[:, 0] > 0) & (sf.iloc[:, 0] < 1)]

    t_vals = sf.index
    s_vals = sf.iloc[:, 0].values
    ll = np.log(-np.log(s_vals))

    ax.plot(np.log(t_vals), ll, color=color, linewidth=2, label=label)

ax.set_xlabel('log(t)')
ax.set_ylabel('log(−log(S(t)))')
ax.set_title('Log-Log Plot — Checking Proportional Hazards\n(parallel lines → PH holds)')
ax.legend()
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

> 💡 **How to read the log-log plot**: Roughly parallel curves → PH assumption plausible. Curves that cross or diverge systematically → PH assumption violated for this covariate. The log-log plot is qualitative — pair it with the formal Schoenfeld test.

---

## 6.3 Formal Test: Schoenfeld Residuals

**Schoenfeld residuals** are computed for each covariate at each event time. If the PH assumption holds, these residuals should show **no time trend** — they should be randomly scattered around zero.

A formal test regresses Schoenfeld residuals on a function of time (usually ranked time). A significant slope indicates a time-varying coefficient → PH violated.

$$H_0: \beta_k(t) = \text{constant over time}$$

```python
from lifelines import CoxPHFitter
import matplotlib.pyplot as plt

cph = CoxPHFitter()
cph.fit(
    rossi,
    duration_col='week',
    event_col='arrest',
    formula='fin + age + race + wexp + mar + paro + prio'
)

# Check PH assumption — runs Schoenfeld residuals test
cph.check_assumptions(
    rossi,
    p_value_threshold=0.05,
    show_plots=True        # generates diagnostic plots automatically
)
```

**Output includes:**

```
Proportional hazard assumption tests
--------------------------------------
             test_statistic  p  -log2(p)
covariate
fin                   0.023  0.88        0.18
age                   1.245  0.26        1.93
race                  2.871  0.09        3.47
wexp                  0.013  0.91        0.13
mar                   0.004  0.95        0.07
paro                  0.115  0.73        0.45
prio                  3.012  0.08        3.62

All p-values above 0.05 → PH assumption not rejected for any covariate.
```

> 💡 The `check_assumptions()` method does the full diagnostic workflow: Schoenfeld test + residual plots in one call. Always run this after fitting a Cox model. 這個方法會一次完成 Schoenfeld 殘差圖和統計檢定，是 Cox 模型診斷的首選工具。

### Manual Schoenfeld Residuals Plot

```python
# Plot scaled Schoenfeld residuals for a specific covariate
residuals = cph.compute_residuals(rossi, kind='scaled_schoenfeld')

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

for ax, col in zip(axes, ['fin', 'prio']):
    ax.scatter(rossi.loc[rossi['arrest'] == 1, 'week'],
               residuals[col],
               alpha=0.5, s=25, color='#3B82F6')

    # LOWESS trend line
    from statsmodels.nonparametric.smoothers_lowess import lowess
    x_vals = rossi.loc[rossi['arrest'] == 1, 'week'].values
    smoothed = lowess(residuals[col].values, x_vals, frac=0.5)
    ax.plot(smoothed[:, 0], smoothed[:, 1], color='red', linewidth=2)
    ax.axhline(0, color='gray', linestyle='--')
    ax.set_xlabel('Time (weeks)')
    ax.set_ylabel(f'Scaled Schoenfeld Residual ({col})')
    ax.set_title(f'PH Diagnostic: {col}')
    ax.grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

> A flat red LOWESS line → no time trend → PH holds.  
> A sloped or curved LOWESS line → time-varying effect → PH violated.

---

## 6.4 What to Do When PH Is Violated

| Violation Type                        | Recommended Fix                                      |
| ------------------------------------- | ---------------------------------------------------- |
| One covariate violates PH             | Stratify on that covariate (Section 5.7)             |
| Several covariates violate PH         | Time × covariate interaction terms                   |
| PH violated throughout                | Accelerated Failure Time (AFT) model                 |
| Crossing hazards                      | RMST comparison instead of HR                        |
| Period-specific effects               | Piecewise exponential model                          |

### Option 1: Time-Varying Coefficients (Interaction with Time)

```python
# Add an interaction between a covariate and log(time)
# This allows the HR to change over time

from lifelines.utils import to_episodic_format
from lifelines import CoxTimeVaryingFitter

# Convert to long format for time-varying analysis
rossi_long = to_episodic_format(rossi, duration_col='week', event_col='arrest',
                                 id_col=rossi.index)

ctvf = CoxTimeVaryingFitter()
ctvf.fit(
    rossi_long,
    id_col='id',
    start_col='start',
    stop_col='stop',
    event_col='arrest',
    formula='fin + age + prio'
)
ctvf.print_summary(decimals=3)
```

### Option 2: Accelerated Failure Time (AFT) Model

AFT models are a parametric alternative to Cox that **do not assume proportional hazards**. Instead of modeling the hazard, they model the effect of covariates on the log of survival time directly:

$$\log T = \mu + \boldsymbol{\beta}^T \mathbf{x} + \sigma \varepsilon$$

```python
from lifelines import WeibullAFTFitter, LogNormalAFTFitter

# Fit Weibull AFT model
aft = WeibullAFTFitter()
aft.fit(rossi, duration_col='week', event_col='arrest',
        formula='fin + age + race + wexp + mar + paro + prio')

aft.print_summary(decimals=3)
```

**Interpreting AFT coefficients:**

| exp(β) in AFT | Interpretation                                        |
| -------------- | ----------------------------------------------------- |
| > 1.0          | Covariate **accelerates** survival time (event happens sooner) |
| < 1.0          | Covariate **decelerates** survival time (event happens later)  |
| = 1.0          | No effect on timing                                   |

> 💡 In AFT models, exp(β) is called the **acceleration factor** or **time ratio** — the ratio of the expected survival time between groups. This is often more interpretable than a hazard ratio in non-medical contexts.  
> AFT 模型的係數解釋為「存活時間的倍數」，在工程可靠度、商業存活等場景往往比 HR 更直覺。

---

## 6.5 Influential Observations: dfbeta Residuals

**dfbeta residuals** measure how much each observation influences the estimated coefficient. Large absolute values indicate influential observations.

```python
# Compute dfbeta residuals
dfbeta = cph.compute_residuals(rossi, kind='delta_beta')

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

for ax, col in zip(axes, ['fin', 'prio']):
    ax.stem(dfbeta.index, dfbeta[col], markerfmt='o',
            linefmt='gray', basefmt='k-')
    # Highlight influential observations (|dfbeta| > threshold)
    threshold = 2 * dfbeta[col].std()
    ax.axhline(threshold, color='red', linestyle='--', linewidth=1)
    ax.axhline(-threshold, color='red', linestyle='--', linewidth=1)
    ax.set_xlabel('Subject Index')
    ax.set_ylabel(f'dfbeta ({col})')
    ax.set_title(f'Influential Observations: {col}\n(red = ±2 SD threshold)')
    ax.grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

---

## 6.6 Model Fit: Concordance Index (C-index)

The **C-index** (concordance index) measures the Cox model's **discriminative ability** — how well it ranks subjects by their risk. It is the survival analogue of the AUC for binary outcomes.

$$C = P(\hat{h}(t \mid x_i) > \hat{h}(t \mid x_j) \mid T_i < T_j)$$

| C-index   | Interpretation                          |
| --------- | --------------------------------------- |
| 0.50      | No discrimination (random guessing)     |
| 0.60–0.70 | Modest discrimination                   |
| 0.70–0.80 | Good discrimination                     |
| > 0.80    | Excellent discrimination                |

```python
from lifelines.utils import concordance_index

ci = concordance_index(
    rossi['week'],
    -cph.predict_partial_hazard(rossi),   # negate: higher risk → lower time
    rossi['arrest']
)
print(f"C-index: {ci:.4f}")
print(f"Interpretation: {'Good' if ci > 0.7 else 'Modest'} discrimination")

# lifelines also reports this automatically in the model summary
print(f"\nC-index from model summary: {cph.concordance_index_:.4f}")
```

---

## 6.7 Calibration and Validation

Model validation ensures that predictions generalize beyond the training dataset.

| Type | Description | Method |
|---|---|---|
| **Internal validation** | Tests reproducibility using bootstrap or cross-validation | `bootcov()` in R, resampling in Python |
| **External validation** | Apply model to an independent cohort | Check C-index, calibration, and AUC on new data |
| **Calibration plots** | Compare predicted vs. observed survival; ideally close to the 45° line | `rms::calibrate()` in R; `scikit-survival` in Python |

> ⚠️ A high C-index does not guarantee calibration. A model can rank subjects correctly but still systematically over- or under-estimate absolute survival probabilities. Always check both discrimination (C-index) and calibration.  
> 高 C-index 不代表模型校準良好。辨別力（discrimination）和校準（calibration）是兩個獨立的面向，都需要檢查。

### Cook's Distance and Overall Influence

For a broader measure of each observation's overall influence on the model fit (beyond per-coefficient dfbeta):

```python
# Deviance residuals identify poorly fitted subjects
deviance_resid = cph.compute_residuals(rossi, kind='deviance')

import matplotlib.pyplot as plt
plt.figure(figsize=(8, 4))
plt.scatter(range(len(deviance_resid)), deviance_resid['deviance'],
            alpha=0.5, s=20, color='#3B82F6')
plt.axhline(2, color='red', linestyle='--', linewidth=1, label='±2 threshold')
plt.axhline(-2, color='red', linestyle='--', linewidth=1)
plt.xlabel('Subject Index')
plt.ylabel('Deviance Residual')
plt.title('Deviance Residuals — Identifying Outliers')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()
# |deviance| > 2 suggests an outlier or poorly fitted observation
```

> 💡 In R, `residuals(cox_model, type = "dfbeta")` gives per-coefficient influence, while `residuals(cox_model, type = "deviance")` and Cook's distance give overall influence measures.

---

## 6.8 Complete Diagnostic Workflow

```python
# Complete post-fitting diagnostic checklist

cph = CoxPHFitter()
cph.fit(rossi, duration_col='week', event_col='arrest',
        formula='fin + age + race + wexp + mar + paro + prio')

print("=" * 60)
print("STEP 1: Model Summary")
print("=" * 60)
cph.print_summary(decimals=3)

print("\n" + "=" * 60)
print("STEP 2: Proportional Hazards Test")
print("=" * 60)
cph.check_assumptions(rossi, p_value_threshold=0.05, show_plots=False)

print("\n" + "=" * 60)
print("STEP 3: Discrimination (C-index)")
print("=" * 60)
print(f"C-index: {cph.concordance_index_:.4f}")

print("\n" + "=" * 60)
print("STEP 4: Linearity (Martingale Residuals)")
print("=" * 60)
print("→ Plot martingale residuals vs. continuous covariates")
print("  (see Section 5.5 for code)")
```

---

## 6.9 Key Takeaways

| Concept                        | Key Point                                                                     |
| ------------------------------ | ----------------------------------------------------------------------------- |
| **PH assumption**              | The most critical assumption in Cox models — must always be checked           |
| **Log-log plot**               | Visual check: parallel curves → PH holds                                      |
| **Schoenfeld residuals**       | Formal test: significant time trend → PH violated                             |
| **Stratified Cox**             | Fixes PH violation for one variable by allowing separate baseline hazards     |
| **AFT models**                 | Parametric alternative when PH is violated throughout; time ratio interpretation |
| **C-index**                    | Model discrimination: 0.5 = random, >0.7 = good predictive ability           |
| **dfbeta residuals**           | Detect influential observations that may be driving your results              |

---
