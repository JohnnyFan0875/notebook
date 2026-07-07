# Tableau Overview and Workflow

## What Tableau Is Good At

Tableau is a visual analytics tool built for interactive exploration, fast prototyping, and stakeholder-facing dashboards.

Its practical strengths are:

- low-friction visual exploration through drag-and-drop
- fast iteration on questions and chart design
- interactive dashboards for self-serve analysis
- a workflow that connects data prep, calculation, and presentation

## Where Tableau Fits in the Analytics Process

A useful Tableau mental model is:

`question framing -> connect data -> define fields -> analyze -> compose dashboard -> communicate decisions`

This matters because Tableau is most effective when it is treated as the delivery layer of an analysis workflow, not just a charting surface.

## Typical Workflow

| Step | Main question |
| --- | --- |
| Connect | Which data sources and tables are needed? |
| Prepare | Do fields need cleaning, recoding, or regrouping? |
| Calculate | Which metrics or derived fields are missing? |
| Analyze | Which dimensions and measures reveal the pattern? |
| Present | Which worksheet or dashboard best supports the decision? |

## Dimensions and Measures

Tableau relies heavily on the distinction between dimensions and measures.

| Type | Meaning |
| --- | --- |
| Dimension | Categorical or qualitative field used to group, slice, or label |
| Measure | Numeric field that is usually aggregated |

One common modeling task is reclassifying fields when a numeric value should behave like a label instead of an aggregatable metric.

## Why People Use Tableau

- accessible to both analysts and business users
- strong support for exploratory analysis
- fast path from prototype to stakeholder-ready dashboard
- suitable for turning business questions into interactive visual products

## Dashboard Role

Dashboards in Tableau combine multiple worksheets into one interactive decision surface.

They are most useful when the goal is not just to show one chart, but to support:

- drill-down
- comparison across segments
- KPI monitoring
- guided exploration

The broader design principles still live in [Dashboard Design](../../data-manipulation-and-eda/visualization/dashboard-design.md).

## Practical Takeaways

- Tableau is strongest when it sits between analysis and communication.
- Good Tableau work starts with the analytical question, not with a blank dashboard.
- Dimensions, measures, calculated fields, and data relationships determine what the visuals can say.
- Dashboards are most valuable when they support decisions, not when they simply showcase interactivity.
