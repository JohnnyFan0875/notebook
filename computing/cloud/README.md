[Computing](../README.md) › Cloud

# 雲端 (Cloud)

雲端平台的共通概念與 AWS、Azure、GCP 各自的服務。價格、服務名稱、考試代號會變動，以官方文件為準。

## 建議順序

```
雲端運算基礎 ──┬─► AWS：服務總覽 → 安全與成本 → Boto3（→ Cloud Practitioner 考試）
               ├─► Azure：基礎 → 服務總覽 → 管理與治理
               └─► GCP：基礎
```

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [雲端運算基礎](cloud-computing-fundamentals.md) | IaaS / PaaS / SaaS、部署模式、共享責任、全球基礎設施、計費與 egress | 雲端是什麼？該保留多少控制權？ |
| [AWS 服務總覽](aws-services-overview.md) | 運算、儲存、資料庫、網路、AI/ML、管理工具 | 這個需求該用哪個 AWS 服務？ |
| [AWS 安全與成本管理](aws-security-and-cost-management.md) | IAM、root 保護、加密、定價模式、Budgets、Cost Explorer、支援方案 | 權限與花費怎麼控管？ |
| [Boto3](boto3-for-aws-services.md) | 憑證順序、S3、SNS、Rekognition、Translate、Comprehend | 怎麼用 Python 操作 AWS？ |
| [AWS Cloud Practitioner 考試](aws-certified-cloud-practitioner.md) | CLF-C02 範圍、比重、Well-Architected、遷移、準備策略 | 考試考什麼、怎麼準備？ |
| [Azure 基礎](azure-fundamentals.md) | 資源階層、區域、運算模型、儲存體帳戶與冗餘 | Azure 資源怎麼組織？ |
| [Azure 服務總覽](azure-services-overview.md) | 運算、容器、儲存、資料庫與分析、網路、AI | 這個需求該用哪個 Azure 服務？ |
| [Azure 管理與治理](azure-management-and-governance.md) | Portal / CLI、ARM / Bicep、成本、RBAC / Policy、Monitor | Azure 怎麼部署、控成本、訂規則、監控？ |
| [GCP 基礎](gcp-fundamentals.md) | 專案階層、`gcloud`、Compute / Cloud Run / BigQuery / Vertex AI | GCP 有什麼、生資平台為何常在 GCP？ |

## 服務對照

| 類別 | AWS | Azure | GCP |
| --- | --- | --- | --- |
| 虛擬機 | EC2 | Virtual Machines | Compute Engine |
| Serverless 函式 | Lambda | Functions | Cloud Run functions |
| Serverless 容器 | Fargate、App Runner | Container Apps | Cloud Run |
| Kubernetes | EKS | AKS | GKE |
| 批次運算 | AWS Batch | Azure Batch | Google Batch |
| 物件儲存 | S3 | Blob Storage | Cloud Storage |
| 封存 | S3 Glacier | Blob Archive tier | Archive storage class |
| 檔案共享 | EFS | Azure Files | Filestore |
| 區塊磁碟 | EBS | Managed Disks | Persistent Disk |
| 關聯式資料庫 | RDS、Aurora | Azure SQL、Database for PostgreSQL | Cloud SQL、AlloyDB、Spanner |
| NoSQL | DynamoDB | Cosmos DB | Firestore、Bigtable |
| 資料倉儲 | Redshift | Synapse、Fabric | BigQuery |
| 查詢物件儲存上的檔案 | Athena | Synapse serverless SQL | BigQuery external tables |
| 託管 Spark | EMR | Databricks、Synapse Spark | Dataproc |
| ML 平台 | SageMaker | Azure Machine Learning | Vertex AI |
| 生成式 AI | Bedrock | Azure OpenAI / AI Foundry | Vertex AI（Gemini） |
| 虛擬網路 | VPC | VNet | VPC |
| 身分 | IAM、Identity Center | Entra ID、RBAC | Cloud IAM |
| 監控 | CloudWatch | Azure Monitor | Cloud Monitoring / Logging |
| 稽核紀錄 | CloudTrail | Activity Log | Cloud Audit Logs |
| IaC | CloudFormation、CDK | ARM / Bicep | Infrastructure Manager（Terraform） |
| 命令列 | `aws` | `az` | `gcloud` |

| 相關 | 筆記 |
| --- | --- |
| 容器與 Kubernetes | [容器與環境](../containers-and-env/README.md) |
| 雲端上跑生資 pipeline | [工作流引擎](../workflow-engines/README.md) |
| 雲端資料平台 | [資料工程](../../data-science/data-engineering/README.md)、[雲端資料倉儲](../../data-science/data-engineering/cloud-data-warehouses.md) |
| 模型部署 | [MLOps](../../data-science/machine-learning/production/mlops-overview.md) |
