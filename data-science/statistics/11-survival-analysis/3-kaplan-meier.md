# 3. Kaplan-Meier Estimator

The **Kaplan-Meier (KM) estimator** is the standard non-parametric method for estimating the survival function from observed data. It handles censored observations correctly without assuming any particular parametric distribution.

> 📌 **KM 是存活分析的起點**：幾乎每一份存活分析報告都從 KM 曲線開始。它是描述存活資料的標準視覺化工具，就像連續資料用直方圖一樣。在跑任何模型前，先畫 KM 曲線。

---

## 3.1 The KM Formula

At each time point where an event occurs, KM updates the survival estimate:

$$\hat{S}(t) = \prod_{t_i \leq t} \left(1 - \frac{d_i}{n_i}\right)$$

Where:
- $t_i$ = the distinct event times (only times when events actually occur)
- $d_i$ = number of events at time $t_i$
- $n_i$ = number of subjects at risk just before time $t_i$ (the **risk set**)

> 💡 **The risk set n_i** counts only subjects who are still under observation *just before* time $t_i$ — this automatically accounts for censoring. Subjects who were censored before $t_i$ are no longer in the risk set.  
> 風險集（risk set）只包含在 t_i 時間點之前還在觀測中的個體。設限個體在其設限時間點之後就從風險集中移除，這就是 KM 正確處理設限的關鍵機制。

---

## 3.2 Step-by-Step Manual Calculation

```python
import pandas as pd
import numpy as np

# Small example dataset (8 subjects)
data = pd.DataFrame({
    'time':  [3, 5, 5, 8, 10, 12, 12, 15],
    'event': [1, 0, 1, 1,  0,  1,  1,  0 ]
})

# Build KM table manually
event_times = sorted(data[data['event'] == 1]['time'].unique())
n_total = len(data)

rows = []
n_at_risk = n_total
S = 1.0

for t in event_times:
    d = ((data['time'] == t) & (data['event'] == 1)).sum()  # events at t
    # subtract those censored before this time point
    censored_before = ((data['time'] < t) & (data['event'] == 0)).sum()

    # Recalculate n_at_risk properly
    n_at_risk = (data['time'] >= t).sum()

    prob_survive = 1 - d / n_at_risk
    S = S * prob_survive

    rows.append({
        'time':        t,
        'n_at_risk':   n_at_risk,
        'events (d)':  d,
        '1 - d/n':     round(prob_survive, 4),
        'S(t)':        round(S, 4)
    })

km_table = pd.DataFrame(rows)
print(km_table)
```

**Output:**

| time | n_at_risk | events (d) | 1 - d/n | S(t)   |
| ---- | --------- | ---------- | ------- | ------ |
| 3    | 8         | 1          | 0.8750  | 0.8750 |
| 5    | 6         | 1          | 0.8333  | 0.7292 |
| 8    | 4         | 1          | 0.7500  | 0.5469 |
| 12   | 2         | 2          | 0.0000  | 0.0000 |

> At t=5: one subject was censored at t=5 (not an event), so n_at_risk drops by both the event at t=3 and the censored subject, giving n=6.

---

## 3.3 KM Estimator with lifelines

```python
from lifelines import KaplanMeierFitter
from lifelines.datasets import load_rossi
import matplotlib.pyplot as plt

# Load Rossi recidivism dataset
# Outcome: rearrest (1) or study end (0); time: weeks until event
rossi = load_rossi()
T = rossi['week']
E = rossi['arrest']

kmf = KaplanMeierFitter()
kmf.fit(T, E, label='All subjects')

# Key summary statistics
print(f"Median survival time: {kmf.median_survival_time_:.1f} weeks")
print(f"\nSurvival table (first 10 event times):")
print(kmf.survival_function_.head(10))
```

### Plotting the KM Curve

```python
fig, ax = plt.subplots(figsize=(8, 5))

kmf.plot_survival_function(
    ax=ax,
    ci_show=True,          # show 95% confidence interval
    ci_alpha=0.15,
    color='#3B82F6'
)

# Mark median survival time
median = kmf.median_survival_time_
ax.axhline(0.5, color='gray', linestyle='--', linewidth=1)
ax.axvline(median, color='gray', linestyle='--', linewidth=1)
ax.annotate(f'Median = {median:.0f} wks',
            xy=(median, 0.5), xytext=(median + 5, 0.55),
            arrowprops=dict(arrowstyle='->', color='gray'),
            fontsize=10)

ax.set_xlabel('Weeks')
ax.set_ylabel('Probability of No Rearrest S(t)')
ax.set_title('Kaplan-Meier Survival Curve — Rossi Recidivism Data')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

### Adding a Risk Table

A **risk table** shows how many subjects remain at risk at each time point — essential context for interpreting the width of confidence intervals.

```python
from lifelines.plotting import add_at_risk_counts

fig, ax = plt.subplots(figsize=(9, 5))
kmf.plot_survival_function(ax=ax, ci_show=True)

add_at_risk_counts(kmf, ax=ax, fontsize=9)

