[Data Science](../README.md) › [LLM](README.md) › 生醫領域的 LLM

# 生醫領域的 LLM (LLMs in Biomedicine)

LLM 在生資與醫療研究中最可靠的用途是**處理文字**：文獻篩選、摘要、資訊擷取、寫程式。最危險的用途是把它當知識庫：基因功能、變異致病性、藥物劑量都可能被流暢地編造。原則是**讓 LLM 處理語言，讓資料庫與程式處理事實**。

> 這裡的「語言模型」指處理自然語言的 LLM。直接對 DNA / 蛋白質序列建模的模型（ESM、DNA 語言模型）見 [序列與蛋白模型](../deep-learning/bio-applications/sequence-and-protein-models.md)。

## 用途與可信度

| 用途 | 做法 | 可信度 | 必要的檢查 |
| --- | --- | --- | --- |
| 文獻篩選 (screening) | 依納入 / 排除條件判斷摘要 | 中高；適合做第一輪過濾 | 以人工標註樣本計算 recall；設計成「不確定就保留」 |
| 摘要與改寫 | 摘要論文、改寫給不同讀者 | 中；可能漏掉限制或誇大結論 | 對照原文抽查數字與結論方向 |
| 實體擷取 (NER) | 從文字抽出基因、疾病、藥物、變異 | 中；常見錯在同名異義與縮寫 | 對 [HGNC](../../biology/genetics/databases/gene/hgnc.md)、[HPO](../../biology/genetics/databases/gene-disease-association/hpo.md) 等標準化並驗證 |
| 關係擷取 | 基因-疾病、藥物-不良反應關聯 | 中低；否定句、推測語氣容易誤判 | 要求附原文證據句 |
| 術語標準化 | 自由文字 → 本體 ID（HPO、MONDO、SNOMED CT） | 低（直接生成 ID 常編造）；搭配檢索則高 | 用 [Ontology Lookup Service](../../biology/clinical-informatics-and-standards/clinical-terminology/ontology-lookup-service.md) 查候選，再讓 LLM 從候選中選 |
| 寫分析程式 | pandas / R / Snakemake / 繪圖 | 中高；API 版本與參數常過時 | 執行、測試、檢查版本 |
| 單細胞細胞類型標註 | 給各群的 marker 基因，請模型推測細胞類型 | 中；常見細胞類型尚可，罕見 / 疾病特有狀態不可靠 | 與參考圖譜方法（CellTypist 等）比較、專家確認 |
| 富集結果解讀 | 把 GO / pathway 結果整理成敘述 | 中；容易過度詮釋 | 結論只能根據實際的 [富集分析](../../biology/genomics/workflows/rna-seq/09-annotation-and-functional-enrichment.md) 結果 |
| 變異解讀 | 詢問變異是否致病 | **低**；不能作為臨床依據 | 以 [ClinVar](../../biology/genetics/databases/variant/clinvar.md)、ACMG 準則與專家判讀為準 |
| 臨床決策 | 診斷、治療建議 | **不可直接使用** | 屬受監管用途，見 [EU AI Act](../responsible-ai/understanding-the-eu-ai-act.md) |

## 文獻探勘流程

```
PubMed 查詢（E-utilities / Biopython Entrez）
        ↓  PMID、標題、摘要、MeSH
LLM 篩選（structured output：include / exclude / uncertain + 理由）
        ↓  人工審查 uncertain 與抽樣檢查
全文取得（PMC Open Access）→ 依章節切段
        ↓
LLM 擷取（實體 + 關係 + 證據句）→ JSON
        ↓
程式標準化與驗證（HGNC / MONDO ID、PMID 存在、證據句確實出現在原文）
        ↓
彙整成表格 → 人工審閱
```

```python
from Bio import Entrez
from pydantic import BaseModel

Entrez.email = "you@example.org"                     # NCBI 要求提供 email；大量查詢加 api_key
ids = Entrez.read(Entrez.esearch(db="pubmed", term="ferroptosis AND single-cell RNA-seq", retmax=200))["IdList"]
records = Entrez.read(Entrez.efetch(db="pubmed", id=",".join(ids), retmode="xml"))

class Relation(BaseModel):
    gene: str                     # 原文寫法
    disease: str
    direction: str                # "up" / "down" / "associated" / "none"
    evidence: str                 # 原文中的完整證據句

class Extraction(BaseModel):
    pmid: str
    relations: list[Relation]

# 呼叫 LLM 取得 Extraction（structured output 的寫法見 llm-api-patterns），之後：
def evidence_in_text(rel: Relation, abstract: str) -> bool:
    return rel.evidence.strip() in abstract       # 證據句必須逐字出現在原文，否則視為幻覺
```

