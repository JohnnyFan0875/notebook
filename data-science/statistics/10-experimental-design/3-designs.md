# 3. Common Experimental Designs

Choosing the right design structure is as important as the analysis method. The design determines how variance is partitioned, how degrees of freedom are allocated, and whether interactions can be detected.

> 📌 **選擇設計的邏輯**：先確認有幾個因子、有無需要控制的干擾變數、每個受試者能接受幾種處理。從這三個問題出發，就能縮小設計的選擇範圍。

---

## 3.1 Overview: Which Design for Which Situation?

| Design                            | # of Factors  | Blocking? | Subjects per Treatment | Key Feature                        |
| --------------------------------- | ------------- | --------- | ----------------------- | ---------------------------------- |
| **CRD** (Completely Randomized)   | 1+            | ❌ None    | Different subjects      | Simplest; requires homogeneous units |
| **RCBD** (Randomized Complete Block) | 1+         | ✅ 1 blocking variable | Different per block | Controls one nuisance variable  |
| **Latin Square**                  | 1             | ✅ 2 blocking variables | Different per cell | Controls two nuisance variables |
| **Factorial**                     | 2+            | Optional  | Different or same       | Detects interactions between factors |
| **Crossover**                     | 1+            | ✅ Subject = block | Same subjects get all treatments | Each subject is their own control |
| **Split-Plot**                    | 2+            | ✅ Whole-plot = block | Mixed | Some factors harder to randomize |

---

## 3.2 Completely Randomized Design (CRD)

The simplest design: each experimental unit is assigned to a treatment entirely at random, with no blocking.

**When to use:**
- Experimental units are **homogeneous** (similar to each other)
- No known nuisance variable to control
- Lab settings with well-controlled conditions

**Structure:**

```
t treatments, n replicates each → t × n total experimental units
All units randomized independently to treatments
```

```python
import pandas as pd
import numpy as np
from scipy import stats

np.random.seed(42)

# CRD: 3 fertilizer treatments, 5 plots each
treatments = ['Fertilizer_A', 'Fertilizer_B', 'Control']
n_reps = 5

data = pd.DataFrame({
    'plot_id': range(1, 16),
    'treatment': np.repeat(treatments, n_reps),
    'yield_kg': np.concatenate([
        np.random.normal(85, 10, n_reps),  # Fertilizer A
        np.random.normal(95, 10, n_reps),  # Fertilizer B
        np.random.normal(75, 10, n_reps),  # Control
    ])
})

# Shuffle to mimic actual random assignment
data = data.sample(frac=1, random_state=1).reset_index(drop=True)
print(data.sort_values('plot_id').head(10))

# One-way ANOVA
groups = [data[data['treatment'] == t]['yield_kg'] for t in treatments]
f_stat, p_val = stats.f_oneway(*groups)
print(f"\nOne-way ANOVA: F = {f_stat:.3f}, p = {p_val:.4f}")
```

> ⚠️ CRD is **not recommended** when experimental units are heterogeneous (e.g., animals of different ages, plots with different soil types). The between-unit variability ends up in the error term, reducing power.

---

## 3.3 Randomized Complete Block Design (RCBD)

Experimental units are grouped into **blocks** of similar units. Each treatment appears exactly once in each block. Within each block, treatments are randomized.

**When to use:**
- One known source of variability (nuisance variable) that can be identified before the experiment
- Blocks could be: time periods, locations, operators, batches, litters

**Structure:**

```
b blocks × t treatments = b × t total EUs
Each treatment appears exactly once per block
Randomize treatment assignment within each block
```

```python
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

np.random.seed(7)

# RCBD: 3 drug doses, 4 hospital blocks, 1 patient per cell
n_blocks = 4
treatments = ['Low', 'Medium', 'High']
block_effects = [0, 10, -8, 5]   # hospitals differ substantially

rows = []
for b_idx in range(n_blocks):
    for trt in np.random.permutation(treatments):  # randomize within block
        t_eff = {'Low': 0, 'Medium': 5, 'High': 9}[trt]
        bp = 130 + block_effects[b_idx] + t_eff + np.random.normal(0, 3)
        rows.append({
            'block': f'Hospital_{b_idx+1}',
            'treatment': trt,
            'blood_pressure': round(bp, 1)
        })

df = pd.DataFrame(rows)
print(df.pivot(index='block', columns='treatment', values='blood_pressure'))

# Two-way ANOVA (treatment + block; no interaction since 1 rep per cell)
model = smf.ols('blood_pressure ~ C(treatment) + C(block)', data=df).fit()
from statsmodels.stats.anova import anova_lm
print("\nANOVA Table:")
print(anova_lm(model, typ=2))
```

