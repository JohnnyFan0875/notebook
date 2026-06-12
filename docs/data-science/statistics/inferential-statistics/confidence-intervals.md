# Confidence Intervals

A **confidence interval (CI)** provides a range of plausible values for a population parameter, based on sample data. Instead of just saying "our estimate is 5.84 cm," a CI says "we're 95% confident the true value is between 5.71 and 5.97 cm." This communicates both the estimate _and_ the uncertainty.

Key point: Why confidence intervals are more useful than p-values: Confidence intervals tell you both the "size" and "precision" of an effect, while p-value only tells you whether the effect is significant. Modern statistics places increasing emphasis on reporting confidence intervals rather than just p-values.

## The Concept: What Does "95% Confident" Mean?

This is one of the most commonly misunderstood ideas in statistics.

Why CIs work — the CLT connection: When we repeatedly draw samples of size n, the sample means $\bar{x}$ follow an approximately normal distribution (by the Central Limit Theorem). The CI is built from this sampling distribution — it marks the range where the center of that distribution plausibly lies.

Correct interpretation: If we repeated the sampling process many times and constructed a CI each time, 95% of those intervals would contain the true population parameter.

Warning: Incorrect interpretations (very common): - ❌ "There is a 95% probability that μ is in this specific interval." - ❌ "95% of the data falls within this interval." - ❌ "This interval will contain μ 95% of the time." The parameter μ is a fixed (unknown) value — it either is or isn't in any given interval. The probability refers to the _procedure_, not the specific interval.

Two analogies for the same idea:

- 🎣 **Fishing net**: cast 100 times into a lake — 95 casts catch the fish (μ). Any single cast either catches it or not.
- 🎯 **Archery**: shoot 100 arrows, each time drawing a ring around where the arrow lands. 95 rings contain the bullseye — but any single ring either covers it or doesn't.

## Confidence Interval for a Mean

### When σ is known — z-interval (rare in practice)

\[
CI = \bar{x} \pm z_{\alpha/2} \cdot \frac{\sigma}{\sqrt{n}}
\]

### When σ is unknown — t-interval (standard case)

\[
CI = \bar{x} \pm t_{\alpha/2,\, n-1} \cdot \frac{s}{\sqrt{n}}
\]

| Component | Meaning |
| --------------- | -------------------------------------------------------------- |
| x̄ | Sample mean (point estimate) |
| t\_{α/2, n−1} | Critical value from t-distribution with n−1 degrees of freedom |
| s / √n | Standard error (SE) |
| Margin of Error | t \* SE — the ± half-width of the interval |

**Margin of Error (E)** — the maximum expected distance between the sample mean and the true parameter:

\[
E = \begin{cases} z_{\alpha/2} \times \dfrac{\sigma}{\sqrt{n}} & \text{if } \sigma \text{ is known} \\ t_{\alpha/2,\,n-1} \times \dfrac{s}{\sqrt{n}} & \text{if } \sigma \text{ is unknown} \end{cases}
\]

So the interval is simply: $\text{CI} = \bar{x} \pm E$

**Common critical values (z) for reference:**

| Confidence Level | α | z\_{α/2} |
| ---------------- | ---- | -------- |
| 90% | 0.10 | 1.645 |
| 95% | 0.05 | 1.960 |
| 99% | 0.01 | 2.576 |

Tip: Use z when n is large (n > 30) and σ is known or well estimated. In practice, using t from `scipy` is usually safer because it converges to z as n grows. A full comparison appears later in this page.

```python
import numpy as np
import scipy.stats as stats
from sklearn.datasets import load_iris

df = load_iris(as_frame=True).frame
x = df['sepal length (cm)']

n      = len(x)
x_bar  = x.mean()
s      = x.std(ddof=1)
se     = s / np.sqrt(n)

# 95% CI using t-distribution
alpha  = 0.05
t_crit = stats.t.ppf(1 - alpha / 2, df=n - 1)
margin = t_crit * se

ci_lower = x_bar - margin
ci_upper = x_bar + margin

print(f"Sample mean:     {x_bar:.4f}")
print(f"Standard error:  {se:.4f}")
print(f"t critical value:{t_crit:.4f}")
print(f"Margin of error: {margin:.4f}")
print(f"95% CI:         ({ci_lower:.4f}, {ci_upper:.4f})")

# One-liner using scipy
ci = stats.t.interval(confidence=0.95, df=n-1, loc=x_bar, scale=se)
print(f"95% CI (scipy):  ({ci[0]:.4f}, {ci[1]:.4f})")
```

