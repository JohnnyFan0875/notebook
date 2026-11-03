[Computing](../README.md) › [Cloud](README.md) › AWS Cloud Practitioner 考試

# AWS Certified Cloud Practitioner（CLF-C02）

AWS 入門級認證，驗證對 AWS 雲端的整體理解，不考寫程式、架構設計、除錯與實作。本篇只整理考試範圍、題型與準備策略；服務內容見 [AWS 服務總覽](aws-services-overview.md)、[AWS 安全與成本管理](aws-security-and-cost-management.md)，一般雲端概念見 [雲端運算基礎](cloud-computing-fundamentals.md)。

> 考試資訊以 [AWS 官方頁面](https://aws.amazon.com/certification/certified-cloud-practitioner/) 與 [考試指南](https://docs.aws.amazon.com/aws-certification/latest/cloud-practitioner-02/cloud-practitioner-02.html) 為準（2026-11 查核）。

## 考試資訊

| 項目 | 內容 |
| --- | --- |
| 代號 | CLF-C02 |
| 題數 / 時間 | 65 題（50 題計分 + 15 題不計分且不標示）/ 90 分鐘 |
| 題型 | 單選（4 選 1）、複選（5 個以上選項選 2 個以上） |
| 計分 | 量尺分數 100–1000，**700 分及格**；不倒扣，未作答算錯；整體及格即可（各 domain 不必分別及格） |
| 費用 | 100 USD |
| 目標考生 | 最多約 6 個月 AWS 接觸經驗 |

## 考試範圍

| Domain | 比重 | 重點 | 筆記 |
| --- | --- | --- | --- |
| 1. 雲端概念 | 24% | 雲端價值、雲端經濟學（固定 → 變動成本）、Well-Architected Framework、遷移策略與 AWS CAF | [雲端運算基礎](cloud-computing-fundamentals.md)、下方 |
| 2. 安全與合規 | 30% | 共享責任模型、IAM（使用者 / 群組 / 角色 / 政策）、root 保護、MFA、加密、合規工具 | [AWS 安全與成本管理](aws-security-and-cost-management.md) |
| 3. 雲端技術與服務 | 34% | 全球基礎設施、運算、資料庫、儲存、網路、AI/ML、部署與管理工具 | [AWS 服務總覽](aws-services-overview.md) |
| 4. 帳單、定價與支援 | 12% | 定價模式、Budgets、Cost Explorer、Organizations、Support 方案 | [AWS 安全與成本管理](aws-security-and-cost-management.md#成本管理) |

## Well-Architected Framework 六大支柱

| 支柱 | 問的問題 |
| --- | --- |
| 卓越營運 (Operational Excellence) | 系統是否容易營運、觀察、自動化與改進？ |
| 安全 (Security) | 權限、資料保護、偵測與回應是否到位？ |
| 可靠性 (Reliability) | 故障或流量變化時能否穩定運作、自動復原？ |
| 效能效率 (Performance Efficiency) | 資源選型是否符合工作負載？ |
| 成本最佳化 (Cost Optimization) | 是否避免過度配置與不必要支出？ |
| 永續性 (Sustainability) | 是否減少浪費與環境影響？ |

## 遷移

| 主題 | 要點 |
| --- | --- |
| AWS CAF（Cloud Adoption Framework） | 規劃雲端採用與轉型的框架：業務、人員、治理、平台、安全、營運六個面向 |
| 遷移策略（7 Rs） | Retire、Retain、Rehost（lift-and-shift）、Relocate、Repurchase（改用 SaaS）、Replatform、Refactor |
| AWS DMS | 資料庫遷移與複寫，遷移期間來源仍可運作 |
| AWS Snow 系列 | 實體裝置搬運大量資料（TB–PB 級，網路傳太慢時） |
| AWS Application Migration Service | 伺服器 rehost |

## 準備策略

| 做法 | 說明 |
| --- | --- |
| 先建立分類，再記服務名 | 題目多是「某情境該用哪個服務」，用類別（運算 / 儲存 / 資料庫 / 網路）縮小範圍 |
| 熟記容易混淆的組合 | EC2 vs Lambda、S3 vs EBS vs EFS、RDS vs DynamoDB vs Redshift、Security Group vs NACL、CloudWatch vs CloudTrail、Budgets vs Cost Explorer |
| 共享責任模型 | 每年必考；判斷某件事是 AWS 還是客戶的責任 |
| 官方資源 | AWS Skill Builder 的 Cloud Practitioner Essentials 與官方練習題 |
| 動手做 | 用免費方案建一個 S3 bucket、一台 EC2、一個 IAM 使用者，比背誦有效（記得刪除資源、設預算警示） |
