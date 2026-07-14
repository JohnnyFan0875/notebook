# LLM Fine-Tuning

`Fine-Tuning with Llama 3`、`Working with Llama 3`、`Working with DeepSeek in Python` 這些抽取內容，最值得整合的是一個實務判斷：什麼時候真的該 fine-tune，而不是先用 prompt engineering、RAG 或更小的 adaptation 方法。

## 什麼時候考慮 fine-tuning

- 需要穩定輸出特定格式
- 有明確領域資料，希望模型更貼近任務語氣或知識分布
- prompt 已經很長、很脆弱，仍無法穩定達標

## 先不要急著 fine-tune 的情況

- 問題主要是缺少最新知識，而不是模型行為不對
- 你沒有足夠高品質標註資料
- 其實用 RAG、tool use 或更好的 system prompt 就能解決

## 實務流程

1. 明確定義任務與輸出格式
2. 準備高品質示範資料
3. 決定是 full fine-tuning、LoRA 還是其他 PEFT 方法
4. 保留 validation set 檢查退化與 overfitting
5. 比較 fine-tuned model 與 baseline prompt / RAG 流程

## 常見風險

- 資料品質不足，模型只學到噪音或偏差
- 只看訓練 loss，沒有看真實任務輸出品質
- fine-tune 後犧牲泛化能力，反而讓模型更脆弱

## 和其他章節怎麼切分

- 若重點是模型參數更新與訓練策略，放在這一章。
- 若重點是知識檢索、代理流程或應用系統，回到 [LLM / RAG](../../llm/rag/README.md)。
