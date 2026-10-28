# Biomedical Image Analysis in Python

這份筆記整理的是傳統 biomedical image analysis workflow，不是 CNN 訓練本身，而是影像如何被讀進來、轉成 mask、標記物件、量測結構，最後再做 registration 與 resampling。

## 為什麼 Biomedical Image 和一般照片不太一樣

一般照片常把每個 pixel 當成純視覺資訊，但 biomedical image 通常還帶有空間語意：

- 2D 影像是 pixels
- 3D 影像是 voxels
- 每個元素除了 intensity，還有 physical location

Key point: 在醫學影像裡，`shape` 只告訴你陣列大小，不等於真實世界的尺寸。

## 載入單張切片與 3D volume

課程內容主要用 `imageio` 示範，重點不是特定套件，而是「影像最後會進到 NumPy array」這件事。

```python
import imageio
import numpy as np

im = imageio.imread("body-001.dcm")
type(im)
im.shape
im.dtype
```

多張切片可以自己堆成 volume：

```python
im1 = imageio.imread("chest-000.dcm")
im2 = imageio.imread("chest-001.dcm")
im3 = imageio.imread("chest-002.dcm")

vol = np.stack([im1, im2, im3])
vol.shape
```

或直接把一整個目錄讀成 volume：

```python
vol = imageio.volread("chest-data")
vol.shape
```

## Shape、Sampling、Field of View

對 biomedical image 來說，這三件事要分開想：

- `shape`: 每個軸上有幾個 voxel
- `sampling`: 每個 voxel 代表多少實際距離，例如 mm
- `field of view`: 整張影像沿每個軸覆蓋的實際空間

```python
n0, n1, n2 = vol.shape
d0, d1, d2 = vol.meta["sampling"]

fov = (n0 * d0, n1 * d1, n2 * d2)
```

Warning: 兩個 volume 就算 `shape` 一樣，若 `sampling` 不同，代表的真實空間大小也可能不同。

## Intensity、Histogram、Threshold Mask

灰階或掃描強度常是最早的分割線索。實務上常先看 intensity histogram，再決定 threshold。

```python
import scipy.ndimage as ndi

hist = ndi.histogram(im, min=0, max=255, bins=256)
mask_soft = im > 32
mask_bone = im > 64
band = mask_soft & ~mask_bone
```

如果只是想保留特定組織或區域，可以直接把 mask 套回原圖：

```python
import numpy as np

im_bone = np.where(im > 64, im, 0)
```

Key point: Thresholding 在 biomedical image 很常見，但它其實是假設不同組織在 intensity 上足夠可分。這個假設不一定總是成立。

## 用形態學操作修 mask

原始 threshold mask 常常有洞、鋸齒或斷裂區塊，所以會接 dilation / erosion 這類二值形態學操作。

```python
m = np.where(im > 64, 1, 0)

m_dilated = ndi.binary_dilation(m, iterations=5)
m_eroded = ndi.binary_erosion(m, iterations=5)
```

- dilation: 擴張前景，補小裂縫
- erosion: 收縮前景，去小噪點

這兩步通常不是為了「美化」，而是讓後續的 labeling 和 measurement 更穩定。

## Connected Components、Labels、Object Measurement

Segmentation 之後，常見下一步不是直接丟模型，而是把每個連通區塊標成不同物件。

```python
labels, nlabels = ndi.label(mask)
```

有了 labels 後，就能對某個特定結構做量測，例如左心室：

```python
mask_lv = np.where(labels == 1, 1, 0)
```

### Distance Transform

Distance transform 可以把每個前景 voxel 轉成「距離背景多遠」。

```python
d_vox = ndi.distance_transform_edt(mask_lv)
d_mm = ndi.distance_transform_edt(
    mask_lv,
    sampling=vol.meta["sampling"],
)
```

Key point: 不帶 `sampling` 時，距離單位是 voxel；帶了 `sampling` 才接近真實空間距離。

### Center of Mass

```python
com = ndi.center_of_mass(vol, labels, index=1)
```

這類量測常用來：

- 找結構的大致中心
- 初始化 registration
- 把不同 subject 的 ROI 對齊到類似位置

### 從 voxel 數換成實際體積

如果 segmentation 是 3D 或 time-series volume，體積通常來自：

1. 算出目標 label 的 voxel 數
2. 乘上單一 voxel 的實體體積

```python
d0, d1, d2, d3 = vol_ts.meta["sampling"]
dvoxel = d1 * d2 * d3

ts = np.zeros(vol_ts.shape[0])
for t in range(vol_ts.shape[0]):
    nvoxels = ndi.sum(1, labels[t], index=1)
    ts[t] = nvoxels * dvoxel
```

這種作法很適合把 segmentation 結果轉成可分析的時間序列，例如 cardiac cycle 中每個時間點的 ventricle volume。

## Registration 與 Spatial Transformations

Biomedical image 常來自不同病人、不同時間點、不同掃描姿勢，所以對齊很重要。

Registration 的核心目標是：

- 把影像對到 template 或參考影像
- 降低空間變異
- 讓後續比較和量測更有意義

### Translation

一個簡單起點是先把結構中心移到固定位置：

```python
com = ndi.center_of_mass(im)
d0 = 128 - com[0]
d1 = 128 - com[1]

xfm = ndi.shift(im, shift=[d0, d1])
```

### Rotation

```python
xfm = ndi.rotate(im, angle=25)
xfm_fixed = ndi.rotate(im, angle=25, reshape=False)
```

Key point: `reshape=False` 會保留原本陣列大小，但也可能裁掉旋轉後超出邊界的內容。

### Affine Transform

Affine transform 是 registration 裡很重要的一層，因為它能同時表達平移、縮放、旋轉、剪切等效果。

```python
mat = [
    [0.8, 0.0, -20],
    [0.0, 0.8, -10],
    [0.0, 0.0, 1.0],
]

xfm = ndi.affine_transform(im, mat)
```

## Resampling 與 Interpolation

當你改變解析度、對齊到另一個 grid、或統一不同掃描時，通常就會發生 resampling。

```python
vol_dn = ndi.zoom(vol, zoom=0.5)
```

- downsampling: 降低解析度、減少記憶體與計算量
- upsampling: 提高 array size，但不會憑空增加新資訊

Key point: Resampling 不是單純改 shape，而是在新的空間座標系上重新估計像素值。

這時 interpolation 很重要：

- nearest-neighbor: 常用於 label mask，避免類別值被混成小數
- linear / spline: 常用於連續強度影像

Warning: 不要用平滑 interpolation 去 resample segmentation label，否則類別邊界可能被破壞。

## 一個很實用的心智模型

傳統 biomedical image analysis 常可以拆成這條鏈：

1. 讀影像與 metadata
2. 確認 shape / spacing / field of view
3. 用 intensity 建 mask
4. 用 morphology 修 mask
5. 用 labeling 把結構拆成物件
6. 把物件轉成可量測特徵
7. 視需要做 registration / resampling

這條鏈條很值得先熟，因為即使後面改用深度學習做 segmentation，這些空間與量測概念仍然會一直出現。
