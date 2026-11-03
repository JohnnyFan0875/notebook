[Computing](../README.md) › 容器與環境

# 容器與環境 (Containers and Environments)

讓分析在別台電腦、半年後、交給別人時仍然跑得出同樣結果：用環境管理器固定套件版本，用容器固定整個執行環境。生資工具通常透過 Bioconda 或 BioContainers 安裝，工具清單見 [生資工具](../../biology/bioinformatics-tools/README.md)。

## 選哪個

| 工具 | 隔離什麼 | 需要 root | 可重現程度 | 適合 |
| --- | --- | --- | --- | --- |
| [uv](../../data-science/python-foundations/python-packages.md) | Python 套件 | 否 | 高（`uv.lock`） | 純 Python 專案、腳本 |
| [renv](../../data-science/r-foundations/reproducible-environments-with-renv.md) | R 套件 | 否 | 中高（`renv.lock`，不含系統函式庫） | R 專案 |
| [conda / mamba](conda.md) | 任何語言的套件 + 部分系統函式庫 | 否 | 中（固定版本的 `environment.yml`）；高（lock 檔） | 生資命令列工具、混合語言、HPC 上安裝軟體 |
| [Docker](docker/README.md) | 整個使用者空間（OS 套件、函式庫、工具） | daemon 需要 | 很高（映像檔 tag / digest） | 交付分析環境、服務、CI、本機與雲端 |
| [Apptainer](apptainer.md) | 同 Docker，可直接執行 Docker 映像檔 | 否 | 很高（`.sif` 檔） | 共用 HPC 叢集 |
| [虛擬機](virtual-machine.md) | 整台電腦（含核心與 OS） | — | 很高但笨重 | 需要不同 OS、完整桌面、強隔離 |

```
只有 Python？ ── 是 ──► uv
   │否
需要生資命令列工具 / 混合語言？ ── 是 ──► conda / mamba（bioconda）
   │                                        │ 要交付給別人、長期重現、在 HPC 跑
   │                                        ▼
   └──────────────────────────────► 容器：本機 / 雲端用 Docker，HPC 用 Apptainer
                                       多個服務一起跑 → Compose；叢集營運 → Kubernetes
```

> 常見組合：開發時用 conda / uv；工作流引擎（Nextflow、Snakemake）每個步驟指定一個 BioContainers 映像檔，在 HPC 上以 Apptainer 執行。

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [Conda](conda.md) | Miniforge、mamba、bioconda channel、`environment.yml`、匯出與 lock | 不用 sudo 怎麼裝生資工具？環境怎麼重建？ |
| [容器與虛擬化](containerization-and-virtualization.md) | VM vs 容器、映像檔與 registry、編排 | 容器和虛擬機差在哪？ |
| [Docker](docker/README.md) | 映像檔、容器、Dockerfile、掛載、網路、Compose | 怎麼建置、執行、分享容器？ |
| [Apptainer](apptainer.md) | 與 Docker 的差異、`pull` / `exec` / `--bind`、Slurm 中使用、`.def` 建置 | HPC 上怎麼跑 Docker 映像檔？ |
| [Kubernetes](kubernetes.md) | Pod、Deployment、Service、`kubectl`、除錯 | 叢集上怎麼營運大量容器？ |
| [虛擬機](virtual-machine.md) | VirtualBox 常見問題：縮小磁碟、共用資料夾、sudo | 什麼時候用 VM？常見問題怎麼解？ |
