[臨床資訊與標準](../README.md) › [法規資料庫](README.md) › FDA 藥物資料庫

# FDA 藥物資料庫 (FDA Drug Databases)

美國 FDA 公開的藥品核准與伴隨診斷資料。做精準醫療或藥物研究時，用來確認藥物核准時間、適應症、仿單內容，以及該藥是否有指定的伴隨診斷 (companion diagnostic, CDx)。

| 資源 | 內容 | 格式 / 更新 | 何時用 |
| --- | --- | --- | --- |
| [伴隨診斷清單](https://www.fda.gov/medical-devices/in-vitro-diagnostics/list-fda-authorized-companion-diagnostic-devices-in-vitro-and-imaging-tools) | FDA 核准的體外與影像伴隨診斷 | 網頁表格 | 某標靶藥要用哪個檢測選病人 |
| [Drugs@FDA](https://www.accessdata.fda.gov/scripts/cder/daf/) / [Data Files](https://www.fda.gov/drugs/drug-approvals-and-databases/drugsfda-data-files) | 核准的藥品、申請案、審查文件、仿單 | ZIP 內 12 個 tab 分隔表，工作日每天更新 | 核准日期、上市狀態、批量分析 |
| [First Generic Drug Approvals](https://www.fda.gov/drugs/drug-and-biologic-approval-and-ind-activity-reports/first-generic-drug-approvals) | 每年首次核准的學名藥（ANDA） | 年度網頁表格 | 追蹤專利到期後的學名藥上市 |

## 伴隨診斷清單

每列包含：檢測名稱與廠商、適應症與檢體類型、對應藥物（NDA / BLA）、生物標記、核准途徑與日期（PMA、510(k)、De Novo、HDE）。

| 例 | 生物標記 | 藥物類型 |
| --- | --- | --- |
| NGS 腫瘤 panel（組織或液態切片） | *EGFR*、*ALK*、*BRAF*、*KRAS*、*BRCA1/2* 等多基因 | 多種標靶藥 |
| IHC | HER2、PD-L1 | 抗 HER2、免疫檢查點抑制劑 |

> 伴隨診斷是「這個藥必須用這個檢測選病人」的法規指定，和臨床指引（[NCCN](../../genomics/cancer-genomics/nccn.md)）或證據資料庫（[CIViC](../../genetics/databases/variant/civic.md)）的「建議」不同。實驗室自建檢測 (LDT) 即使驗證過，也不在此清單內。

## Drugs@FDA Data Files

| 資料表 | 內容 |
| --- | --- |
| `Applications` | 申請案號（NDA / ANDA / BLA）、申請者 |
| `Products` | 藥名、成分、劑型、劑量 |
| `Submissions` | 每次送件（原始核准、補充申請）與日期 |
| `MarketingStatus` | 處方藥、OTC、已停售 |
| `ApplicationDocs` | 核准信、審查報告、仿單的連結 |
| `TE` | 治療等效代碼（與 Orange Book 相同） |

```python
import pandas as pd

# 下載 drugsatfda.zip 解壓後
apps = pd.read_csv("Applications.txt", sep="\t", encoding="latin-1")
subs = pd.read_csv("Submissions.txt", sep="\t", encoding="latin-1")
first_approval = (subs[subs["SubmissionType"] == "ORIG"]
                  .merge(apps, on="ApplNo"))
```

程式化查詢（藥品標籤、不良事件、召回）可用 [openFDA API](https://open.fda.gov/apis/)。
