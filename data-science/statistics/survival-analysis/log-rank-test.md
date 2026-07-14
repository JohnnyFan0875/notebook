# Log-Rank Test

The **log-rank test** is the standard non-parametric hypothesis test for comparing survival curves between two or more groups. It tests whether the observed survival distributions are the same, correctly accounting for censoring.

Key point: Positioning of Log-rank test: It is a supporting hypothesis test for the KM curve, just like t-test is a tool for comparing the averages of two groups. Visually two KM curves look different, which does not mean they are statistically significantly different. The log-rank test gives a formal p-value.

## The Null Hypothesis

\[
H_0: S_1(t) = S_2(t) \text{ for all } t
\]

The null hypothesis states that the survival functions of all groups are identical at every time point. Equivalently: there is no difference in the hazard rates between groups.

## How the Test Works

The log-rank test compares **observed vs. expected events** at each event time across groups:

1. At each distinct event time $t_j$, compute how many events would be **expected** in each group if H₀ were true (proportional to each group's share of the risk set)
2. Sum up the deviations (observed − expected) over all event times
3. Compute a test statistic that follows a χ² distribution under H₀

\[
\chi^2 = \frac{\left(\sum_j (O_{1j} - E_{1j})\right)^2}{\text{Var}}
\]

Where $O_{1j}$ and $E_{1j}$ are observed and expected events in group 1 at time $t_j$.

Tip: The log-rank test gives equal weight to all event times. It is most sensitive when the hazard ratio is roughly constant across time. If hazards cross or diverge only late, weighted variants may work better.

## Two-Group Log-Rank Test in Python

### Example

```r
library(survival)

fit <- survdiff(Surv(time, status) ~ sex, data = lung)
fit
# Output: chi-square statistic and p-value
# p < 0.05 → significant difference in survival distributions
```

### Python Example

```python
from lifelines.statistics import logrank_test
from lifelines.datasets import load_rossi
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter

rossi = load_rossi()
T = rossi['week']
E = rossi['arrest']

# Split by financial aid status
T_aid    = T[rossi['fin'] == 1]
E_aid    = E[rossi['fin'] == 1]
T_no_aid = T[rossi['fin'] == 0]
E_no_aid = E[rossi['fin'] == 0]

result = logrank_test(T_aid, T_no_aid,
                      event_observed_A=E_aid,
                      event_observed_B=E_no_aid)

print(f"Log-rank test statistic: {result.test_statistic:.4f}")
print(f"p-value:                 {result.p_value:.4f}")
print(f"Degrees of freedom:      1")

if result.p_value < 0.05:
    print("\n→ Reject H₀: survival differs significantly between groups (α=0.05)")
else:
    print("\n→ Fail to reject H₀: no significant difference detected (α=0.05)")
```

### Visualizing the Result

```python
fig, ax = plt.subplots(figsize=(9, 5))

for group, color, label in [(1, '#3B82F6', 'Received Aid'), (0, '#EF4444', 'No Aid')]:
    mask = rossi['fin'] == group
    kmf = KaplanMeierFitter()
    kmf.fit(T[mask], E[mask], label=label)
    kmf.plot_survival_function(ax=ax, ci_show=True, color=color)

ax.set_xlabel('Weeks')
ax.set_ylabel('S(t)')
ax.set_title(
    f'KM Curves by Financial Aid Status\n'
    f'Log-rank p = {result.p_value:.4f}'
)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

## Multi-Group Log-Rank Test

When comparing three or more groups, the log-rank test generalizes to a χ² statistic with (k−1) degrees of freedom.

```python
from lifelines.statistics import multivariate_logrank_test

# Compare survival across different age groups (prio = number of prior convictions)
# Bin prior convictions into 3 groups
rossi['prio_group'] = pd.cut(rossi['prio'],
                              bins=[-1, 0, 3, 20],
                              labels=['None', 'Low (1–3)', 'High (4+)'])

result_multi = multivariate_logrank_test(
    event_durations=T,
    groups=rossi['prio_group'],
    event_observed=E
)

print(f"Multivariate log-rank test")
print(f"Test statistic: {result_multi.test_statistic:.4f}")
print(f"p-value:        {result_multi.p_value:.4f}")
print(f"Degrees of freedom: {result_multi.degrees_of_freedom}")

# Plot all three groups
fig, ax = plt.subplots(figsize=(9, 5))
colors = ['#3B82F6', '#F59E0B', '#EF4444']

for group, color in zip(['None', 'Low (1–3)', 'High (4+)'], colors):
    mask = rossi['prio_group'] == group
    kmf = KaplanMeierFitter()
    kmf.fit(T[mask], E[mask], label=group)
    kmf.plot_survival_function(ax=ax, color=color, ci_show=False)

ax.set_title(
    f'KM Curves by Prior Conviction Count\n'
    f'Log-rank p = {result_multi.p_value:.4f}'
)
ax.set_xlabel('Weeks')
ax.set_ylabel('S(t)')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

Warning: A significant multivariate log-rank result only tells you that at least one group differs. It does not tell you *which* groups differ from each other. Use pairwise log-rank tests with Bonferroni or Holm correction for post-hoc comparisons. Post hoc comparisons required correction for multiple assays.

```python
from itertools import combinations
from scipy.stats import chi2

groups_list = ['None', 'Low (1–3)', 'High (4+)']
n_comparisons = len(list(combinations(groups_list, 2)))

print(f"\nPairwise log-rank tests (Bonferroni α = {0.05/n_comparisons:.4f}):")
for g1, g2 in combinations(groups_list, 2):
    m1 = rossi['prio_group'] == g1
    m2 = rossi['prio_group'] == g2
    r = logrank_test(T[m1], T[m2], event_observed_A=E[m1], event_observed_B=E[m2])
    sig = '✅' if r.p_value < 0.05/n_comparisons else '  '
    print(f"  {g1:12s} vs {g2:12s}: p = {r.p_value:.4f} {sig}")
```

## Weighted Log-Rank Variants

The standard log-rank test weights all event times equally. Alternative weights emphasize different parts of the survival curve:

| Variant | Weights at time $t_j$ | Most Sensitive To |
| ---------------------- | ---------------------------------- | ---------------------------------------- |
| **Log-rank (standard)** | 1 | Constant hazard ratio; late differences |
| **Gehan-Breslow** | $n_j$ (risk set size) | Early differences; common in medical use |
| **Tarone-Ware** | $\sqrt{n_j}$ | Balance of early and late |
| **Peto-Peto** | $\hat{S}(t_j)$ | More robust to late censoring |

```python
from lifelines.statistics import logrank_test

# Gehan-Breslow-Wilcoxon (emphasizes early differences)
result_gbw = logrank_test(
    T_aid, T_no_aid,
    event_observed_A=E_aid,
    event_observed_B=E_no_aid,
    weightings='wilcoxon'       # Gehan-Breslow weighting
)

result_tw = logrank_test(
    T_aid, T_no_aid,
    event_observed_A=E_aid,
    event_observed_B=E_no_aid,
    weightings='tarone-ware'
)

print("Standard log-rank:    p =", f"{result.p_value:.4f}")
print("Gehan-Breslow-Wilcoxon: p =", f"{result_gbw.p_value:.4f}")
print("Tarone-Ware:          p =", f"{result_tw.p_value:.4f}")
```

Tip: When to choose which weight: If you expect the treatment to act early (e.g., a vaccine preventing infection in the first few weeks), use Gehan-Breslow. If effects are expected late (long-term treatment benefits), stick with standard log-rank. Pre-specify your choice before looking at the data — choosing after the fact inflates false positives. Which weighting method to choose should be decided before looking at the data. Choosing the method that minimizes the p-value after the fact is a form of p-hacking.

## Limitations of the Log-Rank Test

| Limitation | Description | Alternative |
| ---------------------------------------- | -------------------------------------------------------------------- | ------------------------------------ |
| **Cannot adjust for covariates** | Only compares groups; cannot control for confounders | Cox proportional hazards model |
| **Loses power with crossing curves** | If one group has better early and the other better late survival | RMST difference, weighted log-rank |
| **Assumes proportional hazards** | Most powerful when hazard ratio is constant over time | Cox model + PH check; stratified Cox |
| **Only tests equality, not magnitude** | p < 0.05 says groups differ, not by how much | Hazard ratio from Cox model |
| **Sensitive to late censoring** | Very heavy censoring at later time points can distort the test | Restrict analysis horizon; RMST |

Warning: The log-rank test answers only "are these groups different?" — not "how different?" and not "why?". For effect quantification and covariate adjustment, move to a Cox model.

## Key Takeaways

| Concept | Key Point |
| ------------------------- | ---------------------------------------------------------------------------- |
| **H₀** | Survival functions are identical across groups for all t |
| **Equal weighting** | Log-rank weights all event times equally → best power under proportional hazards |
| **Multi-group** | (k−1) df; significant result only says "at least one group differs" |
| **Pairwise tests** | Bonferroni correction needed for post-hoc group comparisons |
| **Weighted variants** | Choose weights based on where you expect the difference to appear — pre-specify |
| **No covariate adjustment** | Use Cox model when confounders need to be controlled |

## What the Log-Rank Test Is Most Sensitive To

The standard log-rank test is strongest when group differences are fairly consistent over time. If hazards cross or one group is only better early or late, the single global test can miss important structure.

Tip: When curves cross, report the plot prominently and consider RMST or weighted alternatives.
