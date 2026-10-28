[Statistics](../README.md) › 存活分析

# 存活分析 (Survival Analysis)

分析**事件發生時間 (time-to-event)** 的資料：不只問「有沒有發生」，還問「**何時**發生、風險如何隨時間變化、哪些因素加速或延緩它」。核心挑戰是**設限 (censoring)**：研究結束時事件還沒發生的觀測。

一般迴歸做不到的原因：(1) 設限，直接刪除或當成未發生都會造成偏誤；(2) 風險隨時間改變，邏輯斯迴歸把結果當二元，完全忽略時間。

| 領域 | 事件 | 時間 |
| --- | --- | --- |
| 醫學 | 死亡、復發、發病 | 診斷 / 手術到事件的天數 |
| 工程 | 零件故障 | 運轉時數 |
| 商業 / SaaS | 顧客流失、取消訂閱 | 註冊後天數 |
| 人資 | 員工離職 | 到職後月數 |
| 金融 | 貸款違約 | 核貸後月數 |

## 建議順序

```
資料結構與設限 → S(t) / h(t) → Kaplan-Meier + log-rank → Cox 模型 → 診斷 → 參數模型 → 解讀與視覺化
```

時間軸與設限邏輯還不直覺之前，不要急著跳到 Cox 模型。

## 筆記

| 筆記 | 回答的問題 |
| --- | --- |
| [核心概念與設限](core-concepts.md) | 存活資料長什麼樣？什麼是設限？ |
| [存活函數與風險函數](survival-hazard-functions.md) | 怎麼用數學描述存活過程？ |
| [Kaplan-Meier](kaplan-meier.md) | 怎麼估計與畫存活曲線？ |
| [Log-rank 檢定](log-rank-test.md) | 兩組以上的存活曲線不同嗎？ |
| [Cox 比例風險模型](cox-ph-model.md) | 共變數如何影響風險？什麼是 hazard ratio？ |
| [模型診斷](diagnostics.md) | 比例風險假設成立嗎？怎麼修？ |
| [參數模型](parametric-models.md) | 何時用 Weibull、Exponential、Log-normal、AFT？ |
| [結果解讀](interpretation.md) | 怎麼把輸出翻成有意義的結論？ |
| [視覺化](visualization.md) | 該畫哪些圖、怎麼讀？ |

主要套件：Python `lifelines`、`scikit-survival`；R `survival`、`survminer`。
