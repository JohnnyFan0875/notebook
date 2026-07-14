# Data Types & Measurement Scales

Before applying any statistical method, you need to know **what kind of data you're working with**.  
The data type determines which statistics are valid, which visualizations are appropriate, and which tests can be used later in inferential analysis.

## The Four Measurement Scales (NOIR)

| Scale        | Core Property                                   | Examples                                           | Valid Statistics          |
| ------------ | ----------------------------------------------- | -------------------------------------------------- | ------------------------- |
| **Nominal**  | Categories only, no order                       | Gender, Blood type, Country, Color                 | Count, Mode, %            |
| **Ordinal**  | Ordered categories, but gaps are unequal        | Likert scale (1–5), Education level, Movie ratings | Count, Mode, Median, IQR  |
| **Interval** | Equal gaps between values, but **no true zero** | Temperature (°C/°F), Year, IQ score                | Mean, SD, Correlation     |
| **Ratio**    | Equal gaps + **true zero** exists               | Height, Weight, Income, Age, Duration              | All of the above + Ratios |

> What does **true zero** mean?

- A true zero means that **0** really indicates the quantity is absent.
  - 0°C does not mean temperature does not exist. Celsius is an Interval scale
  - $0 income means there is no income. Income is a Ratio scale.
- In practice, this means ratio comparisons only make sense when a true zero exists. You can say someone earns twice as much, but you should not say _20°C_ is twice as hot as _10°C_.

## Two Broad Categories in Practice

| Category                      | Includes         | Core Question                   |
| ----------------------------- | ---------------- | ------------------------------- |
| **Categorical** (Qualitative) | Nominal, Ordinal | What group does this belong to? |
| **Numerical** (Quantitative)  | Interval, Ratio  | How much / how many?            |

## Representation Also Matters

Before you even reach measurement scale, it helps to ask how the data is represented.

| Representation | Typical form                                             | Practical implication                                                       |
| -------------- | -------------------------------------------------------- | --------------------------------------------------------------------------- |
| Structured     | Tables with rows, columns, labels, and consistent fields | Easier to filter, summarize, and analyze directly                           |
| Unstructured   | Text, images, audio, video, free-form documents          | Richer context, but usually needs preprocessing before statistical analysis |

Examples:

- structured: sales records, attendance logs, weather tables
- unstructured: interviews, images, videos, free-text notes

Key point: A dataset can be valuable and still be hard to analyze. Unstructured data often contains important context, but it usually needs extraction, labeling, or transformation before standard statistical workflows apply.

Numerical data is further split into:

| Type           | Description                              | Example                                            |
| -------------- | ---------------------------------------- | -------------------------------------------------- |
| **Continuous** | Any value in a range, including decimals | Height, Temperature, Price                         |
| **Discrete**   | Only countable, whole values             | Number of children, Count of defects, Goals scored |

## Why It Matters — Decision Table

This table summarizes which methods are appropriate for each data type:

| Data Type                        | Central Tendency | Spread    | Visualization       | Notes                            |
| -------------------------------- | ---------------- | --------- | ------------------- | -------------------------------- |
| **Nominal**                      | Mode only        | —         | Bar chart           | Cannot rank or compute distances |
| **Ordinal**                      | Median, Mode     | IQR       | Bar chart (ordered) | Gaps between levels are unequal  |
| **Interval / Ratio (symmetric)** | Mean             | SD, Range | Histogram, Boxplot  | Most statistical methods apply   |
| **Interval / Ratio (skewed)**    | Median           | IQR       | Histogram, Boxplot  | Use robust measures              |

## Checking Data Types (Python)

```python
import seaborn as sns

df = sns.load_dataset("iris").copy()

# check the data type of each column
df.dtypes

# numerical summary
df.describe()

# categorical summary
df.describe(include='object')
```

Common pandas dtype mappings:

| pandas dtype       | Likely Scale       | Action                                                               |
| ------------------ | ------------------ | -------------------------------------------------------------------- |
| `int64`, `float64` | Interval or Ratio  | Check if it's truly numerical or just coded (e.g., 1=Male, 2=Female) |
| `object`           | Nominal or Ordinal | Check if ordering exists                                             |
| `category`         | Nominal or Ordinal | Explicit category type — set `ordered=True` for ordinal              |
| `bool`             | Nominal (binary)   | Treat as categorical                                                 |
| `datetime64`       | Special            | Use time series methods                                              |

Warning: Common trap: Coded categorical variables (e.g., 1 = Strongly Disagree, 5 = Strongly Agree; Likert scale) may appear as int64 in pandas, but they are Ordinal, not numerical. Always check the data dictionary.

Another common trap: metadata and identifiers may look like ordinary variables but should not be analyzed as measurements.

Examples:

- customer ID
- encounter number
- file path
- timestamp stored as raw text

Tip: Always ask whether a column represents a measured attribute, a category, a key, or supporting metadata.

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

Tip: Data typing is not clerical cleanup. It is an early statistical judgment.
