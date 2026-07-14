# A/B Testing

**A/B testing** is a randomized experiment used to compare a current experience against one or more variants. It is one of the most common modern applications of experimental design because it connects causal inference, product decisions, and large-scale behavioral data.

Key point: An A/B test is not just "compare two dashboards and look at the p-value." The design has to specify the unit of randomization, the metric, the stopping rule, and the decision threshold before results are inspected.

## When A/B Testing Is A Good Fit

A/B testing is especially useful when:

- you want to compare a current experience against a proposed change
- random assignment is operationally feasible
- the metric can be defined clearly before launch
- the expected effect is incremental rather than dramatic

Common examples:

- conversion-rate optimization
- signup or checkout flow changes
- ad or notification experiments
- feature-release experiments

The fit is strongest when:

- users can be randomized independently
- the product change affects user behavior directly
- the outcome can be observed within a reasonable measurement window

Do not default to an A/B test when:

- traffic is too low to reach a meaningful sample size
- there is no clear, testable hypothesis
- ethical constraints make random assignment inappropriate
- the opportunity cost of delaying a decision is too high

Be especially careful when:

- users influence each other heavily, creating network effects
- spillovers between control and treatment are hard to prevent
- the intervention changes market-wide or system-wide conditions rather than individual behavior

Tip: A/B testing is best for decisions with clean unit-level assignment. It is a weaker fit when the treatment effect is entangled across users and cannot be isolated cleanly.

Tip: "Can we run a test?" is not the first question. The first question is "Would this decision become materially better if we learned the answer experimentally?"

## A Practical Workflow

An A/B test usually follows this sequence:

1. define the decision, metric, and variants
2. state the hypothesis and the minimum effect worth detecting
3. estimate the required sample size and stopping rule
4. randomize users into control and treatment
5. validate logging and perform sanity checks
6. aggregate the metric at the correct analysis unit
7. run the appropriate statistical test
8. interpret the effect size, confidence interval, and business impact together

Tip: The metric definition is part of the design, not a post-hoc analytics choice. Changing the primary metric after launch is usually a form of researcher degrees of freedom.

## Metric Definitions Need Eligibility Rules

A metric is not fully defined until the inclusion rules are explicit. This matters whenever users enter the funnel at different times or have different exposure windows.

Example: suppose the metric is **week-two conversion rate after a free trial**. The eligible population might be:

- users who completed the free trial
- users who did not subscribe during week one
- users who had a full second week in which conversion could be observed

Without those rules, the same phrase can describe multiple different denominators.

Tip: Before launch, write the metric as if an analyst had to implement it from scratch with no extra verbal explanation.

## Writing A Better Product Hypothesis

A useful A/B-test hypothesis is concrete enough to connect a product change to a measurable outcome:

```text
Based on X, we believe that if we do Y,
then Z will happen,
as measured by metric M.
```

Example:

```text
Based on user-research evidence, we believe that if we simplify the checkout page,
then the percentage of purchasing users will increase,
as measured by purchase rate.
```

This naturally maps to the statistical framing:

- **Null hypothesis (H0):** the change does not affect the primary metric
- **Alternative hypothesis (H1):** the change affects the primary metric in the prespecified direction or in either direction

Tip: Good product hypotheses are testable, concise, and action-oriented. Vague statements like "make the page better" are hard to falsify and even harder to learn from.

## The Analysis Unit Matters More Than Many Teams Realize

In digital experiments, raw logs often contain repeated events from the same user. That means the row in the table is not always the independent unit for inference.

Warning: If treatment is assigned at the **user** level, the analysis should usually also be performed at the **user** level. Treating repeated events from the same user as if they were independent observations inflates precision and can produce misleadingly small p-values.

For binary outcomes such as signup or purchase, a common pattern is:

```python
# One row per user after aggregation
summary = (
    events
    .groupby(['variant', 'user_id'])['purchased']
    .max()
    .reset_index()
)

conversion = summary.groupby('variant')['purchased'].agg(['sum', 'count'])
conversion['rate'] = conversion['sum'] / conversion['count']
print(conversion)
```

Why use `.max()` here: if a user purchases multiple times, the conversion question is usually "did the user convert at least once?" That is a user-level event, not an event-counting problem.

For between-subject A/B tests, long/tidy data is usually the cleanest storage pattern:

