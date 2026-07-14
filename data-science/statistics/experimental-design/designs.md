# Common Experimental Designs

Choosing the right design structure is as important as the analysis method. The design determines how variance is partitioned, how degrees of freedom are allocated, and whether interactions can be detected.

Key point: The logic of choosing a design: first confirm how many factors there are, whether there are interfering variables that need to be controlled, and how many treatments each subject can accept. Starting from these three questions, you can narrow down your design choices.

## Overview: Which Design for Which Situation?

| Design | # of Factors | Blocking? | Subjects per Treatment | Key Feature |
| --------------------------------- | ------------- | --------- | ----------------------- | ---------------------------------- |
| **CRD** (Completely Randomized) | 1+ | ❌ None | Different subjects | Simplest; requires homogeneous units |
| **RCBD** (Randomized Complete Block) | 1+ | ✅ 1 blocking variable | Different per block | Controls one nuisance variable |
| **Latin Square** | 1 | ✅ 2 blocking variables | Different per cell | Controls two nuisance variables |
| **Factorial** | 2+ | Optional | Different or same | Detects interactions between factors |
| **Crossover** | 1+ | ✅ Subject = block | Same subjects get all treatments | Each subject is their own control |
| **Split-Plot** | 2+ | ✅ Whole-plot = block | Mixed | Some factors harder to randomize |

## Completely Randomized Design (CRD)

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

Warning: CRD is not recommended when experimental units are heterogeneous (e.g., animals of different ages, plots with different soil types). The between-unit variability ends up in the error term, reducing power.

## Randomized Complete Block Design (RCBD)

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

Tip: In RCBD the interaction between block and treatment cannot be estimated when there is only one observation per cell — this is a deliberate tradeoff. If you need to estimate the interaction, add replicates within each cell (a Generalized RCBD).

### How To Think About Block Effects

Blocking is worthwhile when there is meaningful between-block variation that would otherwise inflate the residual error term.

Useful practical questions:

- are units inside each block more similar to each other than to units in other blocks?
- does each treatment appear within every block?
- is the main goal to control nuisance variation rather than estimate many interactions?

Key point: RCBD is not mainly about creating more groups. It is about protecting treatment comparisons from noise caused by a known nuisance variable.

## Balanced Incomplete Block Design (BIBD)

A **Balanced Incomplete Block Design** is used when blocking is still important, but each block cannot feasibly contain **all** treatments.

This happens when:

- there are too many treatments to fit into one block
- each block has a hard capacity limit
- experimental units within a block must remain comparable

The design is:

- **balanced**: each pair of treatments appears together equally often
- **incomplete**: not every treatment appears in every block
- **blocked**: units are still grouped to control nuisance variation

This makes BIBD a useful compromise between two competing goals:

1. preserve the precision benefit of blocking
2. avoid impractically large blocks

### When To Prefer BIBD Over RCBD

Use BIBD when a standard RCBD would make each block too crowded, expensive, or logistically impossible.

Typical examples:

- tasting panels where each judge can only evaluate a subset of products
- field trials with many candidate varieties but limited plot space per block
- educational or clinical settings where each site can only administer a subset of treatments

### A Quick Feasibility Check

For a BIBD, a common parameterization is:

- `t`: number of treatments
- `k`: number of treatments per block
- `r`: number of replications per treatment
- `lambda`: number of times each treatment pair appears together

These quantities are linked by:

\[
\lambda = \frac{r(k - 1)}{t - 1}
\]

If `lambda` is not a whole number, that exact BIBD is not feasible with the chosen `t`, `k`, and `r`.

Warning: BIBD is not just "leave some treatments out of some blocks." The missingness must be structured so that treatment comparisons remain balanced across the full design.

## Factorial Design

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

Tip: In an interaction plot, parallel lines suggest little or no interaction, while non-parallel or crossing lines suggest that the effect of one factor depends on the level of the other factor.

