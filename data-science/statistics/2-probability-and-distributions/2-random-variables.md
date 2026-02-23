# 2. Random Variables

A **random variable** is a variable whose value is determined by the outcome of a random process. Instead of describing a single outcome, it maps outcomes to numbers so we can apply mathematical tools.

> 📌 **為什麼需要隨機變數？**  
> 直接處理「事件」很麻煩，把它轉換成數字之後，我們就可以計算期望值、變異數，並套用各種分佈模型。隨機變數是機率與統計之間的橋樑。

---

## 2.1 Discrete vs Continuous Random Variables

| Type | 中文 | Definition | Example |
|------|------|-----------|---------|
| **Discrete** | 離散型 | Takes countable, separate values | Number of heads in 10 flips: {0,1,2,...,10} |
| **Continuous** | 連續型 | Takes any value in an interval | Exact height of a person: any value in [100, 250] cm |

> 💡 **Quick check**: If you can list all possible values (even if infinite, like whole numbers), it's discrete. If values fill a continuous range with no gaps, it's continuous.

---

## 2.2 Describing a Discrete Distribution: PMF

The **Probability Mass Function (PMF)** gives the probability of each specific outcome for a discrete random variable.

$$P(X = x)$$

**Properties:**
- Each probability is between 0 and 1
- All probabilities sum to exactly 1: Σ P(X = x) = 1

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom

# Example: X = number of heads in 3 fair coin flips
n, p = 3, 0.5
x_values = np.arange(0, n+1)  # {0, 1, 2, 3}
pmf_values = binom.pmf(x_values, n, p)

# Print PMF
for x, prob in zip(x_values, pmf_values):
    print(f"P(X={x}) = {prob:.4f}")

# Plot
plt.bar(x_values, pmf_values, color='steelblue', edgecolor='white', width=0.5)
plt.xlabel('Number of Heads (x)')
plt.ylabel('P(X = x)')
plt.title('PMF — Binomial(n=3, p=0.5)')
plt.xticks(x_values)
plt.show()
```

**Output:**

| x | P(X = x) |
|---|----------|
| 0 | 0.1250 |
| 1 | 0.3750 |
| 2 | 0.3750 |
| 3 | 0.1250 |

---

## 2.3 Describing a Continuous Distribution: PDF

For continuous variables, probability at any exact point is technically 0. Instead, we use the **Probability Density Function (PDF)** — the probability is the **area under the curve** over an interval.

$$P(a \leq X \leq b) = \int_a^b f(x)\, dx$$

> 💡 **直覺解釋**：連續變數無法問「P(X = 170 cm)」（因為身高 170.000...cm 的機率為 0），但可以問「P(169 ≤ X ≤ 171)」，也就是曲線下的面積。  
> Think of PDF as a "density" — the taller the curve at a point, the more probability is concentrated around there.

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

x = np.linspace(-4, 4, 300)
pdf = norm.pdf(x, loc=0, scale=1)  # Standard Normal: mean=0, sd=1

plt.plot(x, pdf, color='steelblue', linewidth=2)
plt.fill_between(x, pdf, where=(x >= -1) & (x <= 1),
                 alpha=0.3, color='steelblue', label='P(-1 ≤ X ≤ 1)')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('PDF — Standard Normal Distribution')
plt.legend()
plt.show()

# Calculate P(-1 ≤ X ≤ 1)
prob = norm.cdf(1) - norm.cdf(-1)
print(f"P(-1 ≤ X ≤ 1) = {prob:.4f}")  # ≈ 0.6827
```

---

## 2.4 Cumulative Distribution Function (CDF)

The **CDF** gives the probability that X is **less than or equal to** some value x.

$$F(x) = P(X \leq x)$$

- Works for **both** discrete and continuous variables
- Always increases from 0 to 1
- Very useful for computing interval probabilities: P(a ≤ X ≤ b) = F(b) − F(a)

```python
from scipy.stats import norm

# P(X ≤ 1.5) for Standard Normal
print(f"P(X ≤ 1.5) = {norm.cdf(1.5):.4f}")   # 0.9332

# P(0 ≤ X ≤ 1.5) using CDF difference
print(f"P(0 ≤ X ≤ 1.5) = {norm.cdf(1.5) - norm.cdf(0):.4f}")  # 0.4332

# For discrete: Binomial CDF
from scipy.stats import binom
print(f"P(X ≤ 2) for Binom(3,0.5) = {binom.cdf(2, n=3, p=0.5):.4f}")  # 0.875
```

### PMF vs PDF vs CDF at a Glance

