# 2. Univariate Analysis — Categorical Data

This section covers how to describe a **single categorical variable** (Nominal or Ordinal scale). Since you cannot compute a meaningful mean or standard deviation for categories, the focus is on **counts, proportions, and visual distributions**.

---

## 2.1 Frequency Table (次數分配表)

A frequency table is the foundation of categorical description. It shows how often each category appears.

| Metric                 | 中文       | Description                                      |
| ---------------------- | ---------- | ------------------------------------------------ |
| **Frequency (n)**      | 次數       | Raw count of each category                       |
| **Relative Frequency** | 相對次數   | Proportion = count ÷ total                       |
| **Percentage (%)**     | 百分比     | Relative frequency × 100                         |
| **Cumulative %**       | 累積百分比 | Running total — most useful for **ordinal** data |

```python
import pandas as pd
from sklearn.datasets import load_iris

iris = load_iris(as_frame=True)
df = iris.frame
df['species'] = iris.target_names[iris.target]

# Build frequency table
freq      = df['species'].value_counts()
rel_freq  = df['species'].value_counts(normalize=True)

summary = pd.DataFrame({
    'Count':          freq,
    'Proportion':     rel_freq.round(3),
    'Percentage (%)': (rel_freq * 100).round(1)
})
print(summary)
```

**Output:**

| Species    | Count | Proportion | Percentage (%) |
| ---------- | ----- | ---------- | -------------- |
| setosa     | 50    | 0.333      | 33.3%          |
| versicolor | 50    | 0.333      | 33.3%          |
| virginica  | 50    | 0.333      | 33.3%          |

> 💡 **When to use relative frequency instead of raw count?**  
> When comparing two groups of different sizes, raw counts are misleading. For example, 30 complaints out of 100 customers is very different from 30 out of 1,000.  
> 比較不同大小的群體時，用比例而非原始次數，才不會誤導。

---

## 2.2 Ordinal Data: Preserving Order Matters

For ordinal variables (e.g., satisfaction ratings), the category order is meaningful and must be preserved in both tables and charts.

```python
# Define ordered categories explicitly
ratings = pd.Categorical(
    ['Good', 'Bad', 'Excellent', 'Good', 'Bad', 'Excellent', 'Good'],
    categories=['Bad', 'Good', 'Excellent'],  # logical order
    ordered=True
)

freq_ordered = pd.Series(ratings).value_counts().sort_index()
print(freq_ordered)
```

> ⚠️ Without setting `ordered=True` and specifying `categories`, pandas will sort alphabetically (Bad → Excellent → Good), which breaks the logical order.  
> 如果沒有明確設定順序，pandas 會按字母排序，導致圖表的順序錯誤。

---

## 2.3 Visualization

### Bar Chart — Default Choice for Categorical Data

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Vertical bar chart
sns.countplot(x='species', data=df, palette='Set2')
plt.title('Species Distribution')
plt.ylabel('Count')
plt.show()

# Horizontal bar — better when category names are long
df['species'].value_counts().plot(kind='barh', color='steelblue')
plt.title('Species Distribution')
plt.xlabel('Count')
plt.show()
```

### Pie Chart — Part-of-Whole Story

```python
df['species'].value_counts().plot(
    kind='pie', autopct='%1.1f%%', startangle=90
)
plt.title('Species Proportion')
plt.ylabel('')
plt.show()
```

### When to Use Which Chart

| Chart                      | Use When                                 | Avoid When                              |
| -------------------------- | ---------------------------------------- | --------------------------------------- |
| **Bar chart (vertical)**   | Comparing counts across categories       | Category names are very long            |
| **Bar chart (horizontal)** | Category names are long; many categories | Part-of-whole is the main story         |
| **Pie chart**              | Showing part-of-whole, ≤ 5 categories    | > 5 categories; comparing across groups |
| **Ordered bar chart**      | Ordinal data (e.g., Likert scale)        | Nominal data with no natural order      |

> 💡 **Rule of thumb**: Default to bar charts. Only switch to a pie chart when the "part of a whole" message is the primary focus **and** you have 5 or fewer categories.

---

## 2.4 Cross-Tabulation (交叉表)

A cross-tabulation (contingency table) shows the joint frequency of **two categorical variables**. While technically bivariate, it's introduced here as a natural extension of frequency tables.

```python
import pandas as pd

data = pd.DataFrame({
    'Gender':   ['Male', 'Female', 'Male', 'Female', 'Male', 'Female'],
    'Survived': ['No',   'Yes',    'Yes',  'Yes',    'No',   'No']
})

# Raw counts with row/column totals
ct = pd.crosstab(data['Gender'], data['Survived'], margins=True)
print(ct)

# Proportions within each row (e.g., survival rate by gender)
ct_norm = pd.crosstab(data['Gender'], data['Survived'], normalize='index').round(3)
print(ct_norm)
```

**Raw count output:**

| Gender | No  | Yes | Total |
| ------ | --- | --- | ----- |
| Female | 1   | 2   | 3     |
| Male   | 2   | 1   | 3     |
| Total  | 3   | 3   | 6     |

**Row-normalized (survival rate per gender):**

| Gender | No    | Yes   |
| ------ | ----- | ----- |
| Female | 0.333 | 0.667 |
| Male   | 0.667 | 0.333 |

> 💡 `normalize='index'` → row proportions (most common: "what % of each group did X?")  
> `normalize='columns'` → column proportions  
> `normalize='all'` → proportions of grand total

---

## 2.5 Key Takeaways

| Concept                | Key Point                                                               |
| ---------------------- | ----------------------------------------------------------------------- |
| **Frequency table**    | Always the starting point for categorical description                   |
| **Relative frequency** | Prefer over raw counts when comparing groups of different sizes         |
| **Ordinal data**       | Explicitly define category order — don't let pandas sort alphabetically |
| **Bar chart**          | Default visualization for categorical data                              |
| **Pie chart**          | Only when ≤ 5 categories and part-of-whole is the message               |
| **Cross-tabulation**   | Describes relationship between two categorical variables                |

---

**Next:** [Univariate Analysis – Numerical Data →](./3-univariate-numerical.md)
