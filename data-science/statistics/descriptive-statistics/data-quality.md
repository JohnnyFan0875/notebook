# Data Quality

Good statistics starts with clean data. Before modeling or hypothesis testing, check missing values, outliers, duplicated rows, impossible values, and inconsistent categories.

This note is about **analysis-readiness**: what you should inspect before summary statistics, inference, or modeling. For organization-level data quality operating models, ownership, and monitoring, see [AI Strategy and Governance: Data Quality](../../ai-strategy-and-governance/data-quality.md).

Key point: Data quality problems are not minor flaws. Missing values, outliers, duplicated records, or wrong units can seriously distort averages, p-values, and model coefficients.

## Quick Checks

| Issue | What to Check | Common Fix |
| ----- | ------------- | ---------- |
| Missing values | `isna().sum()` | Drop, impute, or mark as unknown |
| Duplicates | `duplicated()` | Remove true duplicates |
| Outliers | Boxplot, IQR, z-score | Verify, cap, transform, or keep with note |
| Invalid values | Range checks | Correct source data or set missing |
| Category inconsistency | Unique values | Standardize labels |
| Unit mismatch | Summary statistics | Convert units before analysis |

## Missing Data

| Type | Meaning | Risk |
| ---- | ------- | ---- |
| MCAR | Missing completely at random | Least biased, but still reduces power |
| MAR | Missing depends on observed variables | Can often be modeled or imputed |
| MNAR | Missing depends on unobserved value | Highest bias risk |

```python
missing_summary = df.isna().sum().sort_values(ascending=False)
missing_rate = df.isna().mean().sort_values(ascending=False)
print(missing_summary)
print(missing_rate)
```

Tip: Beginner’s rule: Don’t delete all missing rows directly. First look at the proportion of missing items and whether the missing items are concentrated in certain columns or groups.

## Why Missingness Mechanism Matters

The right response to missing data depends on why the values are missing:

- if data are **MCAR**, complete-case analysis may be acceptable, though inefficient
- if data are **MAR**, imputation or model-based adjustment is often reasonable
- if data are **MNAR**, even sophisticated fixes may remain biased

Warning: Missingness is often informative. For example, patients with worse health may be more likely to miss follow-up, and high-income respondents may skip salary questions. Treat missingness as a data pattern, not just an inconvenience.

## Outliers

The IQR rule is a practical first-pass screen:

\[
Lower = Q1 - 1.5 \times IQR,\quad Upper = Q3 + 1.5 \times IQR
\]

| Outlier Type | What to Do |
| ------------ | ---------- |
| Data entry error | Correct or remove |
| Real but extreme value | Keep, but report sensitivity |
| Measurement artifact | Remove if justified |
| Influential model point | Check leverage and residuals |

```python
q1 = df["sepal length (cm)"].quantile(0.25)
q3 = df["sepal length (cm)"].quantile(0.75)
iqr = q3 - q1

lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

outliers = df[(df["sepal length (cm)"] < lower) | (df["sepal length (cm)"] > upper)]
print(outliers)
```

Tip: Outliers should trigger investigation before deletion. Ask whether the point is impossible, unusual but real, or influential only under a particular model.

## Category and Unit Problems

Many practical datasets fail not because of advanced statistical issues, but because labels and units are inconsistent.

| Problem | Example | Why it matters |
| ------- | ------- | -------------- |
| Category spelling drift | `male`, `Male`, `M` | Splits one group into several fake groups |
| Mixed units | cm and inch in one column | Distorts averages and model coefficients |
| Encoded missing labels | `999`, `unknown`, blank string | Hides missingness from standard checks |
| Date formatting mismatch | `2024/01/02` vs `02-01-2024` | Creates wrong ordering and duration values |

## Checklist

| Before Analysis | Done |
| --------------- | ---- |
| Data types match variable meaning | □ |
| Missing values reviewed | □ |
| Duplicates checked | □ |
| Impossible values checked | □ |
| Outliers inspected visually | □ |
| Units and categories standardized | □ |

## A Practical Triage Order

When a dataset first arrives, this sequence usually works well:

1. identifiers and duplicates
2. missingness patterns
3. impossible values and unit mismatches
4. outliers after context is understood

Tip: Many "outliers" are really data-entry or unit problems. Investigate meaning before deleting anything.

## Minimum Standard Before Any Model

Before moving on to inference or modeling, you should be able to answer:

1. what each row represents
2. what each variable means and in what unit
3. where the missingness is concentrated
4. whether any values are impossible, duplicated, or inconsistently labeled

If those answers are still unclear, the next statistical model is usually premature.

## Related Notes

- [Missing Data Mechanisms](../../data-manipulation-and-eda/missing-data.md): when the key issue is specifically missingness assumptions
- [AI Strategy and Governance: Data Quality](../../ai-strategy-and-governance/data-quality.md): when the issue is enterprise rules, ownership, and monitoring
