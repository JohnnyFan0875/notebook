[Computing](../README.md) › [容器與環境](README.md) › 容器與虛擬化

# 容器與虛擬化 (Containerization and Virtualization)

兩者都把軟體與它的執行環境隔離開來，差別在隔離的層級：**虛擬機 (VM)** 模擬一整台電腦、各自有作業系統；**容器 (container)** 共用主機的核心，只隔離程序與檔案系統。容器輕量、啟動快，是打包與交付分析環境的主流方式。

```text
虛擬機                                      容器
┌───────┬───────┬───────┐                ┌───────┬───────┬───────┐
│ App A │ App B │ App C │                │ App A │ App B │ App C │
│ 函式庫 │ 函式庫 │ 函式庫 │                │ 函式庫 │ 函式庫 │ 函式庫 │
│客體 OS│客體 OS│客體 OS│                ├───────┴───────┴───────┤
├───────┴───────┴───────┤                │ 容器執行環境（Docker） │
│ Hypervisor             │                ├───────────────────────┤
├───────────────────────┤                │ 主機 OS 與核心          │
│ 硬體                    │                ├───────────────────────┤
└───────────────────────┘                │ 硬體                    │
                                          └───────────────────────┘
```

## 比較

| 面向 | 虛擬機 | 容器 |
| --- | --- | --- |
| 隔離邊界 | 完整的客體 OS | 共用核心上的程序與檔案系統隔離 |
| 作業系統 | 每個 VM 自己的 OS（可以是 Windows 跑在 Linux 上） | 共用主機核心（Linux 容器需要 Linux 核心；Windows / macOS 上的 Docker 實際跑在一個輕量 VM 裡） |
| 大小 | GB 級 | MB 到數百 MB |
| 啟動 | 分鐘 | 秒 |
| 資源開銷 | 高 | 低 |
| 隔離強度 | 強 | 較弱（共用核心） |
| 典型用途 | 需要不同 OS、強隔離、整台機器的環境 | 應用程式打包、分析環境交付、微服務 |
| 例子 | VirtualBox、VMware、Hyper-V、雲端 VM（EC2） | Docker、Podman、Apptainer |

## 容器的組成

| 名詞 | 意義 |
| --- | --- |
| 映像檔 (image) | 唯讀的範本：應用程式 + 函式庫 + 相依套件，由多層 (layer) 組成 |
| 容器 (container) | 映像檔的執行個體，有自己的可寫層 |
| Dockerfile | 描述如何建立映像檔的腳本，可重現 |
| Registry | 存放與分享映像檔：Docker Hub、GitHub Container Registry、quay.io（BioContainers） |
| 容器執行環境 | Docker、Podman（不需 root daemon）、Apptainer（HPC） |

> 對分析的意義：把「我這台電腦能跑」變成「任何有容器執行環境的電腦都能跑同一個版本」。工作流引擎（Nextflow、Snakemake）可以讓每個步驟在指定的容器中執行。

## 編排 (Orchestration)

一個容器在一台機器上跑很簡單；很多容器跨多台機器時，需要編排系統處理：

| 問題 | 編排系統負責 |
| --- | --- |
| 放在哪台機器 | 依資源排程 |
| 掛掉了 | 自動重啟、換機器 |
| 流量變大 | 增減副本 (replica) |
| 更新版本 | 滾動更新、回滾 |
| 服務怎麼找到彼此 | 服務發現、內部網路 |

| 工具 | 定位 |
| --- | --- |
| [Docker](docker/README.md) | 打包與在單機執行容器 |
| [Docker Compose](docker/compose.md) | 單機上多個容器一起啟動（API + 資料庫） |
| [Kubernetes](kubernetes.md) | 叢集上大規模運行容器的標準 |
| HPC 排程器 + [Apptainer](apptainer.md) | 批次運算，不是長期服務 |

> 目標是打包與本機執行 → Docker；目標是可靠地營運大量容器 → Kubernetes；在共用 HPC 上跑分析 → Apptainer。
