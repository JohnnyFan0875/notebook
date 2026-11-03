[Notebook](../README.md) › Computing

# 運算與工程 (Computing)

讓分析跑得起來、跑得動、跑得出同樣結果的工程基礎：電腦科學概念、命令列、開發工具、版本控制、環境與容器、HPC 與工作流引擎、雲端、DevOps、Web 開發。分析方法本身在 [Data Science](../data-science/README.md)，生物背景與資料在 [Biology](../biology/README.md)。

> 生資分析的工程問題通常不是演算法，而是：軟體裝不起來、換台機器結果不同、在登入節點跑到被砍、中斷後不知道從哪裡重跑、資料傳輸損壞。本領域的筆記大多在回答這些問題。

## 章節地圖

### 基礎

| 章節 | 核心內容 | 回答的問題 |
| --- | --- | --- |
| [CS 基礎](computer-science-foundations/README.md) | 電腦架構、Big-O、線性 / 非線性資料結構、搜尋、排序、圖走訪、可計算性、範式 | 為什麼這段程式慢？該用 list 還是 set？ |
| [程式語言](programming-languages/README.md) | 語言比較、Java（8 篇）、Scala、Julia | Python / R 以外的語言何時會用到？ |
| [作業系統與命令列](operating-system/README.md) | WSL、Linux 指令、regex、命令列資料處理、shell 腳本 | 怎麼在 Linux 上找檔案、處理表格、寫腳本？ |

### 日常工具

| 章節 | 核心內容 | 回答的問題 |
| --- | --- | --- |
| [開發者工具](developer-tools/README.md) | SSH、tmux / screen、rsync、檢查碼、壓縮、編輯器 | 怎麼連伺服器、傳資料、保持工作不中斷？ |
| [版本控制](version-control/README.md) | Git、GitHub 協作 | 怎麼記錄、還原、合併程式碼？ |
| [Web 開發](web-development/README.md) | Web 基礎、FastAPI、React | 怎麼把模型包成 API、做查詢介面？ |

### 環境、規模化與部署

| 章節 | 核心內容 | 回答的問題 |
| --- | --- | --- |
| [容器與環境](containers-and-env/README.md) | conda / mamba、Docker、Apptainer、Kubernetes、VM | 環境怎麼固定、在別台電腦重現？ |
| [工作流引擎](workflow-engines/README.md) | Slurm、Nextflow、Snakemake、Airflow | 多步驟、多樣本的分析怎麼平行、重跑、上 HPC？ |
| [雲端](cloud/README.md) | 雲端概念、AWS / Azure / GCP 服務對照、安全與成本、Boto3 | 什麼時候上雲？用哪個服務？成本怎麼控？ |
| [DevOps](devops/README.md) | CI/CD、IaC、DORA、GitHub Actions | 怎麼讓每次變更自動測試、可靠部署？ |

## 建議路線

| 讀者 | 路線 |
| --- | --- |
| **生資分析** | [WSL](operating-system/windows-and-wsl.md)（Windows 使用者）→ [Linux 基礎](operating-system/linux-basics.md) → [命令列資料處理](operating-system/command-line-data-processing.md) → [SSH](developer-tools/ssh.md) → [tmux](developer-tools/tmux-and-screen.md) → [rsync](developer-tools/rsync.md) / [檢查碼](developer-tools/checksums.md) → [Conda](containers-and-env/conda.md) → [Slurm](workflow-engines/slurm.md) → [Nextflow](workflow-engines/nextflow/README.md) 或 [Snakemake](workflow-engines/snakemake.md) → [Apptainer](containers-and-env/apptainer.md) → [Git](version-control/git.md) |
| **資料工程** | [Linux 基礎](operating-system/linux-basics.md) → [Shell 腳本](operating-system/shell-scripting.md) → [Git](version-control/git.md) → [Docker](containers-and-env/docker/README.md) → [Airflow](workflow-engines/airflow.md) → [雲端](cloud/README.md) → [GitHub Actions](devops/github-actions.md)；搭配 [資料工程](../data-science/data-engineering/README.md) |
| **一般開發者** | [CS 基礎](computer-science-foundations/README.md) → [Git](version-control/git.md) → [編輯器](developer-tools/editors.md) → [Web 基礎](web-development/web-fundamentals.md) → [FastAPI](web-development/fastapi.md) / [React](web-development/react/README.md) → [Docker](containers-and-env/docker/README.md) → [DevOps](devops/README.md) |

## 一個分析專案的工程骨架

```
本機（VS Code + WSL）──Git──► GitHub（PR、Actions 自動測試）
   │ SSH / rsync
   ▼
HPC 登入節點（tmux）── Nextflow / Snakemake ──► Slurm ──► 計算節點（Apptainer 容器）
   │                                                         │
   └──────────── 環境：conda environment.yml / 容器映像檔 tag ─┘
結果 ──md5sum 驗證──► 長期保存（物件儲存 / 封存）；Git tag + 環境檔 = 可重現
```
