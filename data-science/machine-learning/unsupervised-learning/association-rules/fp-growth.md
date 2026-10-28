[Machine Learning](../../README.md) › [非監督式學習](../README.md) › [關聯規則](README.md) › FP-Growth

# FP-Growth

找頻繁項目集的另一種演算法，結果與 [Apriori](apriori.md) **完全相同**，但通常快很多。它不逐層產生大量候選組合，而是先把交易壓縮成一棵 **FP-tree**（共享前綴的樹），再從樹上遞迴挖掘頻繁模式。

```
1. 掃描一次：計算每個項目的 support，刪掉不頻繁的項目
2. 再掃描一次：每筆交易依項目頻率排序後插入 FP-tree（共同前綴共用節點）
3. 從樹上對每個項目建立條件樹 (conditional FP-tree)，遞迴找頻繁模式
```

## 用法（mlxtend）

```python
from mlxtend.frequent_patterns import fpgrowth, association_rules

# df：TransactionEncoder 產生的布林矩陣（見 Apriori 筆記）
itemsets = fpgrowth(df, min_support=0.6, use_colnames=True)     # 和 apriori 的結果相同
rules = association_rules(itemsets, num_itemsets=len(df), metric="lift", min_threshold=1.0)
```

## Apriori vs FP-Growth

| | Apriori | FP-Growth |
| --- | --- | --- |
| 候選項目集 | 逐層產生大量候選 | 不產生 |
| 掃描資料次數 | 多次（每層一次） | 兩次 |
| 速度 | 項目多、資料密集時很慢 | 通常快很多 |
| 記憶體 | 候選集合可能很大 | FP-tree 在資料稀疏、前綴少共用時也可能很大 |
| 理解難度 | 低 | 較高 |
| 結果 | 相同 | 相同 |

## 什麼時候用

| 情境 | 選擇 |
| --- | --- |
| 項目多、交易多、資料密集 | FP-Growth |
| 教學、小資料 | 任一皆可 |
| 資料大到單機放不下 | Spark MLlib 的 `FPGrowth` |

無論哪個演算法，`min_support`、confidence、lift 的門檻都要謹慎設定，見 [關聯規則](README.md)。
