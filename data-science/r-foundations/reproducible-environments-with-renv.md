[Data Science](../README.md) › [R Foundations](README.md) › renv

# 可重現環境：renv (Reproducible Environments)

半年後重跑分析，DESeq2 或 Seurat 已經更新，結果數字不同甚至跑不動——這是 R 專案最常見的可重現性問題。`renv` 為每個專案建立**獨立的套件庫**，並把確切版本記錄在 `renv.lock`，讓別人（或未來的自己）能還原同一組套件。Python 的對應工具是 `uv` / conda，見 [Python 套件與環境](../python-foundations/python-packages.md)。

## 核心概念

| 元件 | 作用 |
| --- | --- |
| 專案套件庫 `renv/library/` | 此專案專用，與其他專案、全域 library 隔離（不進 git） |
| `renv.lock` | JSON：R 版本、每個套件的版本與來源（CRAN / Bioconductor / GitHub）；**要進 git** |
| `.Rprofile` + `renv/activate.R` | 開啟專案時自動啟用 renv（要進 git） |
| 全域快取 | 相同版本的套件只下載一次，多個專案用連結共享，不會重複佔空間 |

## 常用指令

```r
install.packages("renv")

# 1. 建立：掃描專案程式碼用到的套件，建立專案 library 與 renv.lock
renv::init()
renv::init(bioconductor = "3.21")        # 有用 Bioconductor 時指定版本

# 2. 平常照樣安裝套件（在專案內會裝到專案 library）
renv::install("dplyr")
renv::install("bioc::DESeq2")            # Bioconductor
renv::install("user/repo")               # GitHub

# 3. 確認狀態並記錄
renv::status()                           # lockfile、library、程式碼用到的套件三者是否一致
renv::snapshot()                         # 把目前 library 寫進 renv.lock

# 4. 別人 clone 專案後還原
renv::restore()                          # 依 renv.lock 安裝確切版本

# 其他
renv::update()                           # 更新套件（之後再 snapshot）
renv::history(); renv::revert(commit = "abc123")   # 搭配 git 回到舊的 lockfile
renv::deactivate()                       # 停用
```

```
init() ──→ 開發：install() / 寫程式 ──→ status() ──→ snapshot() ──→ git commit renv.lock
                         ↑                                              │
                         └──────────── 合作者：git pull → restore() ←──┘
```

## renv 管不到的部分

renv 只鎖定 R 套件。完整的可重現性還需要：

| 層級 | 工具 |
| --- | --- |
| R 套件版本 | renv |
| R 本身版本 | `renv.lock` 有記錄但不會幫你安裝；用 `rig`（R 版本管理器）切換 |
| 系統函式庫（libxml2、HDF5、GDAL）與編譯器 | Docker（`rocker/r-ver:4.x` 映像檔）或 conda |
| 外部工具（STAR、samtools） | conda / 容器，見 [容器與環境](../../computing/containers-and-env/README.md) |
| 亂數 | `set.seed()`；平行時見 [平行運算](parallel-programming-in-r.md#可重現性平行亂數) |
| 執行紀錄 | 報告結尾附 `sessionInfo()` 或 `sessioninfo::session_info()` |

> 發表論文或交付分析時：`renv.lock` + 程式碼 + `sessionInfo()` 是最低標準；需要長期重現就再加上 Docker 映像檔。

## 實務注意

| 情況 | 做法 |
| --- | --- |
| 套件很多、安裝很慢 | 設定 [Posit Public Package Manager](https://packagemanager.posit.co/) 取得 Linux 預編譯 binary（`options(repos = ...)`） |
| HPC 上沒有網路 | 在有網路的節點 `restore()`，或用容器 |
| 只是一次性探索 | 不必用 renv；確定要保留或分享時再 `init()` |
| 套件開發 | 套件的 DESCRIPTION 宣告最低版本；renv 用在**使用**套件的分析專案，見 [套件開發](package-development.md#套件-vs-分析專案) |
| 和 R Markdown / Quarto 一起用 | renv 會掃描 `.Rmd` / `.qmd` 中的套件；見 [R Markdown 與 Quarto](reporting-with-r-markdown.md) |
| 版本衝突、`restore()` 失敗 | 先 `renv::status()`；個別套件可 `renv::install("pkg@1.2.3")` 指定版本 |