| 設計重點 | 理由 |
| --- | --- |
| 輸出保留原文寫法與證據句 | 方便人工查核；可程式驗證證據確實存在 |
| 實體 ID 由資料庫查詢而非 LLM 生成 | LLM 會編造看似合理的 ID |
| 篩選時設 `uncertain` 類別並交人工 | 降低漏篩 |
| 記錄模型版本與 prompt 版本 | 方法學需可重現（systematic review 要能報告方法） |
| 用標註子集估計 precision / recall | 論文中報告自動化步驟的表現（見 [評估與幻覺](evaluation-and-hallucination.md)） |

## 生醫模型 vs 通用模型

| 類型 | 例子 | 適合 |
| --- | --- | --- |
| 生醫 encoder（BERT 類） | BioBERT、PubMedBERT (BiomedBERT)、SciBERT | 有標註資料的 NER、分類；小、快、可在本機跑 |
| 生醫 NLP 工具 | scispaCy（含生醫實體模型與 UMLS 連結） | 傳統 NER pipeline，結果穩定可重現 |
| 生醫領域生成模型 | BioGPT、醫療領域微調的開源模型 | 研究用途；通常不如大型通用模型 |
| 大型通用模型 | 各家前沿模型 | zero-shot 擷取、摘要、程式；搭配 RAG 與工具 |
| 工具增強 | 讓 LLM 呼叫 NCBI、UniProt、Ensembl API | 事實查詢交給資料庫，降低幻覺 |

> 大型通用模型在多數生醫文字任務上常勝過早期的領域專用生成模型；但有大量標註資料、需要高通量或本機執行時，微調過的小型 encoder 仍然是更便宜、更可重現的選擇。選擇前用自己的 [評估集](evaluation-and-hallucination.md) 比較。

## 隱私與合規

| 資料類型 | 風險 | 做法 |
| --- | --- | --- |
| 病歷、臨床紀錄 (PHI) | 違反 HIPAA / GDPR / 個資法 | 只用機構核准、有資料處理協議（如 BAA）的服務，或本機模型；先[去識別化](../responsible-ai/anonymization-in-python.md) |
| 個人基因體資料 | 基因資料本身即可識別個人，去識別化困難 | 不送外部 API；受控存取資料（dbGaP 等）須遵守 Data Use Agreement |
| 未發表資料、專利相關內容 | 外洩、被用於訓練 | 確認服務條款是否保留 / 用於訓練輸入；企業方案通常可關閉 |
| 公開文獻、公開資料庫 | 低 | 仍要遵守全文授權與 API 使用規範 |

詳細法規見 [隱私與法規](../responsible-ai/privacy-and-regulation.md)；醫療 AI 的監管分類見 [EU AI Act](../responsible-ai/understanding-the-eu-ai-act.md)。

## 常見錯誤

| 錯誤 | 後果 | 改正 |
| --- | --- | --- |
| 問 LLM「某基因的功能」並直接寫進報告 | 混入過時或編造的功能描述 | 查 [NCBI Gene](../../biology/genetics/databases/gene/ncbi-gene.md)、[UniProt](../../biology/molecular-biology/molecular-databases/uniprot.md)，LLM 只負責整理 |
| 讓 LLM 產生參考文獻清單 | 不存在的 PMID / DOI | 只引用自己檢索到的文獻，並用程式驗證 |
| 用 LLM 做差異表現或統計判斷 | 沒有實際計算 | 統計交給程式（DESeq2、scipy），LLM 只解釋結果 |
| 基因符號未標準化 | 同名異義、舊名、大小寫（人類大寫、小鼠首字大寫） | 對 HGNC / MGI 標準化 |
| 摘要時漏掉研究限制 | 誇大結論 | prompt 要求列出樣本數、研究設計與限制 |
| 把 LLM 的分類結果當 ground truth 訓練下游模型 | 錯誤被放大 | 至少有人工標註的驗證子集 |
