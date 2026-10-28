# Python Foundations

這個章節整理資料科學工作最常反覆用到的 Python 基礎。重點不是把語法全部背下來，而是建立一套能安全處理資料、撰寫可重用腳本、並理解 NumPy / pandas 行為的工作底層。

## 建議閱讀順序

1. [Core Data Types](core-data-types.md): 先把 list、tuple、dict、set 與常見資料容器觀念補穩。
2. [Control Flow](control-flow.md) 與 [Function](function.md): 建立條件判斷、迴圈、函式拆分與參數設計的基本能力。
3. [Scripting and CLI](scripting-and-cli.md): entry point、argparse、設定檔、檔案 I/O、subprocess，把一次性的 notebook 操作改成可重跑腳本。
4. [NumPy](numpy/README.md): 理解 array、shape、broadcasting 與向量化，這是後面 pandas 與 machine learning 的共同基礎。
5. [pandas](pandas/README.md): 把資料清理、篩選、彙總、重塑與時間欄位處理串成日常工作流。
6. [Testing](testing.md) 與 [Errors and Assertions](errors-and-assertions.md): 補上腳本穩定性與除錯能力。

## 主題分組

### 語言與資料結構

| 筆記 | 內容 |
| --- | --- |
| [Core Data Types](core-data-types.md) | list、tuple、dict、set |
| [Control Flow](control-flow.md) | 條件、迴圈、comprehension |
| [Function](function.md) | 參數、scope、lambda、decorator |
| [Class](class.md) | OOP 基礎 |
| [Iterator](iterator.md) | iterator、generator |
| [Datetime](datetime.md) | stdlib `datetime` / timezone 與 pandas datetime 欄位 |
| [Text Cleaning and Regex](text-cleaning-and-regex.md) | `re`、字串清理、thefuzz 模糊比對 |

### 腳本與工程實務

| 筆記 | 內容 |
| --- | --- |
| [Scripting and CLI](scripting-and-cli.md) | `if __name__ == "__main__"`、argparse、設定檔、file I/O、subprocess、常用片段 |
| [Errors and Assertions](errors-and-assertions.md) | try-except、raise、assert |
| [Testing](testing.md) | pytest |
| [Software Engineering](software-engineering.md) | 模組化、文件、風格 |
| [Python Packages](python-packages.md) | 本地 package 結構（待改寫成 pyproject + uv） |

### 資料存取與效能

| 筆記 | 內容 |
| --- | --- |
| [Importing Data](importing-data.md) | flat file、JSON、Excel、HDF5、SAS / Stata、pandas reader、格式互轉 |
| [API HTTP](api-http.md) | requests、REST API |
| [Performance and Scaling](performance-and-scaling/README.md) | Efficient Python、multiprocessing / Dask、Polars |

## 閱讀提醒

- 如果你常卡在 shape、索引或向量化，先補 [NumPy](numpy/README.md)。
- 如果你常卡在資料清理、彙總與欄位操作，先補 [pandas](pandas/README.md)。
- 寫分析腳本時，[Scripting and CLI](scripting-and-cli.md) 與 [Errors and Assertions](errors-and-assertions.md) 會直接影響可維護性。
- 如果你已經能寫 notebook，但常常無法把流程整理成可重跑程式，優先讀「腳本與工程實務」那一組。
- 用 Python 連資料庫見 [Databases](../databases/README.md)（[SQLAlchemy](../databases/python-sqlalchemy.md)、[PyMongo](../databases/mongodb-pymongo.md)）；抓網頁見 [Web Scraping](../web-scraping/README.md)。
