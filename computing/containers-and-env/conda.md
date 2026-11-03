[Computing](../README.md) › [容器與環境](README.md) › Conda

# Conda、Mamba 與 Bioconda

Conda 是跨語言的套件與環境管理器：除了 Python 套件，也能安裝 R、C/C++ 編譯的生資工具（samtools、STAR、bwa）與系統函式庫，且**不需要 sudo**，所以是 HPC 與共用伺服器上安裝生資軟體的標準方式。純 Python 專案用 [uv](../../data-science/python-foundations/python-packages.md) 更快更簡單；兩者可以搭配。

## 發行版與指令

| 名稱 | 是什麼 | 建議 |
| --- | --- | --- |
| Miniforge | 預設使用 conda-forge channel、內建 `mamba` 的安裝程式 | **首選** |
| Miniconda | Anaconda 公司的最小安裝，預設 `defaults` channel | `defaults` channel 在組織中可能有商業授權限制 |
| Anaconda | 預裝數百個套件的完整發行版 | 不需要 |
| `mamba` | conda 的 C++ 重寫，相依性解析快很多，指令相同 | 用 `mamba` 取代 `conda install / create` |
| `micromamba` | 單一執行檔、不需 base 環境 | 容器、CI |
| `pixi` | 以專案為單位、自動產生 lock 檔的新工具，同樣使用 conda 套件 | 新專案可考慮 |

> conda 23.10 起預設的相依性解析器已改為 libmamba，速度差距縮小；`mamba` 仍是常見寫法。

## 安裝與初始設定

```bash
# Linux / WSL：安裝 Miniforge（官方 GitHub 發佈頁有其他平台的安裝檔）
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash Miniforge3-$(uname)-$(uname -m).sh -b -p ~/miniforge3
~/miniforge3/bin/conda init bash && source ~/.bashrc

conda config --set auto_activate_base false        # 開 shell 時不自動進入 base（可選）

# Bioconda：channel 順序有意義，conda-forge 優先
conda config --add channels bioconda
conda config --add channels conda-forge
conda config --set channel_priority strict
conda config --show channels                        # 應為 conda-forge, bioconda（由上到下）
```

> **不要把工具裝在 base 環境**；base 只放 conda / mamba 本身。每個專案或每組相容的工具一個環境。

## 環境操作

```bash
mamba create -n rnaseq python=3.12 samtools=1.21 star salmon fastp   # 建立並安裝
conda activate rnaseq
conda deactivate

mamba install -n rnaseq multiqc            # 安裝到指定環境
mamba install bioconda::bcftools           # 指定 channel
mamba search 'samtools>=1.20'              # 查可用版本
conda list                                 # 目前環境的套件
conda list samtools                        # 單一套件版本
conda env list                             # 所有環境
conda env remove -n rnaseq                 # 刪除環境
conda clean --all                          # 清除快取（套件快取常占數 GB）
```

| 情境 | 做法 |
| --- | --- |
| 需要 pip 才有的套件 | 先用 conda 裝好其他套件，最後在環境中 `python -m pip install`；先確認 `which python` 指向該環境 |
| 工具之間版本衝突 | 分成多個環境（例如 QC 一個、比對一個），不要硬塞進同一個 |
| 環境放在專案資料夾 | `mamba create -p ./env ...`、`conda activate ./env` |
| HPC 家目錄配額小 | `conda config --add pkgs_dirs /project/conda/pkgs`、`envs_dirs` 指到大容量空間 |

## `environment.yml`：可重現的環境

```yaml
# environment.yml
name: rnaseq
channels:
  - conda-forge
  - bioconda
dependencies:
  - python=3.12
  - samtools=1.21
  - star=2.7.11b
  - salmon
  - fastp
  - multiqc
  - pandas
  - pip
  - pip:
      - pydeseq2
```

```bash
mamba env create -f environment.yml         # 建立
mamba env update -f environment.yml --prune # 依檔案更新（--prune 移除檔案中沒有的套件）
conda env export --from-history > environment.yml   # 匯出：只列出你明確安裝的套件（跨平台）
conda env export > environment.lock.yml     # 匯出：所有套件的精確版本與 build（只保證同平台）
```

| 匯出方式 | 內容 | 用途 |
| --- | --- | --- |
| `--from-history` | 只有手動指定的套件 | 分享、跨平台重建 |
| 完整 `export` | 每個相依套件的精確版本與 build 字串 | 同平台精確重現 |
| `conda-lock` / `pixi.lock` | 多平台 lock 檔 | 嚴格可重現 |

> 重要的工具在 `environment.yml` 中**固定版本**（`samtools=1.21`）；不固定的話，半年後重建會拿到不同版本，結果可能不同。更長期的重現性用 [容器](docker/README.md)：每個 bioconda 套件都有對應的 BioContainers 映像檔。

## 與其他工具的分工

| 需求 | 工具 |
| --- | --- |
| 純 Python 專案 | [uv](../../data-science/python-foundations/python-packages.md) |
| R 套件版本 | [renv](../../data-science/r-foundations/reproducible-environments-with-renv.md) |
| 生資命令列工具、混合語言 | conda / mamba（bioconda） |
| 跨機器完全一致、交付給他人 | [Docker](docker/README.md) / [Apptainer](apptainer.md) |
| 工作流中每個步驟一個環境 | Nextflow / Snakemake 的 `conda:` 或 `container:` 指令，見 [工作流引擎](../workflow-engines/README.md) |

| 常見錯誤 | 說明 |
| --- | --- |
| 所有工具裝在 base | base 損壞就整個 conda 不能用 |
| 混用 `defaults` 與 `conda-forge` | 套件 ABI 不相容，奇怪的錯誤；用 Miniforge + strict priority |
| 在 conda 環境中用系統 `pip` | 套件裝到別處；用 `python -m pip` |
| 環境越裝越多東西 | 解析變慢、衝突變多；用 `environment.yml` 重建 |
