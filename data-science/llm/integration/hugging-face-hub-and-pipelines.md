[LLM](../README.md) › [整合](README.md) › Hugging Face

# Hugging Face Hub 與 Pipelines

Hugging Face 是開源模型與資料集的集散地，`transformers` 是使用這些模型的標準函式庫。實務上分兩層：`pipeline` 一行完成常見任務；需要自訂前處理、批次或訓練時，才改用 tokenizer + 模型類別。

## Hub 提供什麼

| 功能 | 用途 |
| --- | --- |
| 模型 | 依任務、語言、授權篩選；含生醫模型（BiomedBERT、BioBERT、ESM 等） |
| Model card | 訓練資料、預期用途、限制、評估結果、授權 → **使用前先讀** |
| Datasets | `datasets` 套件直接載入、切分、串流大型資料集 |
| Spaces | 互動 demo |

| 讀 model card 時確認 | 理由 |
| --- | --- |
| 任務類型（分類、NER、生成、embedding） | 任務不符時程式仍能跑，但結果沒有意義 |
| 訓練資料與領域 | 一般網頁訓練的模型在臨床文字上表現常大幅下降 |
| 標籤定義 | 社群模型常輸出 `LABEL_0`、`LABEL_1`，要查清楚對應什麼 |
| 授權 | 部分模型限制商業使用或需同意條款（gated） |
| 大小與硬體需求 | 參數量決定記憶體需求（fp16 約 2 bytes / 參數） |

## Pipeline：依任務呼叫

```python
from transformers import pipeline

# 1. 零樣本分類：執行時才給標籤，不需訓練
clf = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
clf("Single-cell RNA-seq reveals T cell exhaustion in tumors",
    candidate_labels=["immunology", "neuroscience", "plant biology"])   # labels 依分數排序

# 2. 實體辨識：aggregation_strategy 把子詞合併成完整實體
ner = pipeline("token-classification", model="<生醫 NER 模型>", aggregation_strategy="simple")

# 3. 抽取式問答：答案必須是 context 中的一段文字
qa = pipeline("question-answering", model="deepset/roberta-base-squad2")
qa(question="Which gene was knocked out?", context=methods_text)       # {'answer': ..., 'score': ...}

# 4. 摘要、生成
summ = pipeline("summarization", model="facebook/bart-large-cnn")
summ(long_text, max_length=130, min_length=30)

# 通用參數：device=0（GPU）、batch_size=16、truncation=True
```

| 任務名稱 | 輸出 | 適合 |
| --- | --- | --- |
| `text-classification` | 固定標籤 + 分數 | 已有對應標籤的微調模型 |
| `zero-shot-classification` | 自訂標籤排序 | 快速 baseline、標籤會變動 |
| `token-classification` | 實體與位置 | NER |
| `question-answering` | 原文中的片段 | 文件內查找答案（抽取式，不會編造原文以外內容） |
| `summarization` | 生成的摘要 | 抽象式摘要可能遺漏或捏造 |
| `text-generation` | 續寫文字 | 開源 LLM 對話 / 生成 |
| `feature-extraction` | 向量 | embedding（語意搜尋多用 `sentence-transformers`，見 [Embedding](../rag/embeddings-and-semantic-search.md)） |

| 摘要方式 | 優點 | 缺點 |
| --- | --- | --- |
| 抽取式 (extractive) | 保留原文措辭，不會捏造 | 不連貫 |
| 抽象式 (abstractive) | 自然流暢 | 可能遺漏、扭曲或捏造 |

## Tokenizer 與模型類別

需要自訂批次、檢查中間結果、取得 embedding 或訓練時，改用底層類別。

```python
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

name = "microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext"
tok = AutoTokenizer.from_pretrained(name)
model = AutoModelForSequenceClassification.from_pretrained(name, num_labels=2)   # 分類頭隨機初始化 → 需要微調

batch = tok(texts, padding=True, truncation=True, max_length=512, return_tensors="pt")
with torch.no_grad():
    probs = model(**batch).logits.softmax(dim=-1)
```

| Tokenizer 參數 | 作用 | 陷阱 |
| --- | --- | --- |
| `padding=True` | 補到批次中最長序列 | 搭配 `attention_mask`（tokenizer 自動產生） |
| `truncation=True`、`max_length` | 截斷超長輸入 | BERT 類多為 512 token；**被截掉的內容模型完全看不到**，長文件要先切段 |
| `return_tensors="pt"` | 回傳 PyTorch tensor | — |

| 介面 | 適合 | 代價 |
| --- | --- | --- |
| `pipeline` | 原型、標準任務 | 前處理與輸出格式控制少 |
| `AutoTokenizer` + `AutoModelFor*` | 自訂批次、取中間層、訓練 | 程式較多 |
| `Trainer` / `SFTTrainer` | 微調 | 見 [Fine-tuning](fine-tuning.md) |

## Datasets

```python
from datasets import load_dataset

ds = load_dataset("<dataset-id>")                     # DatasetDict：{"train": ..., "test": ...}
ds["train"].features                                  # 欄位與標籤定義
small = ds["train"].shuffle(seed=0).select(range(200))
tokenized = ds.map(lambda b: tok(b["text"], truncation=True), batched=True)
```

用固定的資料集與切分做比較，實驗才可重現；切分時注意同一篇論文 / 同一病人的資料不要跨訓練與測試集（見 [資料洩漏](../../machine-learning/foundations/data-leakage.md)）。

## 何時用 pipeline、何時不用

| 夠用 | 不夠用 |
| --- | --- |
| 常見任務、快速原型 | 自訂前處理、長文件切段後彙整 |
| 只需最終結果 | 需要 logits、embedding、注意力等中間結果 |
| 小量資料 | 大量資料要精細控制批次與 GPU 記憶體 |
| — | 訓練或微調 |
