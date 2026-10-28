[LLM](../README.md) › [RAG](README.md) › RAG Pipeline

# RAG Pipeline

RAG 不只是「向量搜尋 + LLM」：結果好壞取決於文件怎麼載入與切分、檢索策略、prompt 是否要求只根據來源回答，以及有沒有評估。前置：[Embedding](embeddings-and-semantic-search.md)、[向量資料庫](vector-databases.md)。

## 整體流程

```
離線（建索引）
  文件 → 載入（保留來源 metadata）→ 清理 → 切分 chunk → embedding → 寫入向量庫

線上（回答）
  問題 → [改寫問題] → 檢索 top-k（向量 / hybrid）→ [rerank] → 組 prompt（chunk + 來源標記 + 問題）
       → LLM 生成（附引用；證據不足就拒答）→ [驗證引用] → 回答
```

| RAG 的好處 | 說明 |
| --- | --- |
| 根據文件回答 | SOP、論文、資料庫文件 |
| 降低幻覺 | 答案有來源可查核（但不會降到零） |
| 知識可更新 | 更新文件即可，不必重訓 |
| 權限控制 | 檢索層可依使用者過濾文件 |

## 載入與切分

| 文件類型 | 注意 |
| --- | --- |
| PDF 論文 | 雙欄排版、頁首頁尾、圖表說明、參考文獻都會混入；考慮用 PMC 的 XML 全文或版面感知的解析工具 |
| 表格 | 切碎後失去欄位意義；轉成 Markdown 表格或「每列一句話」 |
| 程式碼 | 依函式 / 類別切分，不要依字元數 |
| HTML / Markdown | 依標題階層切分，保留章節路徑 |

