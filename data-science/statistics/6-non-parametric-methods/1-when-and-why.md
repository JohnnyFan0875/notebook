# 1. What are non-parametric tests?

Non-parametric tests are used when data do **not meet the assumptions** of parametric tests (e.g., normality, homogeneity of variance).  
They are based on **ranks** instead of raw values, making them more robust for skewed distributions, ordinal data, or small samples.

---

# 1. When & Why Non-parametric Methods

The first and most important step is deciding **whether you actually need** a non-parametric method. This section gives you a systematic way to make that decision.

> 📌 **核心問題**：We don't use non-parametric methods because they are "safer" — we use them because the data doesn't meet the requirements of parametric methods. Choosing non-parametric methods unnecessarily wastes statistical power.

---

## 1.1 What Are the Assumptions of Common Parametric Tests?

| Parametric Test           | Key Assumptions                                                                 |
| ------------------------- | ------------------------------------------------------------------------------- |
| **One-sample t-test**     | Data is normally distributed (or n is large enough for CLT)                     |
| **Independent t-test**    | Normality in each group; equal variance (homoscedasticity)                      |
| **Paired t-test**         | The *differences* between pairs are normally distributed                        |
| **One-way ANOVA**         | Normality in each group; equal variance across groups                           |
| **Pearson correlation**   | Both variables are continuous and normally distributed; linear relationship      |

> 💡 **Central Limit Theorem (CLT)**: When n ≥ 30, the sampling distribution of the mean is approximately normal regardless of the original distribution. This means parametric tests become more robust with larger samples.  
> 中央極限定理：當樣本數夠大（n ≥ 30），即使原始資料不是常態分佈，樣本平均數的抽樣分佈仍會趨近常態。

---

## 1.2 Checking Normality

### Step 1: Visual Checks

Always start with visuals — they give intuition that formal tests can miss.

**Histogram + KDE:**
```python
import seaborn as sns
import matplotlib.pyplot as plt

sns.histplot(data, kde=True, color='steelblue')
plt.title('Distribution Check')
plt.show()
```

**Q–Q Plot:**
```python
import scipy.stats as stats
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
stats.probplot(data, dist="norm", plot=ax)
ax.set_title('Q–Q Plot')
plt.show()
```

| Q–Q Plot Pattern                  | Interpretation                  |
| --------------------------------- | ------------------------------- |
| Points fall along the diagonal    | Approximately normal ✅         |
| S-shaped curve                    | Skewed distribution ⚠️          |
| Points bow at both ends           | Heavy tails (leptokurtic) ⚠️    |
| Single extreme outlier at one end | Outlier present ⚠️              |

---

### Step 2: Formal Normality Tests

Formal tests are hypothesis tests where:
- **H₀**: The data follows a normal distribution
- **H₁**: The data does not follow a normal distribution

```python
from scipy import stats
import numpy as np

data = np.array([...])  # your data here

# Shapiro-Wilk — best for small samples (n < 50)
stat, p = stats.shapiro(data)
print(f"Shapiro-Wilk: W = {stat:.4f}, p = {p:.4f}")

# Kolmogorov-Smirnov — for larger samples; requires estimated parameters
stat, p = stats.kstest(data, 'norm', args=(data.mean(), data.std()))
print(f"KS Test: D = {stat:.4f}, p = {p:.4f}")

# D'Agostino-Pearson — uses skewness and kurtosis
stat, p = stats.normaltest(data)
print(f"D'Agostino K²: stat = {stat:.4f}, p = {p:.4f}")
```

| Test                    | Best For               | Limitations                                            |
| ----------------------- | ---------------------- | ------------------------------------------------------ |
| **Shapiro-Wilk**        | n < 50 (small samples) | Less reliable for n > 2000                             |
| **Kolmogorov-Smirnov**  | n > 50                 | Less powerful; sensitive to parameter estimation       |
| **D'Agostino-Pearson**  | General use            | Needs n ≥ 20                                           |

> ⚠️ **Critical warning about normality tests**: With large samples (n > 200), even trivial, practically irrelevant deviations from normality will produce a significant p-value (reject H₀). With small samples (n < 15), tests have low power to detect real non-normality. Always interpret together with visual inspection.  
> 大樣本時，幾乎任何資料都會被判定為非常態；小樣本時，檢定沒有足夠力量。正式檢定的結果必須搭配視覺判斷。

---

## 1.3 Other Assumptions to Check

### Equal Variance (Homoscedasticity 同質變異數)

For tests comparing two or more groups:

```python
# Levene's Test — robust to non-normality
stat, p = stats.levene(group1, group2)
print(f"Levene's Test: stat = {stat:.4f}, p = {p:.4f}")

# Bartlett's Test — assumes normality; more powerful when data is normal
stat, p = stats.bartlett(group1, group2)
print(f"Bartlett's Test: stat = {stat:.4f}, p = {p:.4f}")
```

If p < 0.05 → variances are unequal → consider Welch's t-test (parametric but robust) or a non-parametric alternative.

---

### Outlier Detection

```python
import numpy as np

# Z-score method
z_scores = np.abs(stats.zscore(data))
outliers_z = np.where(z_scores > 3)[0]
print(f"Outliers (Z > 3): indices {outliers_z}")

# IQR method
Q1 = np.percentile(data, 25)
Q3 = np.percentile(data, 75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
outliers_iqr = data[(data < lower) | (data > upper)]
print(f"Outliers (IQR method): {outliers_iqr}")
```

---

## 1.4 Decision Flowchart

```
Is the data ordinal (e.g., Likert scale)?
        │
        ├─── YES → Use non-parametric method
        │
        └─── NO (data is continuous)
                  │
                  Is n < 30?
                  │
                  ├─── YES → Check normality carefully (Shapiro-Wilk + Q-Q plot)
                  │           │
                  │           ├─── Approx. normal → Parametric OK
                  │           └─── Non-normal → Non-parametric
                  │
                  └─── NO (n ≥ 30)
                            │
                            Are there severe outliers?
                            │
                            ├─── YES → Non-parametric more appropriate
                            └─── NO → Parametric OK (CLT applies)
```

---

## 1.5 The Cost of Choosing Non-parametric: Statistical Power

**Statistical power** is the probability of correctly detecting a true effect (i.e., rejecting H₀ when it is false).

| Situation                                          | Power Trade-off                                                  |
| -------------------------------------------------- | ---------------------------------------------------------------- |
| Data is truly normal; using non-parametric anyway  | Power loss ~5–15% — you need a larger sample for same detection  |
| Data is non-normal; using parametric               | Results may be invalid (inflated Type I error)                   |
| Data is ordinal; using parametric                  | Assumptions violated; conclusions unreliable                     |

> 💡 **The takeaway**: Use parametric tests when assumptions are met — they are more powerful. Switch to non-parametric only when needed.  
> 假設成立時，參數方法更有效率。Non-parametric 是必要時的正確選擇，不是保守的預設選項。

---

## 1.6 Key Takeaways

| Principle                         | Details                                                                          |
| --------------------------------- | -------------------------------------------------------------------------------- |
| **Check assumptions first**       | Always verify normality, equal variance, and outliers before choosing a test     |
| **Visual + formal**               | Combine Q–Q plots with Shapiro-Wilk; never rely on a single check                |
| **n matters**                     | Normality tests are unreliable at very small or very large n — use judgment      |
| **Power cost**                    | Non-parametric methods are less powerful; avoid using them unnecessarily         |
| **Ordinal data → non-parametric** | Ordinal variables should never be analyzed with parametric means and SD          |

---
