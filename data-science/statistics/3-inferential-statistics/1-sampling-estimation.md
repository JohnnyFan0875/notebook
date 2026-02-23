# 1. Sampling & Estimation

Before testing any hypothesis, you need to understand **where your data comes from** and **what it can tell you about the broader population**. This section covers how samples relate to populations, and how we use sample statistics to estimate unknown population parameters.

> 📌 **為什麼這一步最重要**：所有推論統計的前提，是你的樣本能代表母體。如果取樣方式有偏差，後續所有分析都會出問題。

---

## 1.1 Population vs. Sample

| Term                       | 中文   | Definition                                                          | Example                                  |
| -------------------------- | ------ | ------------------------------------------------------------------- | ---------------------------------------- |
| **Population (母體)**      | 母體   | The entire group you want to draw conclusions about                 | All adults in Taiwan                     |
| **Sample (樣本)**          | 樣本   | A subset of the population actually observed                        | 1,000 adults surveyed in Taipei          |
| **Parameter (參數)**       | 參數   | A numerical summary of the population (usually unknown)             | True population mean income μ            |
| **Statistic (統計量)**     | 統計量 | A numerical summary computed from the sample                        | Sample mean income x̄                    |
| **Sampling error (抽樣誤差)** | 抽樣誤差 | The difference between a sample statistic and the true parameter | x̄ ≠ μ simply because we didn't survey everyone |

> 💡 We use **Roman letters** (x̄, s, p̂) for sample statistics and **Greek letters** (μ, σ, π) for population parameters. This distinction matters for formulas and interpretation.

---

## 1.2 Sampling Methods

| Method                       | 中文         | Description                                                          | Pros / Cons                                               |
| ---------------------------- | ------------ | -------------------------------------------------------------------- | --------------------------------------------------------- |
| **Simple random sampling**   | 簡單隨機抽樣 | Every individual has an equal probability of being selected          | ✅ Unbiased; ❌ Expensive if population is large/dispersed |
| **Stratified sampling**      | 分層抽樣     | Divide into subgroups (strata), then randomly sample within each     | ✅ Ensures representation of subgroups; ❌ Requires strata info |
| **Cluster sampling**         | 集群抽樣     | Randomly select whole clusters (e.g., schools), then sample within   | ✅ Cheaper for geographically spread populations; ❌ Higher variance |
| **Systematic sampling**      | 系統抽樣     | Select every k-th individual from a list                             | ✅ Easy to implement; ❌ Periodic pattern can introduce bias |
| **Convenience sampling**     | 便利抽樣     | Select whoever is easily accessible                                  | ✅ Fast and cheap; ❌ High risk of selection bias — avoid for inference |

> ⚠️ **Bias vs. Variance tradeoff in sampling**: Random methods minimize bias (systematic error) but may have high variance (noise). Non-random methods are fast but introduce bias that no amount of analysis can fix.

---

## 1.3 Point Estimation

A **point estimate** is a single-value guess for a population parameter, calculated from the sample.

| Population Parameter | Symbol | Point Estimate       | Symbol |
| -------------------- | ------ | -------------------- | ------ |
| Population mean      | μ      | Sample mean          | x̄     |
| Population variance  | σ²     | Sample variance      | s²     |
| Population SD        | σ      | Sample SD            | s      |
| Population proportion| π      | Sample proportion    | p̂     |

**Key limitation**: A point estimate is almost certainly not exactly equal to the true parameter. To communicate this uncertainty, we use **confidence intervals** (Section 2).

```python
import pandas as pd
import numpy as np
from sklearn.datasets import load_iris

df = load_iris(as_frame=True).frame

# Point estimates for sepal length
n       = df['sepal length (cm)'].count()
x_bar   = df['sepal length (cm)'].mean()
s       = df['sepal length (cm)'].std(ddof=1)   # sample SD (ddof=1)
s_sq    = df['sepal length (cm)'].var(ddof=1)   # sample variance

print(f"n     = {n}")
print(f"x̄    = {x_bar:.4f}")
print(f"s     = {s:.4f}")
print(f"s²    = {s_sq:.4f}")
```

