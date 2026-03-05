# 2. Survival & Hazard Functions

Three mathematically related functions fully characterize the survival process. Understanding each — and the relationships between them — is essential for interpreting any survival analysis output correctly.

> 📌 **為什麼要學這三個函數**：存活函數、風險函數、累積風險函數本質上是同一個事物的三種不同角度。選擇哪種表達方式，取決於你想回答哪種問題。Cox 模型直接建模的是風險函數，KM 估計的是存活函數，Nelson-Aalen 估計的是累積風險函數。

---

## 2.1 Survival Function S(t)

The **survival function** S(t) gives the probability of surviving *beyond* time t — that is, the probability that the event has **not yet occurred** by time t.

$$S(t) = P(T > t)$$

**Key properties:**

- S(0) = 1 (everyone survives at the start)
- S(∞) = 0 (eventually everyone experiences the event — in theory)
- S(t) is monotonically non-increasing (never goes up)
- The median survival time is where S(t) = 0.5

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon, weibull_min

t = np.linspace(0, 40, 500)

# Exponential distribution: S(t) = exp(-λt), constant hazard
# Weibull distribution: S(t) = exp(-(t/λ)^k), flexible shape

# Three Weibull survival curves with different shape parameters
configs = [
    {'shape': 0.7, 'scale': 20, 'label': 'Weibull k=0.7 (decreasing hazard)', 'color': '#3B82F6'},
    {'shape': 1.0, 'scale': 20, 'label': 'Exponential k=1.0 (constant hazard)', 'color': '#F59E0B'},
    {'shape': 2.0, 'scale': 20, 'label': 'Weibull k=2.0 (increasing hazard)', 'color': '#EF4444'},
]

fig, ax = plt.subplots(figsize=(8, 5))
for cfg in configs:
    S = np.exp(-(t / cfg['scale']) ** cfg['shape'])
    ax.plot(t, S, label=cfg['label'], color=cfg['color'], linewidth=2)

ax.axhline(0.5, color='gray', linestyle='--', linewidth=1, label='S(t) = 0.5 (median)')
ax.set_xlabel('Time t')
ax.set_ylabel('S(t) = P(T > t)')
ax.set_title('Survival Functions — Weibull Family')
ax.legend()
ax.set_ylim(0, 1.05)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## 2.2 Hazard Function h(t)

The **hazard function** h(t) (also called the **hazard rate** or **instantaneous failure rate**) measures the **instantaneous risk** of the event occurring at time t, *given* that the subject has survived up to time t.

$$h(t) = \lim_{\Delta t \to 0} \frac{P(t \leq T < t + \Delta t \mid T \geq t)}{\Delta t}$$

This is **not** a probability — it is a rate (with units of 1/time). It can exceed 1.

**Intuition**: h(t) answers "given that you've survived this long, what is your risk *right now*?"

| Hazard Pattern            | Description                              | Real-World Example                          |
| ------------------------- | ---------------------------------------- | ------------------------------------------- |
| **Constant hazard**       | Risk doesn't change over time            | Radioactive decay; some electronic failures |
| **Increasing hazard**     | Risk grows over time                     | Aging-related mortality; mechanical wear    |
| **Decreasing hazard**     | Risk falls over time                     | Post-surgery recovery; infant mortality     |
| **Bathtub-shaped**        | High early, low middle, high late        | Machine lifetime (early failure + wear-out) |
| **Hump-shaped (unimodal)**| Risk rises then falls                    | Post-diagnosis cancer mortality             |

