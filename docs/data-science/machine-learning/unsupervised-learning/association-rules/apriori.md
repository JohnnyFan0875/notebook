# Apriori

Apriori is an algorithm for mining frequent itemsets and generating association rules from transactional data.

## Typical Use Case

- Market basket analysis
- Product bundling
- Co-purchase pattern discovery

## Core Terms

- **Support**: how often an itemset appears
- **Confidence**: how often the rule is correct given the left-hand side
- **Lift**: how much more often the rule occurs than expected by chance

## Main Idea

- Frequent supersets can only come from frequent subsets
- Candidate itemsets are expanded level by level
- Infrequent candidates are pruned early

## Practical Notes

- Apriori can become expensive on large, dense datasets.
- Start with sensible minimum support [threshold](../../evaluation/classification-thresholds-and-calibration.md)s.
- Lift is often more informative than confidence alone.

## Related Concepts

- [Association Rules](README.md)
- [FP-Growth](fp-growth.md)
- [Clustering](../clustering/README.md)
- [Feature Engineering Principles](../../foundations/feature-engineering-principles.md)

[Back to Association Rules](README.md)