**Main effect vs. interaction:**

| Term | Definition |
| ----------------- | -------------------------------------------------------- |
| **Main effect** | The average effect of one factor, ignoring all others |
| **Interaction** | The effect of one factor changes at different levels of another |
| **Significant interaction** | Main effects alone are misleading — must interpret jointly |

Warning: When an interaction is significant, do not interpret main effects alone. Report and visualize the interaction.

### A Practical Starting Point For Interactions

Before running the formal model, it often helps to inspect the cell means directly.

Useful displays include:

- a pivot table of mean responses for each factor combination
- an interaction plot
- a heatmap when there are many combinations

Key point: A significant interaction means the factors do not act independently. Once that happens, statements like "Factor A is better on average" can be incomplete or misleading without naming the level of Factor B.

### 2^k Factorial Designs

A **2^k factorial design** is a special case where:

- there are `k` factors
- each factor has exactly **2 levels**
- the full design contains `2^k` treatment combinations

Examples:

- `2^2` design: 2 factors, 4 combinations
- `2^3` design: 3 factors, 8 combinations
- `2^4` design: 4 factors, 16 combinations

These designs are especially common in engineering, manufacturing, and screening experiments because they give a compact way to estimate:

- main effects
- two-way interactions
- higher-order interactions if the full design is run

Tip: The main practical appeal of `2^k` designs is not the notation itself. It is that two-level factors make effect coding, interaction interpretation, and screening workflows much simpler.

### Fractional Factorial Designs

When a full factorial becomes too expensive, a **fractional factorial design** deliberately runs only a subset of all combinations.

Why use it:

- the number of factors is large
- running every combination is too costly
- the main goal is screening for the most important factors first

The tradeoff is **aliasing**: some effects become confounded with others by design.

Key point: Fractional factorial designs buy efficiency by assuming that higher-order interactions are small enough to ignore, at least in the initial screening stage.

## Factorial vs. RCBD

These two designs are often confused because both organize structure before analysis, but they solve different problems.

| Design | Best when | Main payoff | Main tradeoff |
| --- | --- | --- | --- |
| Factorial | You want to study multiple treatments or conditions at once | Detects main effects and interactions | Can require more cells, more subjects, and more interpretation effort |
| RCBD | You want to control one known nuisance source of variability | Reduces within-block variance and improves precision | Usually gives up interaction estimation if there is only one observation per treatment-block cell |

## Latin Square Design

Controls for **two** blocking factors simultaneously, using a square arrangement where each treatment appears exactly once in each row and each column.

**When to use:**
- Two known nuisance variables (e.g., row = day of week, column = operator)
- Number of treatments = number of row blocks = number of column blocks

**Structure (3×3 example):**

|  | Operator 1 | Operator 2 | Operator 3 |
| -------- | ---------- | ---------- | ---------- |
| **Day 1** | A | B | C |
| **Day 2** | B | C | A |
| **Day 3** | C | A | B |

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

Warning: Latin Square has a critical assumption: no interaction between the treatment and either blocking factor. If interactions exist, the Latin Square analysis is invalid. Latin Square has a critical assumption: no interaction between the treatment and either blocking factor. If so, the analysis results are invalid.

## Crossover Design

Each subject receives **all treatments** in sequence, separated by washout periods. The subject itself acts as its own block.

**When to use:**
- Individual variability is large relative to treatment effects
- Carryover effects can be eliminated with adequate washout periods
- Treatments are reversible in their effects

**Key concepts:**

| Term | Definition |
| --------------- | ------------------------------------------------------------------ |
| **Period** | A time slot during which one treatment is administered |
| **Sequence** | The order of treatments a subject receives (e.g., A→B vs. B→A) |
| **Washout** | A rest period between treatments to eliminate carryover effects |
| **Carryover** | The effect of a previous treatment persisting into the next period |

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