> 💡 **Why `ddof=1`?** The sample variance uses n−1 in the denominator (not n) to produce an **unbiased estimate** of σ². This correction is called Bessel's correction. Pandas' default for `.var()` and `.std()` is already `ddof=1`.

---

## 1.4 The Central Limit Theorem (CLT)

The **Central Limit Theorem** is the theoretical backbone of inferential statistics.

> **CLT Statement**: If you draw many random samples of size n from *any* population with mean μ and finite variance σ², the distribution of sample means (x̄) will approach a **Normal distribution** as n increases, regardless of the shape of the original population.

$$\bar{x} \sim N\left(\mu,\ \frac{\sigma^2}{n}\right) \quad \text{as } n \to \infty$$

| Condition                  | Practical Rule of Thumb                                          |
| -------------------------- | ---------------------------------------------------------------- |
| Population is normal       | CLT holds for any n                                              |
| Population is mildly skewed| n ≥ 30 is usually sufficient                                     |
| Population is heavily skewed | n ≥ 100 or more may be needed                                  |

**What CLT enables:**
- We can use z-tests and t-tests even when the original population isn't normal
- The Normal distribution becomes our tool for computing probabilities about sample means

```python
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# Simulate CLT: sample means from a right-skewed (exponential) population
population = np.random.exponential(scale=2, size=100_000)
sample_means = [np.mean(np.random.choice(population, size=30)) for _ in range(5000)]

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].hist(population, bins=80, color='steelblue', edgecolor='white')
axes[0].set_title('Original Population (Exponential — Skewed)')
axes[0].set_xlabel('Value')

axes[1].hist(sample_means, bins=60, color='coral', edgecolor='white')
axes[1].set_title('Distribution of Sample Means (n=30)\n→ Approximately Normal (CLT)')
axes[1].set_xlabel('Sample Mean')

plt.tight_layout()
plt.show()
```

---

## 1.5 Standard Error (SE)

**Standard Error** measures how much the sample statistic (e.g., x̄) varies from sample to sample. It is the **standard deviation of the sampling distribution**.

$$SE_{\bar{x}} = \frac{s}{\sqrt{n}}$$

| n (sample size) | SE behavior         | Implication                                     |
| --------------- | ------------------- | ----------------------------------------------- |
| Small           | Large SE            | Estimates are imprecise; wide confidence interval|
| Large           | Small SE            | Estimates are precise; narrow confidence interval|

```python
se = s / np.sqrt(n)
print(f"Standard Error (SE) = {se:.4f}")
```

> 💡 **SE vs. SD**: Standard Deviation (s) describes how spread out individual observations are. Standard Error (SE) describes how spread out *sample means* are. As n increases, SE decreases — SD does not change much.

| Statistic           | What it describes                          | Changes with n? |
| ------------------- | ------------------------------------------ | --------------- |
| **SD (s)**          | Spread of individual data points           | Not much        |
| **SE (s/√n)**       | Spread of sample means across many samples | Yes — decreases as n grows |

---

## 1.6 Key Takeaways

| Principle                       | Details                                                                            |
| ------------------------------- | ---------------------------------------------------------------------------------- |
| **Sample ≠ Population**         | Statistics from samples always contain sampling error                              |
| **Sampling method matters**     | Non-random samples introduce bias that invalidates inference                       |
| **CLT is foundational**         | Enables use of Normal-based tests even when the population is non-normal           |
| **SE quantifies precision**     | Larger n → smaller SE → more precise estimates                                     |
| **Point estimates need context**| Always accompany point estimates with confidence intervals (Section 2)             |

---

**Next:** [Confidence Intervals →](./2-confidence-intervals.md)
