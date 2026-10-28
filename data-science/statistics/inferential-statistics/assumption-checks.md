[Statistics](../README.md) › [推論統計](README.md) › 假設檢查

# 假設檢查 (Assumption Checks)

母數檢定（t 檢定、ANOVA、迴歸）的前提不成立時，p 值可能無效、型一錯誤膨脹。先檢查，再檢定。

## 三大假設

| 假設 | 需要的方法 | 檢查 | 不成立時 |
| --- | --- | --- | --- |
| **獨立性** (independence) | 所有母數檢定 | **研究設計**、Durbin-Watson | 配對檢定、[混合效應模型](../regression-analysis/mixed-effects-models.md)、GEE、[ARIMA](../time-series-analysis/arima.md) |
| **常態性** (normality) | t 檢定、ANOVA（對殘差） | Q–Q 圖、Shapiro-Wilk | 轉換資料、[無母數方法](../nonparametric-methods/README.md)、n 大時依賴 CLT |
| **變異數同質** (homoscedasticity) | Student's t、ANOVA | Levene's test | Welch's t / Welch's ANOVA |

> **檢查順序：獨立 → 常態 → 等變異**。獨立性是設計問題，一旦違反，其他檢查都沒意義，而且它造成的傷害最大。
>
> 迴歸的假設是針對**殘差**，不是原始資料，見 [迴歸診斷](../multivariate-analysis/assumptions-diagnostics.md)。

## 常態性 (Normality)

H₀：資料來自常態分配。**先看圖**，再看檢定。Q–Q 圖的判讀見 [單變數：數值型](../descriptive-statistics/univariate-numerical.md#視覺診斷)。

| 方法 | 適用 | 特點 |
| --- | --- | --- |
| Q–Q 圖 | 任何 n | **最實用**，能看出偏態、厚尾、離群 |
| Shapiro-Wilk | n ≤ 2000 | 小樣本檢定力最好 |
| Kolmogorov-Smirnov | 一般用途 | 比較經驗 CDF 與理論 CDF；參數由資料估計時需 Lilliefors 校正 |
| Anderson-Darling | 任何 n | 對**尾部**偏離更敏感 |

```python
import scipy.stats as stats
import matplotlib.pyplot as plt
from statsmodels.stats.diagnostic import lilliefors

stats.probplot(data, dist="norm", plot=plt); plt.show()    # Q–Q 圖
stats.shapiro(data)                                        # Shapiro-Wilk：p ≤ 0.05 → 偏離常態
lilliefors(data, dist="norm")                              # K-S（Lilliefors 校正）
stats.anderson(data, dist="norm")                          # statistic > critical value → 拒絕
```

> **常態檢定的兩難**
>
> - n 小（最需要常態假設時）：檢定力不足，偏離了也測不出來。
> - n 大（> 200）：微不足道的偏離也會顯著，但此時 CLT 已讓 t 檢定很穩健。
>
> 所以**以 Q–Q 圖為主**，並思考偏離的程度是否嚴重（強烈偏態、極端離群、Ordinal 資料）。

**不常態時**：(1) log、sqrt、Box-Cox 轉換，見 [資料轉換](../descriptive-statistics/univariate-numerical.md#資料轉換-transformation)；(2) 無母數檢定；(3) n ≥ 30 且偏離輕微時，依賴 CLT；(4) [Bootstrap](../probability-and-distributions/monte-carlo-simulation.md) 或置換檢定。

## 變異數同質 (Homoscedasticity)

H₀：各組變異數相等。

| 檢定 | 何時用 |
| --- | --- |
| **Levene's** | **預設**，對非常態穩健 |
| Brown-Forsythe | 偏態或有離群值（= 以中位數為中心的 Levene） |
| Bartlett's | 已確認近似常態時（檢定力較高，但對非常態敏感） |

```python
stats.levene(g1, g2, g3)                     # 預設 center="median"，即 Brown-Forsythe
stats.levene(g1, g2, g3, center="mean")      # 原始 Levene
stats.bartlett(g1, g2, g3)
```

**不等時**：兩組 → Welch's t（`equal_var=False`）；三組以上 → Welch's ANOVA（`pingouin.welch_anova`）；事後比較 → Games-Howell。

> 實務上很多人直接預設 Welch，跳過變異數檢定，這通常是更好的做法（先檢定再選方法本身也會影響錯誤率）。

## 獨立性 (Independence)

一個觀測值不影響另一個。最好由**隨機抽樣與隨機分派**保證，而不是靠檢定。

| 不獨立的來源 | 例子 | 對策 |
| --- | --- | --- |
| 重複量測 | 同一病人前後測、同一小鼠多個時間點 | 配對檢定、重複量數 ANOVA、混合模型 |
| 群集 / 巢套 (nested) | 病人巢套在醫院內、細胞巢套在樣本內 | 多層次模型 (multilevel model)、GEE |
| 時間相關 | 每日量測 | 時間序列模型 |
| 空間相關 | 相鄰位置的感測器 | 空間模型（Moran's I） |
| 批次效應 | 同批次處理的樣本較相似 | 把批次放進模型當共變數或隨機效應 |

> **假重複 (pseudoreplication)**：把同一隻小鼠的 1,000 個細胞當成 n = 1,000 個獨立樣本，會讓 SE 嚴重低估、p 值小得離譜。單細胞資料比較組別時，常見做法是先把細胞 **pseudobulk**（依樣本加總）再分析，有效樣本數是**生物重複數**。

```python
from statsmodels.stats.stattools import durbin_watson
from statsmodels.sandbox.stats.runs import runstest_1samp

durbin_watson(model.resid)     # ≈ 2 無自相關；< 2 正自相關；> 2 負自相關
runstest_1samp(residuals)      # p ≤ 0.05 → 殘差序列非隨機
```

## 檢定前檢查清單

| 項目 | 檢查 |
| --- | --- |
| ☐ 獨立性 | 隨機抽樣 / 分派？有沒有重複量測、群集、批次？分析單位是什麼？ |
| ☐ 結果變數型態 | 連續？若是 Ordinal → 考慮無母數 |
| ☐ 常態性（每組或殘差） | Q–Q 圖；小樣本搭配 Shapiro-Wilk |
| ☐ 變異數 | 各組 SD 差很多嗎？或直接用 Welch |
| ☐ 離群值 | Boxplot；是否主導了結果？ |

z / t 臨界值與單雙尾的計算見 [信賴區間](confidence-intervals.md#平均數的-ci)。
