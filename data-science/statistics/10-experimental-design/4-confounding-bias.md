# 4. Confounding, Bias & Validity

Even well-intentioned experiments can produce misleading results. Understanding the threats to validity is essential for designing studies that produce credible, generalizable conclusions.

> 📌 **核心問題**：這個實驗測量到的，真的是我想測量的嗎？結論能否推廣到其他情境？這兩個問題分別對應「內部效度」和「外部效度」。

---

## 4.1 Confounding

A **confounding variable** is one that is associated with both the independent variable (treatment) and the dependent variable (outcome), creating a spurious apparent relationship.

### The Confounding Structure

```
   Confounder
      ↙    ↘
Treatment → Outcome
```

If you don't account for the confounder, the treatment-outcome relationship you observe is **distorted** — the effect you estimate is not the true causal effect.

### Classic Example: Shoe Size and Reading Ability

Children with larger shoe sizes tend to read better. Is shoe size a cause of reading ability?

- **Confound**: Age. Older children have both larger feet and better reading skills.
- Without controlling for age, shoe size and reading appear correlated.
- Once you control for age, the association disappears.

```python
import numpy as np
import pandas as pd
from scipy import stats

np.random.seed(42)
n = 200

# Simulate: Age drives both shoe size and reading ability
age = np.random.normal(10, 2, n)                       # ages 6–14
shoe_size = age * 0.8 + np.random.normal(0, 0.5, n)   # age → shoe size
reading = age * 3 + np.random.normal(0, 2, n)          # age → reading

df = pd.DataFrame({'age': age, 'shoe_size': shoe_size, 'reading': reading})

# Naive correlation: ignores confound
r_naive, p_naive = stats.pearsonr(shoe_size, reading)
print(f"Naive r(shoe, reading)   = {r_naive:.3f}  (p = {p_naive:.4f})")

# Partial correlation: controlling for age (residualize both variables)
res_shoe = np.polyfit(age, shoe_size, 1)
shoe_resid = shoe_size - np.polyval(res_shoe, age)

res_read = np.polyfit(age, reading, 1)
reading_resid = reading - np.polyval(res_read, age)

r_partial, p_partial = stats.pearsonr(shoe_resid, reading_resid)
print(f"Partial r(shoe, reading) = {r_partial:.3f}  (p = {p_partial:.4f})")
print("(True causal effect of shoe size on reading is 0)")
```

**Output:**

```
Naive r(shoe, reading)   = 0.963  (p = 0.0000)
Partial r(shoe, reading) = 0.019  (p = 0.7862)
```

> The naive correlation is 0.96 — extremely strong. The partial correlation controlling for age is essentially zero. This is confounding in action.

### How to Handle Confounding

| Strategy            | When Available       | How It Works                                           |
| ------------------- | -------------------- | ------------------------------------------------------ |
| **Randomization**   | Experimental studies | Distributes all confounders (known + unknown) randomly |
| **Restriction**     | Either               | Limit sample to one level of the confounder             |
| **Matching**        | Observational        | Match cases and controls on confounder values           |
| **Statistical control** | Either           | Include confounder as covariate in the model            |
| **Stratification**  | Either               | Analyze separately within each level of confounder      |

> ⚠️ Statistical control only adjusts for **measured** confounders. Randomization is the only method that handles unmeasured confounders. This is the core argument for why experiments > observational studies for causal claims.

---

## 4.2 Types of Bias

Bias is any systematic (non-random) error that causes the estimated effect to consistently differ from the true effect. Unlike random error, **more data does not fix bias**.

| Type                     | 中文       | Description                                                             | Prevention                          |
| ------------------------ | ---------- | ----------------------------------------------------------------------- | ----------------------------------- |
| **Selection bias**       | 選擇偏差   | Treatment and control groups differ at baseline due to non-random assignment | Randomization                  |
| **Attrition bias**       | 流失偏差   | Participants drop out non-randomly (dropouts differ from completers)    | Intention-to-treat analysis         |
| **Observer bias**        | 觀察者偏差 | Researchers assess outcomes differently based on knowing treatment      | Blinding                            |
| **Response bias**        | 反應偏差   | Participants answer differently due to social desirability or demand    | Anonymous surveys, neutral wording  |
| **Recall bias**          | 回憶偏差   | Past events recalled differently by cases vs. controls                  | Objective records, prospective data |
| **Ascertainment bias**   | 確認偏差   | Cases are detected more thoroughly in one group than another            | Standardized diagnosis criteria     |
| **Hawthorne effect**     | 霍桑效應   | Participants change behavior because they know they are being observed  | Blind subjects, naturalistic setting|
| **Regression to the mean** | 均值回歸  | Extreme measurements naturally tend toward the mean on re-testing       | Control group, pre-post design with control |

---

## 4.3 Blinding

**Blinding** prevents knowledge of treatment assignment from influencing the outcome assessment or participant behavior.

| Type                  | Who Is Blinded                              | When Necessary                                    |
| --------------------- | ------------------------------------------- | ------------------------------------------------- |
| **Single-blind**      | Participants only                           | When participant behavior can affect outcomes     |
| **Double-blind**      | Participants + outcome assessors            | Most clinical trials; subjective outcomes         |
| **Triple-blind**      | Participants + assessors + data analysts    | When analytical decisions could introduce bias    |
| **Unblinded (Open)**  | Nobody blinded                              | When blinding is impossible (e.g., surgical trial)|

