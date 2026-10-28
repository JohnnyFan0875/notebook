[Machine Learning](../README.md) › 監督式學習

# 監督式學習 (Supervised Learning)

用帶標籤的資料學習 X → y 的對應。重點不只是哪個演算法最好，而是先分清楚**預測類別還是連續值**，再搭配合適的前處理與評估。

## 建議順序

```
迴歸：線性 → Ridge / Lasso / Elastic Net → 迴歸樹
分類：邏輯斯迴歸 → KNN → 決策樹 → SVM → Naive Bayes
集成：Bagging → 隨機森林 → Boosting（AdaBoost → Gradient Boosting → XGBoost）→ Voting / Stacking
```

## 模組

| 模組 | 內容 | 回答的問題 |
| --- | --- | --- |
| [迴歸](regression/README.md) | 線性、Ridge、Lasso、Elastic Net、迴歸樹 | 連續值怎麼預測？特徵太多或共線怎麼辦？ |
| [分類](classification/README.md) | 邏輯斯迴歸、KNN、決策樹、SVM、Naive Bayes | 類別怎麼預測？各模型的邊界長怎樣？ |
| [集成方法](ensemble/README.md) | Bagging、隨機森林、Boosting、Voting、Stacking | 怎麼組合多個模型讓預測更準、更穩？ |

## 模型速覽

| 模型 | 需要縮放 | 非線性 | 可解釋 | 適合 |
| --- | --- | --- | --- | --- |
| 線性 / 邏輯斯迴歸（+正則化） | 是 | 否（需手動加特徵） | 高 | **baseline**、高維小樣本、要解釋係數 |
| KNN | 是 | 是 | 中 | 小資料、低維 |
| 決策樹 | 否 | 是 | 高（淺樹） | 解釋規則；單獨用很不穩 |
| SVM | 是 | 是（kernel） | 低 | 中小型、高維資料 |
| Naive Bayes | 否 | — | 中 | 文字、計數、極快的 baseline |
| 隨機森林 | 否 | 是 | 中 | 表格資料的穩健預設，幾乎不用調參 |
| Gradient Boosting / XGBoost / LightGBM | 否 | 是 | 中 | **表格資料常勝軍**，需調參 |

模型選擇的完整速查見 [ML 方法速查](../model-selection.md)。

## 實務提醒

| 提醒 | 原因 |
| --- | --- |
| 先做簡單、可解釋的 [baseline](../evaluation/baselines-and-error-analysis.md) | 乳癌資料上，標準化的邏輯斯迴歸（CV AUC 0.992）就和 SVM、XGBoost、stacking 打平 |
| 模型差異常小於資料切分與特徵工程的差異 | 先把 [工作流程](../workflow/README.md) 弄對 |
| 分類要及早想閾值與類別不平衡 | 見 [閾值與校準](../evaluation/classification-thresholds-and-calibration.md)、[類別不平衡](../evaluation/class-imbalance.md) |
| 迴歸要先確認誤差尺度與離群值容忍度 | 見 [迴歸指標](../evaluation/mse-rmse.md) |
| 要推論（係數、p 值）而不只是預測 | 用 [statsmodels](../packages/statsmodels/README.md) 與 [統計迴歸分析](../../statistics/regression-analysis/README.md) |
