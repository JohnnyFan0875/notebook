[資料庫](../README.md) › [基因–疾病關聯](README.md) › HPO

# HPO (Human Phenotype Ontology)

描述人類異常表型的標準化詞彙（本體論），以階層結構組織（`HP:0001250` Seizure → 更專一的子詞），並註解到疾病與基因。它讓臨床表現能被電腦比對，是表型導向分析 (phenotype-driven analysis) 的基礎。

| 項目 | 內容 |
| --- | --- |
| 網站 | [hpo.jax.org](https://hpo.jax.org/) |
| 下載 | `hp.obo` / `hp.json`（詞彙）、`phenotype.hpoa`（疾病–表型註解）、`genes_to_phenotype.txt` |
| 對照 | 疾病 ID 來自 OMIM、Orphanet；與 SNOMED CT、UMLS 有對照 |

## 用途

| 用途 | 工具 |
| --- | --- |
| 記錄病人表型 | 臨床端輸入 HPO 詞彙（PhenoTips、Phenopackets 格式） |
| 依表型排序候選基因 / 變異 | Exomiser、LIRICAL、Phen2Gene |
| 表型相似度找鑑別診斷 | Phenomizer 類工具 |
| 罕病資料交換 | GA4GH Phenopackets |

> 表型越專一、越完整，排序越準；只填「發展遲緩」這類非常廣的詞效果有限。陰性表型（沒有某症狀）也能幫助排除。臨床詞彙標準的其他系統見 [臨床術語](../../../clinical-informatics-and-standards/clinical-terminology/README.md)。
