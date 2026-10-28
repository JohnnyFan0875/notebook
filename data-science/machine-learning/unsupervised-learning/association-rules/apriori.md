[Machine Learning](../../README.md) › [非監督式學習](../README.md) › [關聯規則](README.md) › Apriori

# Apriori

逐層找出頻繁項目集 (frequent itemsets)，再從中產生關聯規則。指標定義見 [關聯規則](README.md)。

## 核心性質：向下封閉 (downward closure)

> 一個項目集若是頻繁的，它的所有子集也一定是頻繁的；反過來，**不頻繁的項目集，其所有超集都不可能頻繁**。

例：`{bread, milk}` 一起出現的比例已經低於 `min_support`，那 `{bread, milk, eggs}` 只會更少，不必再算。Apriori 就靠這個性質逐層剪枝：

```
找頻繁 1-項目集 → 只用它們組合出 2-項目集候選 → 算 support、刪掉不頻繁的
              → 用頻繁 2-項目集組出 3-項目集候選 → … 直到沒有新的頻繁項目集
```

## 用法（mlxtend）

```python
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

transactions = [["bread", "milk"],
                ["bread", "diapers", "beer", "eggs"],
                ["milk", "diapers", "beer", "cola"],
                ["bread", "milk", "diapers", "beer"],
                ["bread", "milk", "diapers", "cola"]]

# 1. 轉成交易 × 項目的布林矩陣
te = TransactionEncoder()
df = pd.DataFrame(te.fit(transactions).transform(transactions), columns=te.columns_)

# 2. 頻繁項目集
itemsets = apriori(df, min_support=0.6, use_colnames=True)
# bread / diapers / milk 0.8；beer 0.6；{diapers, beer}、{diapers, bread}、{milk, bread}、{diapers, milk} 0.6

# 3. 產生規則
rules = association_rules(itemsets, num_itemsets=len(df), metric="confidence", min_threshold=0.7)
rules.sort_values("lift", ascending=False)[["antecedents", "consequents", "support", "confidence", "lift"]]
#   {beer}    → {diapers}  support 0.6  confidence 1.00  lift 1.25
#   {diapers} → {beer}     support 0.6  confidence 0.75  lift 1.25
#   {bread}   → {milk}     support 0.6  confidence 0.75  lift 0.94   ← confidence 高但 lift < 1
```

> 新版 mlxtend 的 `association_rules()` 多了 `num_itemsets` 參數，請傳入交易筆數 `len(df)`；舊教學的寫法沒有這個參數。0.23.0–0.23.3 必須傳入，0.23.4 起改為選填（[changelog](https://rasbt.github.io/mlxtend/CHANGELOG/)）。本筆記以 mlxtend 0.25 驗證。

## 參數

| 參數 | 說明 | 太高 | 太低 |
| --- | --- | --- | --- |
| `min_support` | 頻繁項目集的最低出現比例 | 只剩人人都買的商品 | 候選組合爆炸、規則不穩定 |
| `metric` + `min_threshold` | 篩規則：`"confidence"`、`"lift"`、`"leverage"`… | 規則太少 | 規則太多 |
| `max_len`（apriori） | 項目集的最大長度 | — | 限制計算量 |

## 優缺點

| 優點 | 缺點 |
| --- | --- |
| 概念簡單、結果直觀 | 項目多或資料密集時候選組合爆炸，很慢 |
| 剪枝大幅減少搜尋 | 需要多次掃描資料 |
| — | 只能找共現，無法處理順序（序列模式要用其他方法） |

資料大時改用 [FP-Growth](fp-growth.md)，結果相同但通常快很多。
