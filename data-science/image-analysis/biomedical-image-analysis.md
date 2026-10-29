[Data Science](../README.md) › [Image Analysis](README.md) › 生醫影像分析

# 生醫影像分析 (Biomedical Image Analysis)

古典生醫影像流程：讀入影像與 metadata、建立 mask、標記物件、量測結構，最後做 registration 與 resampling。和一般照片最大的不同是空間語意：2D 的 pixel、3D 的 voxel 除了強度，還有實際的物理位置與大小。

> `shape` 只告訴你陣列大小，不等於真實世界的尺寸；尺寸要靠 spacing。

各成像模態量的物理量（HU、MRI 加權、SUV）與假影見 [Biology：醫學影像](../../biology/medical-imaging/README.md)。

```
讀影像與 metadata → 確認 shape / spacing / FOV / 方向 → 用強度建 mask → 形態學修 mask
  → 標記物件 → 轉成可量測特徵（體積、距離、中心）→ 必要時 registration / resampling
```

## 檔案格式與讀取

| 格式 | 用途 | Python |
| --- | --- | --- |
| DICOM（`.dcm`，每張切片一個檔） | 臨床原始格式，含大量 metadata（含個資） | `pydicom`、SimpleITK |
| NIfTI（`.nii` / `.nii.gz`） | 研究用 3D / 4D volume（神經影像、分割標籤） | `nibabel`、SimpleITK |
| NRRD、MHA | 研究與工具間交換 | SimpleITK |
| TIFF / OME-TIFF、OME-Zarr | 顯微鏡 | `tifffile`、`aicsimageio` |

```python
import SimpleITK as sitk

img = sitk.ReadImage("ct.nii.gz")                    # DICOM 資料夾：見下
arr = sitk.GetArrayFromImage(img)                    # NumPy 陣列，軸順序 (z, y, x)
img.GetSize()                                        # (x, y, z)  ← 順序相反！
img.GetSpacing()                                     # (dx, dy, dz)，單位 mm
img.GetOrigin(), img.GetDirection()                  # 物理座標原點與方向

# DICOM 系列 → 3D volume（自動依切片位置排序）
reader = sitk.ImageSeriesReader()
reader.SetFileNames(reader.GetGDCMSeriesFileNames("chest_dicom/"))
vol = reader.Execute()

# NIfTI：nibabel
import nibabel as nib
nii = nib.load("brain.nii.gz")
data = nii.get_fdata()                               # 軸順序 (x, y, z)
nii.header.get_zooms()                               # voxel 大小
nii.affine                                           # voxel 索引 → 世界座標的 4×4 矩陣
```

> SimpleITK 的陣列是 `(z, y, x)`，但 `GetSize()` / `GetSpacing()` 是 `(x, y, z)`；nibabel 的陣列是 `(x, y, z)`。把 spacing 套到陣列軸上之前，先確認順序，這是最常見的錯誤之一。

舊教材常用 `imageio.imread` / `imageio.volread` 並從 `vol.meta["sampling"]` 取 spacing；新版 imageio 中這組 API 移到 `imageio.v2`，醫學影像建議改用 SimpleITK 或 nibabel，它們保留完整的方向與座標資訊。自己用 `np.stack` 疊切片時，要確認切片依 `ImagePositionPatient` 排序，而不是依檔名。

## Shape、Spacing、FOV

| 概念 | 意義 | 例子 |
| --- | --- | --- |
| Shape | 每軸有幾個 voxel | `(120, 512, 512)` |
| Spacing / sampling | 每個 voxel 代表多少實際距離（mm） | `(2.5, 0.7, 0.7)`：切片厚、平面內細 |
| Field of view (FOV) | 每軸覆蓋的實際範圍 = shape × spacing | `(300, 358, 358)` mm |
| 方向 (direction / affine) | 陣列軸與病人座標（左右、前後、上下）的對應 | 決定左右是否翻轉 |

```python
n = np.array(arr.shape)                       # (z, y, x)
d = np.array(img.GetSpacing())[::-1]          # 轉成 (z, y, x)
fov = n * d
```

