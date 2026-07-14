# MLflow

MLflow 把 experiment tracking、model packaging、registry 與 reproducible project structure 放進同一套工具裡，讓模型從訓練到部署之間比較不會斷線。

## MLflow 在解決什麼

機器學習專案常見的問題不是模型 train 不起來，而是：

- 這次訓練到底用了哪份資料與哪些參數
- 同一個模型如何在不同環境被一致地載入
- 哪個版本已經過審核，哪個版本正在 production
- 團隊如何重現別人幾週前跑過的結果

MLflow 的核心價值，就是把這些資訊變成可追蹤的系統，而不是散落在 notebook、雲端硬碟與訊息紀錄裡。

## 四個核心元件

| 元件 | 用途 |
| --- | --- |
| Tracking | 記錄 run、參數、metrics、artifacts |
| Models | 用統一格式包裝模型，方便載入與部署 |
| Model Registry | 管理模型版本、狀態與交接流程 |
| Projects | 定義可重現的專案結構與執行環境 |

這四塊剛好對應到 MLOps 最容易失控的四件事：實驗紀錄、部署格式、版本治理與重現性。

## Tracking: 把訓練過程留下來

MLflow Tracking 的基本單位是 experiment 與 run。

- `experiment` 用來分組不同主題或專案
- `run` 用來記錄某一次訓練或評估

常見操作像是：

```python
import mlflow

mlflow.set_experiment("churn-model")

with mlflow.start_run():
    mlflow.log_param("max_depth", 6)
    mlflow.log_metric("rmse", 0.82)
```

如果要更細緻地管理 experiments，也可以透過 client API 建立、加 tag 或刪除：

```python
from mlflow import MlflowClient

client = MlflowClient()
client.create_experiment("churn-model")
client.set_experiment_tag("churn-model", "team", "risk")
```

實務上最重要的不是 API 名稱，而是要養成習慣：每次訓練都留下可對帳的參數、metrics、模型產物與必要的程式碼脈絡。

## Autologging 與 artifacts

MLflow 可以替常見框架自動記錄資訊，降低遺漏風險：

```python
import mlflow.sklearn

mlflow.sklearn.autolog()
```

autologging 通常會自動存下：

- 模型參數
- 評估指標
- 模型檔與相關 artifacts
- 執行環境的一部分中繼資訊

在投影片內容裡，模型 artifact 附近常會看到像 `artifact_path`、`python_version`、`mlflow_version`、`sklearn_version` 這類 metadata。這些資訊的價值在於：當模型無法重現時，我們至少知道該往哪裡查。

## Models: 把模型包成可載入的格式

MLflow Models 的重點不是再發明一個新模型，而是替不同 ML library 提供一致的打包與載入方式。

例如 `scikit-learn` 的常見操作：

```python
import mlflow.sklearn

mlflow.sklearn.log_model(model, artifact_path="model")
loaded_model = mlflow.sklearn.load_model("runs:/<run_id>/model")
```

這裡的 `runs:/` URI 很重要。它代表模型不只是某個本機檔案，而是某次 run 底下的一個 artifact。這讓 training 紀錄與部署來源可以直接連起來。

## Flavors 與 `pyfunc`

MLflow 用 `flavor` 來描述模型如何被特定工具鏈理解。

- `mlflow.sklearn`
- `mlflow.xgboost`
- `mlflow.pytorch`
- `mlflow.pyfunc`

其中 `pyfunc` 很值得理解，因為它提供了較通用的 Python 介面。當你的推論流程不只是單純 `model.predict()`，而是還包含額外前處理、後處理或客製化邏輯時，就可能會用到它。

```python
import mlflow.pyfunc

class CustomPredict(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        self.model = context.artifacts["model"]
```

`load_context()` 的概念是：在模型真正被載入時，把需要的 artifacts 一起接回來。這對多檔案推論流程特別重要。

## Registry: 管理模型版本，而不是只留最新檔案

如果 Tracking 解決的是「這次跑了什麼」，Registry 解決的就是「現在該用哪個版本」。

Model Registry 的核心能力包括：

- 集中存放已註冊模型
- 對同一模型建立多個 version
- 用 stage 或其他治理流程標示可用狀態
- 透過 UI 或 client API 做交接

常見註冊方式：

```python
mlflow.register_model("runs:/<run_id>/model", "ChurnModel")
```

也可以在 log model 時直接指定註冊名稱：

```python
mlflow.sklearn.log_model(
    model,
    "model",
    registered_model_name="ChurnModel",
)
```

## Staging、Production、Archived 的意義

教材把 model stage 拆成 `Staging`、`Production`、`Archived`。把它們理解成技術狀態不如理解成團隊流程狀態：

| Stage | 代表的意思 |
| --- | --- |
| Staging | 候選版本，準備驗證 |
| Production | 目前正式服務中的版本 |
| Archived | 保留歷史版本，但不再主動使用 |

stage 的價值不是名字本身，而是把「誰能上線、誰已退役」變成可查詢的狀態，而不是靠口頭同步。

## 以 URI 載入不同來源的模型

MLflow 一個很實用的設計，是用 URI 指向模型來源。

常見形式有：

- `runs:/<run_id>/model`
- `models:/ChurnModel/3`
- `models:/ChurnModel/Production`
- 本機路徑或物件儲存路徑

這讓載入方式更穩定：

```python
staging_model = mlflow.sklearn.load_model("models:/ChurnModel/Staging")
prod_model = mlflow.sklearn.load_model("models:/ChurnModel/Production")
```

如果團隊能接受以 registry stage 作為部署入口，那推論服務就不必硬編碼某個本機檔名。

## Serving: 從 model artifact 到可呼叫服務

MLflow 也提供 CLI serving 方式：

```bash
mlflow models serve -m "models:/ChurnModel/Production"
```

這種做法適合：

- 快速驗證模型可否被服務化
- 做本機或測試環境 demo
- 讓團隊先建立「模型包裝與載入一致」的習慣

但在真正 production 環境，通常還是會把 MLflow 當成模型來源與治理層，外面再接 API、batch job 或更完整的 serving infrastructure。

## Projects: 把可重現性寫進專案結構

MLflow Projects 想解決的是「程式碼明明有，但你跑不起來」。

典型專案結構像這樣：

```text
project/
  MLproject
  train_model.py
  python_env.yaml
  requirements.txt
```

這些檔案各自扮演不同角色：

- `MLproject`: 定義專案入口與參數
- `train_model.py`: 實際訓練邏輯
- `python_env.yaml`: Python 執行環境描述
- `requirements.txt`: 套件依賴

如果一個模型只能在原作者的筆電上跑通，那就還不算可維護的 MLOps 資產。Projects 的意義正是把執行方式明文化。

## 一個實務上的心智模型

可以把 MLflow 想成四層：

1. Tracking 記住你做過什麼
2. Models 定義模型如何被包裝與載入
3. Registry 決定哪個版本可被團隊採用
4. Projects 幫你重現整個訓練流程

當這四層連起來時，模型才比較接近真正可交接、可部署、可回滾的 production asset。

## 常見誤區

- 只記錄 metrics，不記錄資料版本與前處理脈絡
- 只有 `model.pkl`，沒有清楚的 model URI 與 registry 流程
- 把 `Production` 當成一個手動改名的資料夾，而不是治理狀態
- 以為有 MLflow 就自動完成部署、監控與重訓

## Related Concepts

- [MLOps Overview](mlops-overview.md)
- [Deployment and Monitoring](deployment-and-monitoring.md)
- [Model Lifecycle](../workflow/model-lifecycle.md)

[Back to Production](README.md)