> 💡 In RCBD the interaction between block and treatment **cannot be estimated** when there is only one observation per cell — this is a deliberate tradeoff. If you need to estimate the interaction, add replicates within each cell (a Generalized RCBD).

---

## 3.4 Factorial Design

A factorial design varies **two or more factors simultaneously**. Every combination of factor levels is tested.

**Key advantage:** You can detect **interactions** — cases where the effect of one factor depends on the level of another. This is impossible with one-factor-at-a-time experiments.

**Notation:** A **2 × 3 factorial** has 2 levels of Factor A and 3 levels of Factor B → 6 treatment combinations.

```python
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm

np.random.seed(0)

# 2×2 Factorial: Drug (A, B) × Dose (Low, High), 5 reps per cell
design = pd.DataFrame([
    {'drug': drug, 'dose': dose}
    for drug in ['DrugA', 'DrugB']
    for dose in ['Low', 'High']
    for _ in range(5)
])

# True effects: Drug B works better, High dose works better
# Interaction: DrugB's advantage is amplified at High dose
effects = {
    ('DrugA', 'Low'): 100,
    ('DrugA', 'High'): 108,
    ('DrugB', 'Low'): 105,
    ('DrugB', 'High'): 120,   # interaction: extra benefit
}
design['response'] = design.apply(
    lambda r: effects[(r['drug'], r['dose'])] + np.random.normal(0, 5),
    axis=1
).round(1)

print("Cell means:")
print(design.groupby(['drug', 'dose'])['response'].mean().unstack())

# Two-way ANOVA with interaction
model = smf.ols('response ~ C(drug) * C(dose)', data=design).fit()
print("\nANOVA Table (with interaction):")
print(anova_lm(model, typ=2))
```

**Interpreting interaction plots:**

```python
import matplotlib.pyplot as plt

cell_means = design.groupby(['drug', 'dose'])['response'].mean().unstack()

cell_means.T.plot(marker='o', figsize=(6, 4))
plt.title('Interaction Plot: Drug × Dose')
plt.xlabel('Dose')
plt.ylabel('Mean Response')
plt.legend(title='Drug')
plt.tight_layout()
plt.show()
```

> 💡 **Parallel lines** in an interaction plot → no interaction (the two factors act independently).  
> **Non-parallel or crossing lines** → interaction present (the effect of one factor changes depending on the other).  
> 交互作用圖中，如果兩條線平行代表沒有交互作用；不平行或交叉代表有交互作用。

**Main effect vs. interaction:**

| Term              | Definition                                               |
| ----------------- | -------------------------------------------------------- |
| **Main effect**   | The average effect of one factor, ignoring all others    |
| **Interaction**   | The effect of one factor changes at different levels of another |
| **Significant interaction** | Main effects alone are misleading — must interpret jointly |

> ⚠️ When an interaction is significant, **do not interpret main effects alone**. Report and visualize the interaction.

---

## 3.5 Latin Square Design

Controls for **two** blocking factors simultaneously, using a square arrangement where each treatment appears exactly once in each row and each column.

**When to use:**
- Two known nuisance variables (e.g., row = day of week, column = operator)
- Number of treatments = number of row blocks = number of column blocks

**Structure (3×3 example):**

|          | Operator 1 | Operator 2 | Operator 3 |
| -------- | ---------- | ---------- | ---------- |
| **Day 1**| A          | B          | C          |
| **Day 2**| B          | C          | A          |
| **Day 3**| C          | A          | B          |

```python
from itertools import product

# 4×4 Latin Square
# Rows = Days, Columns = Machines, Letters = Treatments (A, B, C, D)
latin_square = [
    ['A', 'B', 'C', 'D'],
    ['B', 'A', 'D', 'C'],
    ['C', 'D', 'A', 'B'],
    ['D', 'C', 'B', 'A'],
]

np.random.seed(5)
rows = []
for day_idx, row in enumerate(latin_square):
    for machine_idx, trt in enumerate(row):
        t_eff = {'A': 0, 'B': 3, 'C': 6, 'D': 9}[trt]
        day_eff = day_idx * 2
        machine_eff = machine_idx * (-1.5)
        value = 50 + t_eff + day_eff + machine_eff + np.random.normal(0, 1.5)
        rows.append({
            'day': f'Day_{day_idx+1}',
            'machine': f'Machine_{machine_idx+1}',
            'treatment': trt,
            'yield': round(value, 2)
        })

df_ls = pd.DataFrame(rows)
print(df_ls.pivot(index='day', columns='machine', values='treatment'))  # layout
```

