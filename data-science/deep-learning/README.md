# Deep Learning

這個章節整理深度學習的核心觀念與常見任務，涵蓋入門、影像、文字、transformer、訓練效率與 LLM fine-tuning。內容已從零散的 framework 筆記重整成概念與任務導向的結構，方便用一般 Markdown 連續閱讀。

## 建議學習順序

1. [Fundamentals](fundamentals/README.md): 先理解 tensor、linear layer、activation、loss、backpropagation 與 initialization。
2. [Training Workflows](training-workflows/README.md): 把訓練、checkpoint、遷移學習與效率優化串成完整流程。
3. [Computer Vision](computer-vision/README.md): 以影像分類任務理解 CNN 與資料管線。
4. [NLP and Transformers](nlp-and-transformers/README.md): 從文字表示、序列模型一路到 transformer 與 LLM fine-tuning。

## 先備知識

- [NumPy](../python-foundations/numpy/README.md): 張量 shape、broadcasting 與矩陣運算觀念會大量重用。
- [Machine Learning Foundations](../machine-learning/foundations/README.md): 尤其是 loss、generalization、overfitting 與 regularization。

## 補充說明

- `Fundamentals` 除了觀念本身，也開始補上 TensorFlow/Keras 的基礎工作流，避免整個 deep learning 區只剩 PyTorch 視角。

## 章節設計原則

- 以「觀念」與「任務」分類，而不是以套件名稱分類。
- PyTorch 仍然是主要範例框架，但不再當成最上層目錄。
- 與 `llm/` 章節切分方式為：本章講模型與訓練，`llm/` 講應用與系統。
