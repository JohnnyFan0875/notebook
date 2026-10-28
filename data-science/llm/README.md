[Data Science](../README.md) › LLM

# 大型語言模型應用 (LLM Applications and Systems)

怎麼把 LLM 用成可靠的工具：prompt、API 整合、檢索 (RAG)、agent、評估與上線營運。訓練模型與做出好用的 LLM 應用是兩件事；本章著重後者。Transformer 內部機制見 [Deep Learning](../deep-learning/nlp-and-transformers/transformers-and-attention.md)。

> 多數 LLM 應用的失敗其實是**系統**問題：檢索不到對的段落、工具定義不清、沒有評估集、沒有人工把關，而不是模型本身不夠強。

## 建議順序

```
基礎 → Prompt → API 整合 → RAG → Agent → 評估與幻覺 → LLMOps
                                          └→ 生醫應用（依需要）
```

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [LLM 基礎](llm-foundations.md) | token、embedding、next-token 預測、取樣參數、訓練階段、生成式模型家族、限制 | LLM 實際在做什麼？為什麼會以可預期的方式出錯？ |
| [Prompt Engineering](prompt-engineering.md) | prompt 結構、few-shot、拆解推理、prompt chaining、system prompt、可重用模板 | 怎麼把任務講清楚，讓輸出穩定？ |
| [整合](integration/README.md) | API 模式、structured output、tool calling、選模型、Hugging Face、LangChain、多模態、fine-tuning | 怎麼在程式裡可靠地使用模型？ |
| [RAG](rag/README.md) | embedding、向量資料庫、chunking、hybrid search、reranking、RAG 評估 | 怎麼讓模型根據文件回答，並附來源？ |
| [Agent](agents/README.md) | tool use、LangGraph、多 agent、guardrail、human-in-the-loop | 什麼時候該讓 LLM 自己決定下一步？ |
| [評估與幻覺](evaluation-and-hallucination.md) | 評估集設計、指標、LLM-as-judge、幻覺偵測、樣本數與信賴區間 | 怎麼知道改了 prompt 是真的變好？ |
| [LLMOps](llmops.md) | 版本管理、回歸測試、監控、成本 / 延遲、agent 系統營運 | 上線後怎麼維持品質與成本？ |
| [生醫領域的 LLM](bio-and-medical-llm.md) | 文獻探勘、實體擷取與標準化、細胞類型標註、生醫模型、隱私與限制 | 生資 / 醫療情境能怎麼用？哪裡不能信？ |

## 系統分層

| 層 | 負責 | 主要筆記 |
| --- | --- | --- |
| Prompt | 任務定義、輸出格式、限制 | [Prompt Engineering](prompt-engineering.md) |
| 檢索 / 工具 | 引入外部事實、API、精確計算 | [RAG](rag/README.md)、[API 模式](integration/llm-api-patterns.md) |
| 狀態 | 對話歷史、流程進度、記憶 | [LangGraph](agents/langgraph-agent-workflows.md) |
| 編排 (orchestration) | 下一步由哪個工具 / agent 執行 | [Agent](agents/README.md) |
| Guardrail | 擋掉不安全、低信心、超出範圍的行為 | [API 模式](integration/llm-api-patterns.md#guardrail-與-moderation)、[Responsible AI](../responsible-ai/README.md) |
| 評估 | 品質、可靠度、延遲、成本 | [評估與幻覺](evaluation-and-hallucination.md)、[LLMOps](llmops.md) |

## 建議路線

| 讀者 | 路線 |
| --- | --- |
| 想用 LLM 加速分析工作 | [基礎](llm-foundations.md) → [Prompt](prompt-engineering.md) → [生醫應用](bio-and-medical-llm.md) |
| 要做文獻 / 文件問答系統 | [API 模式](integration/llm-api-patterns.md) → [RAG](rag/README.md) → [評估與幻覺](evaluation-and-hallucination.md) |
| 要做會呼叫工具的自動化流程 | [API 模式](integration/llm-api-patterns.md) → [Agent](agents/README.md) → [LLMOps](llmops.md) |
| 考慮微調模型 | [評估與幻覺](evaluation-and-hallucination.md) → [Fine-tuning](integration/fine-tuning.md)（先確認 prompt / RAG 不夠） |