| Format | Structure | Better Choice? |
| ------ | --------- | -------------- |
| Wide | one column per variant, many structural missing values | usually no |
| Long | one row per unit, one column for variant, one for outcome | yes |

Tip: Long format is usually easier to validate, group, visualize, and pass into statistical workflows. A/B test data with separate columns for each variant often creates unnecessary missing values and fragile code.

## Metric Type Drives Test Choice

The statistical test should follow the metric structure, not team habit.

| Metric Type | Common Example | Typical Comparison |
| ----------- | -------------- | ------------------ |
| Binary proportion | signup, click, purchase | two-proportion z-test or chi-square |
| Continuous mean | time on page, revenue per user | Welch's t-test |
| Ratio metric | revenue per session, clicks per user | ratio-aware methods such as the delta method |

See [Common Statistical Tests](../inferential-statistics/statistical-tests.md) for the core test-selection logic.

Tip: Many product metrics are better defined per user than per event. "Revenue per user" and "clicks per user" usually align with user-level randomization more naturally than raw event totals.

## Ratio Metrics Need Extra Care

Ratio metrics are common in product analytics:

- revenue per session
- clicks per user
- orders per visitor

These are not simple means of independent rows when each user contributes both a numerator and a denominator.

A robust workflow is:

1. aggregate numerator and denominator at the user level
2. compute the ratio metric per variant
3. use a method that accounts for ratio variance, such as a delta-method approximation

```python
A_per_user = pd.DataFrame({
    'order_value': checkout[checkout['checkout_page'] == 'A'].groupby('user_id')['order_value'].sum(),
    'page_view': checkout[checkout['checkout_page'] == 'A'].groupby('user_id')['user_id'].count(),
})

B_per_user = pd.DataFrame({
    'order_value': checkout[checkout['checkout_page'] == 'B'].groupby('user_id')['order_value'].sum(),
    'page_view': checkout[checkout['checkout_page'] == 'B'].groupby('user_id')['user_id'].count(),
})
```

Tip: The main design lesson is more important than the specific formula. Build ratio metrics from the same independent unit that was randomized, then choose an inference method that respects that structure.

## Sanity Checks Before Inference

Before testing the main outcome, check whether the experiment behaved as designed:

- assignment counts are reasonably balanced
- observable user characteristics are reasonably balanced across variants
- logging coverage is consistent across variants
- eligibility rules were applied correctly
- duplicates caused by instrumentation issues were removed
- the metric trend over time looks operationally plausible
- important time effects such as weekday vs. weekend exposure were not ignored
- unusual calendar effects such as holidays or major events are accounted for

Warning: A statistically significant result from broken instrumentation is still broken evidence.

Tip: Balance checks do not prove that randomization worked perfectly, but they are a strong first filter for obvious assignment or data-pipeline problems.

Warning: Be careful when a metric was unusually high or low before the intervention. Some apparent "improvements" are simply **regression to the mean** rather than a real treatment effect.

## Peeking And Multiple Comparisons

One of the most common mistakes in experimentation is repeatedly checking significance during data collection and stopping as soon as the result looks favorable.

Warning: Optional stopping inflates false positive rates. In practical terms, repeatedly "peeking" at the p-value behaves like running multiple comparisons without correcting for them.

That is why the stopping rule should be specified before launch:

- fixed sample size
- fixed experiment duration
- or a formal sequential-testing design

If you compare multiple variants or many primary outcomes, your false-positive risk rises further. This connects directly to the multiple-comparisons issue covered elsewhere in statistics.

## Interpreting Results Like A Decision-Maker

A mature A/B-test readout should answer all of these:

1. What is the estimated lift or difference?
2. What is the confidence interval?
3. Is the result statistically compatible with no effect?
4. Is the effect large enough to matter in practice?
5. What design or data-quality risks remain?

Tip: Statistical significance alone is rarely the business decision. A tiny but precise uplift may be unimportant, while a meaningful uplift with a wide interval may justify a longer follow-up test.

## Key Takeaways

| Idea | Why It Matters |
| ---- | -------------- |
| Randomization unit drives analysis unit | Prevents pseudoreplication and inflated certainty |
| Metrics must be defined before launch | Protects against p-hacking and post-hoc storytelling |
| Ratio metrics are special | They often require user-level aggregation and ratio-aware inference |
| Peeking is a design problem, not a dashboard habit | It inflates false positives |
| Effect size + CI + business value | Better decision rule than p-value alone |
