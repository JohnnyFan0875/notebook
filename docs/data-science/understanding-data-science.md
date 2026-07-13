# Understanding Data Science

Data science is the practice of turning data into usable understanding, predictions, and decisions.

Key point: Data science is not only modeling. A real workflow usually includes question framing, data collection, preparation, exploration, experimentation, modeling, and interpretation.

## What Data Science Is Trying To Do

A simple way to think about data science is:

1. start with a question or decision problem
2. gather relevant data
3. prepare the data so it can be trusted
4. analyze or model it
5. turn the result into action

This is why data science sits between technical work and decision-making. It needs both sound methods and useful framing.

## A Practical Workflow

Most beginner-friendly data science workflows follow a pattern like this:

| Stage | Main goal | Typical output |
| --- | --- | --- |
| Problem framing | Clarify what needs to be answered | Question, hypothesis, success metric |
| Data sourcing | Find relevant internal or external data | Raw tables, logs, files, APIs |
| Data preparation | Clean and standardize messy data | Analysis-ready dataset |
| Exploration | Understand structure, patterns, and risks | Summary statistics, charts, hypotheses |
| Experiment or modeling | Test claims or predict outcomes | Statistical result or trained model |
| Interpretation | Connect result back to decisions | Recommendation, report, next action |

Warning: Many projects fail before modeling because the question is vague, the data is weak, or the preparation step is skipped.

## Common Data Sources

The introductory material split data sources into two broad groups.

| Source type | Description | Examples |
| --- | --- | --- |
| Company data | Data created inside an organization | web events, customer data, survey data, logistics data, financial transactions |
| Open data | Publicly available data that can be used and shared more broadly | government datasets, research datasets, public repositories |

Useful reminder: Knowing where data came from matters as much as knowing what the columns contain. Source affects trust, bias, freshness, and reuse constraints.

Another useful split is:

- **observed / passively collected data**: logs, transactions, clickstreams, operational records
- **solicited data**: surveys, reviews, in-app questionnaires, focus groups

Solicited data is often used when teams need to:

- capture opinions that behavior logs cannot show directly
- create structured feedback loops
- de-risk decisions before a launch or major change
- monitor perceived quality, satisfaction, or unmet needs

Warning: solicited data is useful, but it is shaped by wording, sampling, and response bias. Treat it as evidence with its own collection process, not as a neutral ground truth.

## Why Data Preparation Comes Early

Real-world data is messy. Preparation exists to prevent:

- obvious errors
- incorrect analytical results
- hidden bias in later models or decisions

Common preparation work includes:

- fixing wrong data types
- standardizing formats and units
- removing true duplicates
- handling missing values deliberately
- checking inconsistent categories

Key point: Cleaning is not clerical overhead. It is part of the reasoning layer of data science.

## Experiments In Data Science

One important branch of data science is experimentation.

The basic loop is:

1. form a question
2. form a hypothesis
3. collect data
4. test the hypothesis with an appropriate statistical method
5. interpret the result

`A/B testing` is one common business version of this pattern. It is useful when you want to compare two alternatives such as titles, interfaces, offers, or workflows.

Tip: Experiments are especially valuable when the goal is to support a decision rather than only describe what happened.

## Modeling And Machine Learning

The course also framed modeling as representing a real-world process using mathematical relationships between variables.

Two useful distinctions:

| Concept | What it emphasizes |
| --- | --- |
| Statistical modeling | Explain relationships, assumptions, and uncertainty |
| Machine learning | Learn patterns from data to improve prediction |

In supervised machine learning, the model learns from labeled examples and then predicts outcomes for new inputs.

Examples:

- customer churn prediction
- recommendation systems
- image diagnosis or classification

Warning: A model can look sophisticated while still being built on weak assumptions, weak labels, or badly prepared data.

One more distinction matters in business settings:

- **predictive** work asks whether the model can forecast or classify future cases accurately
- **explanatory** work asks whether the model helps people understand what drives the outcome

These goals overlap, but they are not identical. A model with strong predictive power may be hard to explain, while an explanatory model may intentionally sacrifice some raw predictive accuracy in exchange for interpretability.

## Where Python Fits

Python is not data science itself. It is one of the main tools used to implement the workflow.

Teams commonly use Python to:

- load data from files, databases, or APIs
- clean and reshape data
- visualize patterns
- run statistics and experiments
- train machine learning models
- automate repeatable analysis workflows

## A First End-To-End Workflow

Many introductory courses teach data science through a very small loop:

1. load a table from a CSV file
2. inspect the columns and a few example rows
3. ask a simple question about one or two variables
4. make a basic plot
5. interpret what the plot suggests

For example:

```python
import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv("data.csv")

print(df.head())
print(df.dtypes)

plt.scatter(df["age"], df["height"])
plt.xlabel("Age")
plt.ylabel("Height")
plt.show()
```

This is a useful beginner workflow because it connects three ideas early:

- imported files become tables you can inspect
- table columns become inputs to analysis
- plots are part of reasoning, not decoration

The goal is not to make a perfect chart on the first pass. The goal is to shorten the distance between raw data and a testable observation.

## A Healthy Beginner Mental Model

If you are new to data science, keep this order in mind:

1. understand the problem
2. inspect the data source
3. prepare and profile the data
4. choose the right analytical method
5. communicate the result in decision language

The common mistake is reversing the order and asking "Which model should I use?" before the data and the question are stable.

## Related Notes

- Use [Data Manipulation and EDA](./data-manipulation-and-eda/README.md) for profiling, missingness, and exploration before modeling.
- Use [Data Communication](./data-communication/README.md) for problem framing, stakeholder alignment, and decision-oriented reporting.
- Use [Statistics](./statistics/README.md) when the core task becomes estimation, hypothesis testing, or experimental reasoning.
- Use [Machine Learning](./machine-learning/README.md) when the core task becomes prediction, evaluation, and deployment.
