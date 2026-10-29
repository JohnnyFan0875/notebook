[Biology](../README.md) › 醫學影像

# 醫學影像 (Medical Imaging)

常見成像模態的物理原理、強弱項與臨床角色。做影像分析或醫療 AI 前先知道每種模態「量的是什麼物理量」，才能理解強度值的意義、常見假影與跨模態整合的限制。用 Python 處理影像（DICOM / NIfTI 讀取、spacing、mask、registration）見 [Data Science：影像分析](../../data-science/image-analysis/README.md)。

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [X 光與 CT](x-ray-ct.md) | 投影 vs 斷層、Hounsfield unit、windowing、輻射劑量、顯影劑 | CT 的數值代表什麼？為什麼同一張 CT 要用不同 window 看？ |
| [MRI](mri.md) | T1 / T2 / FLAIR / DWI 加權、顯影劑、安全篩檢 | 這個序列裡什麼是亮的？MRI 強度為什麼不能跨機器直接比較？ |
| [PET](pet.md) | 放射性示蹤劑、FDG、SUV、PET-CT / PET-MRI | SUV 怎麼算？FDG 高攝取一定是腫瘤嗎？ |
| [超音波](ultrasound.md) | 頻率 vs 穿透深度、B-mode、Doppler、假影 | 為什麼超音波看不到肺與骨頭後方？ |

## 模態比較

| 模態 | 量的物理量 | 解析度 | 游離輻射 | 速度 | 強項 | 限制 |
| --- | --- | --- | --- | --- | --- | --- |
| X 光 | X 光衰減（投影） | 高（2D） | 低 | 秒 | 骨折、胸部、初步評估 | 結構重疊、軟組織對比差 |
| CT | X 光衰減（斷層，HU） | 次毫米 | 中–高 | 秒–分 | 急診、出血、肺、骨、癌症分期 | 輻射；軟組織對比不如 MRI |
| MRI | 氫原子核的磁化與弛豫 | 約 1 mm | 無 | 數十分鐘 | 腦、脊髓、肌肉骨骼、軟組織 | 時間長、金屬禁忌、強度無絕對單位 |
| PET | 示蹤劑的分布（功能 / 代謝） | 4–6 mm | 有（示蹤劑） | 數十分鐘 | 癌症分期與療效、腦與心臟功能 | 解析度低，需搭配 CT / MRI 定位 |
| 超音波 | 聲波反射 | 依探頭頻率 | 無 | 即時 | 床邊、腹部、婦產、心臟、血流、穿刺導引 | 依賴操作者；氣體與骨頭阻擋 |

## 影像資料的共同概念

| 概念 | 說明 | 詳見 |
| --- | --- | --- |
| DICOM | 臨床影像的標準格式：像素 + 大量 metadata（病人、設備、spacing、切片位置） | [生醫影像分析：檔案格式](../../data-science/image-analysis/biomedical-image-analysis.md#檔案格式與讀取) |
| NIfTI | 研究常用的 3D / 4D volume 格式（神經影像） | 同上 |
| Voxel spacing | 每個 voxel 的實際尺寸（mm），不同掃描不同；量體積、resample 必須用到 | [Shape、Spacing、FOV](../../data-science/image-analysis/biomedical-image-analysis.md#shapespacingfov) |
| 強度標準化 | CT 有絕對單位（HU）；MRI 沒有，需 z-score / histogram matching | [MRI](mri.md#資料分析時的注意) |
| 去識別化 | DICOM header 與燒進影像的文字都可能含個資 | [匿名化](../../data-science/responsible-ai/anonymization-in-python.md) |
| 深度學習 | 分割（U-Net、nnU-Net）、分類、偵測 | [Computer Vision](../../data-science/deep-learning/computer-vision/README.md) |

相關：[FHIR](../clinical-informatics-and-standards/clinical-terminology/fhir.md)（ImagingStudy 資源）、[腫瘤浸潤淋巴球](../immunology/tumor-infiltrating-lymphocytes.md)（數位病理影像）。
