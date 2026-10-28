[LLM](../README.md) › [整合](README.md) › Fine-tuning

# 微調 LLM (Fine-Tuning LLMs)

Fine-tuning 用任務資料更新預訓練模型的參數。它最貴、最難回頭，所以通常是最後一個選項：先確認問題不能靠 prompt、RAG 或 tool calling 解決。一般深度學習的遷移學習概念見 [遷移學習](../../deep-learning/training-workflows/transfer-learning.md)。

## Prompt vs RAG vs Fine-tuning

| 症狀 | 先試 | 理由 |
| --- | --- | --- |
| 指令不清、輸出格式不穩 | [Prompt engineering](../prompt-engineering.md)、[structured output](llm-api-patterns.md#structured-output) | 成本最低，改完立即生效 |
| 缺少最新或私有知識 | [RAG](../rag/README.md) | 知識可更新、可追溯來源，不必重訓 |
| 需要精確計算或查資料庫 | [tool calling](llm-api-patterns.md#tool-calling) | 模型負責決策，程式負責精確結果 |
| 大量樣本上行為 / 格式 / 語氣仍不穩；或想把很長的 prompt「內化」以省 token 與延遲 | Fine-tuning | 改的是模型行為分布，不是知識庫 |
| 需要在本機跑小模型，又要接近大模型的表現 | Fine-tuning（用大模型產生的標註訓練小模型 = 蒸餾） | 降低成本、資料不出機構 |
| 有大量標註資料的分類 / NER | 微調 encoder（BiomedBERT 等） | 小、快、穩定，常勝過 zero-shot LLM |

> Fine-tuning 適合「行為不對」，不適合「知識不夠」。缺知識時微調常讓模型更有自信地編造。

| 先不要微調 | 原因 |
| --- | --- |
| 沒有評估集 | 無法證明微調有幫助 |
| 高品質示範資料不到數百筆 | 學到的是雜訊 |
| 問題其實是缺知識或缺工具 | RAG、tool calling 更合適 |
| 基礎模型會頻繁更換 | 每次換模型都要重訓 |

## 方法比較

| 方法 | 訓練什麼 | 記憶體 | 適合 |
| --- | --- | --- | --- |
| Full fine-tuning | 全部參數 | 最高（權重 + 梯度 + optimizer 狀態，約為模型大小的數倍） | 小模型、資料多、需要大幅改變行為 |
| LoRA | 在權重旁加低秩矩陣 $\Delta W = BA$（rank $r \ll d$），只訓練 $A$、$B$ | 低；可訓練參數常 < 1% | 多數情況的預設選擇 |
| QLoRA | base model 以 4-bit 量化載入，再訓練 LoRA adapter | 更低；單張消費級 GPU 可微調數十億參數模型 | GPU 有限 |
| Prefix / prompt tuning | 只學一段連續的 soft prompt 向量 | 最低 | 參數最少；表現通常不如 LoRA |
| 供應商微調 API | 上傳資料，由供應商訓練 | 不需 GPU | 閉源模型；資料要上傳給供應商 |

LoRA adapter 檔很小（MB 級），同一個 base model 可替換多個 adapter，也可合併回原權重以免推論延遲。

## 訓練流程

```
定義任務與輸出格式 → 準備示範資料（chat 格式）→ 切 train / validation / test
→ 跑 baseline（未微調模型 + 最佳 prompt）→ LoRA 訓練 → 在 test 上與 baseline 比較 → 檢查一般能力是否退化
```

```python
from datasets import load_dataset
from peft import LoraConfig
from trl import SFTConfig, SFTTrainer

# 1. 資料：每筆是一段對話（messages 格式），SFTTrainer 會套用模型的 chat template
ds = load_dataset("json", data_files={"train": "train.jsonl", "validation": "val.jsonl"})
# {"messages": [{"role": "system", ...}, {"role": "user", "content": 摘要}, {"role": "assistant", "content": 標準 JSON}]}

# 2. LoRA 設定
peft_config = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05,
                         target_modules="all-linear", task_type="CAUSAL_LM")

# 3. 訓練
trainer = SFTTrainer(
    model=BASE_MODEL_ID,                       # 字串會自動載入模型與 tokenizer
    train_dataset=ds["train"], eval_dataset=ds["validation"],
    peft_config=peft_config,
    args=SFTConfig(output_dir="out", num_train_epochs=2, learning_rate=2e-4,
                   per_device_train_batch_size=4, gradient_accumulation_steps=4,
                   eval_strategy="epoch", logging_steps=10, bf16=True),
)
trainer.train()
trainer.save_model("out/adapter")              # 只存 adapter；tokenizer / chat template 一併保存
```

| 超參數 | 常見範圍 | 說明 |
| --- | --- | --- |
| `r` | 8–64 | adapter 容量；資料少用小值 |
| `lora_alpha` | 常設 `2 * r` | 縮放係數 |
| `target_modules` | attention 投影層，或 `"all-linear"` | 加在越多層，容量越大、記憶體越多 |
| learning rate | 1e-4–2e-4（LoRA）；full FT 小一個數量級 | 太大會破壞原有能力 |
| epochs | 1–3 | 資料少時多 epoch 容易過擬合 |

## 評估

| 任務 | 指標 |
| --- | --- |
| 分類 | accuracy、precision、recall、F1 |
| 擷取 / 結構化輸出 | schema 通過率、欄位層級 F1、exact match |
| 翻譯 | BLEU、chrF |
| 摘要 | ROUGE + 人工或 LLM-as-judge 檢查忠實度 |
| 生成 | perplexity（只反映語言建模，不反映任務品質）+ rubric 評分 |

| 常見風險 | 檢查 |
| --- | --- |
| 只看訓練 loss 下降 | 在獨立 test set 上看任務指標 |
| 過擬合（validation loss 回升） | early stopping、減少 epoch |
| 災難性遺忘 (catastrophic forgetting) | 用一般能力的題目（指令遵循、拒答）檢查退化 |
| 資料偏誤被放大 | 檢查各子群表現（見 [資料偏誤](../../responsible-ai/data-bias-and-representativeness.md)） |
| 測試資料與訓練資料重疊 | 依文件 / 病人切分，避免同一來源跨集合 |
| 比較不公平 | baseline 也要用最好的 prompt，而非裸模型 |

評估方法、樣本數與統計不確定性見 [評估與幻覺](../evaluation-and-hallucination.md)。

> 許多團隊試圖用訓練解決流程問題，但真正的問題是輸入品質差、評估不足或任務定義不清。
