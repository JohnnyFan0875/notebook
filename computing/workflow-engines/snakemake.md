[Computing](../README.md) › [工作流引擎](README.md) › Snakemake

# Snakemake

Snakemake 是以 Python 為基礎的工作流引擎，概念來自 GNU Make：每條規則 (rule) 宣告「由哪些輸入檔產生哪些輸出檔、用什麼指令」，Snakemake 從你要的最終檔案**往回推**，算出需要執行哪些步驟、哪些可以平行、哪些已經是最新的可以跳過。語法貼近 Python，學習門檻比 Nextflow 低，在學術生資圈很常見。官方支援 Linux、macOS 與 [WSL](../operating-system/windows-and-wsl.md)。

| | Snakemake | [Nextflow](nextflow/README.md) |
| --- | --- | --- |
| 思考方向 | 從目標檔案往回推（pull） | 資料從 channel 往前流（push） |
| 語言 | Python + 規則 DSL | Groovy DSL |
| 中間檔 | 在你指定的路徑 | 在 `work/` 雜湊目錄，`publishDir` 才複製出來 |
| 重跑判斷 | 輸出檔是否存在、輸入 / 程式碼 / 參數是否改變 | 任務快取（`-resume`） |
| 社群 pipeline | Snakemake Workflow Catalog | nf-core（更大、更標準化） |
| 適合 | 熟悉 Python、檔案路徑結構清楚的分析專案 | 大型標準化 pipeline、雲端與多環境部署 |

## 安裝

```bash
mamba create -n snakemake -c conda-forge -c bioconda snakemake   # 建議用 conda（各規則可再用 conda 環境）
# 或：uv tool install snakemake
snakemake --version
```

## 範例

```
data/{sample}_R1.fastq.gz ──count_reads──► results/counts/{sample}.txt ──summarize──► results/summary.tsv
```

```yaml
# config.yaml
samples: [A, B]
```

```python
# Snakefile
configfile: "config.yaml"
SAMPLES = config["samples"]

rule all:                                    # 第一條規則 = 預設目標：要什麼最終檔案
    input:
        "results/summary.tsv"

rule count_reads:
    input:
        r1="data/{sample}_R1.fastq.gz",      # {sample} 是萬用字元 (wildcard)，由輸出檔名推得
        r2="data/{sample}_R2.fastq.gz",
    output:
        "results/counts/{sample}.txt"
    threads: 1
    resources:
        mem_mb=1000
    log:
        "logs/count_reads/{sample}.log"
    conda:
        "envs/qc.yaml"                       # 這條規則的軟體環境（--software-deployment-method conda 時使用）
    shell:
        """
        n=$(( $(zcat {input.r1} | wc -l) / 4 ))
        printf '%s\\t%s\\n' {wildcards.sample} $n > {output} 2> {log}
        """

rule summarize:
    input:
        expand("results/counts/{sample}.txt", sample=SAMPLES)   # 展開成 A、B 兩個檔案
    output:
        "results/summary.tsv"
    shell:
        "cat {input} > {output}"
```

```bash
snakemake -n                         # 乾跑 (dry run)：列出會執行哪些 job，不實際執行
snakemake -c 8                       # 用 8 個核心執行（-c / --cores 必填）
snakemake -c 8 results/counts/A.txt  # 只產生指定的目標
snakemake --dag | dot -Tpng > dag.png   # 畫出依賴圖（需 graphviz）
snakemake -c 8 --rerun-incomplete    # 上次中斷留下不完整的輸出時
snakemake -c 8 -k                    # --keep-going：某個 job 失敗時繼續跑其他獨立的 job
```

上例的乾跑結果：`count_reads` × 2、`summarize` × 1、`all` × 1，共 4 個 job。

| 元素 | 說明 |
| --- | --- |
| `input` / `output` | 檔案路徑；可具名（`input.r1`） |
| 萬用字元 `{sample}` | 由**要求的輸出檔名**比對出值，再代入輸入路徑 |
| `expand()` | 依清單產生多個檔名 |
| `shell` / `run` / `script` | 執行 shell 指令 / Python 程式碼 / 外部 R 或 Python 腳本（`script: "scripts/plot.R"`，腳本內用 `snakemake@input` 取得路徑） |
| `threads` / `resources` | 該 job 的核心數與資源，排程器據此分配 |
| `log` | log 檔路徑；失敗時保留 |
| `params` | 非檔案的參數 |
| `temp()` / `protected()` | 用完自動刪除的中間檔 / 防止被覆寫 |
| `config` | 從 `config.yaml` 讀入的設定，可用 `--config key=value` 覆蓋 |

## 軟體環境

```bash
snakemake -c 8 --software-deployment-method conda       # 每條規則依 conda: 建立環境（簡寫 --sdm conda）
snakemake -c 8 --sdm apptainer                           # 依 container: 使用容器（HPC）
```

```yaml
# envs/qc.yaml
channels: [conda-forge, bioconda]
dependencies:
  - fastp=0.23.4
```

> Snakemake 8 起，舊的 `--use-conda`、`--use-singularity` 改為 `--software-deployment-method`（舊旗標仍可用但建議更新）。

## 在 Slurm 上執行

Snakemake 8 以上用 executor plugin 把每個 job 送到 [Slurm](slurm.md)：

```bash
pip install snakemake-executor-plugin-slurm       # 或 mamba install
snakemake --executor slurm --jobs 50 \
    --default-resources slurm_partition=normal mem_mb=4000 runtime=60 \
    --sdm apptainer
```

| 參數 | 意義 |
| --- | --- |
| `--executor slurm` | 每個 job 以 `sbatch` 送出 |
| `--jobs 50` | 同時最多 50 個 job 在排程器中 |
| `--default-resources` | 規則沒寫時的預設資源；`runtime` 單位為分鐘 |
| profile（`--profile profiles/slurm`） | 把上述參數寫成 `config.yaml`，不必每次輸入 |

Snakemake 主程序本身很輕，在登入節點的 [tmux](../developer-tools/tmux-and-screen.md) 中執行，或用一個小的 Slurm job 執行。

## 實務守則

| 守則 | 原因 |
| --- | --- |
| 每次執行前先 `-n` | 確認會跑哪些 job，避免意外重跑整個專案 |
| 輸出路徑包含萬用字元，結構清楚 | 規則比對靠檔名 |
| 每條規則寫 `log` | 失敗時有線索 |
| 固定 conda 環境或容器版本 | 可重現 |
| 大檔中間結果用 `temp()` | 節省空間 |
| 樣本清單放 `config.yaml` 或 samplesheet | 不寫死在 Snakefile |

| 相關 | 筆記 |
| --- | --- |
| 比較其他引擎 | [工作流引擎](README.md) |
| 規則中使用的工具 | [NGS 工具](../../biology/bioinformatics-tools/ngs-tools/README.md) |
| 環境 | [Conda](../containers-and-env/conda.md)、[Apptainer](../containers-and-env/apptainer.md) |
