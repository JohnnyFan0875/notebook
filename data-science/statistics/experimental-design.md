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

## Randomization Methods

Randomization reduces **selection bias** and balances both known and unknown confounding variables across groups.

### 1. Simple Randomization

- Each participant has an equal chance of being assigned to any group.
- Easy to implement, but may cause:
  - **Uneven sample sizes** → resolved with **block randomization**.
  - **Imbalance in covariates** → resolved with **stratified randomization**.

![Image](https://www.scribbr.com/wp-content/uploads/2023/02/random-sample-vs-random-assignment.webp)

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

### 2. Block Randomization

- Ensures equal numbers across groups at **regular intervals**.
- Prevents imbalance if the study ends early or participant enrollment is staggered.

Steps:

1. Group participants into blocks.
2. Randomly assign within each block.
3. Each block maintains balanced allocation.

![Image](https://discovery.cs.illinois.edu/static/learn/Blocking-WebG.png)

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

### 3. Stratified Randomization

- Ensures equal distribution of participants based on **stratification factors** (covariates like age, gender).
- Especially important when covariates are strongly associated with outcomes.

- **Covariate:** A variable controlled for in a model, may or may not distort the true relationship.
- **Confounder:** A variable that **distorts the causal relationship** between independent and dependent variables.

![Image](https://www.scribbr.com/wp-content/uploads/2020/09/stratified-sample-7-2048x863.png)

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

### 1. Randomized Block Design

- Group similar experimental units into **blocks** (e.g., age groups).
- Randomly assign treatments within each block.
- Reduces variability due to known confounders.
- Related to stratified randomization, but applied at the design level.

### 2. Factorial Designs

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

| Method / Design          | Purpose                                  | Key Feature                     | Limitation                   |
| ------------------------ | ---------------------------------------- | ------------------------------- | ---------------------------- |
| Simple Randomization     | Random assignment                        | Easy to apply                   | May cause imbalance          |
| Block Randomization      | Balance groups at intervals              | Equal group sizes               | More complex                 |
| Stratified Randomization | Control for covariates/confounders       | Even distribution within strata | Needs stratification data    |
| Randomized Block Design  | Reduce confounder effect at design level | Blocking units                  | Limited to known confounders |
| Factorial Designs        | Study multiple factors + interactions    | Efficient exploration           | Costly if many factors       |
