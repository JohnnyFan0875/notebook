[Data Science](../README.md) › Image Analysis

# 影像分析 (Image Analysis)

古典影像處理 (classical image processing)：不訓練模型，直接對影像做濾波、增強、閾值、形態學、物件量測與 registration。顯微鏡細胞核計數、組織面積量測、醫學影像體積計算，很多時候用這些方法就夠；即使之後改用 CNN / U-Net 做分割，spacing、mask、interpolation、物件量測這些概念仍然會用到。

## 建議順序

```
scikit-image 基本功（灰階、濾波、對比、閾值、分割、量測）→ 生醫影像（3D volume、spacing、mask、體積、registration）
```

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [scikit-image 影像處理](image-processing-with-scikit-image.md) | 影像即陣列、濾波、對比增強、去噪、閾值、細胞核分割（watershed）、regionprops、邊緣與角點 | 不用模型時，怎麼把影像變乾淨、分出物件並量測？ |
| [生醫影像分析](biomedical-image-analysis.md) | DICOM / NIfTI 讀取、shape / spacing / FOV、強度閾值、形態學、標記與量測、registration、resampling | 醫學影像怎麼從原始 volume 走到可量測的特徵？ |

## 與其他章節的關係

| 主題 | 去哪裡 |
| --- | --- |
| 深度學習分割（U-Net、Cellpose、StarDist、nnU-Net） | [U-Net 分割](../deep-learning/computer-vision/u-net-segmentation.md)、[Computer Vision](../deep-learning/computer-vision/README.md) |
| 成像模態原理（MRI、CT、PET、超音波） | [Medical Imaging](../../biology/medical-imaging/README.md) |
| 影像搭配 LLM / 多模態模型 | [Multimodal](../llm/integration/multimodal.md) |
| 臨床影像去識別化（DICOM metadata） | [匿名化](../responsible-ai/anonymization-in-python.md) |

| 工具 | 適合 |
| --- | --- |
| scikit-image、`scipy.ndimage` | Python 古典處理與量測 |
| SimpleITK、nibabel、pydicom | 醫學影像讀寫、spacing / 方向資訊、registration |
| Fiji (ImageJ)、napari | 互動檢視、手動標註、外掛生態 |
| CellProfiler | 不寫程式的批次細胞影像量測流程 |
