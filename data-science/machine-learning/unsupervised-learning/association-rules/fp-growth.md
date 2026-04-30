# FP-Growth



FP-Growth is an alternative to [Apriori](apriori.md) for mining frequent itemsets more efficiently.

## Why It Is Often Preferred

- Avoids generating large numbers of explicit candidate itemsets
- Can be much faster on large transactional datasets
- Uses a compressed tree structure called an FP-tree

## Core Idea

- Build an FP-tree from transactions
- Mine frequent patterns recursively from the tree

## Comparison with Apriori

- [Apriori](apriori.md): simpler to understand, often slower at scale
- FP-Growth: more efficient, especially when the dataset is large or dense

## Practical Notes

- Use when [Apriori](apriori.md) becomes computationally heavy.
- Still choose support, confidence, and lift [threshold](../../evaluation/classification-thresholds-and-calibration.md)s carefully.

## Related Concepts

- [Association Rules](README.md)
- [Apriori](apriori.md)
- [Clustering](../clustering/README.md)
- [Feature Engineering Principles](../../foundations/feature-engineering-principles.md)

[Back to Association Rules](README.md)
