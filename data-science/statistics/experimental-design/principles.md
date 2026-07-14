# Principles of Experimental Design

Three fundamental principles underpin every valid experiment. Without them, the results may be biased, imprecise, or not generalizable. These principles were formalized by Ronald A. Fisher in the 1920s and remain the foundation of modern experimental design.

Key point: Fisher's three principles: Randomization, Replication, and Blocking. These three principles are not optional suggestions, but necessary conditions for experiments to draw valid conclusions.

## Principle 1: Randomization

**Randomization** means that experimental units are assigned to treatment groups using a random mechanism — not the researcher's judgment, convenience, or any systematic pattern.

### Why It Matters

Randomization is the **only design strategy** that can control for confounding variables — including ones you haven't thought of. When assignment is random, confounders are distributed roughly equally across groups by chance.

| Without Randomization | With Randomization |
| ---------------------------------------------- | ---------------------------------------------------- |
| Sicker patients may end up in the treatment group | Sickness is distributed roughly equally by chance |
| Researcher bias may influence assignment | Bias is eliminated by the random mechanism |
| Cannot establish causation | Causation can be inferred (if well-executed) |

### Types of Randomization

| Type | Description | When to Use |
| ------------------------ | --------------------------------------------------------------- | ------------------------------------------------------- |
| **Simple randomization** | Each unit independently assigned, like a coin flip | Large samples where balance will emerge naturally |
| **Block randomization** | Units are grouped into blocks, randomized within each block | Small samples; ensures balance on a known variable |
| **Stratified randomization** | Pre-stratify by a key variable, then randomize within strata | Ensures treatment groups are balanced on critical vars |
| **Cluster randomization** | Entire clusters (e.g., schools, clinics) are assigned together | When individual randomization is impractical |

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

Warning: Randomization ≠ Haphazard: Researchers sometimes assign "randomly" by alternating, using patient ID parity, or by convenience. These are systematic, not random. Use a random number generator or randomization table. "Random" does not mean "casual". Alternate grouping and grouping by odd and even numbers are systematic allocations, not true randomization.

## Principle 2: Replication

**Replication** means having multiple experimental units per treatment group. It is what allows you to:

1. **Estimate experimental error** — the natural variability between units given the same treatment
2. **Detect real effects** — separate true treatment effects from random noise
3. **Generalize findings** — results from a single observation cannot be generalized

Tip: Replication ≠ Repeated Measurement: Measuring the same unit twice is a repeated measurement, not replication. True replication requires independent experimental units per treatment. Repeated measurement of the same individual does not equal replication. Replications must be independent experimental units.

### How Many Replicates?

The number of replicates needed depends on:

- The **effect size** you want to detect (smaller effects need more replicates)
- The **variability** in your data (higher variability needs more replicates)
- The **significance level** α and desired **power** 1−β

This is covered formally in [Sample Size and Statistical Power](./sample-size-power.md).

**Quick rule of thumb:**

| Study Type | Typical Minimum Replicates per Group |
| ------------------------------ | ------------------------------------- |
| Screening / pilot study | 3–5 |
| Lab / well-controlled experiment | 5–10 |
| Clinical trial | Determined by formal power analysis |
| A/B test (web) | Hundreds to thousands (low effect size) |

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

The SE shrinks as n grows — more replicates → more precise estimates.

## Principle 3: Blocking

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

| Block when... | Don't block when... |
| ------------------------------------------------ | ---------------------------------------------------- |
| You can identify a nuisance variable in advance | No meaningful grouping variable exists |
| The nuisance variable explains substantial variance | The grouping variable explains very little variance |
| Blocks are naturally formed (batches, sites, days) | You have very few EUs and blocking wastes df |

Tip: Rule of thumb: Block on variables you expect to explain at least 10–15% of the total variance. If the nuisance variable is weak, blocking actually hurts precision by consuming degrees of freedom without removing much error.

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

## The Three Principles Working Together

| Principle | Controls for... | Improves... |
| ----------------- | ------------------------ | ------------------------- |
| **Randomization** | Confounding (unknown and known) | Internal validity |
| **Replication** | Random sampling error | Statistical power |
| **Blocking** | Known nuisance variables | Precision (smaller error) |

A practical experiment typically uses **all three**:

1. **Block** units by the known nuisance variable (e.g., hospital)
2. **Randomize** treatment assignment within each block
3. Use enough **replicates** to achieve adequate power

## Local Control

A fourth principle sometimes listed alongside the original three is **local control** — the idea that experimental conditions should be kept as uniform as possible within groups to minimize extraneous variation. This includes:

- Standardizing protocols (same equipment, same time of day, same operators)
- Controlling the environment (temperature, humidity, lighting)
- Using trained and calibrated personnel

Warning: Randomization handles between-group confounding. Local control handles within-group variability. Both are needed.

## Key Takeaways

