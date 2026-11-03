[Computing](../README.md) › 工作流引擎

# 工作流引擎 (Workflow Engines)

多步驟分析（QC → 修剪 → 比對 → 定量 → 報告）用腳本串起來，很快會遇到：哪些步驟已經跑過？失敗後從哪裡重跑？怎麼平行處理 100 個樣本？怎麼換到 HPC 或雲端？工作流引擎把步驟與依賴建成 DAG（有向無環圖），自動處理平行、重跑、軟體環境與執行位置。

## 比較

| | Make | [Snakemake](snakemake.md) | [Nextflow](nextflow/README.md) | [Airflow](airflow.md) |
| --- | --- | --- | --- | --- |
| 定位 | 建置工具 | 檔案導向的分析流程 | 檔案導向的分析流程 | 定時的資料編排 |
| 語言 | Makefile | Python + 規則 | Groovy DSL | Python |
| 單位 | 目標檔案 | 規則（輸入 → 輸出檔案） | process + channel | task（任何動作） |
| 觸發 | 手動 | 手動 | 手動 / Seqera Platform | **排程**、事件 |
| 平行 | `make -j` | 自動 | 自動 | 自動 |
| 重跑 | 依檔案時間戳記 | 依檔案與程式碼變更 | `-resume` 任務快取 | 重試、補跑日期區間 |
| HPC / 雲端 | — | Slurm、雲端 executor plugin | Slurm、AWS / Google / Azure Batch、K8s | Kubernetes、Celery |
| 容器 / conda | — | 每條規則 | 每個 process | 每個 task（K8s / Docker operator） |
| 社群 pipeline | — | Snakemake Workflow Catalog | **nf-core** | providers（整合各系統） |
| 典型用途 | 小專案、報告建置 | 學術生資分析 | 標準化生資 pipeline、臨床與大型專案 | ETL / ELT、資料倉儲、跨系統協調 |

```
樣本級的生資分析（FASTQ → BAM → VCF / counts）？
├─ 有現成 nf-core pipeline → Nextflow（nf-core）
├─ 自己寫、偏好 Python      → Snakemake
└─ 自己寫、要跨 HPC / 雲端標準化部署 → Nextflow
定時從資料庫 / API 擷取、轉換、寫入倉儲？ → Airflow（或 Dagster、Prefect）
幾個指令的小流程？ → shell 腳本或 Makefile
```

> 生資引擎與資料工程編排器的分工：前者處理「一批樣本檔案經過一串工具」，後者處理「每天定時協調多個系統」。兩者可以合用：Airflow 每天觸發一次 Nextflow pipeline。資料工程的觀點見 [處理與 Pipeline](../../data-science/data-engineering/processing-and-pipelines.md)。

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [Slurm](slurm.md) | `sbatch` 腳本、`squeue` / `sacct` / `seff`、array job、依賴、`srun` 互動式 | HPC 上怎麼申請資源、送工作？ |
| [Nextflow](nextflow/README.md) | process / channel、範例、成對 FASTQ、容器 | Nextflow pipeline 怎麼寫？ |
| [執行 Nextflow pipeline](nextflow/running-pipelines.md) | 參數、`-resume`、nf-core、`nextflow.config`、profile、除錯 | 怎麼跑 nf-core、怎麼換到 HPC？ |
| [Snakemake](snakemake.md) | 規則、萬用字元、`expand`、乾跑、conda / 容器、Slurm executor | 用 Python 風格寫分析流程？ |
| [Airflow](airflow.md) | DAG、TaskFlow、排程與邏輯日期、感測器、模板、除錯（Airflow 3） | 定時的資料 pipeline 怎麼編排？ |

| 相關 | 筆記 |
| --- | --- |
| 這些引擎編排的生資分析 | [分析流程](../../biology/genomics/workflows/README.md) |
| 軟體環境 | [容器與環境](../containers-and-env/README.md) |
| 雲端執行 | [Cloud](../cloud/README.md) |
| 圖與拓撲排序的原理 | [圖走訪](../computer-science-foundations/graph-traversal.md) |
