# Workflow

Workflow 是機器學習教材裡最值得反覆閱讀的部分。模型種類會變，但問題定義、資料切分、避免洩漏、交叉驗證、pipeline 與監控這些原則幾乎每個專案都會用到。

## 核心流程

1. [Problem Framing](problem-framing.md): 先確認要預測什麼、怎麼衡量成功、有哪些限制。
2. [Data Splitting and Leakage](data-splitting-and-leakage.md): 先把資料切對，再做任何會從資料學習的步驟。
3. [Cross-Validation](cross-validation.md): 用與資料型態相符的驗證策略估計泛化能力。
4. [Pipeline Basics](pipeline-basic.md): 把前處理與模型包成單一流程，降低人為錯誤。
5. [Hyperparameter Tuning](hyperparameter-tuning.md): 在正確驗證框架下比較參數，而不是靠直覺反覆試。
6. [Model Lifecycle](model-lifecycle.md): 把模型視為會持續演進的系統，而不是一次性產物。

## 這一章最重要的觀念

- 先定義問題，再選模型。
- 先切資料，再做補值、編碼、標準化、特徵選擇。
- 驗證設計必須符合資料的時間、群組或抽樣方式。
- 指標好看不代表流程正確，很多高分其實來自 leakage。

## 常見失誤

- 在整份資料上先做 scaling 或 target encoding，再切 train/test。
- 時間序列資料卻用隨機切分。
- 測試集被反覆拿來選模型，最後失去獨立性。
- 專案只紀錄最佳分數，卻沒有記錄資料版本與前處理設定。

## 一句話原則

任何會從資料中「學到」資訊的步驟，包括 [imputation](../preprocessing/imputation.md)、scaling、encoding、feature selection 與 threshold tuning，都應該只在訓練資料或訓練 fold 內完成，最好交給 [pipeline](pipeline-basic.md) 管理。

[Back to Machine Learning](../README.md)
