# Core Concepts & Terminology

This note defines the vocabulary behind experiments: units, factors, levels, covariates, and confounding. For survival-analysis data structure and censoring concepts, use [Core Concepts & Censoring](../survival-analysis/core-concepts.md); for anomaly-detection concepts, use [Core Concepts](../../machine-learning/unsupervised-learning/anomaly-detection/core-concepts.md).

Before designing any experiment, you need a shared vocabulary. These terms define the **structure of the experiment** and determine how data is collected, organized, and analyzed.

Key point: Why learn terminology first: Many errors in experimental design come from conceptual confusion. For example, mistaking "confounding variables" for "control variables" or confusing "observation units" and "experimental units" will lead to analysis errors.

## The Core Variable Types

| Variable Type | Definition | Example (Drug Trial) |
| ------------------------- | ----------------------------------------------------------------- | --------------------------------------- |
| **Independent Variable** | The variable the researcher manipulates; the "cause" | Drug dose (0 mg, 10 mg, 20 mg) |
| **Dependent Variable** | The outcome being measured; the "effect" | Blood pressure after treatment |
| **Confounding Variable** | A variable that influences both IV and DV, distorting the effect | Patient age (affects both dose and BP) |
| **Nuisance Variable** | Affects DV but is not of interest; introduces unwanted variability | Lab technician, time of day |
| **Blocking Variable** | A nuisance variable that is controlled by design (blocking) | Hospital site in a multi-site trial |
| **Covariate** | A variable measured alongside the IV; used to reduce error | Baseline blood pressure before treatment |

Tip: Confounding vs. Nuisance: A confounding variable is dangerous because it distorts the relationship between IV and DV. A nuisance variable just adds noise but doesn't systematically bias the result. Blocking controls nuisance; randomization controls confounding. The distinction is clear and the handling is completely different.

## Experimental Units vs. Observational Units

Warning: This distinction is one of the most common sources of errors in analysis — especially for degrees of freedom and standard errors.

| Term | Definition | Example |
| ------------------------- | ------------------------------------------------------------------ | ------------------------------------------- |
| **Experimental Unit (EU)** | The smallest unit to which a treatment is **independently applied** | The patient who receives a drug |
| **Observational Unit (OU)** | The unit on which measurements are actually **taken** | A blood sample from that patient |
| **Subject** | A human experimental unit (used in behavioral/medical research) | The patient in the trial |

**When EU ≠ OU:** If you apply a treatment to one cow but measure 5 milk samples from it, your EU is the cow and your OU is the milk sample. Using n = 5 as if these are independent samples is **pseudoreplication** — a serious statistical error.

```python
# Pseudoreplication example — WRONG
# 3 cows, 5 samples each → 15 rows in dataset
# Treating n=15 as independent when n=3 (cows) is the true sample size

import pandas as pd
import numpy as np

np.random.seed(42)
data = pd.DataFrame({
    'cow_id': np.repeat([1, 2, 3], 5),           # 3 experimental units
    'treatment': np.repeat(['A', 'B', 'A'], 5),
    'milk_yield': np.random.normal(20, 2, 15)     # 5 measurements each
})

# WRONG: treating all 15 rows as independent
print(f"Wrong n: {len(data)}")   # 15

# CORRECT: aggregate to EU level first
eu_means = data.groupby('cow_id')['milk_yield'].mean().reset_index()
print(f"Correct n: {len(eu_means)}")  # 3
```

## Treatment, Factor, and Level

| Term | Definition | Example |
| ------------- | --------------------------------------------------- | --------------------------------------- |
| **Factor** | A categorical independent variable being studied | Drug type (A, B, Placebo) |
| **Level** | A specific value or category of a factor | "Drug A", "Drug B", "Placebo" |
| **Treatment** | A specific combination of factor levels applied | Drug A at 10 mg |
| **Control** | A baseline treatment — often no treatment or placebo | Placebo group |
| **Placebo** | An inert treatment that mimics the real one | Sugar pill identical in appearance |

**Single-factor vs. multi-factor experiment:**

```
Single factor:   Drug type (3 levels) → 3 treatment groups
Two factors:     Drug type (3 levels) × Dose (2 levels) → 3 × 2 = 6 treatment combinations
```

Tip: A full factorial design tests all combinations of all factor levels. This is powerful because it lets you detect interactions (where the effect of one factor depends on another). A full factorial design tests all combinations of all factor levels. This is powerful because it lets you detect interactions (where the effect of one factor depends on another).

## Experimental vs. Observational Studies

