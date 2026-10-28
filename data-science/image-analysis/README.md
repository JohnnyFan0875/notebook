# Image Analysis

古典影像處理（classical image processing）：不訓練模型，直接對影像做濾波、增強、閾值、形態學、物件量測與 registration。深度學習方法見 [Computer Vision](../deep-learning/computer-vision/README.md)；各成像模態（MRI、CT、PET、超音波）的原理見 [Medical Imaging](../../biology/medical-imaging/README.md)。

## 建議順序

1. [Image Processing with scikit-image](image-processing-with-scikit-image.md)：灰階、濾波、對比增強、去噪、閾值、輪廓、邊緣與角點偵測。
2. [Biomedical Image Analysis in Python](biomedical-image-analysis.md)：讀 2D / 3D 醫學影像與 metadata、spacing、mask、connected components、物件量測、registration 與 resampling。

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [Image Processing with scikit-image](image-processing-with-scikit-image.md) | filtering、contrast、inpainting、thresholding、contours、Canny、corners | 不用模型時，怎麼把影像變乾淨、抽出邊界與形狀？ |
| [Biomedical Image Analysis in Python](biomedical-image-analysis.md) | `imageio` / volume、sampling 與 field of view、morphology、labeling、registration | 醫學影像怎麼從原始 volume 走到可量測的特徵？ |

> 即使後續改用 CNN / U-Net 做 segmentation，spacing、mask、interpolation 這些概念仍然會用到。
