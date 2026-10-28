# Tableau

Tableau 是偏向分析與溝通交界處的 BI 工具：把資料來源、計算欄位、分析視角與 dashboard 交付串成一個工作流。

## Overview and Workflow

### What Tableau Is Good At

Tableau is a visual analytics tool built for interactive exploration, fast prototyping, and stakeholder-facing dashboards.

Its practical strengths are:

- low-friction visual exploration through drag-and-drop
- fast iteration on questions and chart design
- interactive dashboards for self-serve analysis
- a workflow that connects data prep, calculation, and presentation

### Where Tableau Fits in the Analytics Process

A useful Tableau mental model is:

`question framing -> connect data -> define fields -> analyze -> compose dashboard -> communicate decisions`

This matters because Tableau is most effective when it is treated as the delivery layer of an analysis workflow, not just a charting surface.

### Typical Workflow

| Step | Main question |
| --- | --- |
| Connect | Which data sources and tables are needed? |
| Prepare | Do fields need cleaning, recoding, or regrouping? |
| Calculate | Which metrics or derived fields are missing? |
| Analyze | Which dimensions and measures reveal the pattern? |
| Present | Which worksheet or dashboard best supports the decision? |

### Dimensions and Measures

Tableau relies heavily on the distinction between dimensions and measures.

| Type | Meaning |
| --- | --- |
| Dimension | Categorical or qualitative field used to group, slice, or label |
| Measure | Numeric field that is usually aggregated |

One common modeling task is reclassifying fields when a numeric value should behave like a label instead of an aggregatable metric.

### Why People Use Tableau

- accessible to both analysts and business users
- strong support for exploratory analysis
- fast path from prototype to stakeholder-ready dashboard
- suitable for turning business questions into interactive visual products

### Dashboard Role

Dashboards in Tableau combine multiple worksheets into one interactive decision surface.

They are most useful when the goal is not just to show one chart, but to support:

- drill-down
- comparison across segments
- KPI monitoring
- guided exploration

The broader design principles still live in [Dashboard Design](../dashboard-design.md).

### Practical Takeaways

- Tableau is strongest when it sits between analysis and communication.
- Good Tableau work starts with the analytical question, not with a blank dashboard.
- Dimensions, measures, calculated fields, and data relationships determine what the visuals can say.
- Dashboards are most valuable when they support decisions, not when they simply showcase interactivity.

## Connecting and Combining Data

### Why Data Combination Matters

In Tableau, visual quality depends heavily on whether the underlying data is combined correctly. A clean worksheet can still mislead if joins or unions were chosen incorrectly.

### Two Common Combination Patterns

| Pattern | Use when | Result |
| --- | --- | --- |
| Union | Tables share the same columns and should be stacked vertically | More rows |
| Join | Tables contain complementary columns and should be matched by keys | More columns |

### Union

A union appends records from multiple tables with the same schema.

Use it when:

- data is split across months, regions, or files
- each source has the same column structure
- you want one longer table for consistent downstream analysis

The main risk is schema inconsistency across files.

### Join

A join combines tables horizontally based on matching keys.

Typical join types:

| Join type | Effect |
| --- | --- |
| Inner join | Keep only matched rows |
| Left join | Keep all rows from the left table plus matches |
| Right join | Keep all rows from the right table plus matches |
| Full join | Keep matched and unmatched rows from both sides |

### Choosing the Right Join

The join decision should be driven by the business question and the expected grain of the data.

Ask:

- what is the key?
- what is the unit of analysis?
- do I need unmatched rows?
- will the join duplicate records unexpectedly?

Incorrect joins are a common source of inflated counts and broken aggregates.

### Practical Tableau Prep Questions

Before building views, check:

- do any fields need refinement?
- are there enough categorical fields for slicing and grouping?
- do some numeric fields belong in dimensions instead of measures?
- are additional calculated fields needed to tell the story?

### Practical Takeaways

- Use unions to stack like-with-like tables.
- Use joins to enrich one table with fields from another.
- Join type changes the row set, so it changes every downstream visual.
- Data modeling choices in Tableau are analytical decisions, not just UI actions.

## Calculated Fields

### Why Calculations Matter

Calculated fields let you create new analytical logic from data that already exists in the source.

They are commonly used to:

- create missing metrics
- transform existing fields
- recode or bucket categories
- build business logic directly into the visualization layer

### Main Calculation Types

Tableau calculations are often grouped into four broad categories:

| Type | Main idea |
| --- | --- |
| Row-level calculations | Evaluated on each record individually |
| Aggregate calculations | Evaluated over a set of records in the current view |
| Level of Detail expressions | Define aggregation at a specific grain independent of the visible view |
| Table calculations | Compute across already rendered values in the worksheet |

### Row-Level vs Aggregate Logic

This distinction is one of the most important Tableau concepts.

| Type | Meaning |
| --- | --- |
| Row-level | Works record by record before aggregation |
| Aggregate | Works on grouped data such as `SUM()` or `AVG()` |

Many Tableau calculation errors happen because row-level and aggregate logic are mixed incorrectly.

### Typical Use Cases

- derived margins or ratios
- date part extraction
- customer segmentation buckets
- conditional labels
- comparison fields used in dashboards

### Common Error Patterns

Watch for:

- mixing row-level and aggregate expressions unintentionally
- applying functions to incompatible data types
- syntax problems such as missing `END`, commas, or brackets

A valid formula can still be analytically wrong if the aggregation level does not match the business meaning.

### Good Practices

- decide first whether the logic belongs at row level or grouped level
- keep formulas small and composable when possible
- name calculated fields by business meaning, not just implementation
- verify the result against a manual spot-check before using it in a dashboard

### Practical Takeaways

- Calculated fields are part of the analytical model, not just convenience helpers.
- The most important design choice is often the level at which the calculation should happen.
- Strong Tableau work depends on aligning formulas with business grain, aggregation, and interpretation.
