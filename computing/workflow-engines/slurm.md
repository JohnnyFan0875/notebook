[Computing](../README.md) › [工作流引擎](README.md) › Slurm

# Slurm：HPC 工作排程 (Slurm Workload Manager)

HPC 叢集由登入節點與大量計算節點組成；Slurm 是最常見的排程器 (scheduler)：你描述工作需要多少 CPU、記憶體、時間，送進佇列，Slurm 在有資源時把它分派到計算節點執行。生資的比對、變異呼叫、組裝等重運算都在這裡跑；Nextflow 與 Snakemake 也把每個步驟以 Slurm job 送出。

```text
你 ──SSH──► 登入節點 (login node)：編輯、送出工作、輕量操作
                │ sbatch
                ▼
           Slurm 控制器：依資源、優先權、公平分享排隊
                │
                ▼
           計算節點 (compute nodes)：實際執行
```

> **不要在登入節點跑重運算**（比對、組裝、大型 R / Python 分析）；它是所有人共用的，管理者通常會砍掉這類程序。連線方式見 [SSH](../developer-tools/ssh.md)。

| 名詞 | 意義 |
| --- | --- |
| Partition | 一組節點的佇列，各有時間上限與硬體（`normal`、`gpu`、`bigmem`） |
| Job | 一次送出的工作 |
| Task | job 中的程序（MPI 用；生資多為 1 個 task 多個 CPU） |
| Account | 計費 / 配額單位（實驗室或計畫） |
| QOS | 服務品質：優先權、同時可跑的 job 數上限 |

## 批次工作：`sbatch`

```bash
#!/bin/bash
#SBATCH --job-name=star_align
#SBATCH --partition=normal
#SBATCH --account=mylab
#SBATCH --cpus-per-task=8            # 多執行緒程式用這個
#SBATCH --mem=32G                    # 整個 job 的記憶體（或 --mem-per-cpu=4G）
#SBATCH --time=04:00:00              # 時間上限 HH:MM:SS；超過會被終止
#SBATCH --output=logs/%x_%j.out      # %x = job 名稱，%j = job ID（logs/ 目錄要先存在）
#SBATCH --error=logs/%x_%j.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=me@example.edu

set -euo pipefail
module load star/2.7.11b              # 載入軟體（或 conda activate / apptainer exec）

STAR --runThreadN "$SLURM_CPUS_PER_TASK" \
     --genomeDir /ref/star_index \
     --readFilesIn R1.fq.gz R2.fq.gz --readFilesCommand zcat \
     --outSAMtype BAM SortedByCoordinate --outFileNamePrefix out/S1_
```

```bash
mkdir -p logs out
sbatch align.sh                       # 送出，回傳 job ID
sbatch --mem=64G align.sh             # 命令列參數覆蓋腳本中的 #SBATCH
```

> 執行緒數用 `$SLURM_CPUS_PER_TASK`，不要寫死；申請 8 核卻讓程式跑 32 執行緒會拖慢整個節點。

## 查看與管理

```bash
squeue -u $USER                       # 我的 job：狀態 PD（等待）、R（執行中）
squeue -u $USER --start               # 預估開始時間
scancel <jobid>                       # 取消；scancel -u $USER 取消全部
sinfo                                 # partition 與節點狀態
sacct -j <jobid> --format=JobID,JobName,State,Elapsed,MaxRSS,ReqMem,AllocCPUS,ExitCode   # 結束後的紀錄
seff <jobid>                          # 效率摘要：CPU 與記憶體實際用了多少（若叢集有安裝）
scontrol show job <jobid>             # 詳細資訊；PD 狀態的原因 (Reason)
```

| 狀態 / 原因 | 意義 |
| --- | --- |
| `PD (Resources)` | 等資源釋出 |
| `PD (Priority)` | 其他人的優先權較高 |
| `PD (QOSMaxJobsPerUserLimit)` | 超過同時可跑的 job 上限 |
| `TIMEOUT` | 超過 `--time`，被終止 |
| `OUT_OF_MEMORY` / `OOM` | 超過 `--mem`，被終止 |
| `FAILED` | 程式以非 0 結束，看 `.err` |

