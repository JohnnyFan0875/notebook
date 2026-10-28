[Machine Learning](../../README.md) › [非監督式學習](../README.md) › 異常偵測

# 異常偵測 (Anomaly Detection)

找出明顯偏離主要模式的觀測值。和前處理的 [離群值處理](../../preprocessing/outlier-handling.md) 不同，這裡的目標通常是**把罕見但重要的案例找出來**（詐欺、故障、異常樣本），而不是刪掉它們。

## 建議順序

```
核心概念（型態、分數 vs 閾值）→ Isolation Forest → 距離 / 密度方法（LOF）→ 時間序列異常
```

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [核心概念](core-concepts.md) | 離群 / 異常 / 新奇、異常型態、contamination、評估 | 什麼算異常？怎麼評估？ |
| [Isolation Forest](isolation-forest.md) | 隨機切分的隔離路徑長度 | 大型表格資料的預設方法？ |
| [距離與密度方法](distance-density.md) | KNN 距離、LOF、Gower 距離 | 局部異常、混合型資料怎麼處理？ |
| [時間序列異常](time-series-anomalies.md) | 趨勢 / 季節分解、殘差、滾動基準 | 「這個時間點」不尋常嗎？ |

## 方法速覽

| 方法 | sklearn | 擅長 | 弱點 |
| --- | --- | --- | --- |
| Isolation Forest | `IsolationForest` | 全域異常、高維、大資料 | 局部異常 |
| Local Outlier Factor | `LocalOutlierFactor` | 局部異常、密度不均 | 慢、對 `n_neighbors` 敏感 |
| KNN 距離 | `NearestNeighbors` | 簡單直覺 | 密度不均時誤判 |
| One-Class SVM | `OneClassSVM` | 乾淨訓練資料的新奇偵測 | 對參數敏感、大資料慢 |
| 穩健共變異 | `EllipticEnvelope` | 近似多變量常態 | 非常態資料 |
| 規則 / 統計門檻 | — | 可解釋、單變量 | 抓不到多變量異常 |

> 同一個罕見點，在詐欺偵測中是訊號，在資料清理中是雜訊；處理方式由情境決定。有標籤後，問題就變成 [不平衡分類](../../evaluation/class-imbalance.md)。