| 切分參數 | 影響 | 起點 |
| --- | --- | --- |
| Chunk 大小 | 太小 → 缺上下文；太大 → 混入無關內容、稀釋相似度 | 300–1000 token |
| Overlap | 避免句子或概念被切斷 | 10–20% |
| 切分邊界 | 依段落 / 標題 > 依句子 > 依固定字元 | `RecursiveCharacterTextSplitter` 依序嘗試段落、句子、字元 |
| 附加脈絡 | 每個 chunk 前加上文件標題與章節名 | 見 [豐富輸入](embeddings-and-semantic-search.md#豐富輸入-enriched-embeddings) |

> Chunking 是檢索設計的一部分，不是前處理細節。切壞了，embedding 再好也找不到對的段落。用評估集比較不同 chunk 大小，不要憑感覺選。

## 檢索策略

| 策略 | 做法 | 解決的問題 |
| --- | --- | --- |
| 向量檢索 | embedding 相似度 top-k | 同義改寫 |
| Hybrid search | BM25 + 向量分數合併（如 Reciprocal Rank Fusion） | 基因符號、ID、專有名詞的精確比對 |
| Metadata 過濾 | 年份、物種、文件類型、權限 | 範圍與權限 |
| Reranking | 先取 top-20～50，再用 cross-encoder 重新排序取 top-5 | 提升前幾名的精準度 |
| 問題改寫 | 用 LLM 把口語問題改寫成檢索用語，或拆成多個子問題 | 問題與文件用語差距大、多面向問題 |
| 父子 chunk | 用小 chunk 檢索，回傳其所屬的大段落 | 兼顧檢索精準與上下文完整 |

```python
# LangChain 範例：載入 → 切分 → 向量庫 → retriever
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

docs = PyPDFLoader("lab_sop.pdf").load()                          # 每頁一個 Document，metadata 含 source、page
chunks = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100).split_documents(docs)
store = Chroma.from_documents(chunks, HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"),
                              persist_directory="sop_index")
retriever = store.as_retriever(search_kwargs={"k": 5})
retriever.invoke("離心機轉速上限是多少？")                        # 回傳 5 個 Document
```

串成完整問答 chain 的寫法見 [LangChain](../integration/langchain-application-orchestration.md#檢索也是一個步驟)。

## Prompt Grounding 與引用

```text
你只能根據 <sources> 中的資料回答。
- 每個陳述後標註來源編號，如 [2]。
- 資料中找不到答案時，回答「提供的文件中沒有這項資訊」，不要用自己的知識補充。
- 不同來源互相矛盾時，列出各自說法與來源。

<sources>
[1] (SOP-離心機.pdf, p.3) ...
[2] (SOP-離心機.pdf, p.4) ...
</sources>

問題：{question}
```

| 要求 | 理由 |
| --- | --- |
| 明確限定只用來源 | 否則模型會混用參數知識，且看不出哪些是編的 |
| 定義找不到時的回答 | 讓「拒答」成為合法輸出 |
| 每個陳述附來源編號 | 使用者可查核；程式可檢查引用的編號是否存在 |
| 來源標記包含檔名、頁碼 / PMID | 可回溯到原文 |
| 問題放在來源之後 | 長 context 時模型較能聚焦於問題 |

> 即使有 RAG，模型仍可能曲解來源或引用錯的段落。高風險用途要驗證引用：被引用的 chunk 是否真的支持該陳述（見 [幻覺偵測](../evaluation-and-hallucination.md#幻覺-hallucination)）。

## 評估 RAG

把錯誤分成**檢索錯**與**生成錯**分別評估，才知道該改哪裡。

| 層面 | 指標 | 怎麼量 |
| --- | --- | --- |
| 檢索 | recall@k（正確段落是否在前 k 筆）、MRR | 需要「問題 → 正確 chunk」標註 |
| 生成：忠實度 (faithfulness) | 答案陳述是否都被檢索到的內容支持 | LLM-as-judge 逐句比對、NLI |
| 生成：答案相關性 | 是否回答了問題 | LLM-as-judge、人工 |
| 拒答 | 文件中沒有答案的題目，是否正確拒答 | 評估集中放入無解題 |
| 端到端 | 答案正確率 | 與標準答案比對 |

| 症狀 | 多半是 | 改善 |
| --- | --- | --- |
| 正確段落不在 top-k | 檢索問題 | 調 chunk、hybrid search、問題改寫、換 embedding 模型 |
| 正確段落有找到但答錯 | 生成問題 | 改 prompt、rerank 讓正確段落排前面、減少雜訊 chunk |
| 文件中沒有答案卻回答了 | grounding 不足 | 加強拒答指令、檢查相似度門檻 |
| 答案引用了錯的來源 | 生成問題 | 驗證引用 |

RAGAS 等框架提供上述指標的自動化實作；但 LLM 評審要先與人工標註校正（見 [評估與幻覺](../evaluation-and-hallucination.md#llm-as-judge)）。

## 向量 RAG 的限制與進階做法

| 限制 | 例子 | 進階做法 |
| --- | --- | --- |
| 多跳推理 | 「與 X 基因有交互作用的蛋白中，哪些是藥物標的？」 | 拆解子問題、agentic RAG（[Agent](../agents/README.md) 反覆檢索） |
| 實體關係 | 跨文件的基因-疾病-藥物網絡 | GraphRAG / 知識圖譜檢索 |
| 全局問題 | 「這 500 篇論文的主要研究趨勢？」 | 先分群摘要再彙整（map-reduce），而非 top-k 檢索 |
| 結構化資料 | 「2023 年後有幾個 RNA-seq 資料集？」 | 轉成 SQL / API 查詢（tool calling），不要用向量檢索 |
| 資訊過時 | 指引改版 | 文件版本 metadata、定期重建索引 |

> 長 context 模型讓「整份文件直接放進 prompt」變得可行。文件少（幾份到幾十份）時，先試直接放入，與 RAG 比較品質與成本；文件多、需要權限控制或來源引用時，RAG 仍然必要。

## 上線前檢查

| 問題 | 對應段落 |
| --- | --- |
| 文件如何載入、切分？是否保留來源 metadata？ | [載入與切分](#載入與切分) |
| 檢索策略是否用評估集比較過？專有名詞是否需要 hybrid？ | [檢索策略](#檢索策略) |
| Prompt 是否要求只用來源、附引用、找不到就拒答？ | [Prompt Grounding](#prompt-grounding-與引用) |
| 是否分別評估檢索與生成？ | [評估 RAG](#評估-rag) |
| 哪些問題類型不適合向量檢索？ | [限制與進階做法](#向量-rag-的限制與進階做法) |
