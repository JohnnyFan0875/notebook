[Machine Learning](../README.md) › 上線與維運

# 上線與維運 (Production)

上線不是把 `model.pkl` 存起來就結束：輸入資料、特徵流程、模型版本、監控與重訓規則都要能長期運作。

## 建議順序

```
MLOps 概觀 → 部署與監控 → MLflow（實驗追蹤、模型註冊）→ DVC（資料與 pipeline 版本）
```

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [MLOps 概觀](mlops-overview.md) | MLOps 流程、和 DevOps 的差別、成熟度 | 為什麼模型需要「維運」？ |
| [部署與監控](deployment-and-monitoring.md) | 部署型態、四層監控、漂移指標 (PSI)、重訓 | 上線後怎麼知道模型壞了？ |
| [MLflow](mlflow.md) | Tracking、Models、Registry（aliases） | 怎麼追蹤實驗、管理模型版本？ |
| [DVC](dvc.md) | 資料版本、`dvc.yaml` pipeline、`params.yaml`、remote storage | 怎麼讓資料和實驗可重現？ |

## 核心問題

| 問題 | 相關筆記 |
| --- | --- |
| 上線後輸入 schema 改了，模型會不會默默壞掉？ | [部署與監控](deployment-and-monitoring.md) |
| 表現下降是資料漂移、概念漂移，還是流程 bug？ | [部署與監控](deployment-and-monitoring.md)、[抽樣與代表性](../foundations/sampling-and-representativeness.md) |
| 誰決定何時重訓、怎麼回滾、怎麼驗證新版本？ | [模型生命週期](../workflow/model-lifecycle.md)、[MLflow](mlflow.md) |

> 沒有 [Pipeline](../workflow/pipeline-basic.md) 的紀律與 [評估](../evaluation/README.md) 的基準，上線後幾乎一定出問題，也很難知道模型是否退化。
