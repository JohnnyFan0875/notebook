[容器與環境](../README.md) › [Docker](README.md) › 網路

# Docker 網路 (Network)

容器有自己的網路介面：**在容器內，`localhost` 指的是容器自己**，不是主機。三種常見連線：外部 → 容器（port 對應）、容器 → 主機（`host.docker.internal`）、容器 → 容器（自訂網路 + 容器名稱）。

## 外部連到容器：port 對應

```bash
docker run -d -p 8000:8000 myapi          # 主機 8000 → 容器 8000
docker run -d -p 3000:8080 myapp          # 主機 3000 → 容器 8080
docker run -d -p 127.0.0.1:8888:8888 jupyter/minimal-notebook   # 只允許本機連線
docker port <container>                    # 查看對應
```

> 容器內的服務要監聽 `0.0.0.0`，不能只聽 `127.0.0.1`，否則 port 對應了也連不到（例如 `uvicorn --host 0.0.0.0`、`jupyter lab --ip 0.0.0.0`）。

## 容器連到主機：`host.docker.internal`

容器要呼叫主機上執行的資料庫或 API 時，用 Docker 提供的特殊名稱 `host.docker.internal`：

```bash
curl http://host.docker.internal:8000
mongodb://host.docker.internal:27017/mydb
```

| 平台 | 支援 |
| --- | --- |
| Docker Desktop（Windows / macOS） | 內建 |
| Linux Docker Engine | 需加 `--add-host=host.docker.internal:host-gateway` |

不要用 `docker inspect` 查到的 IP（如 `172.17.0.1`）寫死在設定中：IP 不穩定、換機器就失效。

## 容器之間：自訂網路

同一個自訂網路上的容器可以用**容器名稱**當主機名互相連線（內建 DNS），不需要對外開 port：

```bash
docker network create appnet
docker run -d --name mongodb --network appnet mongo:7
docker run -d --name api --network appnet -p 3000:3000 myapi
# api 容器的程式中：mongodb://mongodb:27017/mydb
```

```bash
docker network ls
docker network inspect appnet          # 哪些容器在這個網路上
docker network connect appnet <container>
docker network rm appnet
```

| 網路驅動 | 說明 |
| --- | --- |
| `bridge`（預設） | 單機上容器的私有網路；**預設 bridge 不支援以名稱互連**，要用自訂網路 |
| `host` | 容器直接使用主機網路（Linux），不需 `-p` |
| `none` | 無網路 |

> 多個服務一起啟動時，[Compose](compose.md) 會自動建立網路，服務之間直接用服務名稱連線。
