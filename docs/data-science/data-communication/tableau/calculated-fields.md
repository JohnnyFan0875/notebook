# Calculated Fields in Tableau

## Why Calculations Matter

Calculated fields let you create new analytical logic from data that already exists in the source.

They are commonly used to:

- create missing metrics
- transform existing fields
- recode or bucket categories
- build business logic directly into the visualization layer

## Main Calculation Types

Tableau calculations are often grouped into four broad categories:

| Type | Main idea |
| --- | --- |
| Row-level calculations | Evaluated on each record individually |
| Aggregate calculations | Evaluated over a set of records in the current view |
| Level of Detail expressions | Define aggregation at a specific grain independent of the visible view |
| Table calculations | Compute across already rendered values in the worksheet |

## Row-Level vs Aggregate Logic

This distinction is one of the most important Tableau concepts.

| Type | Meaning |
| --- | --- |
| Row-level | Works record by record before aggregation |
| Aggregate | Works on grouped data such as `SUM()` or `AVG()` |

Many Tableau calculation errors happen because row-level and aggregate logic are mixed incorrectly.

## Typical Use Cases

- derived margins or ratios
- date part extraction
- customer segmentation buckets
- conditional labels
- comparison fields used in dashboards

## Common Error Patterns

Watch for:

- mixing row-level and aggregate expressions unintentionally
- applying functions to incompatible data types
- syntax problems such as missing `END`, commas, or brackets

A valid formula can still be analytically wrong if the aggregation level does not match the business meaning.

## Good Practices

- decide first whether the logic belongs at row level or grouped level
- keep formulas small and composable when possible
- name calculated fields by business meaning, not just implementation
- verify the result against a manual spot-check before using it in a dashboard

## Practical Takeaways

- Calculated fields are part of the analytical model, not just convenience helpers.
- The most important design choice is often the level at which the calculation should happen.
- Strong Tableau work depends on aligning formulas with business grain, aggregation, and interpretation.
