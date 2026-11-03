[容器與環境](../README.md) › [Docker](README.md) › Volume 與掛載

# Volume 與掛載 (Volumes and Bind Mounts)

容器的檔案系統是短暫的：容器刪除後，裡面寫入的東西就消失。要讓資料進出容器、或在容器之間共用與持久保存，用掛載 (mount)。分析工作最常用 bind mount：把主機上的資料夾掛進容器，工具讀主機的輸入、輸出寫回主機。

## 三種掛載

| 類型 | 語法 | Docker 管理 | 需要主機路徑 | 持久 | 典型用途 |
| --- | --- | --- | --- | --- | --- |
| Bind mount | `-v /host/path:/container/path` | 否 | 是 | 是（就是主機檔案） | 分析資料、開發時即時編輯程式碼 |
| Named volume | `-v mydata:/container/path` | 是 | 否 | 是 | 資料庫等應用程式的持久資料 |
| Anonymous volume | `-v /container/path` 或 Dockerfile `VOLUME` | 是 | 否 | 是；容器用 `--rm` 啟動時一併刪除 | 暫存資料 |

```bash
# bind mount：分析資料（$PWD 為目前目錄；路徑有空白要加引號）
docker run --rm -v "$PWD/data":/data:ro -v "$PWD/results":/results myimg \
    run_analysis --in /data --out /results

# named volume：資料庫資料
docker volume create pgdata
docker run -d --name db -v pgdata:/var/lib/postgresql/data -e POSTGRES_PASSWORD=example postgres:16

# --mount：較冗長但明確的寫法
docker run --mount type=bind,source="$PWD"/data,target=/data,readonly myimg
```

| 選項 | 意義 |
| --- | --- |
| `:ro` | 唯讀：容器不能修改來源資料（輸入資料建議都加） |
| 目的路徑不存在 | 自動建立 |
| bind mount 到容器內已有內容的目錄 | 主機目錄**覆蓋**容器內原本的內容 |
| named volume 第一次掛到有內容的目錄 | 容器內原本的內容會複製進 volume |

## 檔案權限

Linux 上容器常以 root 執行，寫到 bind mount 的輸出檔會變成 root 擁有，之後主機上的一般使用者無法刪除。

```bash
docker run --rm --user "$(id -u):$(id -g)" -v "$PWD":/work -w /work myimg ...
```

> Windows / macOS 的 Docker Desktop 會自動處理權限，但跨檔案系統的 bind mount 較慢；在 Windows 上把專案放在 [WSL](../../operating-system/windows-and-wsl.md) 的檔案系統中再掛載，速度快很多。

## 管理 volume

```bash
docker volume ls
docker volume inspect pgdata        # 實際存放位置等資訊
docker volume rm pgdata
docker volume prune                 # 刪除所有未被容器使用的 volume（資料會消失）
```

```dockerfile
# Dockerfile 中宣告 VOLUME：未指定掛載時，Docker 自動建立 anonymous volume
VOLUME ["/app/feedback"]
```

anonymous volume 的名稱是隨機的，難以在容器之間重用；需要保存的資料用 named volume 或 bind mount。
