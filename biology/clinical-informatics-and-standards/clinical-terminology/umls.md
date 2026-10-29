[臨床資訊與標準](../README.md) › [臨床術語](README.md) › UMLS

# 統一醫學語言系統 (UMLS)

UMLS (Unified Medical Language System) 是 NLM 把上百套生醫術語（SNOMED CT、ICD、LOINC、RxNorm、MeSH…）整合在一起的系統：不同術語中意義相同的詞被歸到同一個概念 (CUI)。它是跨術語對應與醫療 NLP 的基礎資源。

| 項目 | 內容 |
| --- | --- |
| 維護 | U.S. National Library of Medicine (NLM) |
| 網站 | [nlm.nih.gov/research/umls](https://www.nlm.nih.gov/research/umls/)、[UTS 瀏覽與 API](https://uts.nlm.nih.gov/uts/) |
| 規模 | 2026AA 版約 353 萬個概念、195 套來源術語 |
| 發布 | 每年兩次（`AA` 約 5 月、`AB` 約 11 月） |
| 授權 | 免費，但需申請個人 UMLS 授權與 UTS 帳號；部分來源術語（如 SNOMED CT、CPT）另有使用限制 |

## 三個組成

| 組成 | 內容 | 用途 |
| --- | --- | --- |
| Metathesaurus | 概念 (CUI)、各術語的詞 (AUI)、同義詞、關係 | 跨術語對應 |
| Semantic Network | 約 130 種語意類型 (semantic type) 與其間關係 | 給每個概念分大類（如 *Disease or Syndrome*、*Pharmacologic Substance*） |
| SPECIALIST Lexicon & Lexical Tools | 詞形變化、拼寫變體 | NLP 的詞彙正規化 |

## CUI 如何串起不同術語

| 術語 | 代碼 | 名稱 |
| --- | --- | --- |
| UMLS CUI | `C0011860` | Diabetes Mellitus, Non-Insulin-Dependent |
| SNOMED CT | `44054006` | Diabetes mellitus type 2 |
| ICD-10-CM | `E11` | Type 2 diabetes mellitus |
| MeSH | `D003924` | Diabetes Mellitus, Type 2 |

> 同一個 CUI 底下的代碼「意義相同」是 UMLS 編輯的判斷，粒度不一定完全一致；做正式對應（例如申報、法規）仍應使用各術語官方的 map。

## 常見用途

| 任務 | 做法 |
| --- | --- |
| 跨術語對應 | 代碼 → CUI → 目標術語的代碼（UTS API 或下載 `MRCONSO.RRF`） |
| 臨床文字 NLP | 用 MetaMap、cTAKES、scispaCy 等把自由文字對到 CUI |
| 依語意類型過濾 | `MRSTY.RRF` 取出某類概念（如所有 *Neoplastic Process*） |
| LLM 術語標準化 | 先用 UMLS / OLS 檢索候選概念，再讓模型從候選中選，見 [生醫 LLM](../../../data-science/llm/bio-and-medical-llm.md) |

研究用本體（HPO、MONDO、GO）多不在 UMLS 或版本較舊，改用 [Ontology Lookup Service](ontology-lookup-service.md)。