This distinction is fundamental — it determines whether you can establish **causation**.

| Feature | **Experimental Study** | **Observational Study** |
| ------------------------ | --------------------------------------------- | ---------------------------------------------- |
| Treatment assignment | Researcher assigns randomly | Subjects self-select or are observed naturally |
| Causal inference | ✅ Valid (if randomized) | ❌ Association only |
| Confounding control | ✅ Via randomization | ❌ Statistical adjustment only |
| Common in | Clinical trials, A/B testing, lab experiments | Epidemiology, surveys, retrospective studies |

**Sub-types of observational studies:**

| Type | Description | Example |
| ------------------- | -------------------------------------------------------------- | ------------------------------------------ |
| **Cross-sectional** | Single snapshot in time | Survey measuring income and health today |
| **Cohort** | Follow a group forward in time | Track smokers vs. non-smokers for 10 years |
| **Case-control** | Compare cases (outcome present) vs. controls (outcome absent) | Compare lung cancer patients vs. healthy |
| **Retrospective** | Look backward using existing records | Review hospital records from past 5 years |

Warning: The Bradford Hill Criteria provide a framework for judging whether an observed association is likely causal, even in observational studies. Key criteria include: strength of association, consistency, temporality (cause must precede effect), dose-response, and biological plausibility.

## Python: Structuring Experimental Data

A well-structured experimental dataset follows **tidy data principles**: one row per observation, one column per variable.

```python
import pandas as pd
import numpy as np

# Example: 2-factor experiment (Drug × Dose)
# Factor A: Drug type — 2 levels (DrugA, DrugB)
# Factor B: Dose — 3 levels (Low, Medium, High)
# 3 replicates per treatment combination
np.random.seed(0)

data = pd.DataFrame({
    'subject_id': range(1, 19),
    'drug':       np.repeat(['DrugA', 'DrugB'], 9),
    'dose':       np.tile(['Low', 'Medium', 'High'], 6),
    'block':      np.repeat([1, 2, 3], 6),
    'blood_pressure': np.round(
        np.random.normal(130, 10, 18), 1
    )
})

print(data.head(9))
```

**Output:**

| subject_id | drug | dose | block | blood_pressure |
| ---------- | ----- | ------ | ----- | -------------- |
| 1 | DrugA | Low | 1 | 139.7 |
| 2 | DrugA | Medium | 2 | 124.0 |
| 3 | DrugA | High | 3 | 127.2 |
| ... | ... | ... | ... | ... |

```python
# Always verify the experimental structure
print("Treatments per cell:")
print(data.groupby(['drug', 'dose']).size().unstack())

# Check for missing cells
print("\nMissing combinations:")
print(data.groupby(['drug', 'dose']).size().unstack().isnull().any())
```

Tip: Balanced vs. unbalanced designs: A balanced design has the same number of replicates in every treatment cell. Balanced designs are easier to analyze and more powerful — aim for them in the planning stage.

## Key Takeaways

| Concept | Key Point |
| ------------------------------ | --------------------------------------------------------------------------------- |
| **IV vs. Confounding** | Confounders distort effects; randomization neutralizes them |
| **EU vs. OU** | Never use OU count as your sample size if EU ≠ OU — this is pseudoreplication |
| **Factors and levels** | Identify all factors and their levels before collecting data |
| **Experimental vs. Observational** | Only experiments with randomization support causal claims |
| **Tidy data structure** | One row per observation, separate columns for each factor and the response |

# Experimental Design

Experimental design is the framework for planning studies so that results are valid, reproducible, and interpretable.
It defines how participants/subjects are allocated, how treatments are assigned, and how confounding variables are minimized.

## Key Terms

- **Randomized Controlled Trial (RCT):**
  A type of experiment where participants are randomly assigned to an experimental group or a control group. Considered the gold standard for causal inference.

- **Placebo:**
  A substance or treatment with no therapeutic effect, often used as a control to measure the true effectiveness of an intervention.

- **Blinding:**

  - **Single-blind:** Participants do not know their group assignment.
  - **Double-blind:** Both participants and researchers are unaware of group assignments (reduces bias).

- **Controlled Experiments:**
  Researchers manipulate one variable (independent) while controlling for confounders to study its effect on the dependent variable.

## Internal vs. External Validity

Experimental design always balances two goals:

| Goal | Main Question |
| ---- | ------------- |
| **Internal validity** | Did the treatment truly cause the observed effect in this study? |
| **External validity** | Will this result generalize outside the study setting? |

Tip: Tighter control usually improves internal validity, but may reduce realism.