ax.set_title('KM Curve with At-Risk Table')
ax.set_xlabel('Weeks')
ax.set_ylabel('S(t)')
plt.tight_layout()
plt.show()
```

> 💡 **Confidence intervals widen at later time points** because fewer subjects remain at risk — even a single event has a large impact on the estimate. When fewer than ~10 subjects remain at risk, KM estimates become unreliable. Always check the risk table before interpreting the tail of a KM curve.  
> 曲線尾端的信賴區間非常寬，因為風險集很小。若尾端的風險集只剩幾人，那段估計幾乎沒有參考價值。

---

## 3.4 Comparing KM Curves by Group

The most common use of KM curves is comparing survival between two or more groups.

```python
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt

# Split by financial aid status (fin: 1 = received aid, 0 = no aid)
groups = rossi['fin'].unique()
colors = ['#3B82F6', '#EF4444']

fig, ax = plt.subplots(figsize=(9, 5))
kmf_list = []

for group, color in zip([1, 0], colors):
    mask = rossi['fin'] == group
    label = 'Received Aid' if group == 1 else 'No Aid'

    kmf_group = KaplanMeierFitter()
    kmf_group.fit(T[mask], E[mask], label=label)
    kmf_group.plot_survival_function(ax=ax, ci_show=True, color=color)
    kmf_list.append(kmf_group)

    print(f"{label}: Median = {kmf_group.median_survival_time_:.1f} weeks")

ax.set_xlabel('Weeks')
ax.set_ylabel('Probability of No Rearrest S(t)')
ax.set_title('KM Curves by Financial Aid Status')
ax.grid(alpha=0.3)
plt.tight_layout()
plt.show()
```

> ⚠️ **Visual comparison is not statistical testing**. Two curves that look different may not be significantly different, and vice versa. Use the **log-rank test** (Section 4) to formally test whether survival differs between groups.  
> 目視比較 KM 曲線不等於統計檢定。要判斷兩條曲線是否顯著不同，必須用 log-rank test。

---

## 3.5 Confidence Intervals for KM

The `lifelines` default confidence interval uses **Greenwood's formula** with log transformation — this ensures the CI stays within [0, 1] and performs better in the tails.

$$\text{Var}[\hat{S}(t)] = \hat{S}(t)^2 \sum_{t_i \leq t} \frac{d_i}{n_i(n_i - d_i)}$$

```python
# Print KM estimate with confidence intervals at specific time points
timeline = [10, 20, 30, 40, 52]
kmf.fit(T, E, timeline=timeline)

summary = pd.DataFrame({
    'S(t)':     kmf.survival_function_['KM_estimate'],
    'CI Lower': kmf.confidence_interval_['KM_estimate_lower_0.95'],
    'CI Upper': kmf.confidence_interval_['KM_estimate_upper_0.95']
}).round(4)

print("KM estimates at selected time points:")
print(summary)
```

---

## 3.6 Restricted Mean Survival Time (RMST)

The **RMST** is the area under the KM curve up to a specified time horizon τ — the average event-free time up to τ. It is an alternative summary to the median that:

- Is always defined (unlike median, which requires S(t) to cross 0.5)
- Has a clear interpretation: expected time event-free up to τ
- Is directly comparable between groups

$$\text{RMST}(\tau) = \int_0^\tau \hat{S}(t)\, dt$$

```python
from lifelines.utils import restricted_mean_survival_time

tau = 52  # restrict to 52 weeks

rmst_aid    = restricted_mean_survival_time(kmf_list[0], t=tau)
rmst_no_aid = restricted_mean_survival_time(kmf_list[1], t=tau)

print(f"RMST (Received Aid, up to {tau} wks): {rmst_aid:.2f} weeks")
print(f"RMST (No Aid,       up to {tau} wks): {rmst_no_aid:.2f} weeks")
print(f"Difference: {rmst_aid - rmst_no_aid:.2f} weeks event-free")
```

> 💡 Use RMST when the median is undefined (S(t) never crosses 0.5) or when comparing groups with crossing survival curves where the hazard ratio is not constant. 當存活曲線交叉時，風險比（hazard ratio）沒有意義，RMST 是更好的比較指標。

---

## 3.7 Key Takeaways

| Concept                          | Key Point                                                                   |
| -------------------------------- | --------------------------------------------------------------------------- |
| **KM is non-parametric**         | Makes no assumption about the distribution of T; lets data speak            |
| **Risk set shrinks over time**   | Both events and censorings remove subjects from the risk set                |
| **Median survival time**         | Where the KM curve crosses 0.5; undefined if curve stays above 0.5         |
| **CI widens at tails**           | Fewer at-risk subjects → unreliable estimates → check risk table            |
| **Group comparison ≠ significance** | Use the log-rank test for formal statistical comparison                  |
| **RMST as alternative summary**  | More robust than median when curves cross or median is undefined            |

---

**← Previous:** [Survival & Hazard Functions](./2-survival-hazard-functions.md)  
**Next:** [Log-Rank Test →](./4-log-rank-test.md)
