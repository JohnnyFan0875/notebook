[工作流引擎](../README.md) › [Nextflow](README.md) › 執行 pipeline

# 執行 Nextflow Pipeline (Running Pipelines)

執行自己或別人（nf-core）的 pipeline：傳參數、從中斷處接續、用設定檔與 profile 切換執行環境、調整資源。Pipeline 的寫法見 [Nextflow](README.md)。

## 啟動

```bash
nextflow run main.nf                                   # 本機的腳本
nextflow run nextflow-io/hello                         # 直接從 GitHub 拉取並執行
nextflow run https://github.com/nextflow-io/hello
nextflow run nf-core/rnaseq -r 3.14.0 \                # -r：固定版本（tag），可重現
    -profile singularity \
    --input samplesheet.csv --outdir results --genome GRCh38
```

| 選項 | 意義 |
| --- | --- |
| 單一連字號 `-xxx` | **Nextflow 本身**的選項：`-resume`、`-profile`、`-c`、`-r`、`-work-dir` |
| 雙連字號 `--xxx` | **pipeline 參數**，對應 `params.xxx` |
| `-resume` | 重用 `work/` 中已完成且輸入未變的任務，只重跑失敗或改過的部分 |
| `-profile a,b` | 套用設定檔中的 profile（可多個） |
| `-params-file params.yaml` | 參數寫在檔案中 |
| `-c custom.config` | 額外載入設定檔 |
| `-with-report`、`-with-timeline`、`-with-trace` | 產出執行報告：每個任務的時間、CPU、記憶體 |
| `-bg` | 背景執行 |
| `-stub` | 執行 process 的 `stub:` 區塊（假輸出），快速測試流程結構 |

## 參數

```bash
nextflow run main.nf --project_name demo
nextflow run main.nf --verbose               # 沒有值 → params.verbose = true
nextflow run main.nf --files "*.fasta"       # 萬用字元加引號，交給 Nextflow 而不是 shell 展開
nextflow run main.nf -params-file params.yaml
```

```yaml
# params.yaml：參數多、要保存每次執行的設定時
input: samplesheet.csv
outdir: results/
min_quality: 20
```

| 優先順序（低 → 高，高的覆蓋低的） | 來源 |
| --- | --- |
| 1 | 腳本中的預設值 `params.foo = 'default'` |
| 2 | 設定檔中的 `params { }` |
| 3 | `-params-file` |
| 4 | 命令列 `--foo bar` |

## 設定檔與 profile

Nextflow 自動載入 pipeline 目錄的 `nextflow.config`、目前目錄的 `nextflow.config` 與 `~/.nextflow/config`；`-c` 再疊加，`-C` 則**只用**指定的檔案。

```groovy
// nextflow.config
params {
    input  = 'data/'
    outdir = 'results'
}

process {
    cpus   = 2                                 // 所有 process 的預設資源
    memory = '4 GB'
    time   = '2h'
    errorStrategy = { task.exitStatus in 137..140 ? 'retry' : 'terminate' }   // 被 OOM / 超時殺掉時重試
    maxRetries    = 2

    withName: 'STAR_ALIGN' {                   // 個別 process 的資源
        cpus   = 16
        memory = { 32.GB * task.attempt }      // 每次重試加倍記憶體
    }
    withLabel: 'process_high' { cpus = 12; memory = '72 GB' }
}

profiles {
    standard { process.executor = 'local' }
    slurm {
        process.executor = 'slurm'
        process.queue    = 'normal'
        executor.queueSize = 50                // 同時最多送出 50 個 job
    }
    docker      { docker.enabled = true }
    singularity {
        singularity.enabled    = true
        singularity.autoMounts = true
        singularity.cacheDir   = '/project/containers'   // 映像檔快取放共用目錄
    }
    test {
        params.input = "${projectDir}/assets/test_samplesheet.csv"
    }
}
```

```bash
nextflow run main.nf -profile slurm,singularity
nextflow run main.nf -c hpc.config                 # 疊加：自訂的叢集設定
nextflow -C only.config run main.nf                # 只用 only.config（-C 是 nextflow 的頂層選項，放在 run 之前）
nextflow config                                    # 顯示合併後的設定
nextflow config -profile slurm                     # 套用某 profile 後的設定
```

> 用 profile 切換環境，不要為了換機器而修改 pipeline 程式碼。很多機構在 [nf-core/configs](https://github.com/nf-core/configs) 有現成的叢集設定（`-profile <institution>`）。

| 設定 | 作用 |
| --- | --- |
| `process.executor` | `local`、`slurm`、`sge`、`pbspro`、`awsbatch`、`google-batch`、`azurebatch`、`k8s` |
| `process.cpus` / `memory` / `time` | 資源；送到 Slurm 時轉成對應的 `#SBATCH` 參數 |
| `process.container` / `conda` | 軟體環境 |
| `workDir` | 工作目錄；HPC 上放 scratch（大量中間檔） |
| `executor.queueSize` | 同時送出的 job 上限，避免塞爆排程器 |

## nf-core pipeline

```bash
nextflow run nf-core/rnaseq -r 3.14.0 -profile test,docker --outdir test_out   # 先用內建小資料測試環境
nextflow run nf-core/rnaseq -r 3.14.0 -profile singularity \
    --input samplesheet.csv --outdir results --genome GRCh38 -resume
```

| 檢查 | 說明 |
| --- | --- |
| 固定版本 `-r` | 不指定會用預設分支的最新版，結果可能隨時間改變 |
| 先跑 `-profile test` | 確認 Nextflow、容器、叢集設定都正常 |
| samplesheet 格式 | 依該 pipeline 的文件（usage 頁）準備 CSV |
| 參考基因組 | `--genome` 使用 iGenomes 的設定；正式分析常改用 `--fasta` + `--gtf` 指定版本 |
| 輸出 | `results/pipeline_info/` 有執行報告與軟體版本，論文方法段落需要 |

## 專案管理與檢查指令

```bash
nextflow pull nf-core/rnaseq                  # 下載 / 更新到本機快取（~/.nextflow/assets）
nextflow list                                 # 已下載的 pipeline
nextflow info nf-core/rnaseq                  # 版本、分支、本機路徑
nextflow view nf-core/rnaseq                  # 顯示主腳本；-l 列出檔案
nextflow clone nf-core/rnaseq my_rnaseq       # 複製成可修改的本機副本
nextflow drop nf-core/rnaseq                  # 刪除本機快取

nextflow log                                  # 歷次執行紀錄（run name、狀態）
nextflow log <run_name> -f name,status,workdir   # 某次執行每個任務的工作目錄
nextflow clean -f -before <run_name>          # 清除舊執行的 work 目錄（釋放空間，之後無法 resume 那些任務）
nextflow inspect main.nf -profile docker      # 列出 pipeline 會用到的容器（可預先下載）

nf-core modules install multiqc               # nf-core 工具（pip install nf-core）：安裝共用模組到自己的 pipeline
```

## 除錯

| 問題 | 做法 |
| --- | --- |
| 某任務失敗 | 錯誤訊息會列出 work 目錄；進去看 `.command.sh`（實際執行的指令）、`.command.err`、`.command.log`，可 `bash .command.run` 重跑 |
| `exit status 137` | 記憶體不足被殺掉 → 提高 `memory` 或設定重試加倍 |
| 改了程式碼卻全部重跑 | 輸入或 script 改變會讓快取失效；只改了後面步驟時前面應該被重用 |
| `work/` 太大 | 結束後 `nextflow clean`；HPC 上把 `workDir` 放 scratch |
| 執行太久 | `-with-report` 找出耗時、資源配置過多或過少的步驟 |