| Principle | What It Prevents | Python Tool |
| ----------------- | ----------------------------------- | ----------------------------------------- |
| **Randomization** | Confounding and selection bias | `numpy.random.choice`, `random.shuffle` |
| **Replication** | Pseudoreplication, under-powered tests | Sample size calculations (`statsmodels`) |
| **Blocking** | Nuisance variable inflation | Block structure in DataFrame + ANOVA |
| **Local control** | Within-group extraneous variation | Protocol standardization (not statistical) |

## Randomization Methods

Randomization reduces **selection bias** and balances both known and unknown confounding variables across groups.

### Simple Randomization

- Each participant has an equal chance of being assigned to any group.
- Easy to implement, but may cause:
  - **Uneven sample sizes** → resolved with **block randomization**.
  - **Imbalance in covariates** → resolved with **stratified randomization**.

| Concept | Meaning |
| ------- | ------- |
| Random sampling | Randomly choose people/items from a population |
| Random assignment | Randomly assign sampled participants to treatment groups |
| Why it matters | Sampling supports generalization; assignment supports causality |

```python
# Example: split dataset randomly into two groups
group1 = df.sample(frac=0.5, replace=False, random_state=42)
group2 = df.drop(group1.index)
```

```python
import random
participants = ["P1", "P2", "P3", "P4", "P5", "P6"]
treatment_groups = ['Treatment A', 'Treatment B']

assignments = {p: random.choice(treatment_groups) for p in participants}
```

### Block Randomization

- Ensures equal numbers across groups at **regular intervals**.
- Prevents imbalance if the study ends early or participant enrollment is staggered.

Steps:

1. Group participants into blocks.
2. Randomly assign within each block.
3. Each block maintains balanced allocation.

| Block | Treatment A | Treatment B |
| ----- | ----------- | ----------- |
| Block 1 | Random subset | Random subset |
| Block 2 | Random subset | Random subset |
| Block 3 | Random subset | Random subset |

```python
participants = [i for i in range(1, 11)]
block_type = ['block1', 'block2']
n_blocks = len(participants) // len(block_type)

blocks = block_type * n_blocks
np.random.shuffle(blocks)

blocked_random_df = pd.DataFrame({
    'participant': ['P'+str(i) for i in participants],
    'block': blocks
})
```

### Stratified Randomization

- Ensures equal distribution of participants based on **stratification factors** (covariates like age, gender).
- Especially important when covariates are strongly associated with outcomes.

- **Covariate:** A variable controlled for in a model, may or may not distort the true relationship.
- **Confounder:** A variable that **distorts the causal relationship** between independent and dependent variables.

| Stratum | Sample Within Stratum |
| ------- | --------------------- |
| Under 50, Female | Randomly sample or assign |
| Under 50, Male | Randomly sample or assign |
| 50+, Female | Randomly sample or assign |
| 50+, Male | Randomly sample or assign |

```python
df = pd.DataFrame({
    'Age': np.random.choice(['Under 50', 'Over 50'], size=100),
    'Gender': np.random.choice(['Male', 'Female'], size=100)
})

def assign_treatment(group):
    group['Treatment'] = np.random.choice(['Treatment A', 'Treatment B'], size=len(group))
    return group

df_strat = df.groupby(['Age', 'Gender']).apply(assign_treatment)
```

## Experimental Designs

### Randomized Block Design

- Group similar experimental units into **blocks** (e.g., age groups).
- Randomly assign treatments within each block.
- Reduces variability due to known confounders.
- Related to stratified randomization, but applied at the design level.

### Factorial Designs

- Evaluate the effect of **two or more factors simultaneously**.
- Allows study of **interactions** between factors.

- **Full Factorial Design:**
  Tests **all combinations** of factor levels. Gives maximum information but requires more runs.

- **Fractional Factorial Design:**
  Tests only a **subset of combinations**, reducing cost and effort at the expense of some interaction information.

📌 **Extra Notes:**

- Factorial designs are widely used in clinical trials, manufacturing, and A/B testing.
- They are efficient but require careful interpretation of interaction effects.

## Summary Table

| Method / Design | Purpose | Key Feature | Limitation |
| ------------------------ | ---------------------------------------- | ------------------------------- | ---------------------------- |
| Simple Randomization | Random assignment | Easy to apply | May cause imbalance |
| Block Randomization | Balance groups at intervals | Equal group sizes | More complex |
| Stratified Randomization | Control for covariates/confounders | Even distribution within strata | Needs stratification data |
| Randomized Block Design | Reduce confounder effect at design level | Blocking units | Limited to known confounders |
| Factorial Designs | Study multiple factors + interactions | Efficient exploration | Costly if many factors |

## A Useful Memory Rule

- randomization fights hidden bias
- replication measures noise
- blocking removes known nuisance variation

Tip: If you remember only one line from this chapter, remember that one.
