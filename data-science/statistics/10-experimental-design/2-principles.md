# 2. Principles of Experimental Design

Three fundamental principles underpin every valid experiment. Without them, the results may be biased, imprecise, or not generalizable. These principles were formalized by Ronald A. Fisher in the 1920s and remain the foundation of modern experimental design.

> 📌 **Fisher 的三大原則**：隨機化（Randomization）、重複（Replication）、區組化（Blocking）。這三個原則不是可選的建議，而是實驗能得出有效結論的必要條件。

---

## 2.1 Principle 1: Randomization (隨機化)

**Randomization** means that experimental units are assigned to treatment groups using a random mechanism — not the researcher's judgment, convenience, or any systematic pattern.

### Why It Matters

Randomization is the **only design strategy** that can control for confounding variables — including ones you haven't thought of. When assignment is random, confounders are distributed roughly equally across groups by chance.

| Without Randomization                          | With Randomization                                   |
| ---------------------------------------------- | ---------------------------------------------------- |
| Sicker patients may end up in the treatment group | Sickness is distributed roughly equally by chance  |
| Researcher bias may influence assignment       | Bias is eliminated by the random mechanism           |
| Cannot establish causation                     | Causation can be inferred (if well-executed)         |

### Types of Randomization

| Type                     | Description                                                     | When to Use                                             |
| ------------------------ | --------------------------------------------------------------- | ------------------------------------------------------- |
| **Simple randomization** | Each unit independently assigned, like a coin flip              | Large samples where balance will emerge naturally       |
| **Block randomization**  | Units are grouped into blocks, randomized within each block     | Small samples; ensures balance on a known variable      |
| **Stratified randomization** | Pre-stratify by a key variable, then randomize within strata| Ensures treatment groups are balanced on critical vars  |
| **Cluster randomization**| Entire clusters (e.g., schools, clinics) are assigned together  | When individual randomization is impractical            |

```python
import pandas as pd
import numpy as np

np.random.seed(42)
n = 20  # 20 experimental units

# Simple randomization
units = pd.DataFrame({'unit_id': range(1, n + 1)})
units['treatment'] = np.random.choice(['Treatment', 'Control'], size=n)
print("Simple randomization balance:")
print(units['treatment'].value_counts())

# Block randomization (ensures equal groups)
# Each block of 4 contains exactly 2 Treatment and 2 Control
def block_randomize(n_blocks, block_size=4, treatments=['Treatment', 'Control']):
    reps = block_size // len(treatments)
    assignments = []
    for _ in range(n_blocks):
        block = treatments * reps
        np.random.shuffle(block)
        assignments.extend(block)
    return assignments

units['block_treatment'] = block_randomize(n_blocks=5)
print("\nBlock randomization balance:")
print(units['block_treatment'].value_counts())
```

> ⚠️ **Randomization ≠ Haphazard**: Researchers sometimes assign "randomly" by alternating, using patient ID parity, or by convenience. These are **systematic**, not random. Use a random number generator or randomization table.  
> 「隨機」不等於「隨便」。交替分組、按奇偶編號分組都是系統性分配，不是真正的隨機化。

---

## 2.2 Principle 2: Replication (重複)

**Replication** means having multiple experimental units per treatment group. It is what allows you to:

1. **Estimate experimental error** — the natural variability between units given the same treatment
2. **Detect real effects** — separate true treatment effects from random noise
3. **Generalize findings** — results from a single observation cannot be generalized

> 💡 **Replication ≠ Repeated Measurement**: Measuring the same unit twice is a repeated measurement, not replication. True replication requires **independent** experimental units per treatment. 重複量測同一個體不等於重複。重複（Replication）必須是獨立的實驗單位。

### How Many Replicates?

The number of replicates needed depends on:

- The **effect size** you want to detect (smaller effects need more replicates)
- The **variability** in your data (higher variability needs more replicates)
- The **significance level** α and desired **power** 1−β

This is covered formally in [Section 5: Sample Size & Statistical Power](./5-sample-size-power.md).

**Quick rule of thumb:**

| Study Type                     | Typical Minimum Replicates per Group |
| ------------------------------ | ------------------------------------- |
| Screening / pilot study        | 3–5                                   |
| Lab / well-controlled experiment | 5–10                                |
| Clinical trial                 | Determined by formal power analysis   |
| A/B test (web)                 | Hundreds to thousands (low effect size) |

```python
# Demonstrating why replication matters
# Compare variability in estimated mean with different n

np.random.seed(1)
true_mean = 50.0
population_sd = 10.0

for n in [3, 10, 30, 100]:
    sample_means = [np.mean(np.random.normal(true_mean, population_sd, n))
                    for _ in range(1000)]
    se = np.std(sample_means)
    print(f"n = {n:4d}: Mean of sample means = {np.mean(sample_means):.2f}, "
          f"SE = {se:.2f}")
```

