# Forming Analytical Questions

Forming analytical questions is the discipline of translating a broad business concern into a question that data, analysis, and a specific method can realistically answer.

Key point: `business question -> analytical question -> analytical solution -> business decision` 是一條完整鏈條。只做其中一段，通常無法真正產生價值。

## Why This Matters

Business teams often ask broad questions such as:

- Why is churn increasing?
- What campaigns should we run to attract new customers?
- How can we reduce costs?

These are important questions, but they are usually too broad to answer directly with one dataset or one technique. The analytics job is to translate them into narrower questions with clear scope, data requirements, and an answer format that supports action.

Warning: 如果問題一開始沒有界定對象、時間範圍或判斷標準，後面的分析很容易變成「做了很多圖，但仍然沒有回答決策問題」。

## The Translation Workflow

A practical workflow looks like this:

1. understand the strategic goal and team-level goal
2. identify the business question that needs to be answered
3. translate it into one or more analytical questions
4. select analytical solutions that can answer those questions
5. feed the analytical results back into business decision-making

| Stage | What happens | Typical output |
| --- | --- | --- |
| Business context | Clarify goals, constraints, and the business environment | A business question |
| Analytical framing | Narrow the question into measurable parts | One or more analytical questions |
| Method selection | Match the question to a suitable technique | Descriptive, diagnostic, predictive, or prescriptive approach |
| Decision support | Convert findings into recommendations | Inputs for action, prioritization, or experimentation |

## Business Questions vs Analytical Questions

Business questions and analytical questions differ along two main dimensions: scope and methodology.

| Dimension | Business question | Analytical question |
| --- | --- | --- |
| Scope | Broad, open-ended, decision-oriented | Specific, focused, answerable |
| Language | Business terms | Data and analysis terms |
| Evidence | May include intuition, experience, or expert opinion | Requires data and an explicit analytical method |
| Output | High-level direction | Measurable insight that supports the direction |

Example:

- Business question: What campaigns should we use to attract new customers?
- Analytical question: Which customer groups generated the most and least revenue over the last 6 months?
- Analytical question: How did past campaigns affect sales volume for each customer group?

Those analytical questions can then be answered with descriptive analysis and data visualization, and their outputs become inputs to a broader campaign discussion.

## What Makes a Good Analytical Question

A strong analytical question is usually:

- specific: it focuses on a clear part of the problem
- measurable: it can be answered with observable data
- actionable: the answer can influence a decision
- relevant: it ties back to the business objective
- time-bound: it defines a period or horizon

This is close to the SMART logic often used in planning.

Example:

- Weak: Which customers matter most?
- Stronger: Which customer group generated the most and least revenue in the last 6 months?

The stronger version identifies the target, metric, and time window, which makes method selection much easier.

## Discover What Really Matters

Before drafting analytical questions, clarify the problem with stakeholders. A clearly defined problem should usually answer:

1. what the business wants to know
2. what decisions need to be made
3. who will use the results
4. what other context or constraints matter

Useful communication habits:

- ask open-ended questions such as `Tell me more about...` or `What led you to this...?`
- paraphrase the problem in your own words and confirm it back with stakeholders
- summarize the key discoveries from the conversation before moving into analysis design

Tip: Paraphrasing is not just politeness. It is a fast validation step that catches hidden assumptions before they become analysis work.

## A Practical Process For Forming The Question

When the business question is still vague, this sequence works well:

1. extract the key elements from the business question
2. break the business question into smaller answerable parts
3. refine those parts into analytical questions
4. confirm that each analytical question still matters to the original decision

Checklist:

- What outcome are we trying to improve or explain?
- Which population, segment, product, or process is in scope?
- What time period matters?
- What data would be needed?
- What kind of answer would be useful: description, explanation, prediction, or recommendation?

## Match The Question To The Right Type Of Analysis

Many analytical questions become clearer once you decide what kind of answer is needed.

| Analytical type | Core question | Example techniques |
| --- | --- | --- |
| Descriptive | What happened? | Summary metrics, descriptive analysis, dashboards, visualization |
| Diagnostic | Why did it happen? | Drill-down analysis, root cause analysis, hypothesis testing, correlation or regression |
| Predictive | What will happen? | Forecasting, classification, predictive modeling |
| Prescriptive | What should we do? | Recommendation systems, optimization, decision rules |

### Descriptive Analytics

Use descriptive analytics when the first job is to understand patterns, trends, or performance.

Examples:

- What are the most common patient complaints in the last 3 months?
- Which suppliers had the most delayed deliveries in the last 6 months?
- Which customer segments generated the most and least revenue in the last 6 months?

Common techniques:

- descriptive summaries
- grouping and comparison
- dashboards
- data visualization

### Diagnostic Analytics

Use diagnostic analytics when you need to identify the drivers or root causes behind a change.

Examples:

- What factors contributed to the decline in enrollment rates over the last 2 years?
- Which manufacturing processes contributed to the rising defect rate?
- What variables are associated with declining email open rates?

Common techniques:

- drill-down analysis
- root cause analysis
- hypothesis testing
- correlation analysis
- regression analysis

### Predictive Analytics

Use predictive analytics when the business needs an estimate of what is likely to happen next.

Examples:

- What is the predicted demand for product X based on historical demand and related variables?
- What is the likelihood that a claim is fraudulent based on historical claims data?
- Can we predict which patients are at risk for a certain health condition?

Common techniques:

- time-series forecasting
- classification models
- predictive modeling

### Prescriptive Analytics

Use prescriptive analytics when the organization wants a suggested action, not just an estimate.

Examples:

- How should prices be adjusted in real time to maximize airline sales?
- Which product should be recommended to a customer next?
- Which retention strategy should be prescribed for customers at high risk of churn?

Common techniques:

- recommendation algorithms
- optimization methods
- decision policies and rules

## One Business Problem Can Produce Several Analytical Questions

A single business problem often requires multiple analytical lenses.

Example:

- Business question: How can we identify which loan applications are most likely to default?
- Descriptive question: Which loan applications defaulted in the past?
- Diagnostic question: Why do certain applications tend to default?
- Predictive question: Can we predict the probability of default from application variables?

This pattern matters because teams often jump straight to prediction before first understanding the baseline and the drivers.

Key point: Descriptive, diagnostic, predictive, and prescriptive work are not competing choices. They often form a sequence.

## Common Failure Modes

- Starting from a preferred method instead of the business need
- Asking a question that the available data cannot answer
- Keeping the question too broad for one analysis cycle
- Producing an answer that is statistically correct but not decision-useful
- Forgetting to confirm whether stakeholders interpret the result the same way

## Practical Heuristics

If you are unsure whether the question is ready, ask:

- Can I point to the exact metric or outcome?
- Do I know which entity or segment is being studied?
- Do I know the relevant time horizon?
- Can I name a realistic dataset?
- Can I describe the likely analysis family?
- Will the answer change a real decision?

If several answers are still `no`, the question probably needs another round of refinement.

## Related Notes

- If the task becomes causal or experimental, continue into [Experimental Design](../statistics/experimental-design/README.md).
- If the task becomes forecasting or prediction, connect this note with [Machine Learning](../machine-learning/README.md).
- If the task becomes chart design and message delivery, connect this note with [Visualization](../data-manipulation-and-eda/visualization/README.md).
