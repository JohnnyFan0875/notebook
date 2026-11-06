[Computing](../README.md) › [Cloud](README.md) › 雲端運算基礎

# 雲端運算基礎 (Cloud Computing Fundamentals)

雲端運算不只是「把伺服器搬到別人的機房」，而是把運算、儲存、網路與平台能力變成**可隨需取得、以 API 操作、依用量計費**的服務。對資料與生資工作者，雲端的價值在於：不必先買機器就能跑大規模分析、直接使用存放在雲端的公開資料集（1000 Genomes、gnomAD、TCGA 等）、用託管服務省去維運。

## 為什麼用雲端

| 傳統自建機房 (on-premises) 的問題 | 雲端的做法 |
| --- | --- |
| 容量要先買，必須預估尖峰 | 隨需擴縮，用多少付多少 |
| 新環境開通慢 | 幾分鐘內建立資源 |
| 備援、災難復原、全球部署門檻高 | 多個區域與可用區現成可用 |
| 固定的資本支出 (CapEx) | 變動的營運支出 (OpEx) |

> 雲端不保證比較便宜：長期滿載的工作負載可能自建更划算；沒有治理的雲端很容易浪費。真正的好處是彈性與速度。

## 服務模式 (Service Models)

| 模式 | 供應商負責 | 你負責 | 例子 | 適合 |
| --- | --- | --- | --- | --- |
| IaaS | 硬體、虛擬化、基礎網路 | OS、執行環境、應用、資料 | EC2、Azure VM、Compute Engine | 需要控制權、搬遷既有系統 |
| PaaS | 上述 + OS 與執行平台 | 應用程式與資料 | Elastic Beanstalk、App Service、Cloud Run、託管資料庫 | 專注開發交付 |
| SaaS | 幾乎整個應用 | 設定、資料、使用治理 | Microsoft 365、Gmail、Salesforce | 直接使用成熟產品 |
| Serverless / FaaS | 連擴縮與伺服器都不見了 | 函式程式碼 | Lambda、Azure Functions、Cloud Run functions | 事件驅動、短時任務 |

```text
控制權高 ◄─────────────────────────────────────────► 維運負擔低
   自建機房 → IaaS → 容器服務 → PaaS → Serverless → SaaS
```

## 部署模式 (Deployment Models)

| 模式 | 說明 | 優點 | 代價 |
| --- | --- | --- | --- |
| 公有雲 (public) | 供應商營運、多客戶共用基礎設施 | 啟動快、服務多、無前期投資 | 需要成本與治理紀律 |
| 私有雲 (private) | 專屬於單一組織（自建或託管） | 控制權高、特殊合規較易 | 前期投資與管理成本高 |
| 混合雲 (hybrid) | 私有 + 公有 | 敏感資料留在內部，彈性運算放公有雲（尖峰時 cloud bursting） | 架構、網路、治理更複雜 |
| 多雲 (multi-cloud) | 同時使用多家公有雲 | 避免綁定、各取所長 | 技能與治理成本加倍 |

## 共享責任模型 (Shared Responsibility Model)

| 供應商負責「雲端**本身**」的安全 | 客戶負責「**雲端裡**」的安全 |
| --- | --- |
| 實體機房、硬體、網路基礎設施、虛擬化層 | 資料、身分與權限、網路規則、OS 修補（IaaS）、應用程式、加密設定 |

上雲不代表安全責任消失，而是分界改變；託管程度越高，客戶負責的範圍越小。最常見的雲端資安事件是客戶自己設定錯誤（公開的儲存桶、過大的權限、外洩的金鑰）。

## 全球基礎設施

| 層級 | 意義 | 決定什麼 |
| --- | --- | --- |
| 區域 (region) | 一個地理區域的一組資料中心 | 延遲、資料主權 / 法規（個資、健康資料常有地域限制）、可用服務、價格 |
| 可用區 (availability zone, AZ) | 區域內彼此獨立的資料中心群 | 高可用：跨 AZ 部署避免單點故障 |
| 邊緣節點 (edge location) | 靠近使用者的快取點 | CDN、降低延遲 |

## 計費的關鍵

| 項目 | 注意 |
| --- | --- |
| 運算 | 依時間與規格計費；閒置的 VM 照樣收費 |
| 儲存 | 依容量與儲存等級；冷儲存便宜但取回要錢、要等 |
| **資料傳出 (egress)** | 資料傳出雲端或跨區域要收費，進入通常免費；TB 級的定序資料下載費用可觀 |
| 託管服務 | 方便但單價較高 |
| 折扣 | 長期承諾（Reserved / Savings Plans / Committed Use）、可中斷的 Spot / Preemptible 執行個體（便宜 60–90%，適合可重試的批次分析） |

> 生資在雲端的常見做法：資料放物件儲存（S3 / Blob / Cloud Storage）、運算在**同一區域**（避免 egress）、用 Nextflow / Snakemake 搭配批次服務（AWS Batch、Azure Batch、Google Batch）與 Spot 執行個體。工作流見 [工作流引擎](../workflow-engines/README.md)。

## 選擇供應商

| 供應商 | 常見印象 |
| --- | --- |
| [AWS](aws-services-overview.md) | 服務最廣、生態最成熟；生資公開資料集（AWS Open Data）很多 |
| [Azure](azure-fundamentals.md) | 與 Microsoft 365、Entra ID、企業 IT 整合；企業與醫院常見 |
| [GCP](gcp-fundamentals.md) | 資料分析（BigQuery）與 AI 強；gnomAD、Terra 等生資平台在 GCP 上 |

實務上比功能表更重要的是：團隊熟悉哪個生態、機構既有的帳號與身分管理、法規要求、主要工作負載（網站、資料平台、ML、批次分析）。

| 常見誤區 | 說明 |
| --- | --- |
| 上雲 = 直接搬 VM (lift-and-shift) | 沒用到託管服務與彈性，成本常更高 |
| 上雲自然會便宜 | 沒有關機、沒有預算警示就會浪費 |
| 沒有治理就大量開資源 | 權限與成本失控 |
| 先選平台再想工作負載 | 應先定義需求 |

容器與虛擬化的概念見 [容器與虛擬化](../containers-and-env/containerization-and-virtualization.md)。
