[容器與環境](../README.md) › [Docker](README.md) › 容器

# Docker 容器 (Container)

容器是映像檔的執行個體：有自己的檔案系統（映像檔 + 一層可寫層）、程序、網路介面與資源限制。容器內的修改在容器刪除後就消失，要保存的資料放在 [volume 或掛載目錄](volumes.md)。

## `docker run`

```bash
docker run -it --rm python:3.12-slim bash                     # 互動式、離開即刪除
docker run -d --name api -p 8000:8000 myapi:1.0               # 背景執行、對應 port
docker run --rm -v "$PWD":/data -w /data \
    quay.io/biocontainers/samtools:<tag> samtools flagstat sample.bam   # 一次性執行工具
docker run --rm --user "$(id -u):$(id -g)" -v "$PWD":/work -w /work myimg ...   # 輸出檔歸自己所有
docker run --cpus 4 --memory 8g --gpus all myimg              # 資源限制、GPU
```

| 選項 | 意義 |
| --- | --- |
| `-i` / `-t` | 保持 STDIN 開啟 / 配置終端機；互動式時合用 `-it` |
| `-d` | 背景 (detached) 執行 |
| `--rm` | 結束後自動刪除容器 |
| `--name` | 容器名稱（之後用名稱代替 ID） |
| `-p 主機port:容器port` | port 對應，見 [網路](network.md) |
| `-v 主機路徑:容器路徑` | 掛載，見 [Volume 與掛載](volumes.md) |
| `-w` | 容器內的工作目錄 |
| `-e KEY=val`、`--env-file .env` | 環境變數 |
| `--user uid:gid` | 以指定身分執行（避免輸出檔變成 root 擁有） |
| `--cpus`、`--memory` | 資源上限 |
| `--gpus all` | 使用 GPU（需 NVIDIA Container Toolkit） |
| `--platform linux/amd64` | 指定平台 |

> 映像檔不存在時 `docker run` 會自動 `pull`。`docker run` = `docker create` + `docker start`（並接上輸出）。

## 管理與除錯

```bash
docker ps                       # 執行中的容器；-a 包含已停止
docker logs -f api              # 容器的 stdout / stderr；-f 持續追蹤；已停止的容器也能看
docker exec -it api bash        # 在執行中的容器開新的 shell（沒有 bash 時用 sh）
docker attach api               # 接上主程序（PID 1）的輸入輸出；Ctrl+C 可能停止容器
docker stop api; docker start api
docker start -ai mycontainer    # 啟動並接上
docker inspect api              # 完整設定（掛載、網路、環境變數）
docker stats                    # 即時 CPU / 記憶體用量
docker top api                  # 容器內的程序

docker cp results.csv api:/app/data/          # 主機 → 容器
docker cp api:/app/output/report.html ./      # 容器 → 主機（停止的容器也可以）

docker rm api                   # 刪除已停止的容器；-f 強制刪除執行中的
docker commit api myapi:debug   # 把容器目前狀態存成映像檔（只用於除錯，正式做法是寫 Dockerfile）
```

| `exec` | `attach` |
| --- | --- |
| 開一個新程序（新的 shell） | 接上既有的主程序 |
| 可同時開多個 | 多個終端機共用同一個輸入輸出 |
| `exit` 只結束這個 shell | `Ctrl + C` 可能讓容器停止；用 `Ctrl + P` `Ctrl + Q` 離開 |
| 除錯首選 | 重新接上用 `-it` 啟動、後來 detach 的互動程式 |

## 清理與磁碟用量

映像檔、停止的容器、volume、建置快取會默默累積數十 GB（Docker Desktop 的虛擬磁碟不會自動縮小）。

```bash
docker system df                         # 各類別占用空間
docker system df -v                      # 詳細

docker container prune                   # 刪除所有停止的容器
docker image prune                       # 刪除 dangling 映像檔（無 tag、未使用）
docker images --filter "dangling=true"   # 先列出看看
docker image prune -a                    # 刪除所有沒有容器在用的映像檔
docker volume prune                      # 刪除未使用的 volume（資料會消失！）
docker builder prune                     # 刪除建置快取
docker system prune                      # 停止的容器 + dangling 映像檔 + 未使用網路 + 建置快取
docker system prune -a --volumes         # 全部未使用的東西（含 volume，小心）
```

| 名詞 | 意義 |
| --- | --- |
| dangling 映像檔 | 沒有 tag、沒有容器使用（重新建置同名映像檔後，舊的就變成 `<none>`） |
| 刪除順序 | 映像檔被容器（含停止的）使用時無法刪除：先刪容器再刪映像檔 |

> `prune` 加上 `--volumes` 或執行 `docker volume prune` 前先確認：資料庫等重要資料可能就存在 volume 裡。
