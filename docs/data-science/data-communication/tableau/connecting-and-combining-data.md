# Connecting and Combining Data in Tableau

## Why Data Combination Matters

In Tableau, visual quality depends heavily on whether the underlying data is combined correctly. A clean worksheet can still mislead if joins or unions were chosen incorrectly.

## Two Common Combination Patterns

| Pattern | Use when | Result |
| --- | --- | --- |
| Union | Tables share the same columns and should be stacked vertically | More rows |
| Join | Tables contain complementary columns and should be matched by keys | More columns |

## Union

A union appends records from multiple tables with the same schema.

Use it when:

- data is split across months, regions, or files
- each source has the same column structure
- you want one longer table for consistent downstream analysis

The main risk is schema inconsistency across files.

## Join

A join combines tables horizontally based on matching keys.

Typical join types:

| Join type | Effect |
| --- | --- |
| Inner join | Keep only matched rows |
| Left join | Keep all rows from the left table plus matches |
| Right join | Keep all rows from the right table plus matches |
| Full join | Keep matched and unmatched rows from both sides |

## Choosing the Right Join

The join decision should be driven by the business question and the expected grain of the data.

Ask:

- what is the key?
- what is the unit of analysis?
- do I need unmatched rows?
- will the join duplicate records unexpectedly?

Incorrect joins are a common source of inflated counts and broken aggregates.

## Practical Tableau Prep Questions

Before building views, check:

- do any fields need refinement?
- are there enough categorical fields for slicing and grouping?
- do some numeric fields belong in dimensions instead of measures?
- are additional calculated fields needed to tell the story?

## Practical Takeaways

- Use unions to stack like-with-like tables.
- Use joins to enrich one table with fields from another.
- Join type changes the row set, so it changes every downstream visual.
- Data modeling choices in Tableau are analytical decisions, not just UI actions.
