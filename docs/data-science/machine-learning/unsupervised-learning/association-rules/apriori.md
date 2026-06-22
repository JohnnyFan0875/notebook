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

## 為什麼這個想法有效

如果某個二項組合本身就不常出現，那把它再加更多商品，只會更不可能常見。因此 Apriori 可以利用這個性質提早刪掉大量不可能成為 frequent itemset 的候選組合。

## 一個簡單例子

如果 `{"bread", "milk"}` 都不常一起出現，那 `{"bread", "milk", "eggs"}` 就更不需要繼續考慮。這讓搜尋空間能被逐層修剪。

## Practical Notes

- Apriori can become expensive on large, dense datasets.
- Start with sensible minimum support [threshold](../../evaluation/classification-thresholds-and-calibration.md)s.
- Lift is often more informative than confidence alone.

## 常見誤解

- `bread -> milk` 的 confidence 高，不代表買麵包會導致買牛奶。
- 規則很多不等於洞見很多，通常需要結合業務背景挑出可行規則。
- support 太低時，容易挖出看似驚喜但其實不穩定的稀有規則。

## Related Concepts

- [Association Rules](README.md)
- [FP-Growth](fp-growth.md)
- [Clustering](../clustering/README.md)
- [Feature Engineering Principles](../../foundations/feature-engineering-principles.md)

[Back to Association Rules](README.md)
