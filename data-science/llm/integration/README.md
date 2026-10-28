[Data Science](../../README.md) › [LLM](../README.md) › 整合

# LLM 整合 (Integration)

從「在聊天介面試過可行」到「在程式中可靠地運作」：怎麼組 API 請求、拿到可解析的輸出、選模型、用開源模型，以及何時值得微調。

## 建議順序

```
API 模式 → 選模型 → Hugging Face（開源模型）→ LangChain（需要組合多步驟時）→ 多模態 / Fine-tuning（依需要）
```

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [API 模式](llm-api-patterns.md) | messages 與 roles、對話狀態、參數、structured output、tool calling、錯誤與重試、moderation、token 計算 | 怎麼寫出可上線的 LLM 呼叫？ |
| [選擇模型與供應商](choosing-llm-providers-and-model-families.md) | 模型層級、選擇準則、開源 vs 商用、本機部署、多供應商平台 | 這個任務該用哪個模型？ |
| [Hugging Face Hub 與 Pipelines](hugging-face-hub-and-pipelines.md) | model card、`pipeline`、tokenizer 與模型類別、datasets、生醫模型 | 怎麼找與使用開源模型？ |
| [LangChain](langchain-application-orchestration.md) | prompt 模板、LCEL、output parser、retriever | 什麼時候值得用框架組合流程？ |
| [多模態](multimodal.md) | 影像 / 文件 / 語音任務、processor、語音 pipeline、多步驟的 API 流程 | 非文字輸入怎麼處理？ |
| [Fine-tuning](fine-tuning.md) | prompt vs RAG vs 微調、LoRA / QLoRA、訓練流程、評估 | 什麼時候該微調？怎麼做？ |

> 先用最簡單可行的介面：直接 API 呼叫或 `pipeline`。只有在確實需要更多控制或要組合多個元件時，才往下層或往框架走。
