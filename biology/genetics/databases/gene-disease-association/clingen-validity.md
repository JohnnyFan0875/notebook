[資料庫](../README.md) › [基因–疾病關聯](README.md) › ClinGen

# ClinGen (Clinical Genome Resource)

NIH 資助的國際計畫，為基因與變異的臨床意義建立有依據的標準：基因–疾病有效性、劑量敏感度、變異判讀規格與可處置性。

| 資源 | 內容 | 連結 |
| --- | --- | --- |
| Gene–Disease Validity | 依遺傳與實驗證據評分，給出關聯強度 | [gene-validity](https://search.clinicalgenome.org/kb/gene-validity) |
| Dosage Sensitivity | 基因 / 區域的單倍劑量不足 (HI) 與三倍劑量敏感 (TS) 評分 | [gene-dosage](https://search.clinicalgenome.org/kb/gene-dosage) |
| Variant Curation Expert Panels (VCEP) | 針對特定基因的 ACMG 調整規格，以及在 ClinVar 的三星分類 | [CSpec](https://cspec.genome.network/)、[ClinVar expert panel 檔案](https://ftp.ncbi.nlm.nih.gov/pub/clinvar/ClinGen/expert_panels/) |
| Clinical Actionability | 成人 / 兒童結果的可處置性評估 | |
| 判讀指引 | SVI 建議（PVS1、PM2、PP3/BP4 校準等） | 見 [ClinGen 指引](../../variant-interpretation/clingen-guidelines.md) |

## 基因–疾病有效性分級

| 分級 | 意義 |
| --- | --- |
| Definitive | 多年、多個獨立研究重複，無矛盾證據 |
| Strong | 多個病人與實驗證據，但尚未長期重複 |
| Moderate | 有一定證據，但不足 |
| Limited | 證據很少；**不應用於臨床報告致病結果** |
| Disputed / Refuted | 有顯著矛盾證據 / 已被推翻 |
| No Known Disease Relationship | 無已知關聯 |

## 劑量敏感度評分

| 分數 | 意義 |
| --- | --- |
| 3 | 充分證據顯示劑量敏感 |
| 2 | 有一些證據 |
| 1 | 證據很少 |
| 0 | 無證據 |
| 30 | 與隱性疾病有關（單一拷貝缺失不致病） |
| 40 | 不太可能劑量敏感 |

HI = 3 的基因，完整缺失可作為 CNV 致病的強證據（見 [DGV：CNV 判讀資源](../population-frequency/dgv.md#cnv-判讀的其他資源)）。
