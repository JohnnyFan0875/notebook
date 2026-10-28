[Data Science](../README.md) › Deep Learning

# 深度學習 (Deep Learning)

用多層可微分的函數從原始資料（影像、序列、圖）直接學表示 (representation)。本章以 PyTorch 為主，講模型與訓練；LLM 的應用與系統見 [LLM](../llm/README.md)。

> 深度學習不會讓 [資料洩漏](../machine-learning/foundations/data-leakage.md)、[交叉驗證設計](../machine-learning/workflow/cross-validation.md)、[評估指標](../machine-learning/evaluation/README.md) 的規則失效；參數越多，越容易把切分錯誤記成「好結果」。

## 模組

| 模組 | 核心內容 | 回答的問題 |
| --- | --- | --- |
| [基礎](fundamentals/README.md) | tensor、linear layer、activation、loss、反向傳播與 optimizer、初始化、dropout / normalization | 神經網路由什麼組成？怎麼學？ |
| [訓練流程](training-workflows/README.md) | Dataset / DataLoader、訓練迴圈、scheduler、early stopping、checkpoint、遷移學習、混合精度 | 怎麼把模型穩定、可重現地訓練起來？ |
| [電腦視覺](computer-vision/README.md) | CNN、影像分類、U-Net 分割 | 影像（含顯微、醫學影像）怎麼建模？ |
| [NLP 與 Transformer](nlp-and-transformers/README.md) | tokenize、embedding、RNN / LSTM、attention、Transformer | 序列資料怎麼建模？Transformer 為何主流？ |
| [表示學習](representation-learning/README.md) | Autoencoder、VAE、圖神經網路 (GNN) | 沒有標籤、或資料是圖結構時怎麼學？ |
| [生資應用](bio-applications/README.md) | DNA / 蛋白質序列模型（CNN、ESM、Enformer、AlphaFold）、單細胞 DL（scVI） | 深度學習在生資實際怎麼用？陷阱是什麼？ |

## 建議路線

| 讀者 | 路線 |
| --- | --- |
| 初學 | 基礎（tensor → linear → activation → loss → 反向傳播 → 初始化 → 正則化）→ [訓練迴圈](training-workflows/pytorch-training-loop.md) → [CNN](computer-vision/convolutional-neural-networks.md) → [Transformer](nlp-and-transformers/transformers-and-attention.md) |
| **生物資訊** | [訓練迴圈](training-workflows/pytorch-training-loop.md) → [遷移學習](training-workflows/transfer-learning.md) → [序列與蛋白模型](bio-applications/sequence-and-protein-models.md) → [VAE](representation-learning/autoencoders-and-vae.md) → [單細胞 DL](bio-applications/single-cell-deep-learning.md) → [U-Net](computer-vision/u-net-segmentation.md) / [GNN](representation-learning/graph-neural-networks.md) 依資料型態選 |
| 已會 Keras | [PyTorch ↔ Keras 對照](fundamentals/tensorflow-and-keras-basics.md) → [訓練迴圈](training-workflows/pytorch-training-loop.md) |

## 先備知識

| 主題 | 為什麼 |
| --- | --- |
| [NumPy](../python-foundations/numpy/README.md) | shape、broadcasting、矩陣乘法與 tensor 完全相同 |
| [ML 基礎](../machine-learning/foundations/README.md) | loss、泛化、bias-variance、正則化 |
| [ML 工作流程](../machine-learning/workflow/README.md) | 切分、交叉驗證、調參在 DL 一樣適用 |

## 什麼時候不用深度學習

| 情境 | 較好的起點 |
| --- | --- |
| 表格資料（臨床變數、基因表現矩陣當特徵）、樣本數幾百 | 正則化線性模型、[梯度提升樹](../machine-learning/supervised-learning/ensemble/README.md) |
| 需要係數解釋、信賴區間 | [統計模型](../statistics/README.md) |
| 樣本少但有大型預訓練模型可用 | [遷移學習](training-workflows/transfer-learning.md) / 抽 embedding 再接簡單模型 |
| 影像、序列、圖、大量未標註資料 | 深度學習 |
