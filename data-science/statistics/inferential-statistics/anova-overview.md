[Statistics](../README.md) › [推論統計](README.md) › ANOVA 總覽

# 變異數分析總覽 (ANOVA Overview)

ANOVA (analysis of variance) 比較三組以上的平均數，問的是：**組間差異是否大於組內的隨機變異？**

$$
F = \frac{MS_{between}}{MS_{within}} = \frac{\text{組別能解釋的變異}}{\text{組內隨機變異}}
$$

F ≈ 1 → 組間差異與雜訊差不多；F ≫ 1 → 至少一組平均數不同。

> ANOVA 是**整體檢定 (omnibus test)**：只回答「是否至少一組不同」，不回答「是哪幾組」。顯著後需要 [事後檢定](post-hoc-effect-size.md)。
>
> ANOVA 本質是**類別自變數的線性迴歸**（`y ~ C(group)`），不必當成孤立的公式背。

## 選哪一種

| 設計 | 方法 | 筆記 |
| --- | --- | --- |
| 一個因子、3+ 獨立組 | 單因子 ANOVA | [One-Way ANOVA](one-way-anova.md) |
| 兩個因子（含交互作用） | 二因子 ANOVA | [Two-Way ANOVA](two-way-anova.md) |
| 同一受試者重複量測 | 重複量數 ANOVA | [Repeated-Measures ANOVA](repeated-measures-anova.md) |
| 找出哪幾組不同、差多大 | 事後檢定 + 效果量 | [Post-hoc & Effect Size](post-hoc-effect-size.md) |
| 加入連續共變數 | ANCOVA | `y ~ C(group) + covariate` |
| 多個結果變數 | MANOVA | [多變量分析](../multivariate-analysis/README.md) |

## 假設

| 假設 | 檢查 | 不成立時 |
| --- | --- | --- |
| 觀測獨立 | 研究設計 | 重複量數 ANOVA、混合模型 |
| 組內殘差近似常態 | Q–Q 圖 | Kruskal-Wallis、資料轉換 |
| 各組變異數相等 | Levene's | Welch's ANOVA + Games-Howell |

## 解讀順序

1. 確認研究設計與 ANOVA 類型相符
2. 先畫 boxplot / violin，看各組分布與樣本數
3. 看整體 F 檢定
4. 顯著 → 事後檢定
5. 報告效果量與各組平均，不只 p 值

## 常見錯誤

| 錯誤 | 問題 |
| --- | --- |
| 用很多個 t 檢定取代 ANOVA | 型一錯誤膨脹（3 組要比 3 次，10 組要比 45 次） |
| 不看圖就解讀 | 漏掉離群值、偏態、變異不等 |
| 只報 p 值 | 看不出差異的大小與方向 |
| 忽略變異不等（尤其各組 n 不同時） | 標準 F 檢定不可靠 |