**Simulation: visualizing the CI procedure** — showing that 95% of repeated intervals capture μ:

```python
import numpy as np

# Simulate sampling from a known population to see the CI procedure in action
np.random.seed(42)
population = np.random.normal(loc=100, scale=15, size=10_000)

sample_size = 50
n_samples = 1000

sample_means = [np.mean(np.random.choice(population, size=sample_size, replace=False))
                for _ in range(n_samples)]
sample_means = np.array(sample_means)

# The middle 95% of sample means — illustrates the sampling distribution
lower = np.percentile(sample_means, 2.5)
upper = np.percentile(sample_means, 97.5)

print(f"Mean of sampling distribution: {sample_means.mean():.2f}  (≈ true μ = 100)")
print(f"95% range of sample means:     ({lower:.2f}, {upper:.2f})")
print(f"This is the sampling distribution basis for CI construction")
```

Tip: This simulation shows _why_ CIs work: the sampling distribution of x̄ is approximately normal (CLT), so the interval $\bar{x} \pm t \cdot SE$ reliably brackets μ across repeated samples.

## Confidence Interval for a Proportion

When the variable of interest is categorical (e.g., proportion of users who clicked), use the **proportion CI**.

\[
CI = \hat{p} \pm z_{\alpha/2} \cdot \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}
\]

**Valid when**: n·p̂ ≥ 10 and n·(1−p̂) ≥ 10 (Normal approximation holds)

```python
from statsmodels.stats.proportion import proportion_confint

# Example: 82 out of 150 customers clicked an email
successes = 82
n = 150

# Wilson method — more accurate than Normal approximation for small n or extreme p
ci_lower, ci_upper = proportion_confint(count=successes, nobs=n, alpha=0.05, method='wilson')
p_hat = successes / n

print(f"Sample proportion p̂ = {p_hat:.4f}")
print(f"95% CI (Wilson):     ({ci_lower:.4f}, {ci_upper:.4f})")
```

Tip: Which method to use for proportion CIs? | Method | When to Use | | --------------- | ------------------------------------------------------ | | Normal (Wald) | Large n, p̂ not too close to 0 or 1 | | Wilson | Recommended default — works well for all n and p̂ | | Clopper-Pearson | Exact method — conservative; good when n is very small |

## Factors Affecting Interval Width

| Factor | Change | Effect on CI width | Intuition |
| -------------------- | ------------- | ------------------ | ------------------------------------------------ |
| **Sample size (n)** | ↑ Increase | ↓ Narrower | More data → more precise estimates |
| **Confidence level** | ↑ e.g. 95→99% | ↑ Wider | Higher certainty requires a wider net |
| **Variability (s)** | ↑ More spread | ↑ Wider | More variable data → harder to pin down the mean |

```python
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

# Show how CI width changes with sample size
np.random.seed(42)
population_mean = 5.84
population_std  = 0.83
sample_sizes    = [10, 30, 50, 100, 200, 500]

ci_widths = []
for n in sample_sizes:
    se    = population_std / np.sqrt(n)
    t_crit = stats.t.ppf(0.975, df=n-1)
    ci_widths.append(2 * t_crit * se)

plt.plot(sample_sizes, ci_widths, marker='o', color='steelblue')
plt.xlabel('Sample Size (n)')
plt.ylabel('95% CI Width')
plt.title('CI Width Decreases as Sample Size Increases')
plt.grid(True, alpha=0.3)
plt.show()
```

## Confidence Intervals vs. p-values

Both are derived from the same calculation, but they convey different things:

| Aspect | p-value | Confidence Interval |
| ----------------- | ---------------------------------------- | ----------------------------------------------- |
| **Answers** | Is the effect statistically significant? | What is the plausible range of the effect size? |
| **Tells you** | Binary: significant or not | Magnitude + direction + precision |
| **Practical use** | Decision: reject H₀ or not | Interpretation: is the effect meaningful? |
| **Relation** | p < 0.05 ↔ 95% CI excludes H₀ value | They are mathematically equivalent |

Tip: Modern best practice: Report both. A p-value tells you whether to reject H₀; a CI tells you what the effect actually looks like. A "statistically significant" result with a CI of [0.001, 0.003] may be practically irrelevant.

## A Common Misread: CI Overlap Between Groups

People often compare two group means by eye and conclude:

- "The intervals overlap, so there is no difference."
- "The intervals do not overlap, so the difference must be significant."

Both shortcuts are unreliable.

