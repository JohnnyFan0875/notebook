[容器與環境](../README.md) › [Docker](README.md) › Compose

# Docker Compose

用一個 `compose.yaml` 宣告多個容器（API、資料庫、快取、前端）以及它們的網路、volume、環境變數，一個指令全部啟動。適合本機開發、小型部署與可重現的示範環境；跨多台機器的正式營運用 [Kubernetes](../kubernetes.md)。

> Compose V2 是 Docker CLI 的子指令：`docker compose`（空格）。舊的獨立程式 `docker-compose`（連字號）已停止維護；檔案中的 `version:` 欄位也已過時，不需要寫。

## 範例

```yaml
# compose.yaml
services:
  api:
    build: .                              # 用目前目錄的 Dockerfile 建置
    ports:
      - "8000:8000"                       # 主機:容器
    environment:
      DATABASE_URL: postgresql://postgres:example@db:5432/app   # 用服務名稱 db 連線
    env_file: .env
    volumes:
      - ./src:/app/src                    # bind mount：開發時即時更新程式碼
    depends_on:
      db:
        condition: service_healthy        # 等 db 通過健康檢查才啟動

  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: example
      POSTGRES_DB: app
    volumes:
      - pgdata:/var/lib/postgresql/data   # named volume：持久保存
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      retries: 10

  jupyter:
    image: quay.io/jupyter/scipy-notebook:2024-10-07
    ports:
      - "127.0.0.1:8888:8888"
    volumes:
      - ./notebooks:/home/jovyan/work
    profiles: ["dev"]                     # 只在 --profile dev 時啟動

volumes:
  pgdata:
```

| 欄位 | 作用 |
| --- | --- |
| `services` | 每個服務一個容器（或多個副本） |
| `build` / `image` | 從 Dockerfile 建置 / 使用現成映像檔 |
| `ports` | `主機:容器` port 對應 |
| `volumes` | bind mount（`./path:...`）或 named volume（在頂層 `volumes:` 宣告） |
| `environment` / `env_file` | 環境變數 |
| `depends_on` | 啟動順序；只保證**啟動**順序，不保證依賴已準備好接受連線 → 搭配 `condition: service_healthy` |
| `healthcheck` | 判斷服務是否就緒 |
| `networks` | 自訂網路；未指定時所有服務在同一個預設網路，可用服務名稱互連 |
| `profiles` | 選擇性啟動的服務 |

## 常用指令

```bash
docker compose up -d                 # 建立並在背景啟動所有服務
docker compose up -d --build         # 先重新建置映像檔
docker compose --profile dev up -d   # 包含 dev profile 的服務
docker compose ps                    # 服務狀態
docker compose logs -f api           # 某個服務的 log
docker compose exec db psql -U postgres   # 在服務容器中執行指令
docker compose run --rm api pytest   # 一次性執行
docker compose restart api
docker compose stop                  # 停止（保留容器）
docker compose down                  # 停止並刪除容器與網路（保留 named volume）
docker compose down -v               # 連 volume 一起刪除（資料會消失）
docker compose config                # 顯示合併變數後的最終設定（檢查 YAML）
docker compose ls                    # 所有 Compose 專案
docker compose top                   # 各服務容器內的程序
```

| 注意 | 說明 |
| --- | --- |
| `.env` 檔 | 與 `compose.yaml` 同目錄的 `.env` 會自動用於變數替換（`${PORT}`）；不要提交到 Git |
| 修改 Dockerfile 後 | 要 `--build`，否則沿用舊映像檔 |
| 資料庫密碼 | 示範可寫在檔案中；正式環境用 secrets 或環境變數 |
