[Data Science](../README.md) › Statistics

# 統計 (Statistics)

從描述資料、機率、推論，到迴歸、無母數、貝氏、時間序列、多變量、實驗設計與存活分析。

> 統計不是一堆檢定的集合。好的流程是：**理解資料 → 選擇合適的模型 → 檢查假設 → 在脈絡中解讀結果**。很多錯誤來自直接套用熟悉的檢定，而好的分析幾乎都從**資料品質檢查與視覺化**開始。

**找方法**：不知道該用哪個檢定或模型時，先看 [統計方法速查](method-selection.md)。

## 模組

| 模組 | 核心內容 | 回答的問題 |
| --- | --- | --- |
| [敘述統計](descriptive-statistics/README.md) | 資料品質、型態、摘要、圖 | 資料長什麼樣？有缺失或離群值嗎？ |
| [機率與分配](probability-and-distributions/README.md) | 機率規則、分配、CLT、MLE、模擬 | 隨機變數如何表現？該用哪個分配？ |
| [推論統計](inferential-statistics/README.md) | CI、假設檢定、多重檢定、ANOVA | 樣本能告訴我們母體什麼？ |
| [迴歸分析](regression-analysis/README.md) | 線性、邏輯斯、GLM、混合效應 | Y 如何隨 X 改變？ |
| [無母數方法](nonparametric-methods/README.md) | 排名檢定、卡方、等級相關 | 常態或等變異假設不成立時怎麼辦？ |
| [貝氏統計](bayesian-statistics/README.md) | 先驗、後驗、MCMC | 如何結合先前知識與新證據？ |
| [時間序列](time-series-analysis/README.md) | 趨勢、季節、自相關、ARIMA | 時間上有什麼規律？如何預測？ |
| [多變量分析](multivariate-analysis/README.md) | PCA、分群、正則化、LDA | 許多變數如何一起形成結構？ |
| [實驗設計](experimental-design/README.md) | 隨機化、區集、偏誤、樣本數 | 如何蒐集能支持有效結論的資料？ |
| [存活分析](survival-analysis/README.md) | 設限、KM、Cox | 事件何時發生？什麼影響它的時間？ |

## 建議路線

| 讀者 | 路線 |
| --- | --- |
| 初學 | 敘述統計 → 機率與分配 → 推論統計 → 迴歸分析 → 實驗設計 |
| **生物資訊** | 資料品質 → [多重檢定校正](inferential-statistics/multiple-testing.md) → [GLM 與計數模型](regression-analysis/glm-count-models.md) → [混合效應模型](regression-analysis/mixed-effects-models.md) → [PCA](multivariate-analysis/pca.md) / [分群](multivariate-analysis/clustering.md) → [干擾與批次效應](experimental-design/confounding-bias.md) → [存活分析](survival-analysis/README.md)；完整套用見 [RNA-seq 分析](../../biology/genomics/workflows/rna-seq/README.md) |
| **機器學習** | [MLE 與損失函數](probability-and-distributions/maximum-likelihood.md) → [偏誤與變異](inferential-statistics/sampling-estimation.md) → [迴歸分析](regression-analysis/README.md) → [正則化](../machine-learning/foundations/regularization.md) → [Bootstrap / 置換檢定](probability-and-distributions/monte-carlo-simulation.md) → [貝氏統計](bayesian-statistics/README.md) |

## 三個貫穿全程的習慣

| 習慣 | 為什麼 |
| --- | --- |
| 先畫圖再檢定 | 圖比 p 值更快揭露結構、離群值、偏態與設計問題 |
| 配適後檢查假設 | 多數假設是關於殘差、相依性或模型形式，而不只是原始資料 |
| 報告效果量與不確定性 | 統計顯著很少能回答「這個結果重不重要」 |
