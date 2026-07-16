# Data Quality

Good statistics starts with clean data. Before modeling or hypothesis testing, check missing values, outliers, duplicated rows, impossible values, and inconsistent categories.

This note is about **analysis-readiness**: what you should inspect before summary statistics, inference, or modeling. For organization-level data quality operating models, ownership, and monitoring, see [AI Strategy and Governance: Data Quality](../../ai-strategy-and-governance/data-quality.md).

**Key point:**

- Data quality problems are not minor flaws.
- Missing values, outliers, duplicated records, or wrong units can seriously distort averages, p-values, and model coefficients.

## Quick Checks

| Issue                  | What to Check         | Common Fix                                |
| ---------------------- | --------------------- | ----------------------------------------- |
| Missing values         | `isna().sum()`        | Drop, impute, or mark as unknown          |
| Duplicates             | `duplicated()`        | Remove true duplicates                    |
| Outliers               | Boxplot, IQR, z-score | Verify, cap, transform, or keep with note |
| Invalid values         | Range checks          | Correct source data or set missing        |
| Category inconsistency | Unique values         | Standardize labels                        |
| Unit mismatch          | Summary statistics    | Convert units before analysis             |

## Missing Data

Detailed definitions of **MCAR / MAR / MNAR**, and how those mechanisms affect deletion or imputation choices, are covered in [Missing Data Mechanisms](../../data-manipulation-and-eda/missing-data.md).

```python
missing_summary = df.isna().sum().sort_values(ascending=False)
missing_rate = df.isna().mean().sort_values(ascending=False)
print(missing_summary)
# species              0
# petal width (cm)     0
# ...
print(missing_rate)
# species              0.0
# petal width (cm)     0.0
# ...
```

**Check before deciding what to do:**

- Which columns have the most missing values?
- What proportion is missing?
- Is missingness concentrated in certain rows, subgroups, or time periods?
- Are placeholder values like `999`, `unknown`, or blank strings hiding as non-missing values?

**Note:**

- Don’t delete all missing rows directly.
- First check how much is missing and whether the pattern is systematic.

## Outliers

Detailed explanation of **IQR-based outlier detection**, boxplots, and interpretation is covered in [Univariate Analysis (Numerical)](./univariate-numerical.md).

| Outlier Type            | What to Do                   |
| ----------------------- | ---------------------------- |
| Data entry error        | Correct or remove            |
| Real but extreme value  | Keep, but report sensitivity |
| Measurement artifact    | Remove if justified          |
| Influential model point | Check leverage and residuals |

**Check before deciding what to do:**

- Is the value impossible, or just rare?
- Could it be a unit mismatch or data-entry error?
- Does it appear in a boxplot or IQR screen?
- Does it materially change the mean, SD, correlation, or model result?

**Note:**

- Outliers should trigger investigation before deletion.
- Ask whether the point is impossible, unusual but real, or influential only under a particular model.

## Category and Unit Problems

Many practical datasets fail not because of advanced statistical issues, but because labels and units are inconsistent.

| Problem                  | Example                        | Why it matters                             |
| ------------------------ | ------------------------------ | ------------------------------------------ |
| Category spelling drift  | `male`, `Male`, `M`            | Splits one group into several fake groups  |
| Mixed units              | cm and inch in one column      | Distorts averages and model coefficients   |
| Encoded missing labels   | `999`, `unknown`, blank string | Hides missingness from standard checks     |
| Date formatting mismatch | `2024/01/02` vs `02-01-2024`   | Creates wrong ordering and duration values |

## Checklist

| Before Analysis                   | Done |
| --------------------------------- | ---- |
| Data types match variable meaning | □    |
| Missing values reviewed           | □    |
| Duplicates checked                | □    |
| Impossible values checked         | □    |
| Outliers inspected visually       | □    |
| Units and categories standardized | □    |

## A Practical Triage Order

When a dataset first arrives, this sequence usually works well:

1. identifiers and duplicates
2. missingness patterns
3. impossible values and unit mismatches
4. outliers after context is understood

**Note:**

- Many "outliers" are really data-entry or unit problems.
- Investigate meaning before deleting anything.

## Minimum Standard Before Any Model

Before moving on to inference or modeling, you should be able to answer:

1. what each row represents
2. what each variable means and in what unit
3. where the missingness is concentrated
4. whether any values are impossible, duplicated, or inconsistently labeled

If those answers are still unclear, the next statistical model is usually premature.
