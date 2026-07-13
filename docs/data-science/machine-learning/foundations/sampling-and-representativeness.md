# Sampling and Representativeness

A model can only learn from the data it sees.
If the data are not representative of the real deployment setting, even a strong model can fail.

## Core Ideas

- **Sampling bias**: the training data are collected in a biased way
- **Selection bias**: some groups are more likely to appear than others
- **Distribution shift**: training and future data come from different distributions

## Why This Matters

- Validation results may not reflect real-world [performance](generalization.md).
- Some groups may be underrepresented.
- Rare but important cases may be missed entirely.

## Common Examples

- Training a fraud model on only reviewed cases
- Training a medical model from one hospital and applying it elsewhere
- Using historical data collected under a different business policy

## Questions to Ask

- Who or what is missing from the data?
- Does the sample reflect the production population?
- Are important edge cases represented?
- Has the data-generating process changed over time?

## Survey-Specific Sampling Pitfalls

Survey data adds an extra layer of risk because the sample is often filtered twice:

- who was invited
- who actually responded

This means a survey can look large and still be unrepresentative.

### Response Rate vs. Response Bias

A higher response rate is usually better, but the real issue is whether non-responders differ systematically from responders.

Examples:

- unhappy customers ignore a satisfaction survey
- overworked employees skip an internal questionnaire
- older or less connected users never see an online-only form

Key point: Non-response is not just "missing rows." It can change the composition of the observed sample and distort downstream estimates.

### Representativeness Checks with Simple Proportions

One practical survey habit is to compare subgroup proportions between the population frame and the realized sample.

```python
pop_gender = survey["gender"].value_counts(normalize=True).rename("population")
sample_gender = sample["gender"].value_counts(normalize=True).rename("sample")

comparison = pd.concat([pop_gender, sample_gender], axis=1)
comparison["gap"] = comparison["sample"] - comparison["population"]
comparison
```

If the gaps are large for important groups, the sample may not support broad inference without redesign or weighting.

### Stratified Sampling as a Representation Tool

When you already know some subgroups matter, a stratified sample is often more useful than a plain random sample.

```python
strat_sample = (
    survey.groupby("gender", group_keys=False)
    .apply(lambda g: g.sample(frac=0.1, random_state=42))
)
```

Use this when:

- subgroup balance matters
- you expect outcome differences by subgroup
- a simple random sample may miss smaller but important groups

### Quotas and Weighting Solve Different Problems

Two ideas are often mixed together in survey work:

- stratified or quota-like sampling tries to shape who enters the sample
- weighting tries to correct how much influence each observed row should have in analysis

Key point: Fixing representation at collection time is usually safer than hoping analysis-time weighting will rescue a badly skewed sample.

## Practical Rule

Bad data coverage cannot be fixed purely by a better algorithm.

## Related Concepts

- [Generalization](generalization.md)
- [Evaluation Mindset](evaluation-mindset.md)
- [Model Lifecycle](../workflow/model-lifecycle.md)
- [Deployment and Monitoring](../production/deployment-and-monitoring.md)

[Back to Foundations](README.md)
