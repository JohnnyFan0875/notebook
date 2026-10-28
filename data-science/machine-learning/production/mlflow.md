[Machine Learning](../README.md) › [上線與維運](README.md) › MLflow

# MLflow

MLflow 把實驗追蹤、模型打包、模型註冊放進同一套工具，讓模型從訓練到部署不會斷線。它回答的是：這次訓練用了哪些資料與參數？同一個模型如何在不同環境一致地載入？哪個版本目前在服務中？別人幾週前的結果怎麼重現？

本筆記以 **MLflow 3.17** 驗證；MLflow 2.x 與 3.x 有幾個重要差異，見下方「版本差異」。

## 核心元件

| 元件 | 用途 | 解決的問題 |
| --- | --- | --- |
| Tracking | 記錄 run 的參數、指標、artifacts | 實驗紀錄散落各處 |
| Models | 統一的模型打包格式（flavors） | 模型換環境就載入不了 |
| Model Registry | 模型版本、別名 (alias)、標籤 | 不知道哪個版本在線上 |
| Projects | 定義可重現的執行環境與入口 | 程式碼在別人電腦跑不起來 |

## 1. Tracking

```python
import mlflow
import mlflow.sklearn

mlflow.set_tracking_uri("sqlite:///mlflow.db")   # 本機用 SQLite；團隊用 tracking server
mlflow.set_experiment("churn-model")             # 實驗 = 一組相關的 runs

with mlflow.start_run(run_name="logreg-C1"):
    mlflow.log_param("C", 1.0)                   # 超參數
    mlflow.log_metric("cv_auc", 0.992)           # 指標（可帶 step 記錄訓練曲線）
    mlflow.set_tag("data_version", "2024-06")    # 資料版本等中繼資料
    mlflow.log_artifact("confusion_matrix.png")  # 任意檔案

# 自動記錄：參數、訓練指標、模型
mlflow.sklearn.autolog()
```

> MLflow 3.x 的本機**檔案型後端 (`./mlruns`) 已進入維護模式**，直接使用會報錯並建議改用資料庫後端（`sqlite:///mlflow.db`）；artifacts 預設仍會寫到目前目錄下的 `mlruns/`。

用 client API 管理實驗時，參數是 **experiment_id**，不是名稱：

```python
from mlflow import MlflowClient

client = MlflowClient()
exp_id = mlflow.get_experiment_by_name("churn-model").experiment_id
client.set_experiment_tag(exp_id, "team", "risk")
```

## 2. Models：打包與載入

```python
# 記錄模型（存整個 pipeline，含前處理）
info = mlflow.sklearn.log_model(pipeline, name="model",
                                input_example=X_train[:5])        # 自動推斷輸入 schema（signature）

loaded = mlflow.sklearn.load_model(info.model_uri)               # 原生 sklearn 物件
pyfunc = mlflow.pyfunc.load_model(info.model_uri)                # 通用介面，只有 predict()
```

| Flavor | 用途 |
| --- | --- |
| `mlflow.sklearn`、`mlflow.xgboost`、`mlflow.pytorch`… | 依框架原生存取 |
| `mlflow.pyfunc` | 通用 Python 介面；任何 flavor 都能用它載入，部署端不必知道是哪個框架 |
| 自訂 `mlflow.pyfunc.PythonModel` | 推論流程含額外前後處理時 |

```python
class CustomModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):          # 載入時取回需要的 artifacts
        import joblib
        self.model = joblib.load(context.artifacts["model_path"])

    def predict(self, context, model_input):
        return self.model.predict_proba(model_input)[:, 1]
```

> MLflow 3.17 的 sklearn 模型預設存成 `model.skops`（不是 pickle）；另有 `MLFLOW_ALLOW_PICKLE_DESERIALIZATION` 設定控制 pickle 載入。pickle 檔載入時可執行任意程式碼，只載入可信來源的模型。

## 3. Model Registry：版本與別名

```python
# 註冊：log 時直接註冊，或之後再註冊
mlflow.sklearn.log_model(pipeline, name="model", registered_model_name="ChurnModel")
mlflow.register_model(info.model_uri, "ChurnModel")

# 用別名 (alias) 標記用途，取代舊的 stage
client.set_registered_model_alias("ChurnModel", "champion", version=3)
client.set_registered_model_alias("ChurnModel", "challenger", version=4)

# 部署端只認別名，不寫死版本號
model = mlflow.pyfunc.load_model("models:/ChurnModel@champion")
```

| 模型 URI | 指向 |
| --- | --- |
| `runs:/<run_id>/model` | 某次 run 的 artifact（MLflow 2.x 常見） |
| `models:/m-<model_id>` | MLflow 3 的 logged model（`log_model` 回傳的 `model_uri`） |
| `models:/ChurnModel/3` | 註冊模型的特定版本 |
| `models:/ChurnModel@champion` | 目前被標為 champion 的版本 |

> **Stage（`Staging` / `Production` / `Archived`）自 MLflow 2.9 起 deprecated**，`transition_model_version_stage()` 會發出警告，未來的主要版本將移除。改用 alias（`@champion`、`@challenger`）與 tag；換版本時只要移動別名，回滾就是把別名指回舊版本。

## 4. Serving

```bash
mlflow models serve -m "models:/ChurnModel@champion" -p 5000 --env-manager local
```

適合快速驗證模型能否服務化與本機 demo。正式環境通常把 MLflow 當作**模型來源與治理層**，外面再接自己的 API、批次作業或服務平台。

## 5. Projects

```text
project/
  MLproject          # 入口與參數
  train.py           # 訓練邏輯
  python_env.yaml    # Python 環境
  requirements.txt   # 套件依賴
```

```bash
mlflow run . -P alpha=0.5
```

## 版本差異（2.x → 3.x）

| 項目 | 舊 | 新 |
| --- | --- | --- |
| `log_model` 的位置參數 | `artifact_path="model"` | `name="model"` |
| 模型 URI | 以 `runs:/<run_id>/model` 為主 | `models:/m-<model_id>`（logged model 成為一級物件） |
| 部署標記 | Stage（Staging / Production） | Alias（`@champion`） |
| 本機後端 | `./mlruns` 檔案系統 | 建議 `sqlite:///mlflow.db` |

## 常見誤區

| 誤區 | 改正 |
| --- | --- |
| 只記錄指標，不記錄資料版本與前處理 | 用 tag 記資料版本；log 整個 pipeline |
| 只有 `model.pkl`，沒有 registry | 註冊模型、用別名部署 |
| 以為有 MLflow 就完成部署、監控、重訓 | 監控與重訓需另外建，見 [部署與監控](deployment-and-monitoring.md) |
| 把病人層級資料當 artifact 上傳 | 只記錄彙總與中繼資料，注意隱私規範 |

相關：[MLOps 概觀](mlops-overview.md)、[模型生命週期](../workflow/model-lifecycle.md)、[Kaggle 競賽流程](../workflow/kaggle-competition-workflow.md)（實驗紀錄）。
