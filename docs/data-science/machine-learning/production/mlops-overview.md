# MLOps Overview

`MLOps Concepts`、`Monitoring Machine Learning in Python`、`Developing Machine Learning Models for Production` 等抽取內容的共同核心，是把模型當成持續運作的產品，而不是一次性 notebook 結果。

## MLOps 在解決什麼

機器學習專案通常不會停在模型訓練完成。真正困難的是：

- 如何穩定部署
- 如何持續監控
- 如何重訓與回滾
- 如何讓資料、程式碼、模型版本彼此對得上

## 一條典型的 MLOps 流程

1. 資料與特徵流程版本化
2. 可重現的訓練 pipeline
3. 模型評估與審核
4. 打包與部署
5. 線上監控與告警
6. 觸發重訓或人工介入

## MLOps 不只是 DevOps 搬過來

MLOps 多了幾個特有問題：

- 模型品質會隨資料分布改變而退化
- 上線後不一定立刻拿得到真實標籤
- 同一份程式碼，不同資料版本會導致完全不同結果

## 核心能力

| 能力 | 重點 |
| --- | --- |
| reproducibility | 資料、參數、模型版本都可追溯 |
| deployment | batch、online、streaming 推論都能穩定執行 |
| monitoring | 追資料漂移、性能退化、系統錯誤 |
| governance | 清楚知道誰批准、誰回滾、誰重訓 |

## 和本章其他頁的關係

- [Deployment and Monitoring](deployment-and-monitoring.md) 講上線與監控實務
- [Model Lifecycle](../workflow/model-lifecycle.md) 講模型從定義到重訓的整體循環

## 常見誤區

- 以為有 CI/CD 就等於完成 MLOps
- 只有模型版本，沒有資料與特徵版本
- 線上監控只看延遲，不看資料漂移與性能

## 小結

如果一個團隊無法穩定重現訓練結果、追蹤上線版本、監控退化並安全回滾，那它還沒有真正建立起 MLOps。