```python
# Demonstrating observer bias impact (simulation)
np.random.seed(1)
n = 50
true_effect = 2.0

# Unblinded assessors: subtly inflate scores in treatment group
observer_inflation = 1.5   # systematic inflation when assessor knows treatment

control_scores_unblinded = np.random.normal(50, 8, n)
treatment_scores_unblinded = np.random.normal(50 + true_effect + observer_inflation, 8, n)

# Blinded assessors: no inflation
control_scores_blinded = np.random.normal(50, 8, n)
treatment_scores_blinded = np.random.normal(50 + true_effect, 8, n)

diff_unblinded = treatment_scores_unblinded.mean() - control_scores_unblinded.mean()
diff_blinded   = treatment_scores_blinded.mean() - control_scores_blinded.mean()

print(f"True effect:              {true_effect:.1f}")
print(f"Estimated (unblinded):    {diff_unblinded:.2f}  (inflated by observer bias)")
print(f"Estimated (blinded):      {diff_blinded:.2f}  (closer to truth)")
```

---

## 4.4 Validity Framework

**Validity** refers to the degree to which a study accurately measures what it intends to measure and whether conclusions can be extended beyond the study context.

### Four Types of Validity

| Type                              | Question It Asks                                                   | Main Threats                                      |
| --------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------- |
| **Internal validity**             | Did the treatment actually cause the observed difference?          | Confounding, selection bias, attrition            |
| **External validity**             | Can findings be generalized beyond this study's sample/setting?   | Unrepresentative sample, artificial setting       |
| **Statistical conclusion validity**| Are the statistical inferences correct?                           | Low power, violated assumptions, multiple testing |
| **Construct validity**            | Did the measures actually capture the intended concepts?           | Poor operationalization, observer bias            |

### Internal Validity Threats (Campbell & Stanley)

| Threat                 | Description                                                                |
| ---------------------- | -------------------------------------------------------------------------- |
| **History**            | An external event occurs between pre- and post-test measurements           |
| **Maturation**         | Participants naturally change over time during the study                   |
| **Testing effect**     | Taking a pre-test improves post-test performance regardless of treatment   |
| **Instrumentation**    | Measurement tools or criteria change over the course of the study          |
| **Statistical regression** | Extreme scores at baseline naturally move toward the mean at follow-up |
| **Selection**          | Groups differ systematically at baseline (non-random assignment)           |
| **Attrition**          | Non-random dropout produces groups that differ at follow-up                |

> 💡 **Randomization** controls for History, Maturation, Testing effect, Instrumentation, Regression, and Selection — all at once. This is why randomized experiments have stronger internal validity than observational studies.

### Internal vs. External Validity Tradeoff

Tightly controlled experiments maximize internal validity but may sacrifice external validity — lab conditions often don't reflect the real world.

```
Highly controlled lab experiment:
  ✅ Internal validity (confounders controlled)
  ❌ External validity (artificial setting, unrepresentative subjects)

Real-world observational study:
  ❌ Internal validity (cannot rule out confounders)
  ✅ External validity (natural setting, representative population)
```

> 💡 Pragmatic trials and field experiments attempt to balance both — they randomize but within naturalistic settings. A/B tests in industry often achieve this balance naturally.

---

## 4.5 Simpson's Paradox

A striking form of confounding where a trend that appears in **combined data** disappears or **reverses** when data is disaggregated by subgroups.

```python
import pandas as pd

# Simpson's Paradox: Treatment appears harmful overall, but helps both subgroups
data = {
    'Group':     ['Mild', 'Mild', 'Severe', 'Severe'],
    'Treatment': ['Yes',  'No',   'Yes',    'No'],
    'Recovered': [81,     234,    192,      55],
    'Total':     [270,    270,    263,      80],
}
df = pd.DataFrame(data)
df['Recovery_rate'] = (df['Recovered'] / df['Total'] * 100).round(1)

print(df[['Group', 'Treatment', 'Recovery_rate']])

# Combined (aggregated) rates
mild_yes    = 81 / 270
mild_no     = 234 / 270
severe_yes  = 192 / 263
severe_no   = 55 / 80

combined_yes = (81 + 192) / (270 + 263)
combined_no  = (234 + 55)  / (270 + 80)

print(f"\nWithin Mild:    Treatment {mild_yes:.1%} vs Control {mild_no:.1%}")
print(f"Within Severe:  Treatment {severe_yes:.1%} vs Control {severe_no:.1%}")
print(f"Combined:       Treatment {combined_yes:.1%} vs Control {combined_no:.1%}")
print("\n→ Treatment helps in BOTH subgroups but appears harmful in combined data!")
print("→ Reason: severe patients were more likely to receive treatment AND less likely to recover")
```

**Output:**

```
Within Mild:    Treatment 30.0% vs Control 86.7%   ← Wait...
Within Severe:  Treatment 73.0% vs Control 68.8%
Combined:       Treatment 50.9% vs Control 83.0%

→ Treatment helps in Severe subgroup but appears harmful in combined data!
→ Confound: severity is associated with both treatment assignment and outcome
```

> ⚠️ Simpson's Paradox is not just a curiosity — it has appeared in real data about UC Berkeley admissions, COVID vaccine effectiveness reports, and baseball batting averages. Always stratify to check. 辛普森悖論在真實資料中屢見不鮮，分析資料時應先檢查是否存在重要的子群體效應。

---

## 4.6 Key Takeaways

| Concept                   | Key Point                                                                  |
| ------------------------- | -------------------------------------------------------------------------- |
| **Confounding**           | Distorts causal estimates; randomization is the only complete solution      |
| **Bias vs. variability**  | Bias is systematic and cannot be fixed by adding data; variability can     |
| **Blinding**              | Prevents observer and response biases; always use when possible            |
| **Internal validity**     | Randomization is the strongest protection                                  |
| **External validity**     | Requires representative sampling and realistic settings                    |
| **Simpson's Paradox**     | Always stratify by important subgroups; aggregated trends can be misleading|

---