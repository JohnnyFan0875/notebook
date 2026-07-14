# AWS Certified Cloud Practitioner

`CLF-C02`

這份筆記不是逐題考點表，而是把 Cloud Practitioner 常見的 AWS 入門概念整理成一套可連起來的心智模型。

## AWS 是什麼

AWS 是 Amazon 提供的雲端平台，核心特徵可以先抓三件事：

- 服務種類很多，從基礎運算到資料、網路、安全與 AI 都有對應產品
- 全球基礎設施完整，方便做跨區域與高可用架構
- 大量能力可以透過 API、管理主控台與 IaC 工具操作

如果 [Cloud Computing Fundamentals](cloud-computing-fundamentals.md) 講的是雲端的一般概念，AWS 這一頁就是把那些概念放到一個實際供應商上理解。

## 先建立三個 AWS 視角

學 AWS 時，先不要急著背服務名稱，可以先用三個視角去看：

1. 全球基礎設施怎麼組成
2. 成本與擴展性為什麼和傳統機房不同
3. 常見 workload 會落在哪些服務類型

## 全球基礎設施

### Region

`Region` 是 AWS 在特定地理區域內的一組雲端基礎設施。

它通常用來回應幾個問題：

- 工作負載要離使用者多近
- 是否有資料主權或法規需求
- 災難復原要不要跨地理區域

### Availability Zone

一個 region 內通常有多個 `Availability Zone`。

重點不是把 AZ 當成名詞背起來，而是理解它的用途：

- 每個 AZ 是一個或多個離散資料中心
- 多個 AZ 可以提高 redundancy
- 高可用架構常會跨 AZ 配置

也就是說，region 解決的是地理層級，AZ 解決的是區域內的可用性層級。

### Edge Location

`Edge Location` 主要用於把內容更靠近使用者，常和 `CloudFront` 這類 CDN 能力一起理解。

它的價值通常在：

- 降低延遲
- 提升靜態內容傳遞速度
- 把流量壓力從核心基礎設施分散出去

## 雲端經濟學

Cloud Practitioner 很常考的不是精算，而是思維轉換。

### Fixed Cost vs Variable Cost

傳統 IT 常見的是固定成本思維：

- 先買硬體
- 先建機房
- 先為尖峰容量預留空間

cloud 常見的是變動成本思維：

- 依使用量付費
- 隨需求擴縮
- 避免長期閒置資源

所以 cloud economics 的核心問題不是「雲一定比較便宜」，而是：

- 你能不能把資源配置跟真實需求對齊
- 你有沒有治理機制避免浪費
- 你的 workload 是否適合用彈性模型運作

## Well-Architected Framework

AWS Well-Architected Framework 可以理解成一套架構檢查框架，用來幫助團隊評估系統是否夠穩定、夠安全、夠有效率。

這套框架的六大支柱是：

- Operational Excellence
- Security
- Reliability
- Performance Efficiency
- Cost Optimization
- Sustainability

入門階段先把它理解成「評估架構品質的六個方向」就夠了。

### 怎麼讀六大支柱

- `Operational Excellence`: 系統是否容易營運、觀察、改動與自動化
- `Security`: 權限、資料保護與風險控管是否清楚
- `Reliability`: 面對故障、流量變化或依賴失效時是否能穩定運作
- `Performance Efficiency`: 資源選型與配置是否符合工作負載
- `Cost Optimization`: 是否避免過度配置與不必要支出
- `Sustainability`: 是否減少浪費，讓資源使用更有效率

## Migration 與 AWS CAF

很多企業接觸 AWS 的第一步不是建新產品，而是遷移既有系統。

### 遷移在做什麼

cloud migration 指的是把組織的資料、應用程式與 workload 搬到雲端。

常見目標包括：

- 降低部分基礎設施成本
- 提升彈性
- 改善擴充能力

### AWS Cloud Adoption Framework

`AWS CAF` 可以理解成雲端採用與遷移的規劃框架。它的價值不是某個單一工具，而是幫團隊用比較系統化的方式設計轉型路徑。

教材裡提到的好處包括：

- 降低風險
- 提升營運效率
- 協助建立更有紀律的遷移策略

## 幾個常見遷移工具

### AWS DMS

`AWS Database Migration Service (DMS)` 用來做資料庫遷移或複寫。

適合理解成：

- 幫助既有資料庫搬遷
- 盡量降低中斷
- 過渡期間仍能維持一定運作

### AWS Snowball

`AWS Snowball` 適合大規模資料搬移。

它的重點是：

- 當資料量很大時，實體設備搬運有時比網路傳輸更實際
- 用於大量資料安全、快速地轉移

## Compute 服務的核心比較

入門階段最重要的不是記所有 compute 產品，而是先理解兩種典型模式：`EC2` 與 `Lambda`。

### EC2

`EC2` 是雲端中的虛擬伺服器。

典型特徵：

- 可自訂 OS、儲存與部署位置
- 控制權高
- 適合需要長時間運行、可客製化的工作負載

常見例子：

- 傳統 web server
- 需要自己管理 runtime 的應用
- 特殊網路或系統設定需求

### Lambda

`Lambda` 是 AWS 的 serverless compute 服務。

典型特徵：

- 事件驅動
- 不需要自己管理伺服器
- 更偏向按觸發執行

常見例子：

- 檔案上傳後的處理
- 資料庫變更後的事件流程
- 輕量 API 或自動化任務

### EC2 vs Lambda

| 面向 | EC2 | Lambda |
| --- | --- | --- |
| 控制權 | 高 | 低到中 |
| 維運責任 | 較多 | 較少 |
| 適合情境 | 長時間運行、需客製化 | 事件驅動、短時任務 |
| 心智模型 | 租一台可調整的伺服器 | 需要時才執行的一段程式 |

簡單說，`EC2` 比較像你自己管理一台車，`Lambda` 比較像叫車服務。

## 共享責任模型

教材摘要提到 Cloud Practitioner 也需要理解 shared responsibility model。最重要的觀念是：

- AWS 負責雲端基礎設施本身的安全
- 客戶負責自己放上去的資料、權限設定、服務配置與應用層安全

也就是說，上了雲不代表安全責任消失，而是責任分界改變了。

## 一個最小 AWS 心智模型

如果你現在只想先抓住最重要的東西，可以記這五點：

1. `Region / AZ / Edge` 是全球基礎設施的三個層次
2. Cloud economics 是從固定成本走向更彈性的變動成本思維
3. Well-Architected Framework 提供六個架構檢查方向
4. Migration 不只是搬主機，還包括治理、流程與資料遷移
5. Compute 入門先分清楚 `EC2` 和 `Lambda`

## Related Concepts

- [Cloud Computing Fundamentals](cloud-computing-fundamentals.md)
- [AWS Security and Cost Management](aws-security-and-cost-management.md)
- [AWS Services Overview](aws-services-overview.md)

[Back to Cloud](README.md)