> ⚠️ Latin Square has a critical assumption: **no interaction** between the treatment and either blocking factor. If interactions exist, the Latin Square analysis is invalid. 拉丁方格假設處理與兩個區組因子之間沒有交互作用。如果有，則分析結果無效。

---

## 3.6 Crossover Design

Each subject receives **all treatments** in sequence, separated by washout periods. The subject itself acts as its own block.

**When to use:**
- Individual variability is large relative to treatment effects
- Carryover effects can be eliminated with adequate washout periods
- Treatments are reversible in their effects

**Key concepts:**

| Term            | Definition                                                         |
| --------------- | ------------------------------------------------------------------ |
| **Period**      | A time slot during which one treatment is administered             |
| **Sequence**    | The order of treatments a subject receives (e.g., A→B vs. B→A)    |
| **Washout**     | A rest period between treatments to eliminate carryover effects    |
| **Carryover**   | The effect of a previous treatment persisting into the next period |

```python
import pandas as pd
import numpy as np

np.random.seed(3)
n_subjects = 10

# 2×2 crossover: half receive A then B, half receive B then A
sequences = np.repeat(['AB', 'BA'], n_subjects // 2)
subjects = pd.DataFrame({
    'subject_id': range(1, n_subjects + 1),
    'sequence': sequences,
    'subject_effect': np.random.normal(0, 5, n_subjects)  # individual variability
})

rows = []
for _, s in subjects.iterrows():
    for period, trt in enumerate(list(s['sequence']), start=1):
        t_eff = {'A': 0, 'B': 8}[trt]
        period_eff = (period - 1) * (-2)  # period effect
        response = 100 + t_eff + period_eff + s['subject_effect'] + np.random.normal(0, 2)
        rows.append({
            'subject_id': s['subject_id'],
            'period': period,
            'treatment': trt,
            'response': round(response, 1)
        })

df_co = pd.DataFrame(rows)
print(df_co.pivot(index='subject_id', columns='period', values='treatment'))
```

> ⚠️ If the washout period is insufficient, carryover effects will **bias** your treatment comparison. Always plan washout duration based on pharmacokinetics or known decay of the treatment effect.

---

## 3.7 Split-Plot Design

Some factors are easy to randomize at the individual unit level; others are logistically difficult and must be applied to larger "whole plots." The **split-plot design** handles this naturally.

**Classic example:** Testing varieties of wheat (easy to randomize within a field) and irrigation levels (requires whole-field flooding — hard to randomize at the row level).

| Level           | Unit         | What's Assigned                        |
| --------------- | ------------ | --------------------------------------- |
| **Whole-plot**  | Large unit   | Hard-to-randomize factor (irrigation)  |
| **Sub-plot**    | Small unit   | Easy-to-randomize factor (variety)     |

> 💡 Split-plot analyses require **two error terms**: one for the whole-plot factor and one for the sub-plot factor. Using a single error term (as in a standard two-way ANOVA) inflates significance for whole-plot effects.  
> 裂區設計需要兩個誤差項。若誤用標準雙因子 ANOVA，會對全區因子的顯著性做出錯誤估計。

---

## 3.8 Choosing the Right Design — Decision Guide

```
Start here:
  ↓
How many factors?
  ├─ 1 factor → Go to (A)
  └─ 2+ factors → Consider Factorial or Split-Plot

(A) Is there a known nuisance variable?
  ├─ No → Completely Randomized Design (CRD)
  ├─ 1 nuisance variable → RCBD
  ├─ 2 nuisance variables, n = t treatments → Latin Square
  └─ Subjects can receive all treatments → Crossover

(B) Multiple factors:
  ├─ All factors easy to randomize → Full or Fractional Factorial
  └─ One factor hard to randomize → Split-Plot
```

---

## 3.9 Key Takeaways

| Design      | Controls Nuisance? | Detects Interaction? | Requires Homogeneous Units? |
| ----------- | ------------------- | --------------------- | --------------------------- |
| CRD         | ❌                  | With multiple factors | ✅                          |
| RCBD        | ✅ (1 variable)     | With multiple factors | ❌                          |
| Latin Square| ✅ (2 variables)    | ❌ Assumes none       | ❌                          |
| Factorial   | Optional            | ✅ Yes                | Optional                    |
| Crossover   | ✅ (subject)        | Limited               | ❌                          |
| Split-Plot  | ✅ (whole-plot)     | ✅ Yes                | ❌                          |

---

**← Previous:** [Principles of Experimental Design](./2-principles.md)  
**Next:** [Confounding, Bias & Validity →](./4-confounding-bias.md)
