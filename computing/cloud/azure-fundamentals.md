[Computing](../README.md) › [Cloud](README.md) › Azure 基礎

# Azure 基礎 (Azure Fundamentals)

Azure 是 Microsoft 的雲端平台，常見於已深度使用 Microsoft 生態（Microsoft 365、Entra ID、Windows Server）的企業與醫院。本篇建立 Azure 的資源組織方式與核心觀念；服務分類見 [Azure 服務總覽](azure-services-overview.md)，管理與治理見 [Azure 管理與治理](azure-management-and-governance.md)。入門認證為 AZ-900（Azure Fundamentals）。

## 資源階層

```
Microsoft Entra ID 租用戶 (tenant)：身分
└── 管理群組 (management group)：多個訂用帳戶的治理
    └── 訂用帳戶 (subscription)：計費與存取邊界
        └── 資源群組 (resource group)：一起管理的一組資源
            └── 資源 (resource)：VM、儲存體帳戶、資料庫、虛擬網路…
```

| 層級 | 作用 |
| --- | --- |
| Entra ID（原 Azure Active Directory） | 使用者、群組、應用程式的身分與登入 |
| 管理群組 | 對多個訂用帳戶套用相同的政策與權限 |
| 訂用帳戶 | 帳單單位；常依環境（dev / prod）或部門區分 |
| 資源群組 | 生命週期相同的資源放一起：同一個應用的 VM、儲存體、資料庫、監控；刪除群組即刪除全部 |
| 資源 | 可被建立、修改、刪除、計費的實體 |

> 權限 (RBAC)、政策、標籤可以設在任一層級，並**向下繼承**。

Azure Resource Manager (ARM) 是所有管理操作的統一入口：不論從 Portal、CLI、PowerShell、SDK 或 IaC 範本操作，都經過 ARM 驗證權限後交給各資源提供者執行。

## 區域與可用性

| 概念 | 說明 |
| --- | --- |
| 區域 (region) | 地理區域；決定延遲、資料主權、可用服務 |
| 區域配對 (region pair) | 同地理範圍內配對的兩個區域，用於災難復原與分批更新 |
| 可用性區域 (availability zone) | 區域內獨立的資料中心群；跨區域部署提高可用性 |

## 運算模型

| 選擇 | 控制權 | 例子 |
| --- | --- | --- |
| IaaS | 高 | Virtual Machines |
| 容器 | 中 | Container Instances、Container Apps、AKS |
| PaaS | 中低 | App Service |
| Serverless | 低 | Functions |

| 容易混淆 | 差別 |
| --- | --- |
| Serverless | **誰管理基礎設施**：平台負責伺服器與自動擴縮，依執行計費 |
| Stateless | **應用是否保留狀態**：每次請求獨立，不記得前一次 |

兩者常一起出現（serverless 函式通常設計成 stateless），但不是同義詞。

## 儲存體帳戶 (Storage Account)

儲存體帳戶是 Azure 儲存服務的管理邊界：命名空間、存取權限、冗餘設定都在這一層。

| 服務 | 類型 | 適合 |
| --- | --- | --- |
| Blob Storage | 物件儲存（類似 S3） | 檔案、影像、備份、data lake（ADLS Gen2 = Blob + 階層命名空間） |
| Azure Files | 檔案共享（SMB / NFS） | 多台機器共用目錄 |
| Queue Storage | 訊息佇列 | 非同步處理、系統解耦 |
| Table Storage | 簡單的 key-value NoSQL | 結構簡單的非關聯式資料 |
| Managed Disks | VM 的區塊磁碟 | OS 與資料磁碟 |

| Blob 存取層 | 用途 |
| --- | --- |
| Hot | 常存取 |
| Cool / Cold | 不常存取，儲存便宜、存取較貴 |
| Archive | 封存，取回需數小時 |

| 冗餘選項 | 複本位置 | 防範 |
| --- | --- | --- |
| LRS | 同一資料中心 3 份 | 硬體故障 |
| ZRS | 同區域的 3 個可用性區域 | 單一資料中心故障 |
| GRS / RA-GRS | 主要區域 LRS + 配對區域 LRS（RA = 次要區域可讀） | 整個區域故障 |
| GZRS / RA-GZRS | 主要區域 ZRS + 配對區域 LRS | 資料中心與區域故障 |

選儲存體時要同時問「存在哪裡」與「故障時怎麼撐住」；冗餘越高成本越高。

## 部署整合

Azure 服務可直接連接 GitHub、Azure DevOps、Bitbucket 做持續部署：程式碼推送後自動建置、部署到 App Service 或容器服務。雲端平台不只提供基礎設施，也是應用交付流程的一部分；CI/CD 見 [DevOps](../devops/README.md)。

| 常見誤區 | 說明 |
| --- | --- |
| Azure 只是租 VM | PaaS 與託管服務才是主要價值 |
| 沒規劃資源群組，資源散落各處 | 難以管理權限、成本與刪除 |
| 所有儲存需求視為同一類 | 依存取模式選 Blob / Files / Disk / Queue |
| 只看服務名稱 | 也要看治理、部署與維運流程 |
