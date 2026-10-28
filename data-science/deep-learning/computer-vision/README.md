[Data Science](../../README.md) › [Deep Learning](../README.md) › 電腦視覺

# 電腦視覺 (Computer Vision)

影像怎麼進入模型、CNN 為何有效，以及兩類最常見的任務：分類（整張圖一個標籤）與分割（每個像素一個標籤）。不訓練模型的古典影像處理（濾波、閾值、形態學、registration）見 [影像分析](../../image-analysis/README.md)；各成像模態的原理見 [Medical Imaging](../../../biology/medical-imaging/README.md)。

## 建議順序

CNN 與影像分類 → [遷移學習](../training-workflows/transfer-learning.md) → U-Net 分割

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [卷積神經網路](convolutional-neural-networks.md) | 卷積、pooling、輸出尺寸、經典架構、影像分類流程、1D CNN | 為什麼影像用 CNN？分類模型怎麼建？ |
| [U-Net 影像分割](u-net-segmentation.md) | encoder-decoder、skip connection、Dice loss、細胞 / 器官分割工具 | 怎麼把每個像素分類（細胞、病灶）？ |

## 任務對照

| 任務 | 輸出 | 生醫例子 | 常用模型 / 工具 |
| --- | --- | --- | --- |
| 分類 | 每張圖一個類別 | 病理切片腫瘤 / 正常、X 光有無肺炎 | ResNet、EfficientNet、ViT |
| 物件偵測 | 邊界框 + 類別 | 細胞核、有絲分裂計數 | YOLO、Faster R-CNN |
| 語意分割 | 每像素類別 | 器官、腫瘤區域 | U-Net、nnU-Net |
| 實例分割 | 每個物件各自的遮罩 | 個別細胞（相鄰細胞要分開） | Cellpose、StarDist、Mask R-CNN |
| 全切片影像 (WSI) | 整張 gigapixel 切片一個標籤 | 預後、分子亞型預測 | 切 patch + 多實例學習 (MIL) |
