[Computing](../README.md) › [Cloud](README.md) › Azure 服務總覽

# Azure 服務總覽 (Azure Services Overview)

把常見 Azure 服務放進穩定的分類：先判斷需求屬於運算、儲存、資料庫還是網路，以及需要多少控制權，再挑服務。資源階層與儲存冗餘見 [Azure 基礎](azure-fundamentals.md)；三家雲對照見 [Cloud](README.md#服務對照)。

## 運算

| 服務 | 類型 | 適合 |
| --- | --- | --- |
| Virtual Machines | IaaS | 需要控制 OS、搬遷舊系統、自由度高的分析工作 |
| Virtual Machine Scale Sets | IaaS | 一組可自動擴縮的相同 VM |
| App Service | PaaS | Web 應用、API 託管 |
| Functions | Serverless | 事件驅動、短時程式 |
| Container Instances (ACI) | 容器 | 快速跑單一容器，不需編排 |
| Container Apps | 容器（serverless） | 微服務、API，平台處理擴縮 |
| AKS | 託管 Kubernetes | 需要完整 [Kubernetes](../containers-and-env/kubernetes.md) 編排 |
| Azure Batch | 批次運算 | 大量平行工作；Nextflow 可用作 executor |
| Azure Virtual Desktop | 桌面虛擬化 | 遠端 Windows 桌面 |

> 想快速跑一個容器 → Container Instances；要編排多個服務 → Container Apps 或 AKS。

## 儲存

| 服務 | 類型 | 適合 |
| --- | --- | --- |
| Blob Storage / Data Lake Storage Gen2 | 物件 | 檔案、備份、非結構化資料、data lake |
| Azure Files | 檔案共享 | 多台機器共用目錄 |
| Managed Disks | 區塊 | VM 磁碟 |
| Queue Storage | 訊息 | 非同步處理 |
| Table Storage | 簡單 NoSQL | 輕量 key-value |

冗餘選項（LRS / ZRS / GRS / GZRS）見 [Azure 基礎：儲存體帳戶](azure-fundamentals.md#儲存體帳戶-storage-account)。

| 資料搬移工具 | 用途 |
| --- | --- |
| AzCopy | 命令列大量上傳下載、同步（`azcopy sync`） |
| Storage Explorer | 圖形介面瀏覽與傳輸 |
| Data Box | 實體裝置搬運 TB 級資料 |
| Azure File Sync | 地端檔案伺服器與 Azure Files 同步 |

## 資料庫與分析

| 服務 | 類型 | 適合 |
| --- | --- | --- |
| Azure SQL Database / Managed Instance | 託管 SQL Server | 交易型應用 |
| Azure Database for PostgreSQL / MySQL | 託管開源關聯式 | 開源技術堆疊 |
| Cosmos DB | 全球分散式 NoSQL（多種 API） | 高擴展、低延遲 |
| Azure Synapse Analytics | 資料倉儲 + Spark + 管線 | 分析工作負載；Microsoft 引導新專案改用 Fabric，但 Synapse 仍受支援 |
| Microsoft Fabric | SaaS 資料平台（OneLake、Data Factory、倉儲、Power BI） | 新的分析與 BI 專案 |
| Azure Databricks | 託管 Spark / lakehouse | 資料工程、ML，見 [Databricks](../../data-science/data-engineering/databricks.md) |
| Data Factory | 資料整合 / ETL 管線 | 排程搬移與轉換資料 |

## 網路

| 服務 | 作用 |
| --- | --- |
| Virtual Network (VNet) | 私有網路邊界；子網切分 |
| Network Security Group (NSG) | 子網或網卡層級的流量規則 |
| VNet peering | 連接兩個 VNet |
| VPN Gateway | 地端與 Azure 之間的加密連線（經網際網路） |
| ExpressRoute | 專線連線，不經公網，穩定且私密 |
| Azure DNS | 託管 DNS 記錄 |
| Load Balancer / Application Gateway | 第 4 層 / 第 7 層（HTTP）負載平衡 |
| Front Door / CDN | 全球入口與內容快取 |

## AI 與身分

| 服務 | 用途 |
| --- | --- |
| Azure AI Foundry、Azure OpenAI | 生成式 AI 模型與應用開發 |
| Azure AI services（Language、Vision、Speech、Document Intelligence） | 預訓練 API |
| Azure Machine Learning | ML 平台：訓練、部署、MLOps |
| Microsoft Entra ID | 身分與單一登入 |
| Key Vault | 金鑰、密碼、憑證 |

## 簡化地圖

| 類別 | 代表服務 | 先記住的用途 |
| --- | --- | --- |
| 運算 | VM、App Service、Functions | 跑應用與程式 |
| 容器 | Container Instances、Container Apps、AKS | 跑容器、編排 |
| 物件儲存 | Blob Storage | 檔案、備份、data lake |
| 檔案儲存 | Azure Files | 共用目錄 |
| 磁碟 | Managed Disks | VM 磁碟 |
| 關聯式資料庫 | Azure SQL | 交易資料 |
| NoSQL | Cosmos DB | 高擴展、低延遲 |
| 分析 | Synapse、Fabric、Databricks | 資料平台與分析 |
| 網路 | VNet、VPN Gateway、ExpressRoute、DNS | 隔離、連線、名稱解析 |

| 常見誤區 | 說明 |
| --- | --- |
| 所有工作負載都當 VM 問題 | 先看 PaaS / serverless 能否滿足 |
| object / file / disk / NoSQL 儲存不分 | 依存取模式選 |
| 容器 = Kubernetes | ACI、Container Apps 不需要自己管 K8s |
| 交易型資料庫與分析平台混用 | OLTP 與 OLAP 分開 |
