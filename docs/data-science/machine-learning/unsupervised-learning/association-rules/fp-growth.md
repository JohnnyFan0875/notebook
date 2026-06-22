# FP-Growth

FP-Growth is an alternative to [Apriori](apriori.md) for mining frequent itemsets more efficiently.

## Why It Is Often Preferred

- Avoids generating large numbers of explicit candidate itemsets
- Can be much faster on large transactional datasets
- Uses a compressed tree structure called an FP-tree

## Core Idea

- Build an FP-tree from transactions
- Mine frequent patterns recursively from the tree

## 為什麼它通常更快

FP-Growth 不需要像 Apriori 一樣逐層產生大量候選組合，而是先把交易資料壓縮成 FP-tree，再從樹結構中遞迴挖掘頻繁模式。當資料集很大、交易很密集時，這個差異會非常明顯。

## Comparison with Apriori

- [Apriori](apriori.md): simpler to understand, often slower at scale
- FP-Growth: more efficient, especially when the dataset is large or dense

## Practical Notes

- Use when [Apriori](apriori.md) becomes computationally heavy.
- Still choose support, confidence, and lift [threshold](../../evaluation/classification-thresholds-and-calibration.md)s carefully.

## 什麼時候特別值得考慮

- 商品種類多、交易筆數多
- 資料相對 dense，Apriori 候選組合爆炸
- 你已經知道要做 market basket 類問題，但希望方法更具伸縮性

## Related Concepts

- [Association Rules](README.md)
- [Apriori](apriori.md)
- [Clustering](../clustering/README.md)
- [Feature Engineering Principles](../../foundations/feature-engineering-principles.md)

[Back to Association Rules](README.md)