Why? Because significance of the **difference** depends on the sampling distribution of the contrast `(mean_1 - mean_2)`, not just on whether two separately computed intervals overlap.

```python
import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns

tips = sns.load_dataset("tips").dropna(subset=["total_bill", "day"])

summary = (
    tips.groupby("day")["total_bill"]
    .agg(["mean", "std", "count"])
    .assign(
        se=lambda d: d["std"] / np.sqrt(d["count"]),
        tcrit=lambda d: stats.t.ppf(0.975, d["count"] - 1),
    )
)
summary["ci_low"] = summary["mean"] - summary["tcrit"] * summary["se"]
summary["ci_high"] = summary["mean"] + summary["tcrit"] * summary["se"]

print(summary[["mean", "ci_low", "ci_high"]].round(2))
```

Tip: Use CIs to communicate effect size and uncertainty, but do not use simple overlap as a substitute for the correct inferential comparison.

## Visualization: Plotting Confidence Intervals

```python
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from sklearn.datasets import load_iris

iris = load_iris(as_frame=True)
df = iris.frame
df['species'] = iris.target_names[iris.target]

# Compute mean and 95% CI per species
results = {}
for species, group in df.groupby('species'):
    x = group['sepal length (cm)']
    n = len(x)
    mean = x.mean()
    se = x.std(ddof=1) / np.sqrt(n)
    t_crit = stats.t.ppf(0.975, df=n-1)
    results[species] = (mean, t_crit * se)

species_names = list(results.keys())
means  = [results[s][0] for s in species_names]
errors = [results[s][1] for s in species_names]

plt.figure(figsize=(7, 4))
plt.errorbar(species_names, means, yerr=errors, fmt='o', capsize=6,
             color='steelblue', markersize=8, linewidth=2)
plt.ylabel('Sepal Length (cm)')
plt.title('Mean Sepal Length with 95% Confidence Intervals by Species')
plt.grid(axis='y', alpha=0.3)
plt.show()
```

## t-score and z-score

The CI formula $\bar{x} \pm \text{critical value} \times SE$ requires a critical value — either a **z** or **t**. Both measure the same thing: how many standard errors the sample mean is from the target value μ.

Key point: Core: z and t have the same structure, the only difference is in the denominator - z uses the known parent standard deviation σ, and t uses the sample estimated s.

### Formulas

|  | z-score | t-score |
| ---------------- | ---------------------------------------------- | ----------------------------------------- |
| **Formula** | $z = \dfrac{\bar{x} - \mu}{\sigma / \sqrt{n}}$ | $t = \dfrac{\bar{x} - \mu}{s / \sqrt{n}}$ |
| **Denominator** | Population SD σ (known) | Sample SD s (estimated) |
| **Distribution** | Standard normal | t-distribution (heavier tails) |
| **Use when** | n ≥ 30 and σ known | σ unknown — the typical case |

As $n \to \infty$, the t-distribution converges to the normal distribution, so t and z become interchangeable for large samples.

Tip: Default: always use t. σ is almost never known in practice, and t converges to z automatically as n grows.

### Getting Critical Values

**Two-tailed** (standard for CIs):

```python
from scipy import stats

alpha = 0.05
z_crit = stats.norm.ppf(1 - alpha / 2)      # ±1.96
t_crit = stats.t.ppf(1 - alpha / 2, df=n-1) # slightly wider than z for small n
```

Common reference values for $z_{\alpha/2}$:

| Confidence Level | α | $z_{\alpha/2}$ |
| ---------------- | ---- | -------------- |
| 90% | 0.10 | 1.645 |
| 95% | 0.05 | 1.960 |
| 99% | 0.01 | 2.576 |

**One-tailed** (used in hypothesis testing, not CIs):

```python
z_right = stats.norm.ppf(1 - alpha)  # right-tailed: +1.645
z_left  = stats.norm.ppf(alpha)      # left-tailed:  −1.645
```

👉 One-tailed tests are covered in [Null and Alternative Hypotheses](./hypothesis-testing.md#null-and-alternative-hypotheses).

## Key Takeaways

| Concept | Key Point |
| ------------------------------- | ----------------------------------------------------------------------------------------- |
| **CI = estimate + uncertainty** | Always pair a point estimate with its interval — never report one without the other |
| **Correct interpretation** | The procedure captures μ 95% of the time — not a probability about this specific interval |
| **t vs. z** | Use t in practice; it converges to z for large n and is always safer |
| **Width trade-offs** | Larger n or lower confidence = narrower CI |
| **CI vs. p-value** | Equivalent mathematically; CI gives more information about practical significance |
