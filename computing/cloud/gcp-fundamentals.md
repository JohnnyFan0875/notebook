[Computing](../README.md) › [Cloud](README.md) › GCP 基礎

# GCP 基礎 (Google Cloud Fundamentals)

Google Cloud (GCP) 是 Google 的雲端平台，特色是全球網路、資料分析（BigQuery）與 AI（Vertex AI）。生資圈不少平台建在 GCP 上：Terra（Broad Institute）、gnomAD 的公開資料、All of Us Researcher Workbench。先用三個問題定位服務：工作負載是跑應用還是處理資料？需要 VM、容器還是 serverless？資料用於交易、分析還是訓練模型？

## 資源階層

```text
組織 (organization)
└── 資料夾 (folder)
    └── 專案 (project)：計費、API 啟用、權限的基本單位
        └── 資源：VM、bucket、BigQuery dataset…
```

| 概念 | 說明 |
| --- | --- |
| 專案 (project) | 所有資源都屬於某個專案；有專案 ID 與帳單帳戶 |
| IAM | 角色指派給使用者、群組、服務帳戶 (service account)，在各層級向下繼承 |
| 區域 / 可用區 | `asia-east1`（台灣彰化）、`asia-east1-a`；部分服務是多區域 (multi-region) |

```bash
gcloud auth login                              # 登入
gcloud config set project my-lab-project       # 設定預設專案
gcloud compute instances list
gcloud storage cp sample.bam gs://my-lab-data/ # 上傳到 Cloud Storage
gcloud storage ls gs://my-lab-data/
```

## 運算

| 路線 | 服務 | 適合 |
| --- | --- | --- |
| VM | Compute Engine | 需要控制 OS、GPU、長時間執行；Spot VM 便宜但可被收回 |
| 容器編排 | GKE | Kubernetes |
| Serverless 容器 | Cloud Run | 把容器當成自動擴縮的 HTTP 服務或批次 job |
| Serverless 函式 | Cloud Run functions（原 Cloud Functions） | 事件觸發的小程式 |
| PaaS | App Engine | 傳統 web 應用 |
| 批次 | Google Batch | 大量批次工作；Nextflow、Snakemake、Cromwell（Terra）的 executor |

## 資料

先依資料型態與用途選服務：

| 服務 | 類型 | 適合 |
| --- | --- | --- |
| Cloud Storage | 物件儲存（類似 S3） | 檔案、媒體、備份、data lake；`gs://` 路徑 |
| Cloud SQL | 託管 MySQL / PostgreSQL / SQL Server | 傳統交易型應用 |
| AlloyDB | PostgreSQL 相容、高效能 | 較大的交易型 + 分析混合工作負載 |
| Cloud Spanner | 全球分散式關聯式資料庫 | 需要水平擴展又要強一致的關聯式資料 |
| Firestore / Bigtable | NoSQL（文件 / 寬欄） | 應用資料 / 大量時間序列 |
| BigQuery | Serverless 資料倉儲 | 大規模 SQL 分析；**依掃描量計費**，選欄位與分區可大幅省錢 |
| Dataflow / Dataproc | 串流與批次處理（Beam）/ 託管 Spark | 資料工程 |
| Looker / Looker Studio | BI 與視覺化 | 分析結果的消費層 |

```sql
-- BigQuery：只選需要的欄位（SELECT * 會掃描並計費全部欄位）
SELECT chrom, COUNT(*) AS n_variants
FROM `my-lab-project.genomics.variants`
WHERE filter = 'PASS'
GROUP BY chrom
ORDER BY n_variants DESC;
```

> BigQuery 不是交易型資料庫；分析型與交易型工作負載分開。資料倉儲的設計見 [雲端資料倉儲](../../data-science/data-engineering/cloud-data-warehouses.md)，Spark SQL 見 [Spark](../../data-science/data-engineering/spark.md#spark-sql)。

## AI

| 服務 | 用途 |
| --- | --- |
| Vertex AI | ML 平台：資料、訓練、調參、部署、監控、模型庫；Gemini 等生成式模型也從這裡使用 |
| 預訓練 API | Vision、Speech-to-Text、Translation、Natural Language、Document AI |
| Healthcare API | FHIR、DICOM、HL7v2 的託管存放與存取 |

## 三家對照

| 類別 | AWS | Azure | GCP |
| --- | --- | --- | --- |
| 物件儲存 | S3 | Blob Storage | Cloud Storage |
| 資料倉儲 | Redshift | Synapse / Fabric | BigQuery |
| 批次 | AWS Batch | Azure Batch | Google Batch |
| ML 平台 | SageMaker | Azure Machine Learning | Vertex AI |

完整對照見 [Cloud](README.md#服務對照)。

| 常見誤區 | 說明 |
| --- | --- |
| GCP 只是另一個 VM 平台 | 價值在 BigQuery、Cloud Run 等託管服務 |
| 沒分資料型態就選服務 | 交易、分析、檔案各有對應 |
| BigQuery 當交易型資料庫 | 它是分析倉儲 |
| BigQuery `SELECT *` 探索大表 | 依掃描量計費；先看預覽與 schema |
