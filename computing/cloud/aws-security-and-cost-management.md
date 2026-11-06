[Computing](../README.md) › [Cloud](README.md) › AWS 安全與成本管理

# AWS 安全與成本管理 (AWS Security and Cost Management)

安全與成本是同一個問題的兩面：權限太鬆增加風險，資源治理太鬆增加浪費。安全的核心是**最小權限 (least privilege)**，成本的核心是**可見性 + 治理**。共享責任模型見 [雲端運算基礎](cloud-computing-fundamentals.md#共享責任模型-shared-responsibility-model)。

## 身分與存取管理 (IAM)

IAM 回答三個問題：誰可以登入或呼叫 API、可以做哪些動作、可以存取哪些資源。

| 元件 | 說明 | 用在 |
| --- | --- | --- |
| Root user | 建立帳號時的帳號，擁有一切權限 | **只**用於少數帳號層級操作（改付款方式、關閉帳號） |
| User | 具名身分，可有密碼與長期 access key | 個人；組織中建議改用 IAM Identity Center 的 SSO |
| Group | 一群 user 共用權限 | 依職責分配權限，人員異動不必逐條調整 |
| Role | 可被「扮演」的身分，給**臨時**憑證 | EC2 / Lambda 存取其他服務、跨帳號、SSO 登入 |
| Policy | JSON 文件，定義允許 / 拒絕哪些動作與資源 | 掛在 user / group / role 上 |

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:GetObject", "s3:ListBucket"],
    "Resource": ["arn:aws:s3:::my-lab-data", "arn:aws:s3:::my-lab-data/*"]
  }]
}
```

> 這個政策只允許讀取一個 bucket，而不是 `s3:*` on `*`。明確的 `Deny` 優先於任何 `Allow`；沒有被允許的預設就是拒絕。

| 守則 | 原因 |
| --- | --- |
| Root 開 MFA、設強密碼、不建立 access key、不日常使用 | 最高權限帳號外洩等於全部失守 |
| 所有人都開 MFA | 密碼本身不可靠 |
| 權限給群組或角色，不直接給個人 | 一致、易稽核 |
| 程式用 role 取得臨時憑證 | 不要把 access key 寫進程式碼、notebook、Git |
| 從最小權限開始，需要再加 | 「先開大再說」的權限只會越堆越多 |
| 定期檢視未使用的權限與金鑰 | IAM Access Analyzer、credential report |

## 網路與資料保護

| 層級 | 工具 |
| --- | --- |
| 身分 / API 權限 | IAM |
| 執行個體網路存取 | Security Group（有狀態）、Network ACL（子網、無狀態） |
| 加密 | KMS 管理金鑰；S3 / EBS / RDS 靜態加密；傳輸用 TLS |
| 機密 | Secrets Manager、Systems Manager Parameter Store |
| S3 公開存取 | 帳號層級開啟「封鎖公開存取」(Block Public Access)，避免資料外洩 |
| 偵測與稽核 | CloudTrail（API 紀錄）、GuardDuty（威脅偵測）、Security Hub、AWS Config（設定合規） |
| 網頁應用防護 | AWS WAF、Shield（DDoS） |
| 合規文件 | AWS Artifact（下載 ISO、SOC、HIPAA 等合規報告） |

> 處理可識別的健康或基因資料時，還要符合機構與法規要求（HIPAA、GDPR、個資法），見 [隱私與法規](../../data-science/responsible-ai/privacy-and-regulation.md)。

## 成本管理

成本問題很少是「不知道 AWS 會收費」，而是不知道**誰**在花、花在**哪個服務**、哪些資源**閒置**。第一步是建立可見性。

### 定價模式

| 模式 | 特徵 | 取捨 | 例子 |
| --- | --- | --- | --- |
| 隨用隨付 (pay-as-you-go) | 用多少付多少 | 彈性最高，單價較高 | On-Demand EC2 |
| 承諾換折扣 (save when you commit) | 承諾 1 或 3 年用量 | 便宜，但彈性低 | Savings Plans、Reserved Instances |
| 用量越多越便宜 (pay less by using more) | 階梯定價 | — | S3 儲存、資料傳出 |
| 可中斷資源 | 用剩餘容量 | 大幅折扣，可能被中斷 | Spot：適合可重試的批次分析 |

### 工具

| 工具 | 作用 |
| --- | --- |
| Pricing Calculator | 建立資源前估算費用 |
| Cost Explorer | 依服務、帳號、標籤分析歷史花費與預測 |
| AWS Budgets | 設定預算與警示門檻（**只通知，不會自動停止資源**；可另設 Budget Actions） |
| Cost Allocation Tags | 以標籤（`project`、`owner`）把費用歸到團隊或專案 |
| Cost and Usage Report | 最詳細的帳單明細，可用 Athena 查詢 |
| Organizations 合併帳單 | 多帳號一張帳單，用量合併可享階梯折扣 |
| Trusted Advisor | 檢查閒置或過度配置的資源、安全與服務限制（完整檢查項目需 Business 以上支援方案） |
| Compute Optimizer | EC2 / Lambda 規格建議 |

### 支援方案

| 方案 | 重點 |
| --- | --- |
| Basic | 免費：文件、帳單問題、部分 Trusted Advisor 檢查 |
| Developer | 工作時間的技術支援 |
| Business | 24/7 技術支援、完整 Trusted Advisor |
| Enterprise On-Ramp / Enterprise | 技術客戶經理 (TAM)、最快回應 |

## 新帳號的治理順序

```text
1. Root 開 MFA，不建立 root access key
2. 建立管理者身分（IAM Identity Center 或 IAM user + MFA），日常不用 root
3. 權限透過群組與角色給，預設最小權限
4. 開 S3 Block Public Access、CloudTrail
5. 建立 Budgets 與警示，資源加上標籤
6. 定期看 Cost Explorer 與 Trusted Advisor：閒置的 EC2、未掛載的 EBS、舊快照
```

| 常見誤區 | 說明 |
| --- | --- |
| 用 root 做日常操作 | 最大的安全風險 |
| 權限直接給個人 | 難以管理與稽核 |
| 有 Budgets 就等於控制了成本 | 它只會提醒 |
| 只看總額 | 要依服務、團隊、閒置資源拆開看 |
| 實驗完忘記刪資源 | EC2、NAT Gateway、未掛載的 EBS、彈性 IP 持續計費 |
