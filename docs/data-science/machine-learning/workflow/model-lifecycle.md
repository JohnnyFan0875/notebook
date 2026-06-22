# Model Lifecycle

模型不是一次性產物，而是一個會隨資料、業務規則與環境改變而持續演進的系統。把 model lifecycle 想清楚，才能避免把大量精力花在一個很快過時的版本上。

## Typical Lifecycle

1. Frame the problem
2. Collect and audit data
3. Split data and define validation
4. Build a [baseline](../evaluation/baselines-and-error-analysis.md)
5. Preprocess and train candidate models
6. Tune and compare models
7. Perform [error analysis](../evaluation/baselines-and-error-analysis.md) and diagnostics
8. Package and deploy the chosen model
9. Monitor predictions, data drift, and outcome drift
10. Retrain or redesign when performance degrades

## 每個階段都該留下什麼

- 問題定義：目標、限制、評估指標、利害關係人。
- 資料階段：資料來源、欄位定義、抽樣規則、清理決策。
- 訓練階段：模型設定、超參數、驗證方式、比較結果。
- 部署階段：版本、服務介面、依賴套件、輸入輸出 schema。
- 監控階段：告警規則、重訓條件、負責人。

## What Often Gets Missed

- baselines
- error analysis
- feature availability checks
- monitoring after deployment
- clear retraining criteria

## 實務上很重要的兩個問題

### 1. 這個模型的輸入在上線後真的拿得到嗎？

很多專案在 notebook 裡表現很好，但某些特徵實際上線時要晚兩天才到，或來自人工標註，導致無法即時推論。

### 2. 什麼情況算模型退化？

若沒有預先定義性能閾值、漂移指標與重訓規則，團隊通常會在問題已經影響業務後才被動處理。

## Good Practice

- Version the dataset or extraction logic
- Log parameters and evaluation results
- Save the preprocessing graph together with the model
- Define who owns monitoring and retraining

## Related Concepts

- [Problem Framing](problem-framing.md)
- [Baselines and Error Analysis](../evaluation/baselines-and-error-analysis.md)
- [Deployment and Monitoring](../production/deployment-and-monitoring.md)
- [Generalization](../foundations/generalization.md)

[Back to Workflow](README.md)
