[Computing](../../README.md) › [工作流引擎](../README.md) › Nextflow

# Nextflow

Nextflow 是生資最常用的工作流引擎之一：用 DSL 描述「process（每個步驟）」與「channel（步驟之間流動的資料）」，同一個 pipeline 不改程式就能在筆電、HPC（Slurm）、雲端（AWS Batch、Google Batch、Azure Batch）執行，並整合 conda / Docker / Apptainer。社群 [nf-core](https://nf-co.re/) 提供 rnaseq、sarek（變異呼叫）、ampliseq 等經過審查的標準 pipeline。

## 核心概念

| 概念 | 意義 |
| --- | --- |
| Process | 一個步驟：輸入、輸出、要執行的指令（`script`）；每個任務在自己的 `work/` 子目錄中執行 |
| Channel | 非同步的資料佇列，把檔案或值送進 process；process 的輸出也是 channel |
| Workflow | 把 process 與 channel 串起來 |
| Operator | 轉換 channel：`map`、`filter`、`flatten`、`collect`、`groupTuple`、`join` |
| Executor | 任務在哪裡跑：`local`、`slurm`、`awsbatch`、`google-batch`、`k8s` |
| Profile | 在 `nextflow.config` 中預先定義的一組設定，用 `-profile` 選擇 |
| Work directory | 所有中間結果在 `work/`；`-resume` 依快取重用已完成的任務 |

```text
channel(樣本 FASTQ) ──► FASTQC ──┐
                    └─► FASTP ──► ALIGN ──► QUANT ──► collect() ──► MULTIQC
（每個樣本的任務自動平行；某個樣本失敗只需重跑該任務）
```

## 安裝

需要 Java 17 以上（建議用 SDKMAN 安裝）：

```bash
curl -s https://get.sdkman.io | bash          # 安裝 SDKMAN，再依提示開新 shell
sdk install java 21-tem                       # 安裝 Java（Temurin 21）
curl -s https://get.nextflow.io | bash        # 下載 nextflow 執行檔
chmod +x nextflow && mv nextflow ~/bin/       # 放到 PATH 中
nextflow info                                 # 確認版本
```

也可用 conda 安裝（`mamba install -c bioconda nextflow`）。詳見 [官方安裝說明](https://www.nextflow.io/docs/latest/install.html)。

## 最小範例

```groovy
// main.nf
params.str = "Hello world!"                     // 預設參數，可用 --str 覆蓋

process SPLIT {
    publishDir "results/lower"                  // 把輸出複製到結果目錄

    input:
    val x

    output:
    path 'chunk_*'

    script:
    """
    printf '${x}' | split -b 6 - chunk_
    """
}

process TO_UPPER {
    publishDir "results/upper"
    tag "$y"                                    // log 中顯示的任務標籤

    input:
    path y

    output:
    path "upper_${y}"

    script:
    """
    tr '[a-z]' '[A-Z]' < $y > upper_${y}
    """
}

workflow {
    ch_str = channel.of(params.str)             // 建立 channel
    ch_chunks = SPLIT(ch_str)                   // process 的輸出是 channel
    TO_UPPER(ch_chunks.flatten())               // flatten：多個檔案拆成各自獨立的元素 → 平行處理
}
```

```bash
nextflow run main.nf
nextflow run main.nf --str "Bonjour le monde" -resume
```

## 生資常見寫法

```groovy
// 讀成對的 FASTQ：[sample_id, [R1, R2]]
ch_reads = channel.fromFilePairs("data/*_R{1,2}.fastq.gz", checkIfExists: true)

process FASTP {
    tag "$sample"
    cpus 4
    memory '8 GB'
    container 'quay.io/biocontainers/fastp:<tag>'   // 每個步驟指定容器（tag 到 quay.io 查詢）
    conda 'bioconda::fastp=0.23.4'                   // 或 conda 環境

    input:
    tuple val(sample), path(reads)

    output:
    tuple val(sample), path("${sample}_R{1,2}.trim.fq.gz"), emit: reads
    path "${sample}.json", emit: json

    script:
    """
    fastp -i ${reads[0]} -I ${reads[1]} \\
          -o ${sample}_R1.trim.fq.gz -O ${sample}_R2.trim.fq.gz \\
          -j ${sample}.json -w ${task.cpus}
    """
}

workflow {
    FASTP(ch_reads)
    MULTIQC(FASTP.out.json.collect())             // collect：等所有樣本完成，合併成一個清單
}
```

## 筆記

| 筆記 | 內容 |
| --- | --- |
| [執行 pipeline](running-pipelines.md) | 參數與優先順序、`-resume`、執行 nf-core pipeline、`nextflow.config`、profile、資源設定、executor、專案管理指令、除錯 |

| 相關 | 筆記 |
| --- | --- |
| 用 Nextflow / nf-core 跑的分析 | [RNA-seq 分析](../../../biology/genomics/workflows/rna-seq/README.md)、[變異呼叫](../../../biology/genomics/workflows/variant-calling.md) |
| process 中常包裝的工具 | [NGS 工具](../../../biology/bioinformatics-tools/ngs-tools/README.md) |
| 容器 | [Apptainer](../../containers-and-env/apptainer.md)、[Docker](../../containers-and-env/docker/README.md) |
| HPC 排程 | [Slurm](../slurm.md) |
