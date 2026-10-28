# Fine-Tuning LLMs

Fine-tuning 是用任務資料更新 pretrained model 的參數。它最貴、最難回頭，所以通常是最後一個選項：先確認問題不能靠 prompt、RAG 或 tool use 解決。

## Prompt vs RAG vs Fine-Tuning

| 症狀 | 先試 | 理由 |
| --- | --- | --- |
| 指令不清、輸出格式不穩 | [Prompt engineering](../prompt-engineering.md)、structured output | 成本最低，改完立即生效 |
| 缺少最新或私有知識 | [RAG](../rag/README.md) | 知識可更新、可追溯來源，不必重訓 |
| 需要呼叫計算、資料庫或外部系統 | tool / function calling（見 [LLM API Patterns](llm-api-patterns.md)） | 讓模型負責決策，程式負責精確計算 |
| 行為、語氣、格式在大量樣本上仍不穩，或要把長 prompt「內化」以省 token / 延遲 | fine-tuning | 改的是模型行為分布，不是知識庫 |

Key point: fine-tuning 適合「行為不對」，不適合「知識不夠」。缺知識時 fine-tune 常讓模型更有自信地胡說。

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

## Fine-Tuning Is a Workflow, Not a Single Step

Fine-tuning usually means adapting a pretrained model to a narrower task using labeled or task-specific data.

At a high level, the workflow looks like this:

1. define the target task and label structure
2. load and inspect the dataset
3. tokenize the training and evaluation examples
4. configure training arguments such as epochs, learning rate, batch size, and evaluation schedule
5. train and monitor the model
6. test the fine-tuned model on held-out or realistic examples
7. save the model and tokenizer together for reuse

Tip: If prompt design or retrieval can solve the problem cheaply, try that before committing to training complexity.

## Full Versus Partial Adaptation

Not every model update needs full fine-tuning.

| Adaptation Style | When It Fits | Main Cost |
| --- | --- | --- |
| full fine-tuning | the task is narrow and strong adaptation is required | highest compute and management cost |
| partial or parameter-efficient adaptation | you need targeted improvement with lower overhead | less expressive than full adaptation |
| no fine-tuning | prompting or retrieval already gets acceptable quality | weakest task specialization |

Key point: Fine-tuning is justified when repeated errors come from task mismatch, not just from vague instructions or missing context.

## LoRA and PEFT

Parameter-efficient fine-tuning（PEFT）只訓練少量新增或選定的參數，凍結原本的權重。

| 方法 | 做法 | 特點 |
| --- | --- | --- |
| LoRA | 在 attention / MLP 權重旁加低秩矩陣 $\Delta W = BA$（rank $r \ll d$），只訓練 $A$、$B$ | 可訓練參數常 < 1%；adapter 檔很小，可替換、可合併回原權重 |
| QLoRA | base model 以 4-bit 量化載入，再訓練 LoRA adapter | 單張消費級 GPU 可微調數十億參數模型 |
| Prefix / prompt tuning | 只學一段連續的 soft prompt 向量 | 參數最少，表現通常不如 LoRA |

實務上常用 Hugging Face `peft` + `transformers`（或 `trl` 的 `SFTTrainer`）：

```python
from peft import LoraConfig, get_peft_model

config = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05,
                    target_modules=["q_proj", "v_proj"], task_type="CAUSAL_LM")
model = get_peft_model(base_model, config)
model.print_trainable_parameters()
```

調參重點：`r`（容量，常見 8–64）、`lora_alpha`（縮放，常設 `2 * r`）、`target_modules`（只加在 attention 或也加在 MLP）、learning rate（比 full fine-tuning 高，常見 1e-4–2e-4）。

## Evaluation Depends on the Task

Evaluation should reflect the kind of output you expect.

| Task Type | Typical Evaluation Thinking |
| --- | --- |
| classification | accuracy, precision, recall, and F1 |
| text generation | fluency, relevance, and often perplexity or human review |
| translation | overlap-oriented metrics such as BLEU |
| summarization | overlap-oriented metrics such as ROUGE plus human usefulness checks |
| extraction or exact QA | exact match where wording precision matters |

Warning: A single metric can hide important failure modes. For example, a summary can score well on overlap and still be misleading or incomplete.

## What an Evaluation Library Really Gives You

Evaluation tooling is useful because it standardizes how predictions and references are compared.

Common benefits include:

1. loading ready-made metrics instead of hand-implementing them
2. checking the expected input structure for each metric
3. comparing models on the same test set
4. separating task evaluation from model training code

This helps make experiments more reproducible and less dependent on ad hoc scripts.

## A Healthy Development Loop

For many projects, the best order is:

1. prototype with a standard model interface
2. inspect outputs on realistic examples
3. add structured evaluation
4. fix prompt, data, or preprocessing issues
5. fine-tune only if the remaining gap is persistent and important

Key point: Many teams try to solve workflow problems with model training when the real issue is poor inputs, weak evaluation, or an unclear task definition.

## Related Notes

- Transformer 內部機制：[Transformers and Attention](../../deep-learning/nlp-and-transformers/transformers-and-attention.md)
- 用 Hugging Face 載入模型與 dataset：[Hugging Face Hub and Pipelines](hugging-face-hub-and-pipelines.md)
- 上線後的監控與版本管理：[LLMOps](../llmops.md)

[Back to Integration](README.md)
