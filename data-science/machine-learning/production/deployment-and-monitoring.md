# Deployment and Monitoring

把模型部署到 production，真正上線的不是單一 estimator，而是一整條從輸入到輸出的推論流程。若 training 與 serving 的前處理不一致，再高分的模型都可能在上線後立即失真。

## 上線前至少要準備什麼

- 完整的前處理 [pipeline](../workflow/pipeline-basic.md)
- 訓練好的模型權重或序列化產物
- 欄位 schema 與資料型別規格
- 模型版本、訓練時間、資料版本與重要超參數

## 部署型態

| 型態 | 適合情境 | 主要風險 |
| --- | --- | --- |
| Batch inference | 每日或每小時批次預測 | 資料延遲、排程失敗、回填邏輯 |
| Real-time inference | 需要即時回應 | 延遲、吞吐量、服務穩定性 |
| Streaming / event-driven | 持續處理事件資料 | schema 漂移、事件遺失、順序問題 |

## 監控不能只看模型分數

### 系統層

- latency
- throughput
- error rate
- timeout / retry 次數

### 資料層

- 缺失值比例是否突然變高
- 類別值是否出現新標籤
- 關鍵特徵分布是否偏移
- schema 是否改動

### 模型層

- prediction 分布是否異常集中
- calibration 是否退化
- 有標籤回流時的性能變化

### 商業層

- 轉換率、流失率、違約率等下游 KPI
- 模型決策是否造成不合理的業務偏差

## 何時應該考慮重訓

- 性能持續下降，而不是短暫波動
- 重要特徵發生顯著漂移
- 上游收集流程、標註規則或目標定義改變
- 商業環境出現制度性變化

## 常見錯誤

- 只存模型，不存前處理與欄位順序。
- 上線服務默默把缺失值或新類別用不同規則處理。
- 只有技術監控，沒有和商業結果對照。
- 每次重訓都覆蓋舊模型，沒有版本與回滾機制。

## 一句話原則

如果你無法在 production 中穩定重現 training 時的資料轉換與欄位定義，那這個模型就還不能算真正可部署。

## Related Concepts

- [Model Lifecycle](../workflow/model-lifecycle.md)
- [Pipeline Basics](../workflow/pipeline-basic.md)
- [Generalization](../foundations/generalization.md)
- [Data Leakage](../foundations/data-leakage.md)

[Back to Production](README.md)
