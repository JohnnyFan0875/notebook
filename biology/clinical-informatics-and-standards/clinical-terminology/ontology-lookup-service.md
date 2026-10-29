[臨床資訊與標準](../README.md) › [臨床術語](README.md) › Ontology Lookup Service

# Ontology Lookup Service (OLS)

EMBL-EBI 的本體查詢服務，集中收錄生醫研究常用的本體 (ontology)，可用關鍵字找術語 ID、瀏覽上下位關係，也有 REST API。研究資料的註解（表型、疾病、組織、細胞類型）通常用這裡的本體，而不是 SNOMED CT 這類臨床術語。

| 項目 | 內容 |
| --- | --- |
| 網站 | [ebi.ac.uk/ols4](https://www.ebi.ac.uk/ols4/) |
| API | `https://www.ebi.ac.uk/ols4/api/`（搜尋、取得術語、取得父 / 子節點） |
| 授權 | 免費、不需帳號 |
| 替代方案 | [BioPortal](https://bioportal.bioontology.org/)（收錄更多本體，需 API key）、臨床術語用 [UMLS](umls.md) |

## 常見本體

| 本體 | 前綴 | 用於 |
| --- | --- | --- |
| Human Phenotype Ontology | `HP` | 罕病表型，見 [HPO](../../genetics/databases/gene-disease-association/hpo.md) |
| Mondo Disease Ontology | `MONDO` | 疾病（整合 OMIM、Orphanet、DOID 等） |
| Gene Ontology | `GO` | 基因功能、富集分析 |
| Experimental Factor Ontology | `EFO` | GWAS Catalog 的性狀、實驗變因 |
| Uberon / Cell Ontology | `UBERON` / `CL` | 組織與細胞類型（單細胞註解） |
| ChEBI | `CHEBI` | 小分子化合物 |

```bash
# 以名稱搜尋 HPO 術語（回傳 JSON，含 obo_id、label、synonym）
curl "https://www.ebi.ac.uk/ols4/api/search?q=seizure&ontology=hp&rows=5"
```

> 本體會改版、術語會被標為 obsolete 並指向新 ID。資料註解時記錄本體版本，分析前檢查是否有已過時的 ID。
