[Computing](../README.md) › [Web 開發](README.md) › FastAPI

# FastAPI

FastAPI 是用 Python type hints 定義 API 的 web 框架：型別同時是輸入驗證、回應 schema 與自動產生的 OpenAPI 文件，程式碼少、契約清楚。常用在資料服務、內部工具、ML 模型推論端點。本篇是**伺服器端**；用 `requests` 呼叫 API 的客戶端寫法、狀態碼的處理方式見 [API 與 HTTP](../../data-science/python-foundations/api-http.md)。

## 核心概念

| 概念 | 在 FastAPI 中 |
| --- | --- |
| 端點 (endpoint) | HTTP 方法 + 路徑，用 decorator 宣告：`@app.get("/samples/{id}")` |
| path 參數 | 路徑中的 `{sample_id}`，依型別自動轉換與驗證 |
| query 參數 | 函式參數中不在路徑裡的簡單型別：`?tissue=liver&limit=10` |
| request body | 型別為 Pydantic `BaseModel` 的參數，從 JSON 解析 |
| response model | `response_model=`：過濾與驗證輸出欄位，也寫進文件 |
| 驗證失敗 | 自動回 `422 Unprocessable Entity` 與哪個欄位錯 |
| 文件 | 啟動後 `/docs`（Swagger UI）、`/redoc`、`/openapi.json` |

### CRUD 對應

| 動作 | 方法 | 路徑 | 成功狀態碼 |
| --- | --- | --- | --- |
| 列出 / 查詢 | `GET` | `/samples?tissue=liver` | `200` |
| 取得一筆 | `GET` | `/samples/{id}` | `200`；不存在 `404` |
| 建立 | `POST` | `/samples` | `201 Created` |
| 整筆取代 | `PUT` | `/samples/{id}` | `200`；不存在 `404` |
| 部分更新 | `PATCH` | `/samples/{id}` | `200` |
| 刪除 | `DELETE` | `/samples/{id}` | `204 No Content`（無 body） |

狀態碼要對應操作的語意，而不只是「函式有沒有跑完」：客戶端錯誤（輸入錯、找不到）回 4xx，伺服器處理失敗回 5xx。完整的狀態碼分類見 [API 與 HTTP：狀態碼](../../data-science/python-foundations/api-http.md#狀態碼)。

## 範例

```python
# main.py
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Sample API")

class SampleIn(BaseModel):                       # request body 的 schema
    name: str = Field(min_length=1)
    tissue: str
    reads_m: float = Field(gt=0)                 # 必須 > 0，否則自動回 422

class Sample(SampleIn):                          # response 多一個 id
    id: int

db: dict[int, Sample] = {}                       # 示範用；實務接資料庫

@app.get("/samples", response_model=list[Sample])
def list_samples(tissue: str | None = None, limit: int = 100):   # query 參數
    rows = [s for s in db.values() if tissue is None or s.tissue == tissue]
    return rows[:limit]

@app.get("/samples/{sample_id}", response_model=Sample)
def get_sample(sample_id: int):                  # path 參數，自動轉 int
    if sample_id not in db:
        raise HTTPException(status_code=404, detail="sample not found")
    return db[sample_id]

@app.post("/samples", response_model=Sample, status_code=status.HTTP_201_CREATED)
def create_sample(body: SampleIn):
    new = Sample(id=len(db) + 1, **body.model_dump())
    db[new.id] = new
    return new

@app.delete("/samples/{sample_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sample(sample_id: int):
    if db.pop(sample_id, None) is None:
        raise HTTPException(status_code=404, detail="sample not found")
```

```bash
uv add "fastapi[standard]"         # 含 uvicorn 與 fastapi CLI
uv run fastapi dev main.py         # 開發模式：自動重載，http://127.0.0.1:8000/docs
uv run fastapi run main.py         # 正式模式（不重載、監聽 0.0.0.0）
```

| 進階功能 | 用途 |
| --- | --- |
| `async def` 端點 | 端點內呼叫非同步 I/O（`httpx`、async DB driver）時用；呼叫阻塞函式（一般 DB driver、`requests`、模型推論）就用一般 `def`，FastAPI 會放到 thread pool |
| `Depends()` | 依賴注入：共用 DB session、認證、分頁參數 |
| `APIRouter` | 把端點拆到多個檔案 |
| 背景任務 `BackgroundTasks` | 回應後再做的小工作（寄信、寫 log）；長時間任務改用佇列（Celery、RQ） |
| 模型推論 | 模型在啟動時載入一次（`lifespan`），不要每個請求重新載入 |

## 測試

| 層級 | 範圍 | 工具 |
| --- | --- | --- |
| 單元測試 | 純函式、商業邏輯 | `pytest` |
| 端點測試 | 經過路由、驗證、序列化的完整請求 | `fastapi.testclient.TestClient`（不需啟動伺服器） |
| 功能 / 整合測試 | 多步驟流程、認證、資料庫 | 測試用資料庫 + `TestClient` |

```python
# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_and_get():
    r = client.post("/samples", json={"name": "S1", "tissue": "liver", "reads_m": 32.1})
    assert r.status_code == 201
    assert client.get(f"/samples/{r.json()['id']}").json()["name"] == "S1"

def test_validation_error():
    r = client.post("/samples", json={"name": "S2", "tissue": "lung", "reads_m": -1})
    assert r.status_code == 422

def test_not_found():
    assert client.get("/samples/999").status_code == 404
```

好的 API 測試涵蓋：成功回應、失敗回應（404、422）、驗證行為、回應 schema 與狀態碼。pytest 的 fixture、marker 等見 [測試](../../data-science/python-foundations/testing.md)；每次 push 自動執行見 [GitHub Actions](../devops/github-actions.md)。

## 部署

| 方式 | 說明 |
| --- | --- |
| `fastapi run` / `uvicorn main:app --workers 4` | 單機多 worker |
| [Docker](../containers-and-env/docker/README.md) | 官方建議的容器化方式，一個容器跑一個 Uvicorn process，由外部（Kubernetes、Compose）負責擴展 |
| 雲端 | 容器服務（Cloud Run、Azure Container Apps、AWS App Runner / ECS） |
| ML 模型服務的監控與版本 | 見 [部署與監控](../../data-science/machine-learning/production/deployment-and-monitoring.md) |
