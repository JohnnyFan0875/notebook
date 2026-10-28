[LLM](../README.md) › [整合](README.md) › 多模態

# 多模態模型 (Multimodal Models)

多模態指輸入或輸出不只是文字：影像、掃描文件、語音、影片。兩條實作路線：用 Hugging Face 的開源模型（自己控制 processor 與模型），或用 API 服務把語音轉文字、生成、文字轉語音串成多步驟流程。生醫影像的專門模型（分割、分類）見 [電腦視覺](../../deep-learning/computer-vision/README.md) 與 [影像分析](../../image-analysis/README.md)。

## 先確定任務，再選模型

| 需求 | 任務名稱 | 輸出 |
| --- | --- | --- |
| 整張圖一個標籤 | image classification | 標籤 + 機率 |
| 找出物件與位置 | object detection | 框 + 類別 |
| 逐像素區域 | image segmentation | mask |
| 用文字描述影像 | image-to-text / captioning | 文字 |
| 針對影像回答問題 | visual question answering (VQA) | 答案 |
| 針對掃描文件、表格、圖表回答問題 | document QA | 答案（版面也是證據） |
| 不訓練就用文字標籤分類影像 | zero-shot image classification（CLIP 類） | 標籤排序 |
| 語音轉文字 | automatic speech recognition (ASR) | 逐字稿 |
| 文字轉語音 | text-to-speech (TTS) | 音訊 |

現在的多模態 LLM（可同時讀圖與文字的對話模型）能直接做 captioning、VQA、讀 PDF 與圖表，常是原型的最快路徑；需要大量處理、精確定位或在本機執行時，才換成專門模型。

> 選錯任務類型比選到稍弱的模型更糟：程式能跑，但輸出不是你需要的東西。

## Hugging Face 路線：Processor + Model

多模態模型的 processor 不只做 tokenize：

| Processor 工作 | 為什麼重要 |
| --- | --- |
| 影像縮放、正規化 | 必須與模型訓練時一致 |
| 音訊重新取樣、特徵擷取 | 取樣率不符時常**靜默**產生錯誤結果 |
| 把文字與影像打包成同一個輸入 | VQA、captioning 需要 |
| 解碼輸出 | 把 ID 轉回標籤或文字 |

```python
from transformers import pipeline
from PIL import Image

# 1. 零樣本影像分類（CLIP）
clip = pipeline("zero-shot-image-classification", model="openai/clip-vit-base-patch32")
clip(Image.open("slide.png"), candidate_labels=["H&E stained tissue", "fluorescence microscopy", "western blot"])

# 2. 語音辨識：pipeline 會依模型需求重新取樣（Whisper 為 16 kHz）
asr = pipeline("automatic-speech-recognition", model="openai/whisper-small")
asr("lab_meeting.wav", return_timestamps=True)

# 3. 需要控制前處理時：processor + model
from transformers import AutoProcessor, AutoModelForImageClassification
processor = AutoProcessor.from_pretrained(ckpt)
model = AutoModelForImageClassification.from_pretrained(ckpt)
inputs = processor(images=Image.open("cell.png"), return_tensors="pt")
pred = model(**inputs).logits.argmax(-1).item()
model.config.id2label[pred]
```

| 模態 | 注意 |
| --- | --- |
| 影像 | 一般網路影像訓練的模型不懂病理、顯微影像；生醫影像需領域模型或微調 |
| 文件 | 表格、圖表的版面就是資訊；純 OCR 會丟失結構 |
| 音訊 | 取樣率、聲道數要符合模型；長音訊要切段 |
| 影片 | 常拆成影格（影像模型）+ 音軌（語音模型），再合併分數 |

微調多模態模型時，大部分工作在資料：train / test 切分、與 processor 一致的轉換、標籤欄位對齊（見 [遷移學習](../../deep-learning/training-workflows/transfer-learning.md)）。

## API 路線：多步驟語音流程

使用者感受到的是「語音進、語音出」，中間通常以文字為主：

```
音訊 → ASR 逐字稿 → [語言偵測 / 翻譯] → [清理：修正術語、斷句] → LLM 生成回應 / 摘要
     → moderation → [TTS 轉語音]
```

| 步驟 | 用途 | 注意 |
| --- | --- | --- |
| ASR | 會議、訪談、門診錄音轉文字 | 專有名詞（基因、藥名）常辨識錯；可提供詞彙提示 |
| 翻譯 | 統一成一種工作語言 | 保留原文逐字稿供追溯 |
| 清理 | 修正術語、斷句 | 獨立成一步，方便比對前後差異 |
| 生成 | 摘要、回覆、分類 | 見 [API 模式](llm-api-patterns.md) |
| Moderation | 生成前後都檢查 | 避免把不當文字轉成語音輸出 |
| TTS | 語音回覆、無障礙 | 口語輸出要更短、句子更簡單 |

```python
from openai import OpenAI
client = OpenAI()

with open("interview.m4a", "rb") as f:
    transcript = client.audio.transcriptions.create(model=ASR_MODEL, file=f).text
summary = client.chat.completions.create(
    model=MODEL, messages=[{"role": "user", "content": f"摘要以下訪談的重點：\n\n{transcript}"}]
).choices[0].message.content
```

| 設計取捨 | 多步驟 | 少步驟 |
| --- | --- | --- |
| 可控性、除錯 | 每步可檢查 | 難定位錯誤 |
| 延遲、成本 | 每步都加 | 較低 |

> 保存每一步的中間產物（原始逐字稿、偵測到的語言、翻譯、清理後文字、最終回覆），才能分辨錯誤出在辨識、翻譯還是生成。錄音若含病人或受試者資訊，適用與病歷相同的[隱私規範](../bio-and-medical-llm.md#隱私與合規)。