| Function | Type | Gives You | Use It To |
|----------|------|-----------|-----------|
| **PMF** | Discrete only | P(X = x) exactly | Find probability of a specific outcome |
| **PDF** | Continuous only | Density at x (not probability itself) | Visualize distribution shape |
| **CDF** | Both | P(X ≤ x) | Find probability in a range; find percentiles |

---

## 2.5 Expected Value (期望值)

The **expected value** E(X) is the long-run average of a random variable — the "center of gravity" of its distribution.

**Discrete:**
$$E(X) = \sum_x x \cdot P(X = x)$$

**Continuous:**
$$E(X) = \int_{-\infty}^{\infty} x \cdot f(x)\, dx$$

```python
import numpy as np

# Manual calculation for discrete case
x_values = np.array([0, 1, 2, 3])
probs     = np.array([0.125, 0.375, 0.375, 0.125])  # Binom(3, 0.5)

E_X = np.sum(x_values * probs)
print(f"E(X) = {E_X:.3f}")  # 1.5

# For Normal distribution
from scipy.stats import norm
dist = norm(loc=5, scale=2)  # mean=5, sd=2
print(f"E(X) = {dist.mean():.1f}")  # 5.0
```

**Key properties of Expected Value:**

| Property | Formula | Example |
|----------|---------|---------|
| **Linearity** | E(aX + b) = a·E(X) + b | If E(X)=3, then E(2X+1) = 7 |
| **Sum of variables** | E(X + Y) = E(X) + E(Y) | Always holds, even if X, Y are dependent |
| **Product (independent)** | E(XY) = E(X)·E(Y) | Only when X and Y are independent |

---

## 2.6 Variance and Standard Deviation of a Distribution

**Variance** of a random variable measures how spread out its distribution is around the mean.

$$\text{Var}(X) = E[(X - \mu)^2] = E(X^2) - [E(X)]^2$$

$$\text{SD}(X) = \sqrt{\text{Var}(X)}$$

```python
# Manual calculation
E_X  = np.sum(x_values * probs)
E_X2 = np.sum(x_values**2 * probs)

Var_X = E_X2 - E_X**2
SD_X  = np.sqrt(Var_X)

print(f"E(X)   = {E_X:.3f}")
print(f"Var(X) = {Var_X:.3f}")
print(f"SD(X)  = {SD_X:.3f}")
```

**Key properties of Variance:**

| Property | Formula | Note |
|----------|---------|------|
| **Scale** | Var(aX) = a²·Var(X) | Variance scales by the square |
| **Shift** | Var(X + b) = Var(X) | Adding a constant doesn't change spread |
| **Sum (independent)** | Var(X + Y) = Var(X) + Var(Y) | Only when X, Y are independent |

> ⚠️ Unlike expected value, **Var(X + Y) ≠ Var(X) + Var(Y)** when X and Y are dependent. This matters in portfolio analysis, for example.

---

## 2.7 Percentiles and the Inverse CDF (Quantile Function)

The **inverse CDF** (quantile function) answers the reverse question: given a probability p, what value x satisfies P(X ≤ x) = p?

```python
from scipy.stats import norm

# What value has 95% of the distribution below it?
x_95 = norm.ppf(0.95, loc=0, scale=1)
print(f"95th percentile of Standard Normal = {x_95:.4f}")  # 1.6449

# What value has 2.5% below and 97.5% below? (used in 95% confidence intervals)
lower = norm.ppf(0.025)
upper = norm.ppf(0.975)
print(f"Middle 95% of Standard Normal: [{lower:.4f}, {upper:.4f}]")
```

> 💡 `.ppf()` stands for "Percent Point Function" — scipy's name for the inverse CDF. You'll use this constantly when computing critical values and confidence intervals in inferential statistics.  
> `.ppf()` 就是反函數 CDF，inferential statistics 中計算臨界值時會大量使用。

---

## 2.8 Key Takeaways

| Concept | Key Point |
|---------|-----------|
| **Discrete vs Continuous** | Discrete = countable values; Continuous = any value in a range |
| **PMF** | Probability at each exact value (discrete only) |
| **PDF** | Density — probability is the area under the curve (continuous only) |
| **CDF** | P(X ≤ x) — works for both; use for interval probabilities |
| **Expected Value** | Long-run average; linear operation |
| **Variance** | Spread of the distribution; scales by a² not a |
| **Inverse CDF (.ppf)** | Given a probability, find the corresponding value — essential for critical values |

---

**Next:** [Discrete Distributions →](./3-discrete-distributions.md)
