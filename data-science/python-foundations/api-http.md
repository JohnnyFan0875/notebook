[Data Science](../README.md) › [Python Foundations](README.md) › API 與 HTTP

# API 與 HTTP (Web APIs with requests)

呼叫 Web API 的流程很固定：組 URL → 加查詢參數、標頭、認證 → 送出請求 → 檢查狀態碼 → 解析回應 → 明確處理錯誤。Python 的預設工具是 `requests`；生資常見的 Ensembl REST、NCBI E-utilities、UniProt 都是這個模式。

## HTTP 請求與回應

```
Request                                   Response
  method   GET / POST / PUT / DELETE        status   200 / 404 / 429 / 500
  URL      https://api.x.org/genes/42       headers  Content-Type: application/json
           └ base ┘└ path ┘?q=TP53          body     {"id": 42, ...}
  headers  Accept, Authorization
  body     JSON（POST / PUT 時）
```

| 方法 | 用途 | 冪等 (idempotent)？ |
| --- | --- | --- |
| `GET` | 取得資源（最常用） | 是 |
| `POST` | 建立資源；也常用於參數太長的查詢 | 否 |
| `PUT` | 整筆取代 | 是 |
| `PATCH` | 部分更新 | 不一定 |
| `DELETE` | 刪除 | 是 |

URL 的 path 指向資源（`/albums/42/tracks`），query string 放篩選、排序、分頁、搜尋條件。

## 基本請求

```python
import requests

r = requests.get(
    "https://rest.ensembl.org/lookup/symbol/homo_sapiens/TP53",
    headers={"Accept": "application/json"},   # 內容協商：要求 JSON
    timeout=10,                               # 一定要設：預設會無限等待
)
r.status_code                  # 200
r.url                          # 實際送出的 URL（含編碼後的參數）
r.headers["Content-Type"]      # 'application/json'
r.json()["id"]                 # 'ENSG00000141510'：解析 JSON → dict
r.text                         # 原始字串；r.content 為 bytes（下載檔案用）

# 查詢參數用 params=，自動處理編碼（空白、&、中文）
r = requests.get(
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
    params={"db": "pubmed", "term": "CRISPR AND 2024[pdat]", "retmode": "json", "retmax": 20},
    timeout=10,
)
r.json()["esearchresult"]["idlist"]

# 送 JSON：用 json=，自動序列化並設 Content-Type: application/json
r = requests.post("https://api.example.com/playlists", json={"name": "Road Trip", "tracks": [1, 2]}, timeout=10)
r.request.headers["Content-Type"]   # 'application/json'
# data= 則是送表單 (application/x-www-form-urlencoded)
```

| 回應屬性 | 內容 |
| --- | --- |
| `status_code` | 數字狀態碼 |
| `ok` | `status_code < 400` |
| `headers` | 回應標頭（不分大小寫的 dict） |
| `json()` | 解析 JSON；回應不是 JSON 時丟 `JSONDecodeError` |
| `text` / `content` | 字串 / bytes |
| `elapsed` | 花費時間 |

`urllib.request` 是標準庫的替代品，不想多裝套件時可用，但寫法較囉嗦；非同步大量請求可用 `httpx`（API 幾乎與 requests 相同，另支援 async 與 HTTP/2）。

## 狀態碼

| 類別 | 代表 | 常見 | 該怎麼做 |
| --- | --- | --- | --- |
| 2xx | 成功 | `200 OK`、`201 Created`、`204 No Content` | — |
| 3xx | 重新導向 | `301`、`302`、`304 Not Modified` | requests 預設自動跟隨 |
| 4xx | **請求有問題** | `400` 參數錯、`401` 未認證、`403` 無權限、`404` 不存在 | 修正請求，重試沒用 |
| | | `429 Too Many Requests` | 降速，依 `Retry-After` 等待後重試 |
| 5xx | **伺服器有問題** | `500`、`502 Bad Gateway`、`503`、`504 Gateway Timeout` | 稍後重試（指數退避） |

## 錯誤處理

```python
import requests

try:
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()                        # 4xx / 5xx → HTTPError
    data = r.json()
except requests.HTTPError as e:
    log.error("HTTP %s for %s: %s", e.response.status_code, e.response.url, e.response.text[:200])
    raise
except (requests.ConnectionError, requests.Timeout) as e:
    log.error("network problem: %s", e)
    raise
except requests.JSONDecodeError:
    log.error("not JSON: %s", r.text[:200])     # 常見：錯誤頁回傳的是 HTML
    raise
```

`raise_for_status()` 讓成功路徑保持簡單、失敗一定浮現；不要只檢查 `if r.status_code == 200` 然後默默略過失敗。

## Session、重試與限速

大量呼叫時用 `Session`：重用 TCP 連線（更快），並統一設定標頭與重試。

