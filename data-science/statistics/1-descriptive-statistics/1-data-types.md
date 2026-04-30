# 1. Data Types & Measurement Scales

Before applying any statistical method, you need to know **what kind of data you're working with**. The data type determines which statistics are valid, which visualizations are appropriate, and which tests can be used later in inferential analysis.

> 📌 **為什麼這一步最重要**：用錯統計方法的根本原因，通常是沒有先確認資料型態。例如對類別資料算平均值，或對連續資料只用眾數，都會得出無意義的結果。

---

## 1.1 The Four Measurement Scales (NOIR)

| Scale        | 中文     | Core Property                                   | Examples                                           | Valid Statistics          |
| ------------ | -------- | ----------------------------------------------- | -------------------------------------------------- | ------------------------- |
| **Nominal**  | 名義尺度 | Categories only, no order                       | Gender, Blood type, Country, Color                 | Count, Mode, %            |
| **Ordinal**  | 次序尺度 | Ordered categories, but gaps are unequal        | Likert scale (1–5), Education level, Movie ratings | Count, Mode, Median, IQR  |
| **Interval** | 等距尺度 | Equal gaps between values, but **no true zero** | Temperature (°C/°F), Year, IQ score                | Mean, SD, Correlation     |
| **Ratio**    | 等比尺度 | Equal gaps + **true zero** exists               | Height, Weight, Income, Age, Duration              | All of the above + Ratios |

> 💡 **What is "true zero"? (真正的零點)**  
> True zero means the value 0 represents a complete absence of the quantity.
>
> - Temperature 0°C does **not** mean "no temperature" exists → Interval scale
> - Income $0 means "no income" → Ratio scale  
>   The practical implication: you can say someone earns **twice as much** (Ratio), but you cannot say 20°C is **twice as hot** as 10°C (Interval).

---

## 1.2 Two Broad Categories in Practice

In day-to-day analysis, you'll mostly think in these two broader terms:

| Category                      | 中文     | Includes         | Core Question                   |
| ----------------------------- | -------- | ---------------- | ------------------------------- |
| **Categorical** (Qualitative) | 類別資料 | Nominal, Ordinal | What group does this belong to? |
| **Numerical** (Quantitative)  | 數值資料 | Interval, Ratio  | How much / how many?            |

Numerical data is further split into:

| Type           | 中文   | Description                              | Example                                            |
| -------------- | ------ | ---------------------------------------- | -------------------------------------------------- |
| **Continuous** | 連續型 | Any value in a range, including decimals | Height (170.5 cm), Temperature, Price              |
| **Discrete**   | 離散型 | Only countable, whole values             | Number of children, Count of defects, Goals scored |

---

## 1.3 Why It Matters — Decision Table

This table summarizes which methods are appropriate for each data type:

| Data Type                        | Central Tendency | Spread    | Visualization       | Notes                            |
| -------------------------------- | ---------------- | --------- | ------------------- | -------------------------------- |
| **Nominal**                      | Mode only        | —         | Bar chart           | Cannot rank or compute distances |
| **Ordinal**                      | Median, Mode     | IQR       | Bar chart (ordered) | Gaps between levels are unequal  |
| **Interval / Ratio (symmetric)** | Mean             | SD, Range | Histogram, Boxplot  | Most statistical methods apply   |
| **Interval / Ratio (skewed)**    | Median           | IQR       | Histogram, Boxplot  | Use robust measures              |

---

## 1.4 Python: Checking Data Types

```python
import pandas as pd

df = pd.read_csv('your_data.csv')

# Check dtype of each column
print(df.dtypes)

# Numerical summary
print(df.describe())

# Categorical summary
print(df.describe(include='object'))
```

Common pandas dtype mappings:

| pandas dtype       | Likely Scale       | Action                                                               |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
| `int64`, `float64` | Interval or Ratio  | Check if it's truly numerical or just coded (e.g., 1=Male, 2=Female) |
| `object`           | Nominal or Ordinal | Check if ordering exists                                             |
| `category`         | Nominal or Ordinal | Explicit category type — set `ordered=True` for ordinal              |
| `bool`             | Nominal (binary)   | Treat as categorical                                                 |
| `datetime64`       | Special            | Use time series methods                                              |

> ⚠️ **Common trap**: Coded categorical variables (e.g., `1 = Strongly Disagree`, `5 = Strongly Agree`) may appear as `int64` in pandas, but they are **Ordinal**, not numerical. Always check the data dictionary.  
> 常見陷阱：問卷的 Likert 量表資料儲存為數字，但本質上是次序尺度，不應直接計算平均值。

---

## 1.5 Key Takeaways

| Principle                     | Details                                                                      |
| ----------------------------- | ---------------------------------------------------------------------------- |
| **Identify scale first**      | Always confirm data type before choosing any statistical method              |
| **NOIR hierarchy**            | Nominal < Ordinal < Interval < Ratio — higher scales support more operations |
| **Downgrading is OK**         | You can treat Ratio data as Ordinal if needed, but never upgrade             |
| **Watch for coded variables** | Numbers don't always mean numerical scale — check context                    |

---