兩個 volume 的 shape 相同，spacing 不同時代表的真實空間大小也不同；各向異性 (anisotropic) 的 voxel（切片厚度遠大於平面解析度）會讓 3D 形態學與距離計算失真。

## 強度、直方圖與閾值

| 模態 | 強度的意義 | 閾值策略 |
| --- | --- | --- |
| CT | Hounsfield unit (HU)，有物理意義：空氣 −1000、水 0、軟組織約 20–80、骨 > 300 | 固定 HU 範圍就能分出組織 |
| MRI | 任意單位，不同掃描、不同機器間不可比 | 先做強度標準化（z-score、bias field 校正）再閾值 |
| 螢光顯微鏡 | 相對亮度，受曝光與染色影響 | 同批次固定設定；Otsu 等自動閾值 |

```python
import scipy.ndimage as ndi

hist, edges = np.histogram(arr, bins=256)          # 先看直方圖再決定閾值
soft = (arr > -100) & (arr < 300)                  # CT：軟組織範圍（HU）
bone = arr > 300
band = soft & ~bone
bone_only = np.where(bone, arr, 0)                 # 只保留骨頭強度
```

閾值假設不同組織在強度上可以分開；造影劑、部分容積效應 (partial volume)、雜訊都會讓這個假設不成立。

## 形態學 (Morphology)

原始閾值 mask 常有洞、鋸齒、斷裂或小雜點，用二值形態學修正，讓後續標記與量測更穩：

| 操作 | 作用 | 用途 |
| --- | --- | --- |
| Dilation（膨脹） | 擴張前景 | 補小裂縫 |
| Erosion（侵蝕） | 收縮前景 | 去小雜點、分開細連接 |
| Opening = erosion → dilation | 去除比結構元素小的突出與雜點 | 去雜訊 |
| Closing = dilation → erosion | 填補小洞與縫隙 | 平滑邊界 |
| Fill holes | 填滿封閉的內部空洞 | 實心器官 mask |

```python
m = arr > 300
m = ndi.binary_opening(m, iterations=2)
m = ndi.binary_closing(m, iterations=2)
m = ndi.binary_fill_holes(m)
```

`iterations` 是以 voxel 為單位；spacing 各向異性時，同樣的迭代次數在不同軸代表不同的實際距離。

## 標記與量測

```python
labels, n = ndi.label(m)                                # 連通區塊 → 整數標籤
sizes = ndi.sum(m, labels, index=range(1, n + 1))       # 每個區塊的 voxel 數
largest = labels == (np.argmax(sizes) + 1)              # 保留最大區塊（常是目標器官）

# 距離轉換：前景 voxel 到背景的距離；帶 sampling 才是 mm
d_vox = ndi.distance_transform_edt(largest)
d_mm = ndi.distance_transform_edt(largest, sampling=d)  # d 為 (z, y, x) spacing
max_radius_mm = d_mm.max()

com = ndi.center_of_mass(largest)                       # 中心（voxel 座標）

# 體積 = voxel 數 × 單一 voxel 體積
voxel_ml = np.prod(d) / 1000                            # mm³ → mL
volume_ml = largest.sum() * voxel_ml
```

時間序列 volume（例如心動週期的心室）可以對每個時間點計算體積，得到體積曲線：

```python
ts = np.array([(labels_t[t] == 1).sum() * voxel_ml for t in range(labels_t.shape[0])])
ejection_fraction = (ts.max() - ts.min()) / ts.max()    # 舒張末期與收縮末期體積
```

| 量測 | 用途 |
| --- | --- |
| 體積、面積 | 腫瘤大小、器官體積、病灶負擔 |
| 距離轉換 | 最大厚度 / 半徑、到邊界的距離 |
| 中心 | 粗略定位、初始化 registration |
| 強度統計（`ndi.mean(arr, labels, index)`） | 病灶內的平均 HU、SUV（PET） |

## Registration 與空間轉換

不同病人、時間點或掃描姿勢的影像要對齊到同一個參考（template 或基線影像），才能比較。