Warning: If the washout period is insufficient, carryover effects will bias your treatment comparison. Always plan washout duration based on pharmacokinetics or known decay of the treatment effect.

## Split-Plot Design

Some factors are easy to randomize at the individual unit level; others are logistically difficult and must be applied to larger "whole plots." The **split-plot design** handles this naturally.

**Classic example:** Testing varieties of wheat (easy to randomize within a field) and irrigation levels (requires whole-field flooding — hard to randomize at the row level).

| Level | Unit | What's Assigned |
| --------------- | ------------ | --------------------------------------- |
| **Whole-plot** | Large unit | Hard-to-randomize factor (irrigation) |
| **Sub-plot** | Small unit | Easy-to-randomize factor (variety) |

Tip: Split-plot analyzes require two error terms: one for the whole-plot factor and one for the sub-plot factor. Using a single error term (as in a standard two-way ANOVA) inflates significance for whole-plot effects. Misuse of standard two-way ANOVA can lead to incorrect estimates of the significance of factors across the region.

## Choosing the Right Design — Decision Guide

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

## Key Takeaways

| Design | Controls Nuisance? | Detects Interaction? | Requires Homogeneous Units? |
| ----------- | ------------------- | --------------------- | --------------------------- |
| CRD | ❌ | With multiple factors | ✅ |
| RCBD | ✅ (1 variable) | With multiple factors | ❌ |
| Latin Square | ✅ (2 variables) | ❌ Assumes none | ❌ |
| Factorial | Optional | ✅ Yes | Optional |
| Crossover | ✅ (subject) | Limited | ❌ |
| Split-Plot | ✅ (whole-plot) | ✅ Yes | ❌ |

# Study Designs in Epidemiology and Clinical Research

## Study Designs

Study designs are broadly divided into three main categories:

1. **Observational studies** – researchers do not intervene, only observe.
2. **Experimental studies** – researchers assign interventions.
3. **Evidence synthesis** – researchers summarize findings across multiple studies.

## Hierarchy

```
Study Designs
├── Observational
│   ├── Cohort
│   │   ├── Prospective
│   │   └── Retrospective
│   ├── Case–Control
│   ├── Cross-Sectional
│   └── Longitudinal
├── Experimental
│   ├── Randomized Controlled Trial (RCT)
│   ├── Experimental Design
│   ├── Explanatory Design
│   ├── Descriptive Design
│   └── Correlational Design
└── Evidence Synthesis
    ├── Systematic Review
    └── Meta-analysis

```

## Observational Studies

Researchers observe exposures and outcomes without intervention.
Includes **Cohort**, **Case–Control**, and **Cross-Sectional** studies.

### Cohort Studies

- Participants are grouped by **exposure status** (exposed vs. unexposed), then followed to determine outcomes.
- Key feature: Exposure identified **before** outcome.

#### a. Prospective Cohort

- Researchers enroll participants now and follow them forward in time.
- Often start with healthy individuals who are free from the disease or outcome of interest
- **Example:** The _Framingham Heart Study_ (since 1948) has followed residents to identify cardiovascular risk factors (e.g., smoking, cholesterol, blood pressure).
- **Strengths:** Clear temporal sequence, less recall bias.
- **Weaknesses:** Time- and cost-intensive.

```text
Exposure measured now -> Follow forward -> Outcome observed later
```

#### b. Retrospective Cohort

- Researchers use **existing records** (e.g., medical charts, registries) to reconstruct past exposures and outcomes.
- **Example:** Hospital employee vaccination records linked to archived infection data.
- **Strengths:** Faster, less expensive.
- **Weaknesses:** Data quality limits, missing confounders.

```text
Existing records -> Reconstruct exposure -> Link to later outcome
```

### Case–Control Studies

- Start with **outcome status**:

  - Cases = individuals with disease/outcome
  - Controls = individuals without disease

