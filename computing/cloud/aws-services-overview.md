[Computing](../README.md) › [Cloud](README.md) › AWS 服務總覽

# AWS 服務總覽 (AWS Services Overview)

把常見 AWS 服務放進穩定的類別，遇到需求時先判斷類別、再挑服務。先問三件事：要解決的是運算、儲存、資料庫還是網路？要基礎資源還是託管服務？工作負載偏應用交付、資料平台還是 AI / ML？三家雲的服務對照見 [Cloud](README.md#服務對照)。

## 全球基礎設施

| 層級 | 說明 |
| --- | --- |
| Region | 地理區域（`us-east-1`、`ap-northeast-1` 東京）；資料不會自動離開區域 |
| Availability Zone | 區域內彼此獨立的一或多個資料中心；高可用架構跨 AZ 部署 |
| Edge location | CloudFront 的快取節點，靠近使用者 |

## 運算 (Compute)

| 服務 | 是什麼 | 適合 |
| --- | --- | --- |
| EC2 | 虛擬機；自選 OS、規格、磁碟 | 長時間執行、需要客製環境、GPU 運算 |
| Lambda | Serverless 函式，事件觸發，單次最長 15 分鐘 | 檔案上傳後處理、輕量 API、自動化 |
| ECS / Fargate | 容器服務；Fargate 不必管伺服器 | 容器化應用 |
| EKS | 託管 Kubernetes | 已採用 [Kubernetes](../containers-and-env/kubernetes.md) |
| AWS Batch | 批次工作排程（底層用 EC2 / Spot / Fargate） | 生資 pipeline：Nextflow、Snakemake 的雲端 executor |
| Elastic Beanstalk | PaaS：上傳程式碼，平台負責部署 | 傳統 web 應用 |

| | EC2 | Lambda |
| --- | --- | --- |
| 控制權 | 高 | 低 |
| 維運責任 | OS 修補、擴縮自己管 | 平台負責 |
| 計費 | 開機時間 | 執行次數 × 時間 |
| 心智模型 | 租一台可調整的伺服器（自己開車） | 需要時才執行的一段程式（叫車） |

| EC2 購買方式 | 說明 |
| --- | --- |
| On-Demand | 依秒 / 小時計費，無承諾 |
| Savings Plans / Reserved Instances | 承諾 1 或 3 年用量換折扣 |
| Spot | 用剩餘容量，大幅折扣，但可能被收回（2 分鐘預告） |
| Dedicated Hosts | 專屬實體主機（授權、合規需求） |

## 儲存 (Storage)

| 服務 | 類型 | 說明 |
| --- | --- | --- |
| S3 | 物件儲存 | 檔案、data lake、備份、靜態網站；以 bucket + key 存取，耐久度 11 個 9 |
| EBS | 區塊儲存 | 掛在單一 EC2 上的磁碟 |
| EFS | 檔案儲存（NFS） | 多台 EC2 共用的檔案系統 |
| FSx for Lustre | 高效能平行檔案系統 | HPC、可與 S3 連動 |
| S3 Glacier | 封存 | 便宜，取回需要時間與費用 |

| S3 儲存類別 | 用途 |
| --- | --- |
| Standard | 常用資料 |
| Intelligent-Tiering | 存取模式不確定時自動分層 |
| Standard-IA / One Zone-IA | 不常存取但需要時要立即可讀 |
| Glacier Instant / Flexible / Deep Archive | 封存，取回時間由毫秒到數小時 |

> 用生命週期規則 (lifecycle rules) 讓原始 FASTQ 在分析完成後自動轉到 Glacier，可大幅降低長期儲存成本。很多公開生資資料集（1000 Genomes、gnomAD、TCGA 的開放部分）以 [AWS Open Data](https://registry.opendata.aws/) 形式放在 S3，可直接在同區域讀取。

## 資料庫

| 服務 | 類型 | 適合 |
| --- | --- | --- |
| RDS | 託管關聯式（PostgreSQL、MySQL、SQL Server 等） | 交易型應用、明確的 schema |
| Aurora | AWS 雲端原生的 MySQL / PostgreSQL 相容資料庫 | 高可用、較高效能的關聯式工作負載 |
| DynamoDB | 託管 NoSQL（key-value / 文件） | 高吞吐、低延遲、schema 彈性 |
| Redshift | 資料倉儲 | BI、大規模分析查詢 |
| Athena | 用 SQL 直接查 S3 上的檔案（Parquet / CSV） | 不想建資料庫的臨時分析 |
| ElastiCache | 託管 Redis / Memcached | 快取 |

交易型 (OLTP) 與分析型 (OLAP) 不要混用；概念見 [資料庫](../../data-science/databases/README.md)、[雲端資料倉儲](../../data-science/data-engineering/cloud-data-warehouses.md)。

## 網路

| 服務 / 元件 | 作用 |
| --- | --- |
| VPC | 邏輯隔離的虛擬網路，所有資源的網路邊界 |
| Subnet | 切分 VPC 位址；公開子網（有路由到 Internet Gateway）vs 私有子網 |
| Route table | 流量往哪裡走 |
| Internet Gateway / NAT Gateway | 對外連線 / 讓私有子網可以連出但不被連入 |
| Security Group | 執行個體層級的防火牆，**有狀態**，只能寫允許規則 |
| Network ACL | 子網層級，**無狀態**，可允許也可拒絕 |
| Route 53 | DNS |
| CloudFront | CDN |
| Direct Connect / Site-to-Site VPN | 機房與 AWS 之間的專線 / 加密連線 |

## AI / ML

| 類型 | 服務 | 用途 |
| --- | --- | --- |
| 預訓練 API | Translate、Polly（文字轉語音）、Transcribe（語音轉文字）、Lex（對話機器人）、Comprehend（NLP；Comprehend Medical 抽取醫療實體）、Rekognition（影像）、Textract（文件 OCR） | 不必自己訓練就能嵌入產品 |
| 生成式 AI | Bedrock | 透過 API 使用多家基礎模型 |
| ML 平台 | SageMaker | 資料準備、訓練、調參、部署、監控 |

用 Python 呼叫這些服務見 [Boto3](boto3-for-aws-services.md)；ML 部署與監控見 [MLOps](../../data-science/machine-learning/production/mlops-overview.md)。

## 管理與監控

| 服務 | 作用 |
| --- | --- |
| CloudWatch | 指標、log、警示（**系統表現如何**） |
| CloudTrail | API 呼叫紀錄（**誰做了什麼**），稽核用 |
| CloudFormation / CDK | 基礎設施即程式碼 (IaC)；跨雲常用 Terraform |
| Systems Manager | 大量 EC2 的修補、指令執行、參數 |
| Organizations | 多帳號管理與合併帳單 |

串流資料（Kinesis + Lambda）見 [串流](../../data-science/data-engineering/streaming.md#awskinesis--firehose--lambda)。

## 常見誤區

| 誤區 | 說明 |
| --- | --- |
| 所有資料都放同一種資料庫 | 依存取模式選 |
| S3、EBS、EFS 可互換 | 物件 vs 單機磁碟 vs 共用檔案系統 |
| AI 需求一律自己訓練模型 | 先看預訓練 API 是否夠用 |
| VPC 只是網路開關 | 它是整個隔離與流量治理的邊界 |
| 運算與資料放不同區域 | 跨區傳輸收費且慢 |
