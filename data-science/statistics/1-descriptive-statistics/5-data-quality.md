# 5. Data Quality

Good statistics starts with clean data. Before modeling or hypothesis testing, check missing values, outliers, duplicated rows, impossible values, and inconsistent categories.

> 📌 **中文重點**：資料品質問題不是小瑕疵。Missing data、outliers、重複資料或錯誤單位，都可能讓平均數、p-value、模型係數完全失真。

---

## Quick Checks

| Issue | What to Check | Common Fix |
| ----- | ------------- | ---------- |
| Missing values | `isna().sum()` | Drop, impute, or mark as unknown |
| Duplicates | `duplicated()` | Remove true duplicates |
| Outliers | Boxplot, IQR, z-score | Verify, cap, transform, or keep with note |
| Invalid values | Range checks | Correct source data or set missing |
| Category inconsistency | Unique values | Standardize labels |
| Unit mismatch | Summary statistics | Convert units before analysis |

---

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

> 💡 初學者原則：不要直接把所有 missing rows 刪掉。先看缺失比例、缺失是否集中在某些欄位或群體。

---

## Outliers

The IQR rule is a practical first-pass screen:

$$Lower = Q1 - 1.5 \times IQR,\quad Upper = Q3 + 1.5 \times IQR$$

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

---

## Checklist

| Before Analysis | Done |
| --------------- | ---- |
| Data types match variable meaning | □ |
| Missing values reviewed | □ |
| Duplicates checked | □ |
| Impossible values checked | □ |
| Outliers inspected visually | □ |
| Units and categories standardized | □ |

