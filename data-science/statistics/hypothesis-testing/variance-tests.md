# Variance Tests

Homogeneity of variance (homoscedasticity) means the variance within each group is constant across levels of a categorical variable.  
This is a key assumption for tests such as **t-tests** and **ANOVA**.

## Why Important?

- Many parametric tests (t-tests, ANOVA) assume equal variances across groups.
- Violating this assumption can:
  - Inflate **Type I error rates** (false positives).
  - Reduce statistical power.

## Hypotheses

- **Null hypothesis (H₀):** Variances across groups are equal.
- **Alternative hypothesis (Hₐ):** At least one group has a different variance.

## Levene’s Test

- Robust to non-normality.
- Preferred when data may not be normally distributed.

```python
from scipy import stats

group1 = [20, 22, 23, 21, 24]
group2 = [30, 31, 32, 29, 33]
group3 = [15, 16, 14, 17, 15]

statistic, p_value = stats.levene(group1, group2, group3)
print("Levene’s test:", statistic, p_value)
```

## Brown–Forsythe Test

- **Purpose:** Robust alternative to Levene’s test.
- **Difference:** Uses the **median** instead of the mean to compute deviations, making it less sensitive to non-normality.
- **Null hypothesis (H₀):** Variances are equal across groups.
- **Alternative hypothesis (Hₐ):** At least one variance differs.

**Python Example:**

```python
from pingouin import homoscedasticity
import pandas as pd

df = pd.DataFrame({
    "group": ["A"]*5 + ["B"]*5 + ["C"]*5,
    "value": [20,22,21,19,23, 30,29,31,32,28, 15,17,16,14,18]
})

# Run Brown–Forsythe test
homoscedasticity(df, dv="value", group="group", method="bf")
```

### Bartlett’s Test

- More powerful if data are normally distributed.
- Sensitive to deviations from normality.

```python
statistic, p_value = stats.bartlett(group1, group2, group3)
print(statistic, p_value)
```

📌 **Summary:**

- Use **Levene’s test** when unsure about normality.
- Use **Bartlett’s test** when data are approximately normal.
- Use **Brown–Forsythe test** as a more robust option when data may be skewed or contain outliers.
- If variances are unequal →
  - Use **Welch’s ANOVA** instead of regular ANOVA.
  - Use **Welch’s t-test** instead of Student’s t-test.
