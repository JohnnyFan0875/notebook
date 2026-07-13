# Geospatial Data in Python

地理空間資料和一般表格資料最大的差別，不是多了一個欄位，而是多了「位置」這個結構。你不只要問某筆資料是什麼，還要問它在哪裡、和其他幾何物件有什麼空間關係。

## What Makes Data Geospatial

最簡單的說法是：geospatial data 是帶有 location information 的資料。

常見形式包括：

- 一個點的位置，例如城市、事故、商店
- 一條線，例如道路、河流、軌跡
- 一個面，例如行政區、地塊、湖泊

對資料分析來說，這代表你除了欄位值，還要理解 geometry。

## Core Python Stack

Python geospatial 工作流最常見的組合是：

- `GeoPandas`: 類似 pandas，但多了 geometry-aware column
- `Shapely`: 幾何物件與空間關係運算
- `matplotlib` 或其他地圖套件：繪圖

典型起手式：

```python
import geopandas as gpd

cities = gpd.read_file("ne_110m_populated_places.shp")
print(cities.head())
```

`GeoDataFrame` 可以先把它想成：

- 普通 DataFrame
- 再加上一個特殊的 `geometry` 欄位

## Geometry Objects

`geometry` 欄位裡放的不是普通字串，而是 Shapely 幾何物件。

```python
brussels = cities.loc[170, "geometry"]
print(brussels)
# POINT (4.33137074969045 50.83526293533032)
```

常見幾何類型：

- `Point`
- `LineString`
- `Polygon`

這些型別的重要性在於：它們不只是資料格式，也決定你能做哪些空間運算。

## Spatial Relationships

Shapely / GeoPandas 真正好用的地方，是你可以直接問幾何之間的關係。

例如這類問題：

- 一個點是否落在某個 polygon 內
- 兩個區域是否相交
- 某條線是否穿越某個區域
- 兩個點相距多遠

這類運算不像普通 `==` 或 `>`，而是空間 predicate，例如：

- `contains`
- `within`
- `intersects`
- `touches`
- `distance`

## CRS: Coordinate Reference System

CRS 是 geospatial 初學最容易忽略、但代價也最高的概念之一。

CRS 的角色是：把座標值對應到地球上的實際位置。

例如：

```text
POINT (2.2945 48.8584)
```

如果不知道 CRS，這組數字本身其實不夠表達「它到底在哪」。

## Longitude Comes First

在 Python geospatial 生態裡，最常見的習慣是：

- `(lon, lat)`
- 不是 `(lat, lon)`

也就是：

- longitude 範圍通常是 `[-180, 180]`
- latitude 範圍通常是 `[-90, 90]`

這個順序錯掉時，資料看起來還是像合法數字，但地圖位置會完全跑掉。

## Geographic vs Projected Coordinates

很多資料一開始用的是 geographic coordinates，也就是經緯度。

特徵：

- 單位是 degree
- 常見於 GPS、web mapping、GeoJSON

但地圖是 2D，而地球表面不是，所以很多分析工作最後需要 projected CRS。

直覺上可以這樣想：

- geographic CRS: 比較適合記錄位置
- projected CRS: 比較適合做平面距離、面積、緩衝區等分析

如果你直接拿經緯度去算距離或面積，結果常常沒有物理意義。

## Inspecting and Reprojecting CRS

GeoPandas 裡最常見的兩個動作是：

- 查看目前 CRS
- 轉換 CRS

```python
print(gdf.crs)

gdf = gdf.to_crs("EPSG:3857")
```

心智模型上要分清楚：

- `set_crs(...)`: 指定資料本來就是什麼 CRS
- `to_crs(...)`: 真正把座標轉換到另一個 CRS

兩者混用是很常見的錯誤。

## File Formats You Will Meet Often

GeoPandas 常用 `read_file()` 讀取多種地理空間格式：

```python
gdf = gpd.read_file("path/to/file.geojson")
```

常見格式包括：

- ESRI Shapefile
- GeoJSON
- GeoPackage (`.gpkg`)
- PostGIS table

其中一個很容易踩坑的點是：

- shapefile 看起來像一個檔案格式
- 但實際上通常由多個檔案共同組成，例如 `.shp`, `.dbf`, `.shx`, `.prj`

所以搬移或複製 shapefile 時，不能只拿單一 `.shp` 檔。

## Typical Workflow

一個常見的 geospatial 分析節奏是：

1. 用 `read_file()` 載入資料
2. 檢查 `geometry` 與 `crs`
3. 必要時轉成合適投影
4. 做空間關係或 join
5. 再進入統計摘要或視覺化

這裡和一般 pandas 很像，但 geometry / CRS 檢查不能省。

## Common Failure Modes

- 把 `(lat, lon)` 和 `(lon, lat)` 搞反
- 不知道資料的 CRS，就直接開始畫圖或算距離
- 在 geographic CRS 上直接算面積或 buffer
- shapefile 缺少伴隨檔案，導致資料不完整
- 把 geometry 當一般字串看待，忽略它其實是可運算物件

## Takeaway

geospatial analysis 的核心不是先學很多地圖 API，而是先建立三個觀念：

1. geometry 是一級資料型別
2. CRS 決定座標的真實意義
3. 空間分析前，先確認座標順序、投影與資料格式都正確
