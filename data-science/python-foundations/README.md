[Data Science](../README.md) › Python Foundations

# Python 基礎 (Python Foundations)

資料科學工作中反覆用到的 Python：語言本身、把 notebook 變成可重跑的腳本與套件、讀取各種資料，以及 NumPy / pandas 與效能工具。R 的對應內容見 [R Foundations](../r-foundations/README.md)。

## 建議順序

```
核心型別 → 控制流程 → 函式 → 迭代器 → NumPy → pandas → 匯入資料
                                          ↓
              腳本與 CLI → 錯誤處理 → 測試 → 套件與環境 → 效能
```

只寫 notebook 的人，常卡在「無法把流程整理成可重跑的程式」：優先讀第二排。

## 語言與資料結構

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [核心資料型別](core-data-types.md) | list、tuple、dict、set、`collections`、淺複製 | 該用哪個容器？為什麼改了 b 連 a 也變了？ |
| [控制流程](control-flow.md) | if、for、while、truthiness、`match` | 迴圈怎麼寫才不出錯？ |
| [函式](function.md) | 參數、scope、閉包、decorator、`functools` | 如何設計可重用的函式？ |
| [類別](class.md) | class、`dataclass`、繼承、property、特殊方法 | 什麼時候該寫 class？ |
| [迭代器與生成器](iterator.md) | iterator 協定、comprehension、generator、`itertools` | 如何逐筆處理比記憶體大的檔案？ |
| [日期與時間](datetime.md) | `datetime`、`zoneinfo`、pandas `.dt`、resample | 時區與日期欄位怎麼處理才不出錯？ |
| [文字清理與正規表示式](text-cleaning-and-regex.md) | `re`、樣本名稱解析、模糊比對 | 如何擷取、驗證、清理文字欄位？ |

## 腳本與工程實務

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [腳本與 CLI](scripting-and-cli.md) | `__main__`、argparse、設定檔、`pathlib`、logging、subprocess | 如何把 notebook 變成可重跑的腳本？ |
| [錯誤處理與斷言](errors-and-assertions.md) | try / except、raise、自訂例外、assert | 何時該捕捉、何時該丟出錯誤？ |
| [測試](testing.md) | pytest、fixture、parametrize、測 DataFrame | 改程式後怎麼確定沒改壞？ |
| [軟體工程實務](software-engineering.md) | 專案結構、ruff、命名、docstring、可重現性 | 如何讓程式幾個月後還能用？ |
| [Python 套件與環境](python-packages.md) | `pyproject.toml`、uv、lock 檔、build / publish | 如何讓別人（或自己換台電腦）重建同樣環境？ |

## 資料、數值與效能

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [NumPy](numpy/README.md) | array、broadcasting、向量化、線性代數 | shape 與向量化怎麼想？ |
| [pandas](pandas/README.md) | 選取、groupby、reshape、merge、缺值、Parquet / HDF5 | 表格資料怎麼清理與彙總？ |
| [匯入資料](importing-data.md) | CSV、Excel、JSON、Parquet、HDF5、生資格式、格式互轉 | 這個檔案該用什麼讀？讀完要檢查什麼？ |
| [API 與 HTTP](api-http.md) | requests、狀態碼、重試、分頁、認證 | 如何穩定地從 Ensembl / NCBI 抓資料？ |
| [scipy.stats 速查](scipy-stats.md) | `default_rng`、機率分配、檢定、R 對照 | 這個統計方法在 Python 裡怎麼寫？ |
| [scipy.sparse](scipy-sparse.md) | CSR / CSC / COO、`*_array` vs `*_matrix`、保持稀疏的運算 | 大部分是 0 的矩陣怎麼存、怎麼算才不爆記憶體？ |
| [AnnData 與 scanpy](anndata-and-scanpy.md) | `.h5ad` 結構、view、QC → HVG → PCA → Leiden、pseudobulk、Seurat 對照 | 單細胞資料在 Python 裡怎麼組織與分析？ |
| [效能與擴展](performance-and-scaling/README.md) | 量測、向量化、Numba、multiprocessing、Dask、Polars | 程式太慢或資料太大怎麼辦？ |

## 相關章節

| 需求 | 去哪裡 |
| --- | --- |
| 用 Python 連資料庫 | [SQLAlchemy](../databases/python-sqlalchemy.md)、[PyMongo](../databases/mongodb-pymongo.md) |
| 抓網頁 | [Web Scraping](../web-scraping/README.md) |
| 畫圖與探索 | [Data Manipulation and EDA](../data-manipulation-and-eda/README.md) |
| 統計方法的選擇與解讀 | [Statistics](../statistics/README.md) |
| 環境：conda、Docker | [Containers and Environments](../../computing/containers-and-env/README.md) |
