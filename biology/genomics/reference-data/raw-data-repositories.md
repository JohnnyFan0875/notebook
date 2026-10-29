[基因體學](../README.md) › [參考資料](README.md) › 原始資料庫

# 原始資料庫 (Raw Data Repositories)

論文發表的定序資料多數存放在 INSDC（國際核酸序列資料庫聯盟）的三個鏡像資料庫中；處理後的表現量矩陣常放在 GEO。重新分析公開資料時，先找到 accession，再決定從哪裡下載。

## 資料庫

| 資料庫 | 機構 | 收錄 | 何時用 |
| --- | --- | --- | --- |
| [SRA](https://www.ncbi.nlm.nih.gov/sra) | NCBI（美國） | 原始 reads | 論文最常提供 SRR / PRJNA |
| [ENA](https://www.ebi.ac.uk/ena/browser/home) | EMBL-EBI（歐洲） | 原始 reads、組裝、註解 | **直接下載 FASTQ.gz 最方便** |
| [DDBJ / DRA](https://www.ddbj.nig.ac.jp/dra/) | 日本 | 原始 reads | 亞洲團隊上傳 |
| [GEO](https://www.ncbi.nlm.nih.gov/geo/) | NCBI | 處理後的表現量、樣本描述（原始 reads 連到 SRA） | 想直接拿 count matrix 或樣本 metadata |
| [ArrayExpress / BioStudies](https://www.ebi.ac.uk/biostudies/arrayexpress) | EMBL-EBI | 功能基因體實驗（與 GEO 類似） | 歐洲團隊的表現量資料 |
| [dbGaP](https://www.ncbi.nlm.nih.gov/gap/) / [EGA](https://ega-archive.org/) | NCBI / EMBL-EBI | **受控存取**的人類資料（可識別個人） | 需提出申請並經資料存取委員會核准 |

> INSDC 三個資料庫每天互相同步：SRA 的 `SRR` 在 ENA 也查得到，反之亦然。

## Accession 的階層

| 層級 | SRA / ENA / DDBJ 前綴 | GEO | 意義 |
| --- | --- | --- | --- |
| 研究 (project) | `PRJNA` / `PRJEB` / `PRJDB`；`SRP` / `ERP` / `DRP` | `GSE` | 一篇論文 / 一個計畫 |
| 樣本 (sample) | `SAMN` / `SAMEA`；`SRS` / `ERS` | `GSM` | 一個生物樣本 |
| 實驗 (experiment) | `SRX` / `ERX` / `DRX` | — | 一個 library |
| Run | `SRR` / `ERR` / `DRR` | — | 一次定序輸出，**實際下載的單位** |

一個樣本可能有多個 run（多個 lane 或重複定序），分析時通常合併。

## 下載

```bash
# 1. 先查出 run 清單與 FASTQ 連結（ENA filereport API）
curl -s "https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJNA123456&result=read_run&fields=run_accession,sample_alias,fastq_ftp,fastq_md5&format=tsv"

# 2a. ENA：直接下載 FASTQ.gz（路徑依 accession 長度多一層子資料夾，以 filereport 的連結為準）
wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR164/ERR164407/ERR164407.fastq.gz
wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/ERR609/001/ERR6090701/ERR6090701_1.fastq.gz

# 2b. SRA：sra-tools
prefetch SRR1234567
fasterq-dump --split-files --threads 8 SRR1234567     # 產生 _1.fastq、_2.fastq（未壓縮，記得再壓縮）

# 2c. 一次處理整個專案（含 metadata 表）
nextflow run nf-core/fetchngs --input ids.csv --outdir fetched
```

| 方法 | 優點 | 注意 |
| --- | --- | --- |
| ENA FTP / HTTPS | 已是 FASTQ.gz，可用 `wget` / `curl`；目錄附 `.md5` 檢查完整性 | 大量資料可改用 Aspera（`ascp`）加速 |
| ENA File Downloader / enaBrowserTools | 依 accession 批次下載 | Java / Python 工具 |
| sra-tools | 官方工具，可取得完整原始資訊 | `fasterq-dump` 需要大量暫存空間 |
| [nf-core/fetchngs](https://nf-co.re/fetchngs) | 自動抓 metadata、下載、產生樣本表 | 需要 Nextflow（見 [Nextflow](../../../computing/workflow-engines/nextflow/README.md)） |

> 下載後先比對 **md5** 與 reads 數；並從 GEO / SRA 的樣本描述整理出 metadata（條件、批次、性別），這往往比下載本身更花時間，也是重新分析最容易出錯的地方。

ENA 下載方式說明：[ENA file download](https://ena-docs.readthedocs.io/en/latest/retrieval/file-download.html)。
