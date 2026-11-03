[Computing](../README.md) › [Web 開發](README.md) › Web 基礎

# Web 基礎 (Web Fundamentals)

在瀏覽器輸入網址到看到頁面，中間經過 DNS、HTTP、HTML / CSS / JavaScript 的分工。理解這條路徑，才看得懂 API、前端框架、SSR 與部署在做什麼；呼叫 API 的 Python 寫法見 [API 與 HTTP](../../data-science/python-foundations/api-http.md)。

## 瀏覽器如何載入頁面

```
輸入 https://example.org/genes
  1. DNS 查詢        example.org → 93.184.215.14
  2. TCP + TLS 連線  建立加密通道（HTTPS，port 443）
  3. HTTP 請求       GET /genes
  4. 伺服器回應      200 OK + HTML
  5. 解析 HTML       建立 DOM；遇到 <link> / <script> / <img> 再發請求取 CSS、JS、圖片
  6. 套用 CSS        計算樣式與版面 (layout)，繪製 (paint)
  7. 執行 JavaScript 修改 DOM、綁定事件、呼叫 API (fetch) 取得更多資料
```

| 名詞 | 意義 |
| --- | --- |
| URL | `https://example.org:443/genes?symbol=TP53#summary`：協定、主機、port、路徑、query string、fragment（只在瀏覽器端） |
| DNS | 網域名稱 → IP 位址 |
| HTTPS | HTTP + TLS 加密；憑證證明伺服器身分 |
| DOM (Document Object Model) | 瀏覽器把 HTML 解析成的樹狀物件，JavaScript 透過它修改頁面 |
| 靜態資源 | HTML、CSS、JS、圖片：檔案本身不隨使用者改變，可放 CDN |
| CDN | 把靜態檔快取在離使用者近的節點 |

## HTML / CSS / JavaScript 分工

| 技術 | 負責 | 例子 |
| --- | --- | --- |
| HTML | **結構與內容**：標題、段落、表格、表單、連結 | `<h1>TP53</h1><table>…</table>` |
| CSS | **外觀與版面**：顏色、字型、間距、排版、響應式 | `h1 { color: steelblue; }` |
| JavaScript | **行為**：事件、修改 DOM、呼叫 API、狀態 | `button.addEventListener("click", load)` |

```html
<!doctype html>
<html>
<head>
  <style>.high { color: tomato; }</style>
</head>
<body>
  <h1>Gene lookup</h1>
  <input id="sym" value="TP53"> <button id="go">Search</button>
  <p id="out"></p>
  <script>
    document.getElementById("go").addEventListener("click", async () => {
      const sym = document.getElementById("sym").value;
      const r = await fetch(`https://rest.ensembl.org/lookup/symbol/homo_sapiens/${sym}?content-type=application/json`);
      const gene = await r.json();
      document.getElementById("out").textContent = `${gene.id} chr${gene.seq_region_name}:${gene.start}-${gene.end}`;
    });
  </script>
</body>
</html>
```

> 頁面越來越互動、狀態越來越多時，手動操作 DOM 會難以維護，這就是 [React](react/README.md) 這類宣告式 UI 函式庫要解決的問題。

## HTTP 請求與回應

```
Request                                   Response
  GET /api/genes?symbol=TP53 HTTP/1.1       HTTP/1.1 200 OK
  Host: example.org                         Content-Type: application/json
  Accept: application/json                  Cache-Control: max-age=3600
  Authorization: Bearer <token>
                                            {"id": "ENSG00000141510", ...}
```

| 元素 | 重點 |
| --- | --- |
| 方法 | `GET` 取得、`POST` 建立、`PUT` 取代、`PATCH` 部分更新、`DELETE` 刪除 |
| 狀態碼 | 2xx 成功、3xx 重新導向、4xx 請求有問題、5xx 伺服器有問題（[詳表](../../data-science/python-foundations/api-http.md#狀態碼)） |
| 標頭 (header) | `Content-Type`（body 格式）、`Accept`（想要的格式）、`Authorization`（認證）、`Cache-Control`（快取） |
| 無狀態 (stateless) | 每個請求獨立；登入狀態靠 cookie 或 token 在每次請求帶上 |
| Cookie | 伺服器用 `Set-Cookie` 存在瀏覽器，之後同網域請求自動帶上 |

## REST API

REST 是設計 HTTP API 的慣例：URL 代表**資源**（名詞），HTTP 方法代表**動作**。

| 好的設計 | 避免 |
| --- | --- |
| `GET /samples/42` | `GET /getSample?id=42` |
| `POST /samples`（body 為新資料） | `GET /createSample?name=...` |
| `GET /samples?tissue=liver&page=2` | 把篩選放在路徑：`/samples/liver/page2` |
| `DELETE /samples/42` → `204` | 刪除失敗也回 `200` 加錯誤訊息 |
| 回 JSON，錯誤也有一致的格式 | 錯誤時回 HTML 錯誤頁 |

用 Python 寫 REST API 見 [FastAPI](fastapi.md)。其他 API 風格：GraphQL（客戶端自訂要哪些欄位）、gRPC（二進位、服務之間的高效能呼叫）。

## 同源政策與 CORS

瀏覽器預設只允許 JavaScript 呼叫**同源**（協定 + 主機 + port 相同）的 API。前端在 `localhost:5173`、API 在 `localhost:8000` 就是不同源，請求會被瀏覽器擋下，錯誤訊息出現 `CORS`。

| 解法 | 說明 |
| --- | --- |
| API 回傳 `Access-Control-Allow-Origin` 標頭 | FastAPI 用 `CORSMiddleware` 設定允許的來源 |
| 開發時用 proxy | Vite 的 `server.proxy` 把 `/api` 轉到後端 |

> CORS 只限制**瀏覽器**；`curl`、Python `requests` 不受影響，所以「Python 呼叫得到、網頁呼叫不到」通常就是 CORS。

## 開發者工具

瀏覽器按 `F12`（macOS：`Cmd + Option + I`）：

| 分頁 | 用途 |
| --- | --- |
| Elements | 檢視與即時修改 DOM、CSS |
| Console | JavaScript 錯誤訊息、執行指令 |
| Network | 每個請求的 URL、狀態碼、標頭、回應內容、耗時；可「Copy as cURL」 |
| Application | Cookie、localStorage |

> 網頁爬蟲先看 Network 分頁：資料常常來自一個 JSON API，直接呼叫比解析 HTML 簡單，見 [網頁爬蟲](../../data-science/web-scraping/README.md)。