```python
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
session.headers.update({"Accept": "application/json", "User-Agent": "mylab-pipeline/0.1 (me@uni.edu)"})
retry = Retry(
    total=5,
    backoff_factor=1,                           # 等待 1, 2, 4, 8... 秒（指數退避）
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET", "POST"],
    respect_retry_after_header=True,
)
session.mount("https://", HTTPAdapter(max_retries=retry))

for gene in genes:
    r = session.get(f"https://rest.ensembl.org/lookup/symbol/homo_sapiens/{gene}", timeout=10)
    if r.status_code == 404:
        continue                                # 查無此基因：記錄後跳過
    r.raise_for_status()
    results.append(r.json())
    time.sleep(0.1)                             # 遵守服務的速率限制
```

| 服務 | 速率限制（以官方文件為準） | 批次端點 |
| --- | --- | --- |
| NCBI E-utilities | 無 API key 每秒 3 次；有 key 每秒 10 次 | `epost` + `efetch`、一次傳多個 ID |
| Ensembl REST | 每秒約 15 次 | `POST /lookup/symbol` 一次查多個 |

> 能批次就批次：一次 POST 1000 個 ID，比 1000 次 GET 快得多也不容易被封鎖。重複執行的分析把回應快取到本地（`requests-cache` 或自己存 JSON），也能讓結果可重現——線上資料庫會更新。

## 分頁 (Pagination)

```python
def fetch_all(url, params, page_size=100):
    """依 offset 分頁抓到沒有資料為止。"""
    offset = 0
    while True:
        r = session.get(url, params={**params, "limit": page_size, "offset": offset}, timeout=10)
        r.raise_for_status()
        items = r.json()["results"]
        if not items:
            break
        yield from items
        offset += page_size

# 另一種常見做法：回應帶下一頁連結
url = "https://rest.uniprot.org/uniprotkb/search?query=gene:TP53&format=json&size=500"
while url:
    r = session.get(url, timeout=30)
    r.raise_for_status()
    handle(r.json()["results"])
    url = r.links.get("next", {}).get("url")    # 解析 Link 標頭
```

| 分頁方式 | 參數 | 注意 |
| --- | --- | --- |
| offset / limit | `offset=200&limit=100` | 資料在分頁期間變動時可能重複或遺漏 |
| page number | `page=3&per_page=100` | 同上 |
| cursor / token | `cursor=abc...` 或 `Link: <...>; rel="next"` | 最穩定，大型 API 常用 |

## 認證 (Authentication)

| 方式 | 寫法 | 備註 |
| --- | --- | --- |
| API key（查詢參數） | `params={"api_key": KEY}` | NCBI 用這種；URL 可能被記錄在 log |
| API key（標頭） | `headers={"X-API-Key": KEY}` | |
| Bearer token | `headers={"Authorization": f"Bearer {TOKEN}"}` | 最常見的現代做法（OAuth 2） |
| Basic auth | `auth=("user", "password")` | requests 自動產生 `Authorization` 標頭；只能走 HTTPS |

```python
import os
TOKEN = os.environ["MY_API_TOKEN"]          # 從環境變數或 .env 讀，不要寫死在程式或 notebook 裡
session.headers["Authorization"] = f"Bearer {TOKEN}"
```

設定檔與 `.env` 的管理見 [腳本與 CLI](scripting-and-cli.md#設定檔-configuration-files)。

## 下載大檔

```python
from pathlib import Path

def download(url, dest: Path, chunk=1 << 20):
    with session.get(url, stream=True, timeout=30) as r:   # stream=True：不一次讀進記憶體
        r.raise_for_status()
        tmp = dest.with_suffix(dest.suffix + ".part")
        with open(tmp, "wb") as f:
            for block in r.iter_content(chunk_size=chunk):
                f.write(block)
        tmp.rename(dest)                                    # 下載完整才改名，避免留下半個檔案
```

下載參考基因組、資料庫檔後，比對官方提供的 checksum（`hashlib.md5` / `sha256`），確認檔案完整。

## 除錯檢查表

| 問題 | 檢查 |
| --- | --- |
| URL、path 正確嗎？ | 印出 `r.url` |
| 參數編碼對嗎？ | 用 `params=`，不要手動拼字串 |
| HTTP 方法對嗎？ | 文件寫 POST 卻用 GET 常回 `405` |
| 必要標頭都有嗎？ | `Accept`、`Content-Type`、`Authorization` |
| 回應真的是 JSON 嗎？ | 先看 `r.headers["Content-Type"]` 再 `.json()` |
| 是 4xx 還是 5xx？ | 4xx 修請求；5xx / 429 重試 |

網頁 HTML 的擷取見 [Web Scraping](../web-scraping/README.md)；把 API 資料讀成 DataFrame 見 [匯入資料](importing-data.md)。
