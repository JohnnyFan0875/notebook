# Cloud Computing Fundamentals

Cloud computing 的核心不是把伺服器搬到別人機房，而是把運算、儲存與平台能力變成可按需取得的服務。

## 為什麼會需要 cloud

傳統 on-premise 架構的問題通常是：

- 容量要先買，尖峰來之前就得預估
- 新環境開通慢，跨團隊協作成本高
- 備援、災難復原與全球部署門檻高

cloud 的價值，主要在於把這些固定成本與前置時間，改成較彈性的資源配置與服務化能力。

## Cloud 不只是「遠端主機」

如果只把 cloud 理解成遠端 VM，會低估它真正的差異。比較完整的理解是：

- 資源可按需配置
- 多數能力透過 API 與管理介面操作
- 計費通常跟使用量或配置量綁定
- 網路、儲存、身分管理、監控與資料服務可一起組合

因此 cloud 比較像是一整套可程式化的基礎設施平台。

## Service Models

最常見的三種 service model 是 `IaaS`、`PaaS`、`SaaS`。

| 模式 | 供應商主要負責 | 使用者主要負責 |
| --- | --- | --- |
| IaaS | 底層硬體、虛擬化、基礎網路 | OS、runtime、應用程式、資料 |
| PaaS | 基礎設施加上平台層 | 應用邏輯與資料 |
| SaaS | 幾乎整個應用服務 | 使用設定、資料輸入、流程治理 |

### IaaS

IaaS 適合需要較高控制權的情境，例如：

- 自己管理作業系統
- 自訂網路與安全規則
- 搬遷既有應用到雲端

代價是營運責任仍然不小。

### PaaS

PaaS 適合想把更多精力放在開發與交付，而不是管理底層環境的團隊。

常見特徵：

- 平台幫你處理一部分 runtime 與部署細節
- 開發速度通常較快
- 自由度比 IaaS 低，但維運負擔也較低

### SaaS

SaaS 是最接近「直接使用產品」的模式。

例如：

- 協作工具
- CRM
- 企業郵件
- BI 或文件平台

使用者不需要管底層部署，但換來的是客製化範圍通常較有限。

## Deployment Models

除了 service model，另一個常見維度是 deployment model，也就是資源到底如何被部署與管理。

### Public Cloud

public cloud 指的是由雲端供應商營運、對多個客戶提供服務的環境。

優點通常是：

- 啟動快
- 彈性高
- 服務種類多
- 前期資本支出較低

風險與限制通常是：

- 治理與成本控制需要紀律
- 架構設計若鬆散，資源容易擴張失控

### Private Cloud

private cloud 是為特定租戶或組織提供的專屬雲端環境。

它和傳統 on-premise 不完全一樣，因為 private cloud 仍可能使用虛擬化與按需配置能力，只是資源治理與使用範圍更封閉。

常見考量：

- 對資料與資源有較高直接控制
- 合規與特殊安全需求較容易滿足
- 前期投資與管理成本通常較高

### Hybrid Cloud

hybrid cloud 是把 private 與 public cloud 組合起來。

常見情境：

- 敏感資料留在 private 端
- 對外應用或彈性運算放在 public 端
- 尖峰流量時做 cloud bursting，暫時把需求擴到 public cloud

hybrid 的價值在於折衷，但代價是整體架構、網路與治理會更複雜。

## 怎麼選 service model 與 deployment model

這兩個問題其實都在問同一件事：你想保留多少控制權，又願意承擔多少營運責任？

可以用下面的方式快速判斷：

- 想要最高控制權，通常偏向 `IaaS` 或 private cloud
- 想更快交付應用，通常偏向 `PaaS`
- 想直接使用成熟產品，通常偏向 `SaaS`
- 想要最快啟動與最大彈性，通常偏向 public cloud
- 想兼顧敏感資料與彈性資源，通常考慮 hybrid cloud

## 主要雲端供應商

入門階段最常遇到的三家是 AWS、Azure、GCP。

### AWS

AWS 通常給人的印象是：

- 服務最完整
- 生態成熟
- 文件與社群資源豐富

很多團隊第一次接觸 cloud 時，會先透過 AWS 形成對 region、network、IAM、object storage 與 managed service 的基本觀念。

### Azure

Azure 常出現在企業 IT 與 Microsoft 生態整合情境。

它的優勢通常在：

- 與 Microsoft 產品整合自然
- 企業治理與身分管理情境常見
- 許多既有企業工作負載較容易接軌

### GCP

GCP 常被聯想到資料、分析與 ML 友善度。

常見印象包括：

- 資料平台與分析服務強
- 某些產品設計較偏工程與資料工作流
- 對 data engineering 與 ML 團隊很有吸引力

## Provider 選擇不是只看功能表

很多人在比較雲端平台時，容易只看：

- 哪家服務比較多
- 哪家價格看起來便宜
- 哪家市場聲量比較大

但實務上更重要的通常是：

- 團隊已經熟悉哪個生態
- 公司現有的 IAM、網路與法規要求是什麼
- 主要 workload 是 web app、資料平台，還是 ML
- 需要多少跨區域、跨團隊治理能力

## 常見誤區

- 把 cloud adoption 理解成單純 lift-and-shift
- 以為上了 cloud 就自然會便宜
- 沒有治理機制就大量開資源
- 沒有先定義 workload 特性，就直接選平台或服務

## 一個入門心智模型

理解 cloud 時，可以先分三層看：

1. `service model`
   你是要自己管很多，還是盡量交給平台
2. `deployment model`
   你要 public、private，還是 hybrid
3. `provider choice`
   哪家平台最符合團隊能力、治理需求與主要 workload

這三層想清楚後，再去看各家產品名稱，會比較不容易迷路。

## Related Concepts

- [AWS Certified Cloud Practitioner](aws-certified-cloud-practitioner.md)
- [Containerization and Virtualization](../containers-and-env/containerization-and-virtualization.md)

[Back to Cloud](README.md)
