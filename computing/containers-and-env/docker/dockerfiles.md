[容器與環境](../README.md) › [Docker](README.md) › Dockerfile

# Dockerfile

Dockerfile 描述如何建立映像檔：從哪個基底映像檔開始、複製哪些檔案、安裝哪些套件、容器啟動時執行什麼。寫得好的 Dockerfile 建置快（善用快取）、映像檔小、可重現。

## 指令

| 指令 | 作用 | 執行時機 |
| --- | --- | --- |
| `FROM` | 基底映像檔；每個 `FROM` 開始一個建置階段 | 建置 |
| `WORKDIR` | 之後指令的工作目錄，不存在會自動建立 | 建置 + 執行 |
| `COPY` | 從建置脈絡複製檔案（目的目錄不存在會自動建立） | 建置 |
| `ADD` | 類似 `COPY`，另可解壓本機 tar、下載 URL；一般用 `COPY` | 建置 |
| `RUN` | 執行指令，產生新的一層 | 建置 |
| `ENV` | 環境變數，建置與執行時都有效 | 建置 + 執行 |
| `ARG` | 建置參數，只在建置時有效 | 建置 |
| `USER` | 之後指令與容器執行時的使用者 | 建置 + 執行 |
| `EXPOSE` | **只是文件 / metadata**，不會開啟或對應任何 port | — |
| `CMD` | 容器的預設指令，可被 `docker run <image> <cmd>` 覆蓋 | 執行 |
| `ENTRYPOINT` | 固定的執行檔，`CMD` 成為它的預設參數 | 執行 |
| `HEALTHCHECK` | 定期檢查容器是否健康 | 執行 |

> 沒寫 `CMD` 時沿用基底映像檔的 `CMD`。`CMD` / `ENTRYPOINT` 用 JSON 陣列（exec 形式）`["python", "main.py"]`，訊號才能正確傳給程式。

## 範例：Python 分析環境

```dockerfile
FROM python:3.12-slim

# 1. 系統套件：很少變動，放最前面；同一個 RUN 內安裝並清理快取
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# 2. 先只複製相依清單並安裝：程式碼改變時這層仍可用快取
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# 3. 最後複製程式碼：最常變動
COPY . .
RUN uv sync --frozen --no-dev

# 4. 非 root 使用者執行
RUN useradd --create-home appuser
USER appuser

ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "-m", "mypkg.main"]
```

> uv 的映像檔標籤可固定版本（`ghcr.io/astral-sh/uv:<version>`）以完全重現；`latest` 方便但會變動。

## 範例：生資工具（micromamba + bioconda）

```dockerfile
FROM mambaorg/micromamba:1.5.8
COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/environment.yml
RUN micromamba install -y -n base -f /tmp/environment.yml \
    && micromamba clean --all --yes
# 基底映像檔已設定好啟動時自動啟用 base 環境
```

`environment.yml` 的寫法見 [Conda](../conda.md)。R 環境常用 `rocker/r-ver:<版本>` 為基底，搭配 [renv](../../../data-science/r-foundations/reproducible-environments-with-renv.md) 還原套件。只需要單一工具時，直接用 BioContainers 的現成映像檔，不必自己寫。

## 層與快取

- 建置時逐個指令比對快取；某一層改變，**之後的層全部重建**。
- 很少變動的步驟放前面（系統套件），常變動的放後面（程式碼）。
- 下載、解壓、清理寫在**同一個** `RUN`：分開寫的話，中間檔已經存在前一層，之後刪除也不會讓映像檔變小。

```dockerfile
RUN curl -L https://example.com/tool.tar.gz -o /tmp/tool.tar.gz \
    && tar -xzf /tmp/tool.tar.gz -C /opt \
    && rm /tmp/tool.tar.gz
```

## Multi-stage 建置

把編譯工具留在建置階段，最終映像檔只放執行需要的產物，縮小體積與攻擊面。

```dockerfile
FROM golang:1.22 AS build
WORKDIR /src
COPY . .
RUN go build -o /out/app ./cmd/app

FROM debian:bookworm-slim
COPY --from=build /out/app /usr/local/bin/app
CMD ["app"]
```

## `ARG` vs `ENV`

```dockerfile
ARG VERSION=3.19              # 建置參數；可用在 FROM
FROM alpine:${VERSION}
ARG VERSION                   # FROM 之後要重新宣告才能使用
ENV APP_VERSION=${VERSION} \
    APP_PORT=8080 \
    LOG_LEVEL=info
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]        # 腳本中直接讀 $APP_PORT；Python 用 os.getenv("APP_PORT")
```

```bash
docker build --build-arg VERSION=3.20 -t myimage .     # 建置時覆蓋 ARG
docker run -e LOG_LEVEL=debug myimage                  # 執行時覆蓋 ENV
docker run --env-file .env myimage                     # 從檔案載入（每行 KEY=value）
```

| | `ARG` | `ENV` |
| --- | --- | --- |
| 建置時可用 | 是 | 是 |
| 執行時（容器內）可用 | 否 | 是 |
| 執行時可覆蓋 | 否 | 是（`-e`） |
| 存在映像檔 metadata | 否（但會出現在 `docker history`） | 是 |
| 用途 | 建置邏輯（版本） | 應用程式設定 |

> 密碼、token **不要**用 `ARG` 或 `ENV` 寫進映像檔（任何拿到映像檔的人都看得到）；執行時用 `-e` / `--env-file` 傳入，建置時需要用 `RUN --mount=type=secret`。

## `.dockerignore`：建置脈絡

`docker build .` 會把**整個目錄**（建置脈絡 build context）送給 Docker daemon，`COPY . .` 也會複製所有內容。`.dockerignore`（語法同 `.gitignore`）排除不需要的檔案：

```text
.git
.venv
__pycache__/
*.log
.env
data/
results/
*.bam
*.fastq.gz
```

| 好處 | 說明 |
| --- | --- |
| 建置更快 | 不必傳送 GB 等級的資料目錄 |
| 映像檔更小 | 資料不會被 `COPY . .` 帶進去 |
| 安全 | `.env`、金鑰不會意外進入映像檔 |
| 快取更穩定 | 無關檔案變動不會讓 `COPY` 層失效 |

> 資料不放進映像檔：映像檔放**環境與程式**，資料在執行時用 [掛載](volumes.md) 提供。

## `USER`：不要以 root 執行

```dockerfile
RUN useradd --create-home appuser
USER appuser
```

需要 root 的設定（安裝套件）先做完，最後切換成一般使用者；`docker run` 覆蓋指令時仍沿用 `WORKDIR` 與 `USER`。