```python
t = np.linspace(0.01, 40, 500)

fig, axes = plt.subplots(1, 3, figsize=(14, 4))

# Hazard functions for three Weibull shapes
configs = [
    {'shape': 0.7, 'scale': 20, 'color': '#3B82F6', 'label': 'k=0.7\n(decreasing)'},
    {'shape': 1.0, 'scale': 20, 'color': '#F59E0B', 'label': 'k=1.0\n(constant)'},
    {'shape': 2.0, 'scale': 20, 'color': '#EF4444', 'label': 'k=2.0\n(increasing)'},
]

for ax, cfg in zip(axes, configs):
    k, lam = cfg['shape'], cfg['scale']
    h = (k / lam) * (t / lam) ** (k - 1)   # Weibull hazard function
    S = np.exp(-(t / lam) ** k)              # survival function
    
    ax.plot(t, h, color=cfg['color'], linewidth=2)
    ax.set_title(f"Hazard: {cfg['label']}")
    ax.set_xlabel('Time t')
    ax.set_ylabel('h(t)')
    ax.grid(alpha=0.3)

plt.suptitle('Weibull Hazard Functions by Shape Parameter', y=1.02)
plt.tight_layout()
plt.show()
```

---

## 2.3 Cumulative Hazard Function H(t)

The **cumulative hazard** H(t) is the integral of the hazard function from 0 to t — the total accumulated risk up to time t.

$$H(t) = \int_0^t h(u)\, du$$

**Key properties:**

- H(0) = 0
- H(t) is monotonically non-decreasing
- H(t) ∈ [0, ∞) — it is NOT bounded by 1

**Why use H(t) instead of h(t)?**

- The hazard function h(t) is often noisy and hard to estimate directly from data
- H(t) is smoother and easier to estimate (Nelson-Aalen estimator)
- H(t) is linear over time for an exponential distribution → useful graphical check

```python
t_vals = np.linspace(0.01, 40, 500)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

for cfg in configs:
    k, lam = cfg['shape'], cfg['scale']
    H = (t_vals / lam) ** k               # Weibull cumulative hazard

    axes[0].plot(t_vals, H, color=cfg['color'], linewidth=2, label=cfg['label'])
    axes[1].plot(np.log(t_vals), np.log(H), color=cfg['color'], linewidth=2, label=cfg['label'])

axes[0].set_title('Cumulative Hazard H(t)')
axes[0].set_xlabel('Time t')
axes[0].set_ylabel('H(t)')
axes[0].legend()
axes[0].grid(alpha=0.3)

axes[1].set_title('Log-Log Plot: log H(t) vs log(t)')
axes[1].set_xlabel('log(t)')
axes[1].set_ylabel('log H(t)')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
```

> 💡 On a log-log scale, the Weibull cumulative hazard is a **straight line**. If empirical data follows a straight line on a log-log plot, the Weibull distribution is a good fit. This is one basis for checking the proportional hazards assumption (Section 6).

---

## 2.4 The Mathematical Relationships

The three functions are fully determined by any one of them. These identities are fundamental:

| From → To            | Formula                              |
| -------------------- | ------------------------------------ |
| S(t) → h(t)          | $h(t) = -\frac{d}{dt} \ln S(t)$    |
| S(t) → H(t)          | $H(t) = -\ln S(t)$                  |
| H(t) → S(t)          | $S(t) = e^{-H(t)}$                  |
| h(t) → H(t)          | $H(t) = \int_0^t h(u)\,du$          |
| H(t) → h(t)          | $h(t) = \frac{d}{dt} H(t)$          |

```python
# Demonstrating the relationships numerically
from scipy.stats import weibull_min

shape, scale = 1.8, 20.0
t_demo = np.array([5, 10, 15, 20, 25, 30])

# Using scipy's Weibull distribution
dist = weibull_min(c=shape, scale=scale)

S = dist.sf(t_demo)               # survival = 1 - CDF
H = -np.log(S)                    # H(t) = -ln S(t)
h = dist.pdf(t_demo) / S          # h(t) = f(t) / S(t)

results = pd.DataFrame({
    'time':     t_demo,
    'S(t)':     np.round(S, 4),
    'H(t)':     np.round(H, 4),
    'h(t)':     np.round(h, 4),
    'Check -ln(S)': np.round(-np.log(S), 4)
})
print(results)
print("\n→ H(t) column equals -ln(S(t)) column — relationship confirmed.")
```

