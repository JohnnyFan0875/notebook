[Statistics](../README.md) › 迴歸分析

# 迴歸分析 (Regression Analysis)

建立結果變數 Y 與一或多個預測變數 X 的關係。比相關係數多了「方程式」與「每個變數的效果」，但仍不自動代表因果。

## 三種目的，不要混在一起

| 目的 | 問題 | 重視 |
| --- | --- | --- |
| 描述 (description) | X 與 Y 在這份資料中如何相關？ | 係數、圖 |
| 預測 (prediction) | X 能多準地預測新資料的 Y？ | 測試集誤差、[交叉驗證](../../machine-learning/workflow/cross-validation.md) |
| 解釋 (explanation) | 調整其他變數後，每個係數代表什麼？ | 係數 + CI、研究設計、[干擾因子](../experimental-design/confounding-bias.md) |

## 依結果變數選模型

| 結果變數 | 模型 | 筆記 |
| --- | --- | --- |
| 連續，一個 X | 簡單線性迴歸 | [Simple Linear Regression](simple-linear-regression.md) |
| 連續，多個 X | 多元線性迴歸 | [Multiple Linear Regression](multiple-linear-regression.md) |
| 二元 (0/1) | 邏輯斯迴歸 | [Logistic Regression](logistic-regression.md) |
| 計數 (0, 1, 2, …) | Poisson / 負二項迴歸 | [GLM 與計數模型](glm-count-models.md) |
| 重複量測 / 群集 / 批次 | 混合效應模型 | [Mixed-Effects Models](mixed-effects-models.md) |
| 存活時間（有設限） | Cox 模型 | [存活分析](../survival-analysis/cox-ph-model.md) |
| 很多預測變數（p 大） | Ridge / Lasso | [ML: Regularization](../../machine-learning/foundations/regularization.md) |

診斷（共線性、殘差、影響點）的深入內容見 [多變量：假設與診斷](../multivariate-analysis/assumptions-diagnostics.md)。R 的寫法（`lm`、`glm`、`broom`）見 [Explanatory Modeling in R](../../r-foundations/explanatory-modeling-in-r.md)。

## 常見解讀陷阱

| 陷阱 | 正確解讀 |
| --- | --- |
| 係數顯著 → 因果 | 只代表在模型假設下有關聯 |
| R² 高 → 模型好 | 還要看殘差、泛化能力、函數形式是否合理 |
| 係數不顯著 → 沒有關係 | 可能是檢定力不足、共線性、雜訊或模型設定錯誤 |
| 邏輯斯係數 = 機率變化 | 係數作用在 log-odds；轉成 odds ratio 或預測機率 |
