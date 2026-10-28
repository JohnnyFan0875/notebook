[Machine Learning](../../README.md) › [非監督式學習](../README.md) › 關聯規則

# 關聯規則 (Association Rules)

在交易型資料中找「常一起出現的項目」，並產生 `A → B` 形式的規則。經典應用是購物籃分析，也可用在共同出現的症狀、處方、突變或網頁瀏覽路徑。

## 指標

| 指標 | 定義 | 意義 |
| --- | --- | --- |
| Support | $P(A \cap B)$ | 規則有多常見 |
| Confidence | $P(B \mid A) = \frac{\text{support}(A \cap B)}{\text{support}(A)}$ | 買了 A 的人有多少比例也買 B |
| **Lift** | $\frac{P(B \mid A)}{P(B)}$ | 比「B 本來的出現率」高幾倍；**1 = 獨立**、> 1 正相關、< 1 負相關 |
| Leverage | $P(A \cap B) - P(A)P(B)$ | 實際共現比獨立時多出多少 |
| Conviction | $\frac{1 - P(B)}{1 - \text{confidence}}$ | 規則「失敗」比獨立時少幾倍 |

> **只看 confidence 會被誤導**：B 本身很常見時，任何 A → B 的 confidence 都會很高。下面例子中 bread → milk 的 confidence 0.75，但 lift 0.94 < 1，代表買麵包的人買牛奶的比例**反而略低於**平均。先看 lift。

## 流程

```
交易資料 → one-hot（交易 × 項目的布林矩陣）→ 找頻繁項目集（min_support）→ 產生規則（min confidence / lift）→ 篩選與解讀
```

| 演算法 | 筆記 | 特性 |
| --- | --- | --- |
| Apriori | [Apriori](apriori.md) | 逐層產生候選、剪枝；概念簡單 |
| FP-Growth | [FP-Growth](fp-growth.md) | 壓縮成樹再挖掘，不產生候選；大資料較快 |

兩者找到的頻繁項目集相同，差別只在速度。

## 解讀提醒

| 提醒 | 說明 |
| --- | --- |
| 高 support = 常見，不一定有用 | 「大家都買牛奶」不是洞見 |
| 高 confidence 可能只是 B 很常見 | 用 lift 對照獨立的基準 |
| 共現 ≠ 因果 | `A → B` 不代表 A 導致 B |
| 規則很多 ≠ 洞見很多 | 要結合業務 / 領域背景篩選可行動的規則 |
| support 太低的規則不穩定 | 罕見組合的 lift 容易因幾筆交易而很極端 |
| 多重比較 | 上千條規則中總有一些純屬偶然；重要的規則要在另一段時間的資料上驗證 |