- Look backward to assess exposures.
- **Example:** Doll & Hill (1950s) showed smoking was strongly associated with lung cancer by comparing smoking history of lung cancer patients vs. controls.
- **Strengths:** Efficient for rare diseases, multiple exposures.
- **Weaknesses:** Recall bias, cannot directly measure incidence (case–control starts with outcome, not population at risk).

### Cross-Sectional Studies

- Snapshot of exposure and outcome measured **at the same time**.
- **Example:** The CDC conducts annual telephone surveys of thousands of adults, collecting data at one point in time on smoking, alcohol use, physical activity, obesity, and chronic disease prevalence.
- **Strengths:** Quick, inexpensive, useful for prevalence estimates.
- **Weaknesses:** No temporal sequence, cannot infer causality.

### Longitudinal Studies

- Track the same participants over an extended period, collecting data at multiple time points.
- Can be **prospective** (follow forward) or **retrospective** (using past records).
- Unlike cross-sectional studies, longitudinal designs establish **temporal relationships** between exposure and outcome.

**Examples:**

- The Nurses’ Health Study (since 1976) following >100,000 women to examine diet, lifestyle, and chronic disease.
- Long-term school-based studies assessing how early-life factors affect adult outcomes.

**Strengths:**

- Can observe **changes over time** within individuals.
- Establishes temporal sequence (exposure precedes outcome).
- Useful for incidence, risk factor identification, and natural history of disease.

**Weaknesses:**

- Time- and cost-intensive.
- Attrition bias (participants dropping out).
- Requires strong data management and follow-up.

| Design | Timing | Best For |
| ------ | ------ | -------- |
| Cross-sectional | One time point | Prevalence and snapshots |
| Longitudinal | Repeated time points | Change over time and temporal order |

## Experimental Studies

Researchers intervene and randomly assign participants to groups.

### Randomized Controlled Trial (RCT)

- Participants are randomly assigned to intervention vs. control groups.
- **Example:** The _Women’s Health Initiative (WHI)_ hormone therapy trial tested estrogen/progesterone vs. placebo in postmenopausal women, showing increased breast cancer and cardiovascular risk.
- **Strengths:** Gold standard for causal inference, minimizes bias.
- **Weaknesses:** Expensive, ethical constraints, may lack generalizability.

```text
Eligible participants -> Random assignment -> Treatment / Control -> Compare outcomes
```

### Experimental Design

- Involves deliberate manipulation of one or more independent variables to measure their effect on dependent variables.
- Often includes control groups, randomization, and replication.
- **Example:** Testing different doses of a new drug on separate patient groups.
- **Strengths:** Establishes causality.
- **Weaknesses:** May be difficult or unethical in human studies.

### Explanatory Design

- Focuses on explaining the relationships or mechanisms underlying observed phenomena.
- Goes beyond description to identify causal links.
- **Example:** Examining how exercise reduces blood pressure through changes in vascular function.
- **Strengths:** Provides mechanistic insights.
- **Weaknesses:** Requires strong theoretical framework and careful control of confounding variables.

### Descriptive Design

- Aims to describe characteristics of a population or phenomenon.
- Does not test hypotheses but provides valuable baseline data.
- **Example:** Describing demographic patterns of diabetes prevalence in a region.
- **Strengths:** Useful for generating hypotheses and informing policy.
- **Weaknesses:** Cannot establish causality.

### Correlational Design

- Examines the relationship between two or more variables without manipulation.
- Determines whether variables are associated (positive, negative, or no correlation).
- **Example:** Investigating the association between physical activity and depression scores.
- **Strengths:** Identifies potential associations.
- **Weaknesses:** Correlation does not imply causation.

## Evidence Synthesis

Researchers summarize and analyze findings from multiple studies.

### Systematic Review

- Comprehensive collection and critical evaluation of all relevant studies.
- **Example:** Cochrane systematic reviews of vaccines or cancer therapies.

### Meta-Analysis

