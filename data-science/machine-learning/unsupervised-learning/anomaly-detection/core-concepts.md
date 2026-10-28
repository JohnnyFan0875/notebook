[Machine Learning](../../README.md) › [非監督式學習](../README.md) › [異常偵測](README.md) › 核心概念

# 異常偵測核心概念 (Anomaly Detection Core Concepts)

異常是指在你選的**特徵表示與假設**下，明顯不同於多數資料的觀測。「不尋常」從來不是純客觀的：它取決於納入哪些特徵、尺度、時間脈絡，以及問題在乎哪種異常。

（實驗設計的術語見 [實驗設計核心概念](../../../statistics/experimental-design/core-concepts.md)；存活分析的設限見 [存活分析核心概念](../../../statistics/survival-analysis/core-concepts.md)。）

## 離群 vs 異常 vs 新奇

| 名詞 | 意義 | 訓練資料 | 常見用途 | sklearn |
| --- | --- | --- | --- | --- |
| 離群值偵測 (outlier detection) | 資料中遠離其他點的觀測 | 本身可能含異常 | 資料清理、QC | `fit_predict` |
| 異常 (anomaly) | 可疑、不正常的觀測 | — | 監控、詐欺、故障 | — |
| 新奇偵測 (novelty detection) | 新資料是否偏離「乾淨」的基準 | 假設是乾淨的 | 上線後的偵測 | `LocalOutlierFactor(novelty=True)` 後 `predict` |

## 異常的型態

| 型態 | 意義 | 例子 |
| --- | --- | --- |
| 點異常 (point) | 單一觀測本身就不尋常 | 一筆比平常大 100 倍的交易 |
| 情境異常 (contextual) | 只在特定情境下不尋常 | 凌晨 3 點的高用電量；冬天的高溫 |
| 集體異常 (collective) | 一連串觀測合起來才不尋常 | 10 分鐘內大量登入失敗 |
| 多變量異常 (multivariate) | 每個特徵單看都正常，組合起來不合理 | 身高正常、體重正常，但這組身高體重不可能 |

> 多變量異常是單變量規則（z-score、IQR）不夠的原因：一個點可能在每一欄都正常，在聯合空間卻很異常。

## 工作流程

```
1. 釐清目的：清理資料？告警？分流審查？自動封鎖？
2. 定義分析單位：事件、使用者、裝置、日、時間窗
3. 選能表達「正常行為」的特徵
4. 縮放與前處理
5. 選擇符合資料結構的偵測器
6. 先檢視異常分數的分布，再決定閾值
7. 用領域回饋、標籤或下游效用評估
```

## 分數 vs 閾值：contamination

多數非監督式偵測器輸出的是**分數 / 排序**，二元標籤要靠閾值。sklearn 的 `contamination` 參數就是「預期異常比例」，用來把分數切成標籤：

| 概念 | 說明 |
| --- | --- |
| `contamination` | 你願意標記為異常的比例；是**建模假設**，不是從資料發現的事實 |
| 設錯時 | 排序可能仍然很好，但二元標籤會誤導 |
| `score_samples` / `decision_function` | 取得連續分數，自己依審查容量決定閾值 |

```python
from sklearn.ensemble import IsolationForest

iso = IsolationForest(contamination=0.01, random_state=0).fit(X)
scores = -iso.score_samples(X)          # 越大越異常
flags = iso.predict(X) == -1            # 依 contamination 切出的 1% 異常
top_100 = scores.argsort()[::-1][:100]  # 或直接依審查容量取前 100 名
```

## 評估

有部分標籤時，分開評估兩件事：

| 問題 | 指標 |
| --- | --- |
| 真正的異常有沒有排在前面？ | PR-AUC、precision@k（異常極少時不要只看 ROC-AUC，見 [類別不平衡](../../evaluation/class-imbalance.md)） |
| 選定的閾值是否產生可接受的取捨？ | 該閾值下的 precision / recall |

> 二元結果很差不一定代表偵測器差：可能排序有用，只是閾值選錯。沒有標籤時，請領域專家審查分數最高的案例，是最實際的評估方式。

## 縮放與特徵選擇

距離型與隔離型方法都強烈依賴特徵表示：

| 檢查 | 原因 |
| --- | --- |
| 數值特徵是否在可比較的尺度 | 單位大的特徵會主導距離 |
| 罕見類別如何編碼 | one-hot 後罕見類別本身就會看起來「異常」 |
| 是否缺少時間 / 日曆脈絡 | 情境異常需要情境特徵 |
| 是否有單一雜訊特徵主導 | 異常分數只反映那個特徵 |

> 好的異常偵測，關鍵通常在特徵設計與閾值紀律，而不是更花俏的演算法。
