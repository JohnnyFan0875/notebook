[Machine Learning](../README.md) › 工作流程

# 工作流程 (Workflow)

模型種類會變，但問題定義、資料切分、避免洩漏、交叉驗證、pipeline 與監控這些原則每個專案都會用到，是這個章節最值得反覆讀的部分。

## 建議順序

```
問題定義 → 資料切分與洩漏 → 交叉驗證 → Pipeline → 調參 → 模型生命週期
                                                          ↘ Kaggle 競賽流程（實戰整合）
```

> **一句話原則**：任何會從資料「學到」東西的步驟（補值、縮放、編碼、特徵選擇、閾值調整）都只能在訓練資料或訓練 fold 內 fit，最好交給 [Pipeline](pipeline-basic.md) 管理。

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [問題定義](problem-framing.md) | 目標、預測單位、預測時點、錯誤代價 | 到底要預測什麼？怎樣算成功？ |
| [資料切分與洩漏](data-splitting-and-leakage.md) | 切分策略、正確順序、洩漏預防 | 資料要怎麼切才不會騙自己？ |
| [交叉驗證](cross-validation.md) | K-Fold、分層、分組、時間序列、Nested CV | 怎麼穩定地估計泛化能力？ |
| [Pipeline](pipeline-basic.md) | `Pipeline`、`ColumnTransformer`、存檔 | 怎麼讓前處理不洩漏、上線可重現？ |
| [超參數調整](hyperparameter-tuning.md) | Grid / Random / Bayesian（Optuna） | 怎麼有效率地挑參數？ |
| [模型生命週期](model-lifecycle.md) | 各階段產出、退化與重訓 | 模型上線後怎麼持續演進？ |
| [Kaggle 競賽流程](kaggle-competition-workflow.md) | local validation、baseline、blending / stacking | 怎麼建立能穩定判斷改動是否有效的實驗系統？ |

## 常見失誤

| 失誤 | 後果 |
| --- | --- |
| 在整份資料上先做 scaling 或 target encoding，再切 train / test | 分數虛高 |
| 時間序列資料用隨機切分 | 用未來預測過去 |
| 測試集被反覆拿來選模型 | 測試集失去獨立性 |
| 只記錄最佳分數，沒記資料版本與前處理設定 | 結果無法重現 |