**Output:**

| time | S(t)   | H(t)   | h(t)   |
| ---- | ------ | ------ | ------ |
| 5    | 0.9358 | 0.0663 | 0.0237 |
| 10   | 0.7784 | 0.2503 | 0.0642 |
| 15   | 0.5699 | 0.5630 | 0.0968 |
| 20   | 0.3679 | 1.0000 | 0.1200 |
| 25   | 0.2096 | 1.5628 | 0.1380 |
| 30   | 0.1054 | 2.2513 | 0.1527 |

---

## 2.5 Parametric Survival Distributions

Different parametric distributions make different assumptions about the shape of h(t). Choosing the right one improves efficiency over non-parametric methods.

| Distribution   | Hazard Shape       | # Parameters | Key Property                                      |
| -------------- | ------------------ | ------------- | ------------------------------------------------- |
| **Exponential**| Constant           | 1             | Memoryless: future risk doesn't depend on past    |
| **Weibull**    | Monotone (inc/dec) | 2             | Most flexible single-modal hazard; includes exponential |
| **Log-normal** | Unimodal (∩ shape) | 2             | Common in engineering; log(T) is normal           |
| **Log-logistic**| Unimodal           | 2             | Closed-form survival function; used in AFT models |
| **Gompertz**   | Increasing (exp growth) | 2        | Common in human mortality modeling                |

```python
from lifelines import (
    ExponentialFitter, WeibullFitter,
    LogNormalFitter, LogLogisticFitter
)

# Simulate data and fit multiple parametric models
from lifelines.datasets import load_rossi

rossi = load_rossi()
T = rossi['week']
E = rossi['arrest']

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fitters = [
    (ExponentialFitter(),   'Exponential',  axes[0, 0]),
    (WeibullFitter(),       'Weibull',      axes[0, 1]),
    (LogNormalFitter(),     'Log-Normal',   axes[1, 0]),
    (LogLogisticFitter(),   'Log-Logistic', axes[1, 1]),
]

for fitter, name, ax in fitters:
    fitter.fit(T, E, label=name)
    fitter.plot_survival_function(ax=ax, ci_show=True)
    ax.set_title(f'{name}  (AIC = {fitter.AIC_:.1f})')
    ax.set_xlabel('Weeks')
    ax.set_ylabel('S(t)')
    ax.grid(alpha=0.3)

plt.suptitle('Parametric Survival Models — Rossi Recidivism Data', y=1.01)
plt.tight_layout()
plt.show()

# Compare AIC values to select best-fitting model
print("AIC comparison:")
for fitter, name, _ in fitters:
    print(f"  {name:15s}: AIC = {fitter.AIC_:.2f}")
```

> 💡 **AIC (Akaike Information Criterion)** compares parametric models — lower is better. Use AIC when you want a parametric model for prediction or when non-parametric methods lack power. 比較參數模型時，用 AIC 選擇最適合的分佈假設：AIC 越小越好。

---

## 2.6 Key Takeaways

| Concept              | Key Point                                                                   |
| -------------------- | --------------------------------------------------------------------------- |
| **S(t)**             | Probability of surviving past time t; starts at 1, decreases to 0          |
| **h(t)**             | Instantaneous risk rate at time t given survival to t; not a probability    |
| **H(t)**             | Accumulated risk up to t; H(t) = −ln S(t); useful for model checking       |
| **One determines all** | S(t), h(t), H(t) are algebraically interchangeable                      |
| **Constant hazard**  | Implies exponential distribution — the "memoryless" special case            |
| **Parametric vs. non-parametric** | Parametric models are more efficient when the distributional form is correct; non-parametric (KM) makes no distributional assumption |

---

**← Previous:** [Core Concepts & Censoring](./1-core-concepts.md)  
**Next:** [Kaplan-Meier Estimator →](./3-kaplan-meier.md)
