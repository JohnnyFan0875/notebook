[Computing](../README.md) › [容器與環境](README.md) › Apptainer

# Apptainer（Singularity）

Apptainer（原名 Singularity）是 **HPC 上的容器執行環境**。共用叢集不允許一般使用者跑 Docker（Docker daemon 需要 root，等於給了整台機器的權限），Apptainer 則以使用者本人的身分執行容器，不需要 daemon，且能直接執行 Docker 映像檔。生資的 Nextflow / nf-core、Snakemake 在 HPC 上大多透過它使用容器。

## 與 Docker 的差異

| | Docker | Apptainer |
| --- | --- | --- |
| 權限 | daemon 以 root 執行 | 以使用者身分執行，容器內也是同一個使用者 |
| 映像檔格式 | 分層，存在 daemon 管理的位置 | 單一 `.sif` 檔，可以像一般檔案一樣複製、放在共用目錄 |
| 檔案系統 | 預設隔離，需 `-v` 掛載 | **預設掛載** 家目錄、目前目錄、`/tmp`；其他路徑用 `--bind` |
| 網路、程序 | 隔離 | 預設與主機共用 |
| 適合 | 服務、開發、本機 | 共用 HPC 上的批次運算 |
| 建置映像檔 | `docker build` | 通常在本機用 Docker 建好、推到 registry，再在 HPC 上 `pull`；或用 `.def` 檔建置 |

> Apptainer 與 SingularityCE（Sylabs 維護的分支）指令幾乎相同；有些叢集的指令名稱仍是 `singularity`。

## 基本用法

```bash
module load apptainer                                    # 很多 HPC 用環境模組載入

# 1. 從 registry 取得映像檔 → 轉成 .sif
#    BioContainers 的 tag 格式是「版本--build」，實際 tag 到 quay.io/biocontainers/samtools 查詢
apptainer pull samtools.sif docker://quay.io/biocontainers/samtools:<version>--<build>
apptainer pull docker://ubuntu:24.04                     # 產生 ubuntu_24.04.sif

# 2. 執行
apptainer exec samtools.sif samtools --version           # 在容器中執行一個指令
apptainer exec samtools.sif samtools view -c sample.bam  # 目前目錄已自動掛載
apptainer shell ubuntu_24.04.sif                         # 進入互動式 shell
apptainer run image.sif                                  # 執行映像檔的預設指令（runscript）

# 3. 掛載其他路徑（如參考基因組、scratch）
apptainer exec --bind /ref:/ref,/scratch/$USER:/work star.sif \
    STAR --genomeDir /ref/star_index --readFilesIn /work/R1.fq.gz ...

# 4. GPU
apptainer exec --nv pytorch.sif python train.py          # NVIDIA GPU
```

| 選項 | 作用 |
| --- | --- |
| `--bind src:dst[,src2:dst2]` / `-B` | 掛載主機路徑；也可設環境變數 `APPTAINER_BINDPATH` |
| `--nv` | 使用 NVIDIA GPU |
| `--cleanenv` / `-e` | 不帶入主機的環境變數（避免主機的 `PYTHONPATH`、conda 設定干擾） |
| `--containall` / `-C` | 更嚴格的隔離（不自動掛載家目錄） |
| `--pwd /work` | 容器內的起始目錄 |

## 在 Slurm 工作中使用

```bash
#!/bin/bash
#SBATCH --job-name=align
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=04:00:00

module load apptainer
apptainer exec --bind /ref:/ref containers/star_2.7.11b.sif \
    STAR --runThreadN "$SLURM_CPUS_PER_TASK" --genomeDir /ref/star_index \
         --readFilesIn R1.fq.gz R2.fq.gz --readFilesCommand zcat --outSAMtype BAM SortedByCoordinate
```

Slurm 的用法見 [Slurm](../workflow-engines/slurm.md)。工作流引擎設定：Nextflow 用 `-profile singularity` / `apptainer.enabled = true`，Snakemake 用 `--software-deployment-method apptainer`（舊版 `--use-singularity`）。

## 自己建置映像檔

```text
# samtools.def
Bootstrap: docker
From: mambaorg/micromamba:1.5.8

%post
    micromamba install -y -n base -c conda-forge -c bioconda samtools=1.21
    micromamba clean -a -y

%environment
    export PATH=/opt/conda/bin:$PATH

%runscript
    exec samtools "$@"
```

```bash
apptainer build samtools.sif samtools.def          # 需要 root 或 --fakeroot（視叢集設定）
apptainer build --fakeroot samtools.sif samtools.def
```

> 多數情況不必自己建：先找 [BioContainers](https://biocontainers.pro/)（每個 bioconda 套件都有對應映像檔，在 `quay.io/biocontainers`）或 Galaxy 的 depot（`https://depot.galaxyproject.org/singularity/`，直接是 `.sif`）。需要自訂時，在本機寫 Dockerfile、推到 registry，再在 HPC 上 `apptainer pull`，同一個映像檔在筆電與叢集都能用。

## 實務守則

| 守則 | 原因 |
| --- | --- |
| 映像檔用明確的版本 tag，不用 `latest` | 可重現；`latest` 會變 |
| `.sif` 放在共用的專案目錄 | 不要每個人各下載一份；家目錄配額小 |
| 設定快取目錄 `APPTAINER_CACHEDIR=/scratch/$USER/apptainer` | `pull` 的暫存檔預設在家目錄，常把配額用完 |
| 遇到奇怪的套件衝突加 `--cleanenv` | 主機環境變數滲入容器 |
| 資料路徑要 `--bind` | 預設只掛載家目錄與目前目錄，其他路徑在容器內看不到 |