> 資源申請要接近實際用量：申請太多會排很久、浪費配額；太少會被砍。先用一個樣本跑，再用 `seff` / `sacct` 的 `MaxRSS` 與實際時間調整。

## 陣列工作：`--array`

同一個腳本跑很多樣本時，用 array job：一次送出，每個子工作有自己的索引 `$SLURM_ARRAY_TASK_ID`。

```bash
#!/bin/bash
#SBATCH --job-name=fastp
#SBATCH --array=1-48%10               # 48 個樣本，同時最多 10 個在跑
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=01:00:00
#SBATCH --output=logs/%x_%A_%a.out    # %A = 陣列 job ID，%a = 索引

set -euo pipefail
sample=$(sed -n "${SLURM_ARRAY_TASK_ID}p" samples.txt)   # samples.txt 每行一個樣本名稱
fastp -i raw/${sample}_R1.fastq.gz -I raw/${sample}_R2.fastq.gz \
      -o trim/${sample}_R1.fq.gz -O trim/${sample}_R2.fq.gz \
      -j qc/${sample}.json -w "$SLURM_CPUS_PER_TASK"
```

```bash
sbatch --array=5,17 fastp_array.sh    # 只重跑失敗的索引
```

## 依賴與互動式工作

```bash
jid=$(sbatch --parsable align.sh)                          # --parsable：只輸出 job ID
sbatch --dependency=afterok:$jid count.sh                  # align 成功後才開始
sbatch --dependency=afterany:$jid cleanup.sh               # 不論成敗

srun --cpus-per-task=4 --mem=16G --time=02:00:00 --pty bash   # 互動式 shell 在計算節點上（除錯、互動分析）
salloc --cpus-per-task=4 --mem=16G --time=02:00:00            # 先配置資源，之後在其中執行 srun
srun --partition=gpu --gres=gpu:1 --time=01:00:00 --pty bash  # 要一張 GPU
```

| 依賴類型 | 條件 |
| --- | --- |
| `afterok:<id>` | 前一個成功結束 |
| `afternotok:<id>` | 前一個失敗 |
| `afterany:<id>` | 前一個結束（不論成敗） |
| `singleton` | 同名的 job 一次只跑一個 |

> 步驟多、依賴複雜時，與其自己串 `--dependency`，不如交給 [Nextflow](nextflow/README.md) 或 [Snakemake](snakemake.md)：它們會自動送出 job、追蹤依賴、失敗時從中斷處重跑。

## 作為工作流引擎的 executor

| 引擎 | 設定 |
| --- | --- |
| Nextflow | `process.executor = 'slurm'`、`process.queue`、`executor.queueSize`；見 [執行 pipeline](nextflow/running-pipelines.md#設定檔與-profile) |
| Snakemake | `--executor slurm --jobs 50 --default-resources ...`；見 [Snakemake](snakemake.md#在-slurm-上執行) |

引擎本身（主程序）很輕，在登入節點的 [tmux](../developer-tools/tmux-and-screen.md) 中執行，或以一個小的長時間 job 執行（依叢集規定）。

## 軟體環境

| 方式 | 指令 |
| --- | --- |
| 環境模組 | `module avail`、`module load samtools/1.21`、`module list`、`module purge` |
| conda | 在 job 腳本中 `source ~/miniforge3/etc/profile.d/conda.sh && conda activate rnaseq`（見 [Conda](../containers-and-env/conda.md)） |
| 容器 | `apptainer exec image.sif ...`（見 [Apptainer](../containers-and-env/apptainer.md)） |

## 實務守則

| 守則 | 原因 |
| --- | --- |
| 先用一個樣本測試資源用量 | 再依 `seff` 調整整批的申請 |
| 中間檔放 scratch，結果放專案目錄 | 家目錄配額小；scratch 快但常會定期清除 |
| 大量小 job 改用 array 或工作流引擎 | 每個 job 都有排程開銷，也可能有數量上限 |
| log 檔名包含 job ID | 方便對照 `sacct` |
| 不在登入節點跑重運算 | 共用資源 |
| 其他排程器 | PBS / Torque（`qsub`、`qstat`）、SGE、LSF（`bsub`）概念相同，指令不同 |
