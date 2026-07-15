# Data Types & Measurement Scales

Before applying any statistical method, you need to know **what kind of data you're working with**.  
The data type determines which statistics are valid, which visualizations are appropriate, and which tests can be used later in inferential analysis.

## The Four Measurement Scales (NOIR)

| Scale        | Category                  | Property                                                          | Central Tendency | Spread    | Visualization      | Examples                            |
| ------------ | ------------------------- | ----------------------------------------------------------------- | ---------------- | --------- | ------------------ | ----------------------------------- |
| **Nominal**  | Categorical (Qualitative) | No order; cannot rank or compute distances                        | Mode             | No spread | Bar chart          | Gender, Blood type                  |
| **Ordinal**  | Categorical (Qualitative) | Ordered, unequal gaps                                             | Median, Mode     | IQR       | Ordered bar chart  | Likert scale (1–5), Education level |
| **Interval** | Numerical (Quantitative)  | Equal gaps between values, no true zero; ratios do not make sense | Mean             | SD, Range | Histogram, Boxplot | Temperature, Year, IQ score         |
| **Ratio**    | Numerical (Quantitative)  | Equal gaps, true zero                                             | Mean/Median      | SD, IQR   | Histogram, Boxplot | Height, Income, Age, Duration       |

**Numerical data** is further split into:

| Type           | Description                              | Example                                            |
| -------------- | ---------------------------------------- | -------------------------------------------------- |
| **Continuous** | Any value in a range, including decimals | Height, Temperature, Price                         |
| **Discrete**   | Only countable, whole values             | Number of children, Count of defects, Goals scored |

> What does **true zero** mean?

- A true zero means that **0** really indicates the quantity is absent.
  - 0°C does not mean temperature does not exist. Celsius is an Interval scale
  - $0 income means there is no income. Income is a Ratio scale.
- In practice, this means ratio comparisons only make sense when a true zero exists. You can say someone earns twice as much, but you should not say _20°C_ is twice as hot as _10°C_.

## Representation Also Matters

Before you even reach measurement scale, it helps to ask how the data is represented.

| Representation | Typical form                                             | Practical implication                                                       | Examples                                    |
| -------------- | -------------------------------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------- |
| Structured     | Tables with rows, columns, labels, and consistent fields | Easier to filter, summarize, and analyze directly                           | Sales records, attendance logs              |
| Unstructured   | Text, images, audio, video, free-form documents          | Richer context, but usually needs preprocessing before statistical analysis | Interviews, images, videos, free-text notes |

**Key point:**

- A dataset can be valuable and still be hard to analyze.
- Unstructured data often contains important context, but it usually needs extraction, labeling, or transformation before standard statistical workflows apply.

## Checking Data Types (Python)

```python
import seaborn as sns

df = sns.load_dataset("iris").copy()

# check the data type of each column
df.dtypes
# sepal_length    float64
# sepal_width     float64
# petal_length    float64
# petal_width     float64
# species          object

# numerical summary
df.describe()
#       sepal_length  sepal_width  petal_length  petal_width
# count       150.00       150.00        150.00       150.00
# mean          5.84         3.06          3.76         1.20
# std           0.83         0.44          1.77         0.76
# ...

# categorical summary
df.describe(include='object')
#        species
# count      150
# unique       3
# top     setosa
# freq        50
```

Common pandas dtype mappings:

| pandas dtype       | Likely Scale       | Action                                                               |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
| `int64`, `float64` | Interval or Ratio  | Check if it's truly numerical or just coded (e.g., 1=Male, 2=Female) |
| `object`           | Nominal or Ordinal | Check if ordering exists                                             |
| `category`         | Nominal or Ordinal | Explicit category type — set `ordered=True` for ordinal              |
| `bool`             | Nominal (binary)   | Treat as categorical                                                 |
| `datetime64`       | Special            | Use time series methods                                              |

**Warning:**

- Coded categorical variables (e.g., Likert scale) may appear as int64 in pandas, but they are **Ordinal**, not numerical. Always check the data dictionary.
- **Metadata and identifiers** (e.g., customer ID, file path, timestamp) may look like ordinary variables but should not be analyzed as measurements.

> Always ask whether a column represents a measured attribute, a category, a key, or supporting metadata.

## Key Takeaways

| Principle                     | Details                                                                      |
| ----------------------------- | ---------------------------------------------------------------------------- |
| **Identify scale first**      | Always confirm data type before choosing any statistical method              |
| **NOIR hierarchy**            | Nominal < Ordinal < Interval < Ratio — higher scales support more operations |
| **Downgrading is OK**         | You can treat Ratio data as Ordinal if needed, but never upgrade             |
| **Watch for coded variables** | Numbers don't always mean numerical scale — check context                    |

## Why Type Errors Cascade

One wrong type decision can quietly contaminate an entire analysis:

- categorical IDs averaged like measurements
- ordinal responses treated as equally spaced quantities
- dates stored as strings so time structure disappears

> Data typing is not clerical cleanup. It is an early statistical judgment.