**Output:**

```
n =    3: Mean of sample means = 50.01, SE = 5.73
n =   10: Mean of sample means = 49.97, SE = 3.14
n =   30: Mean of sample means = 50.00, SE = 1.82
n =  100: Mean of sample means = 50.00, SE = 0.99
```

> The SE shrinks as n grows — more replicates → more precise estimates.

---

## 2.3 Principle 3: Blocking (區組化)

**Blocking** is a technique to **control a known source of variability** by grouping similar experimental units together and ensuring that every treatment appears in every block.

### The Logic of Blocking

If you know that patients in Hospital A tend to have different baseline health from Hospital B, then hospital is a nuisance variable. By blocking on hospital (assigning all treatments within each hospital), you remove hospital-to-hospital variability from the error term — making your test more sensitive.

```
Without blocking:
  Error term = Treatment effect + Block effect + Random noise
  → Block effect inflates error → harder to detect treatment

With blocking:
  Error term = Treatment effect + Random noise (only)
  → Block effect is accounted for → easier to detect treatment
```

### When to Block

| Block when...                                    | Don't block when...                                 |
| ------------------------------------------------ | ---------------------------------------------------- |
| You can identify a nuisance variable in advance  | No meaningful grouping variable exists               |
| The nuisance variable explains substantial variance | The grouping variable explains very little variance |
| Blocks are naturally formed (batches, sites, days) | You have very few EUs and blocking wastes df        |

> 💡 **Rule of thumb**: Block on variables you expect to explain at least 10–15% of the total variance. If the nuisance variable is weak, blocking actually hurts precision by consuming degrees of freedom without removing much error.

```python
import pandas as pd
import numpy as np
from scipy import stats

np.random.seed(0)

# 3 blocks (labs), 2 treatments, 1 replicate per cell
# Block effect is large (labs differ by ~15 units)

block_effects = {'Lab1': 0, 'Lab2': 15, 'Lab3': -10}
treatment_effects = {'Control': 0, 'Treatment': 5}

rows = []
for lab, b_eff in block_effects.items():
    for trt, t_eff in treatment_effects.items():
        value = 100 + b_eff + t_eff + np.random.normal(0, 2)
        rows.append({'block': lab, 'treatment': trt, 'response': round(value, 2)})

df = pd.DataFrame(rows)
print(df)

# Without blocking: compare treatment means directly (ignores lab differences)
grouped = df.groupby('treatment')['response'].mean()
print("\nNaive treatment means (ignoring blocks):")
print(grouped)

# With blocking: look at within-block treatment differences
df_wide = df.pivot(index='block', columns='treatment', values='response')
df_wide['within_block_diff'] = df_wide['Treatment'] - df_wide['Control']
print("\nWithin-block treatment differences:")
print(df_wide)
print(f"\nMean within-block effect: {df_wide['within_block_diff'].mean():.2f}")
print("(True effect is 5.0)")
```

---

## 2.4 The Three Principles Working Together

| Principle         | Controls for...          | Improves...               |
| ----------------- | ------------------------ | ------------------------- |
| **Randomization** | Confounding (unknown and known) | Internal validity   |
| **Replication**   | Random sampling error    | Statistical power         |
| **Blocking**      | Known nuisance variables | Precision (smaller error) |

A practical experiment typically uses **all three**:

1. **Block** units by the known nuisance variable (e.g., hospital)
2. **Randomize** treatment assignment within each block
3. Use enough **replicates** to achieve adequate power

---

## 2.5 Local Control

A fourth principle sometimes listed alongside the original three is **local control** — the idea that experimental conditions should be kept as uniform as possible within groups to minimize extraneous variation. This includes:

- Standardizing protocols (same equipment, same time of day, same operators)
- Controlling the environment (temperature, humidity, lighting)
- Using trained and calibrated personnel

> ⚠️ Randomization handles **between-group** confounding. Local control handles **within-group** variability. Both are needed.

---

## 2.6 Key Takeaways

| Principle         | What It Prevents                    | Python Tool                               |
| ----------------- | ----------------------------------- | ----------------------------------------- |
| **Randomization** | Confounding and selection bias      | `numpy.random.choice`, `random.shuffle`   |
| **Replication**   | Pseudoreplication, under-powered tests | Sample size calculations (`statsmodels`) |
| **Blocking**      | Nuisance variable inflation         | Block structure in DataFrame + ANOVA      |
| **Local control** | Within-group extraneous variation   | Protocol standardization (not statistical)|

---

**← Previous:** [Core Concepts & Terminology](./1-core-concepts.md)  
**Next:** [Common Experimental Designs →](./3-designs.md)
