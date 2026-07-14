# Cohort Analysis

Cohort analysis 是把觀測對象先分成互斥群組，再追蹤這些群組隨時間的表現差異。它常用來回答 retention、repeat purchase、engagement decay 與 monetization 相關問題。

Key point: cohort analysis 的重點不是「看某個月份有多少活躍用戶」，而是「同一批在相近時間或相似條件下進來的用戶，之後表現如何變化」。

## What Is A Cohort

A **cohort** is a mutually exclusive group of observations that share a defined starting condition.

Common cohort types:

- **Time cohort**: grouped by acquisition month, signup week, or first purchase date
- **Behavior cohort**: grouped by first action, activation path, or subscription choice
- **Size cohort**: grouped by company size, order bucket, or account tier

Tip: A cohort definition should be stable and reproducible. If the assignment rule changes mid-analysis, the table becomes hard to interpret.

## Core Structure

A typical cohort table has:

- cohort assignment in rows
- elapsed time since cohort start in columns
- one metric in the cell values

For example:

| Acquisition Month | Month 1 | Month 2 | Month 3 |
| --- | --- | --- | --- |
| 2024-01 | retention | retention | retention |
| 2024-02 | retention | retention | retention |

The row tells you **who started together**. The column tells you **how long it has been since they started**.

## A Common Retention Workflow

The most common use case is customer retention by acquisition month:

1. assign each customer to a cohort based on first observed activity
2. calculate the period index for each later observation
3. count active customers by cohort and period index
4. divide by the original cohort size to get retention rate
5. visualize the matrix with a heatmap

## Example In pandas

```python
import pandas as pd

orders['InvoiceMonth'] = orders['InvoiceDate'].dt.to_period('M')

cohort_map = (
    orders.groupby('CustomerID')['InvoiceMonth']
    .min()
    .rename('CohortMonth')
)

orders = orders.join(cohort_map, on='CustomerID')

period_number = (
    (orders['InvoiceMonth'].dt.year - orders['CohortMonth'].dt.year) * 12
    + (orders['InvoiceMonth'].dt.month - orders['CohortMonth'].dt.month)
    + 1
)

orders['CohortIndex'] = period_number
```

Then aggregate active customers:

```python
cohort_counts = (
    orders.groupby(['CohortMonth', 'CohortIndex'])['CustomerID']
    .nunique()
    .unstack('CohortIndex')
)

cohort_sizes = cohort_counts.iloc[:, 0]
retention = cohort_counts.divide(cohort_sizes, axis=0)
```

## Heatmaps Are Usually The Best First View

A retention matrix is easier to read as a heatmap than as a raw table:

```python
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
sns.heatmap(
    retention,
    annot=True,
    fmt='.0%',
    cmap='Blues',
)
plt.title('Monthly Retention by Acquisition Cohort')
plt.xlabel('Months Since Acquisition')
plt.ylabel('Acquisition Cohort')
plt.tight_layout()
plt.show()
```

Why this works well:

- darker cells quickly show stronger retention
- row-by-row comparison reveals whether newer cohorts are improving
- diagonal patterns can reveal seasonality or lifecycle decay

## Cohort Metrics Are Not Limited To Retention

Retention is the default, but the same structure can track:

- average order quantity
- revenue per active user
- average order value
- number of sessions
- feature adoption rate

Tip: pick one metric per table. Mixing multiple business meanings into one cohort matrix usually makes interpretation worse.

## Common Interpretation Mistakes

- comparing raw active counts instead of normalized retention rates
- forgetting that later cohorts have fewer observed periods
- mixing acquisition cohorts with calendar-month summaries
- redefining “active” midstream
- ignoring major product or pricing changes that affect all cohorts

Warning: cohort analysis is descriptive first. It is excellent for pattern finding, but by itself it does not prove causality.

## When Cohort Analysis Is Especially Useful

- subscription or SaaS retention tracking
- e-commerce repeat purchase analysis
- onboarding and activation monitoring
- comparing customer quality before and after a channel change

## 小結

Cohort analysis 把「不同時間進來的人」拆開來看，因此比單純月報表更能分辨 retention 變化到底來自產品改善、流量品質改變，還是只是新舊客混在一起造成的表面波動。
