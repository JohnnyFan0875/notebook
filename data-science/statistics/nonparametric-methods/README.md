[Statistics](../README.md) › 無母數方法

# 無母數方法 (Non-parametric Methods)

不假設資料服從特定分配（如常態），通常改用**排名 (rank)** 或**符號 (sign)**。適合 Ordinal 資料、小樣本、嚴重偏態或有極端離群值的情況。

> 無母數 ≠ 沒有假設。它的假設較弱，而且**檢定的對象不同**（多半不是平均數）。

## 母數 vs 無母數對照

| 目的 | 母數方法 | 無母數替代 | 筆記 |
| --- | --- | --- | --- |
| 判斷要不要用 | — | — | [何時使用](when-and-why.md) |
| 單一樣本 vs 已知值 | 單一樣本 t | Wilcoxon signed-rank、Sign test | [單一樣本與配對](one-sample-and-paired.md) |
| 兩組配對 | 配對 t | Wilcoxon signed-rank | [單一樣本與配對](one-sample-and-paired.md) |
| 兩組獨立 | 獨立 t | Mann-Whitney U | [兩獨立樣本](two-independent-samples.md) |
| 3+ 組獨立 | 單因子 ANOVA | Kruskal-Wallis → Dunn's test | [Kruskal-Wallis](kruskal-wallis.md) |
| 3+ 次重複量測 | 重複量數 ANOVA | Friedman | [Kruskal-Wallis](kruskal-wallis.md#friedman-檢定重複量測) |
| 兩變數相關 | Pearson r | Spearman ρ、Kendall τ | [等級相關](rank-correlation.md) |
| 類別變數關聯 | — | 卡方、Fisher's exact | [卡方檢定](chi-square.md) |
| 任意統計量 | — | 置換檢定、Bootstrap | [重抽樣](../probability-and-distributions/monte-carlo-simulation.md) |