| 轉換 | 自由度（2D） | 包含 | 用途 |
| --- | --- | --- | --- |
| 平移 (translation) | 2 | 移動 | 粗略對齊中心 |
| 剛體 (rigid) | 3 | 平移 + 旋轉 | 同一病人不同時間（形狀不變） |
| 仿射 (affine) | 6 | + 縮放、剪切 | 不同病人粗對齊 |
| 非線性 (deformable) | 很多 | 局部變形 | 圖譜對齊、呼吸運動校正 |

```python
# scipy.ndimage：簡單轉換（以陣列座標操作）
com = ndi.center_of_mass(im)
centered = ndi.shift(im, shift=[128 - com[0], 128 - com[1]])
rotated = ndi.rotate(im, angle=25, reshape=False)        # reshape=False 保留大小，但可能裁掉邊角
mat = [[0.8, 0, -20], [0, 0.8, -10], [0, 0, 1]]
xfm = ndi.affine_transform(im, mat)                      # 齊次座標矩陣；注意它是「輸出 → 輸入」的映射

# SimpleITK：以物理座標做真正的 registration（最佳化相似度指標）
fixed, moving = sitk.Cast(fixed, sitk.sitkFloat32), sitk.Cast(moving, sitk.sitkFloat32)
init = sitk.CenteredTransformInitializer(fixed, moving, sitk.Euler3DTransform(),
                                         sitk.CenteredTransformInitializerFilter.GEOMETRY)
reg = sitk.ImageRegistrationMethod()
reg.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)   # 不同模態也適用
reg.SetOptimizerAsGradientDescent(learningRate=1.0, numberOfIterations=200)
reg.SetInterpolator(sitk.sitkLinear)
reg.SetInitialTransform(init, inPlace=False)
tx = reg.Execute(fixed, moving)
aligned = sitk.Resample(moving, fixed, tx, sitk.sitkLinear, 0.0)
```

| 相似度指標 | 適合 |
| --- | --- |
| Mean squared error | 同模態、強度可直接比較 |
| Normalized cross-correlation | 同模態、強度有線性差異 |
| Mutual information | 不同模態（CT ↔ MRI、MRI T1 ↔ T2） |

## Resampling 與 Interpolation

改變解析度、對齊到另一個網格、統一不同掃描的 spacing 時都會 resampling：在新的座標網格上重新估計像素值，不只是改 shape。

```python
vol_dn = ndi.zoom(arr, zoom=0.5, order=1)                 # 降採樣：省記憶體與計算
iso = ndi.zoom(arr, zoom=d / 1.0, order=1)                # 重採樣成 1 mm 等向 voxel
mask_iso = ndi.zoom(mask.astype(np.uint8), zoom=d / 1.0, order=0)   # 標籤用最近鄰
```

| 內插 | `order` / SimpleITK | 用於 |
| --- | --- | --- |
| 最近鄰 (nearest neighbor) | `order=0`、`sitkNearestNeighbor` | **分割標籤**、類別 mask |
| 線性 | `order=1`、`sitkLinear` | 連續強度影像 |
| B-spline / cubic | `order=3`、`sitkBSpline` | 平滑的強度影像（可能產生超出原範圍的值） |

> 不要用線性或 spline 內插 resample 分割標籤：類別值會被混成小數（標籤 1 和 3 之間出現 2），邊界被破壞。升採樣只是增加陣列大小，不會憑空增加資訊。

## 常見錯誤

| 錯誤 | 後果 |
| --- | --- |
| 用 voxel 數比較不同掃描的大小 | 忽略 spacing，數字沒有可比性 |
| SimpleITK / nibabel 的軸順序搞混 | spacing 套錯軸，體積與距離錯 |
| 依檔名排序 DICOM 切片 | 切片順序錯亂 |
| MRI 直接用固定閾值 | 不同掃描的強度單位不同 |
| 用線性內插 resample 標籤 | 產生不存在的類別 |
| 分享影像時保留 DICOM header | 洩漏病人姓名、生日、病歷號，見 [匿名化](../responsible-ai/anonymization-in-python.md) |
