# Image Processing with scikit-image

這篇筆記整理的是傳統 image processing workflow，重點不是訓練模型，而是如何直接對影像做增強、修復、邊緣偵測與形狀抽取。

`scikit-image` 很適合拿來學這種流程，因為它把很多常見操作整理成清楚的模組。

## A Useful Mental Model

很多 image processing 任務都能拆成這條鏈：

1. 載入影像
2. 視需要轉成 grayscale
3. 用 filters 改善可見性或壓噪
4. 做 threshold / edge detection
5. 從 binary 或 edge map 抽輪廓、角點或區域

Key point: 傳統 image processing 的核心常常是「先把訊號變乾淨，再把結構抽出來」。

## Grayscale Conversion

很多邊緣、角點或 thresholding 演算法先假設輸入是單通道灰階影像。

```python
from skimage import color

gray = color.rgb2gray(image)
```

不是每個任務都必須轉灰階，但如果你的目標是：

- 邊緣偵測
- 角點偵測
- 全域 thresholding

那灰階通常是很自然的第一步。

## Filtering

image filters 的用途通常是：

- smoothing
- sharpening
- edge detection
- removing noise

### Sobel for Edge Emphasis

```python
from skimage.filters import sobel

edge_sobel = sobel(gray)
```

Sobel 的直覺是量測局部 intensity change。變化大的地方，通常比較像邊界。

### Gaussian Smoothing

```python
from skimage.filters import gaussian

blurred = gaussian(image, channel_axis=-1)
```

Gaussian smoothing 常用來：

- 壓掉高頻噪聲
- 讓後續邊緣或 segmentation 更穩
- 做匿名化或局部模糊

Key point: `sigma` 越大，模糊越強，也越可能把細節一起抹掉。

## Contrast Enhancement

有些影像資訊其實存在，只是對比太弱，看不出來。

### Histogram Equalization

```python
from skimage import exposure

image_eq = exposure.equalize_hist(gray)
```

這會重新分配亮度分布，讓暗亮差異更明顯。

### Adaptive Histogram Equalization

```python
image_adapteq = exposure.equalize_adapthist(gray, clip_limit=0.03)
```

這類方法比全域 equalization 更在意局部對比，因此常用在：

- 光照不均
- 局部細節不明顯
- 醫學或場景影像中局部結構辨識

Warning: 對比增強不只會放大訊號，也可能放大噪聲。

## Inpainting and Restoration

如果影像有刮痕、文字浮水印、logo 或局部缺損，可以先建立 mask，再做 inpainting。

```python
import numpy as np
from skimage.restoration import inpaint

mask = np.zeros(image.shape[:2], dtype=bool)
mask[101:106, 0:240] = True

restored = inpaint.inpaint_biharmonic(
    image,
    mask,
    channel_axis=-1,
)
```

這個流程的關鍵不是 `inpaint_biharmonic` 這個函式名，而是：

1. 先明確標出要修復的區域
2. 再用周邊未受損區域估計內容

## Noise Handling

噪聲處理常見兩種任務：

- 模擬噪聲，測試流程穩定度
- 去噪，提升後續特徵擷取品質

如果只是快速實驗，通常會先：

- 加噪看看演算法是否脆弱
- 用 smoothing 或 median-style filter 壓噪

Tip: 去噪不是越強越好。過度去噪會直接把你想保留的細節一起消掉。

## Thresholding to Binary Images

很多 contour 或 segmentation 流程，都先把灰階圖轉成 binary mask。

```python
from skimage.filters import threshold_otsu

thresh = threshold_otsu(gray)
binary = gray > thresh
```

Otsu 的想法是自動找一個能把前景和背景分開的 threshold。

Key point: thresholding 常是「把連續訊號變成結構假設」的那一步，所以錯了會直接影響後面所有量測。

## Contours

如果你的重點不是每個 pixel 的 label，而是外輪廓形狀，可以從 binary image 找 contours。

```python
from skimage import measure

contours = measure.find_contours(binary, 0.8)
```

這類 contour workflow 很常長這樣：

```python
from skimage import color, measure
from skimage.filters import threshold_otsu

gray = color.rgb2gray(image)
thresh = threshold_otsu(gray)
binary = gray > thresh
contours = measure.find_contours(binary, 0.8)
```

這很適合：

- shape extraction
- object boundary visualization
- downstream geometric reasoning

## Canny Edge Detector

Canny 是經典的 edge detector，通常比單純 gradient-based 邊緣圖更乾淨。

```python
from skimage import color
from skimage.feature import canny

gray = color.rgb2gray(image)
edges = canny(gray, sigma=1.0)
```

`sigma` 影響平滑程度：

- 較小 `sigma`: 保留更多細節，也更敏感
- 較大 `sigma`: 邊緣更平滑，但可能漏掉小結構

## Corner Detection

如果邊緣告訴你「邊界在哪」，角點通常在告訴你「局部幾何變化最劇烈的地方在哪」。

```python
from skimage import color
from skimage.feature import corner_harris

gray = color.rgb2gray(image)
corner_response = corner_harris(gray)
```

角點偵測常用在：

- feature matching
- registration
- tracking
- scene structure understanding

## Classical Detection Pipelines Still Matter

課程後段也碰到 cascade-style detection 與局部模糊，例如：

- 先偵測人臉或目標區域
- 再只對 ROI 做 Gaussian blur

這種 pipeline 提醒一件事：

Key point: 很多實用任務不是「整張圖套同一個變換」，而是「先找區域，再局部處理」。

## Practical Reminders

- 先問你要的是 enhancement、segmentation、geometry，還是 detection。
- 影像前處理常不是可有可無，它會直接決定後續結果是否穩定。
- grayscale、smoothing、thresholding、contours 這條鏈是很值得熟悉的基本功。

[Back to Computer Vision](README.md)
