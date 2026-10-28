[Data Science](../README.md) › [資料處理與 EDA](README.md) › 地理空間資料

# 地理空間資料 (Geospatial Data in Python)

地理空間資料 (geospatial data) 和一般表格的差別不只多一個欄位，而是多了「位置」這個結構：除了值是什麼，還要問它在哪裡、和其他幾何物件有什麼空間關係。流行病學的病例分布、環境暴露、醫療資源可近性都會用到。

## 核心概念

| 概念 | 說明 | 常見錯誤 |
| --- | --- | --- |
| 幾何 (geometry) | 點 `Point`（城市、病例）、線 `LineString`（道路、河流）、面 `Polygon`（行政區、湖泊） | 把 geometry 當字串處理 |
| 座標參考系統 (CRS) | 把座標數字對應到地球上的位置；`POINT (2.2945 48.8584)` 沒有 CRS 就無法確定在哪 | 不知道 CRS 就開始畫圖或算距離 |
| 座標順序 | GeoPandas / Shapely / GeoJSON 一律 `(lon, lat)` = `(x, y)`；經度 [-180, 180]、緯度 [-90, 90] | 寫成 `(lat, lon)`，數字看似合法但位置完全跑掉 |
| 地理座標 vs 投影座標 | 地理 (geographic，如 EPSG:4326) 單位是度，適合記錄位置；投影 (projected，如 UTM) 單位是公尺，適合算距離、面積、緩衝區 | 在經緯度上直接算面積或 buffer，結果沒有物理意義 |

## Python 工具

| 套件 | 用途 |
| --- | --- |
| `geopandas` | `GeoDataFrame` = DataFrame + 一個 `geometry` 欄；讀寫檔案、CRS 轉換、空間 join |
| `shapely` | 幾何物件與空間運算（GeoPandas 底層） |
| `pyproj` | CRS 定義與轉換 |
| `folium` / `geopandas.explore()` | 互動地圖 |

## 常見任務

```python
import geopandas as gpd

# 1. 讀檔：Shapefile、GeoJSON、GeoPackage 都用 read_file
cities = gpd.read_file("ne_110m_populated_places.shp")
cities.geometry.iloc[0]              # POINT (lon lat)：Shapely 物件，不是字串
cities.crs                           # EPSG:4326

# 2. 從經緯度欄位建立（注意 x=經度、y=緯度）
pts = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df["lon"], df["lat"]), crs="EPSG:4326")

# 3. CRS：set_crs 是「宣告」原本的 CRS；to_crs 才是「轉換」座標
gdf = gdf.set_crs("EPSG:4326")              # 檔案缺 .prj 時補上
gdf_m = gdf.to_crs(gdf.estimate_utm_crs())  # 轉成當地 UTM（單位公尺）

# 4. 距離、面積、緩衝區：先轉投影座標
gdf_m.area                                  # m²
gdf_m.buffer(5000)                          # 5 km 緩衝區

# 5. 空間關係與空間 join
districts.contains(point)                   # 也有 within / intersects / touches / distance
cases_in = gpd.sjoin(cases, districts, predicate="within")   # 每個病例屬於哪個區
cases_in.groupby("district_name").size()
```

| `set_crs` | `to_crs` |
| --- | --- |
| 不改座標數字，只標註「這些數字是什麼 CRS」 | 重新計算座標數字到另一個 CRS |
| 資料讀進來 `crs` 是 `None` 時用 | 要算距離 / 面積或兩圖層 CRS 不同時用 |

> EPSG:3857 (Web Mercator) 是網路地圖的顯示用投影，距離與面積在高緯度嚴重失真，不要拿來量測；量測用當地 UTM 或等積投影。

## 檔案格式

| 格式 | 特性 |
| --- | --- |
| Shapefile | 其實是一組檔案（`.shp`、`.shx`、`.dbf`、`.prj`…），複製時要一起搬；欄名限 10 字元 |
| GeoJSON | 單一文字檔，規範要求 WGS84 (EPSG:4326) 經緯度 |
| GeoPackage (`.gpkg`) | 單一 SQLite 檔，可放多個圖層；建議的預設格式 |
| GeoParquet | 欄式儲存，大資料量讀寫快（`gdf.to_parquet()`） |
| PostGIS | PostgreSQL 的空間擴充，資料在資料庫時用 |

## 分析流程

```text
read_file → 檢查 geometry 型態與 crs → 必要時 set_crs / to_crs（兩圖層統一 CRS）
         → 空間 join / 關係運算 → 彙總統計 → 繪圖（gdf.plot(column=...)）
```

> 空間資料的觀測彼此不獨立（相鄰區域相似，空間自相關），一般迴歸的標準誤會低估；需要時改用空間統計模型（如 `pysal`）。
