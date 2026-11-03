[容器與環境](../README.md) › [Docker](README.md) › 映像檔

# Docker 映像檔 (Image)

映像檔是不可變的範本：應用程式 + 執行環境 + 系統函式庫 + 相依套件，由多層 (layer) 疊成，每層可快取、可在不同映像檔間共用。容器是映像檔的執行個體。

## 命名

```
registry.example.com/myteam/rnaseq:1.2.0
└──── registry ────┘ └─ 儲存庫 ─┘ └ tag ┘
```

| 部分 | 說明 |
| --- | --- |
| registry | 省略時為 Docker Hub（`docker.io`）；其他：`ghcr.io`、`quay.io` |
| 儲存庫 (repository) | 官方映像檔沒有前綴（`python`、`ubuntu`）；其他為 `使用者/名稱` |
| tag | 版本標籤；省略時為 `latest` |
| digest | `@sha256:...`：內容的雜湊，**完全**固定的版本 |

> 可重現的分析用明確的 tag（`python:3.12.7-slim`、`rocker/r-ver:4.4.1`），最嚴格時用 digest；`latest` 隨時會變。

## 常用指令

```bash
docker images                                   # 本機映像檔（= docker image ls）
docker pull rocker/r-ver:4.4.1                  # 下載
docker build -t myapp:1.0 .                     # 用目前目錄的 Dockerfile 建置
docker tag myapp:1.0 ghcr.io/me/myapp:1.0       # 新增一個名稱，指向同一個映像檔（不複製）

docker login ghcr.io                            # 登入 registry
docker push ghcr.io/me/myapp:1.0                # 上傳：名稱要包含 registry 與帳號

docker save -o myapp.tar myapp:1.0              # 匯出成檔案（無法連 registry 的環境）
docker load -i myapp.tar                        # 匯入

docker rmi myapp:1.0                            # 刪除；有容器（含已停止）在用時無法刪除
docker image prune                              # 刪除 dangling 映像檔（沒有 tag、沒被使用）
docker image prune -a                           # 刪除所有沒有容器在用的映像檔
```

## 分層與建置快取

Dockerfile 的每個指令產生一層；建置時逐層比對快取，**某一層改變，之後的層全部重建**。

```bash
docker history myapp:1.0                                    # 各層大小與對應指令
docker image inspect myapp:1.0 | jq '.[0].RootFS.Layers | length'   # 層數
docker image inspect myapp:1.0 | jq '.[0].Config.Env'                # 環境變數
```

| 原則 | 說明 |
| --- | --- |
| 很少改變的步驟放前面 | 系統套件、相依套件安裝 |
| 常改變的放後面 | 複製程式碼 |
| 先複製相依清單、安裝，再複製程式碼 | 改程式碼不會讓套件重新安裝 |

寫法細節見 [Dockerfile](dockerfiles.md)。

## 多平台建置：buildx

Apple Silicon（arm64）建的映像檔不能直接在 x86 伺服器（amd64）上跑，反之亦然。

```bash
docker buildx create --name mybuilder --use     # 建立並使用 builder
docker buildx inspect --bootstrap

# 多平台：結果無法載入本機，通常直接推到 registry
docker buildx build --platform linux/amd64,linux/arm64 -t ghcr.io/me/myapp:1.0 --push .

# 單一平台並載入本機
docker buildx build --platform linux/amd64 -t myapp:local --load .

docker buildx rm mybuilder
```

> `exec format error` 通常就是平台不符：在 Mac 上建置要給伺服器用的映像檔時加 `--platform linux/amd64`。