- Statistical pooling of results from multiple studies (often nested within a systematic review).
- **Example:** Meta-analysis of statin RCTs showing reduction in cardiovascular mortality.
- **Strengths:** Provides higher-level evidence, increases power.
- **Weaknesses:** Limited by quality and heterogeneity of included studies.

## Summary Table

| Category | Study type | Direction | Key feature | Example |
| ---------------------- | ---------------------- | -------------------- | ------------------------------------------ | ------------------------------------- |
| **Observational** | Cohort (prospective) | Forward | Exposure → outcome (future follow-up) | Framingham Heart Study |
|  | Cohort (retrospective) | Backward (records) | Exposure → outcome (archived data) | Hospital vaccination vs. infection |
|  | Case–control | Backward | Start with outcome, look for exposures | Doll & Hill smoking–lung cancer study |
|  | Cross-sectional | Snapshot | Exposure & outcome measured simultaneously | NHANES obesity surveys |
| **Experimental** | RCT | Forward (random) | Randomized intervention vs. control | WHI hormone therapy trial |
|  | Experimental design | Forward (controlled) | Manipulation of independent variables | Drug dose testing |
|  | Explanatory design | Forward | Explains causal mechanisms | Exercise and vascular function |
|  | Descriptive design | Snapshot | Describes population characteristics | Diabetes prevalence |
|  | Correlational design | Snapshot | Examines associations between variables | Physical activity vs. depression |
| **Evidence synthesis** | Systematic review | N/A | Critical synthesis of multiple studies | Cochrane vaccine review |
|  | Meta-analysis | N/A | Statistical pooling of study results | Statin RCT meta-analysis |

## Genetic Association and Clinical Endpoint Analysis

Beyond classical epidemiologic study designs, clinical research often requires appropriate statistical methods to evaluate genetic variants (e.g., germline SNPs) in relation to different endpoints. The following summarizes typical analysis strategies:

### Incidence (Disease Risk Analysis)

- **Control group:** Healthy individuals without cancer.
- **Methods:**

  - Chi-square test: initial comparison of SNP distribution.
  - Logistic regression: association between SNP and incidence, adjusting for demographic covariates (age, sex, etc.).
  - ROC curve: evaluate the discriminative ability of SNPs to classify cases vs. controls.

### Treatment Response Analysis

- **Variables:** Specific therapies (chemotherapy, targeted therapy, radiotherapy).
- **Methods:**

  - Chi-square test: SNP vs. binary treatment response (responder/non-responder).
  - Logistic regression: adjusted for age, sex, and stage, to assess SNP as an independent predictor.
  - ROC curve: assess predictive performance.

### Recurrence Risk Analysis

- **Required data:** Recurrence status and follow-up time → definition of Disease-Free Survival (DFS).
- **Starting time:** Surgery or treatment initiation.
- **Methods:**

  - Chi-square test: initial proportion comparison.
  - Cox regression: adjusted analysis of SNP effect on DFS.
  - Kaplan–Meier survival curve: visualize survival differences by SNP genotype.
  - ROC curve: evaluate discriminatory ability.

### Mortality Risk Analysis

- **Required data:** Survival status and follow-up time; exclude non-disease deaths.
- **Starting time:** Surgery or treatment initiation.
- **Methods:**

  - Chi-square test: crude mortality proportion comparison.
  - Cox regression: adjusted hazard ratios for SNP and overall survival (OS).
  - Kaplan–Meier survival curve: survival probability comparison by genotype.
  - ROC curve: predictive performance assessment.

## Design Choice Heuristic

Choose the simplest design that still answers the real question:

| Main challenge | Often suitable design |
| -------------- | --------------------- |
| homogeneous units, one factor | CRD |
| one major nuisance source | RCBD |
| two nuisance sources | Latin square |
| interaction between factors | factorial |
| strong between-subject variability | crossover |

Tip: More complex designs are only better when their extra structure solves a real problem.
