# Python Foundations

這個章節整理資料科學工作最常反覆用到的 Python 基礎。重點不是把語法全部背下來，而是建立一套能安全處理資料、撰寫可重用腳本、並理解 NumPy / pandas 行為的工作底層。

## 建議閱讀順序

1. [Core Data Types](core-data-types.md): 先把 list、tuple、dict、set 與常見資料容器觀念補穩。
2. [Control Flow](control-flow.md) 與 [Function](function.md): 建立條件判斷、迴圈、函式拆分與參數設計的基本能力。
3. [File I/O](file-io.md)、[Config Files](config-files.md) 與 [argparse](argparse.md): 學會把一次性的 notebook 操作改成可重跑腳本。
4. [NumPy](numpy/README.md): 理解 array、shape、broadcasting 與向量化，這是後面 pandas 與 machine learning 的共同基礎。
5. [pandas](pandas/README.md): 把資料清理、篩選、彙總、重塑與時間欄位處理串成日常工作流。
6. [Testing](testing.md)、[assert](assert.md) 與 [try-except](try-except.md): 補上腳本穩定性與除錯能力。

## 核心模組

- [NumPy](numpy/README.md)
- [pandas](pandas/README.md)

## 主題分組

### 語言與資料結構

- [Core Data Types](core-data-types.md)
- [Control Flow](control-flow.md)
- [Function](function.md)
- [Class](class.md)
- [Iterator](iterator.md)
- [Data Type Transformation](data-type-transformation.md)
- [Datetime](datetime.md)
- [Regex](regex.md)
- [String Matching](string-matching.md)

### 腳本與工程實務

- [argparse](argparse.md)
- [Config Files](config-files.md)
- [File I/O](file-io.md)
- [if-name-main](if-name-main.md)
- [Subprocess](subprocess.md)
- [Testing](testing.md)
- [assert](assert.md)
- [try-except](try-except.md)
- [Software Engineering](software-engineering.md)
- [Efficient Python](efficient-python.md)

### 資料存取與應用工作流

- [Importing Data](importing-data.md)
- [API HTTP](api-http.md)
- [Database Access with SQLAlchemy](database-access-sqlalchemy.md)
- [MongoDB](mongodb.md)
- [Web Scraping](web-scraping.md)
- [Dask](dask.md)
- [Multiprocessing](multiprocessing.md)
- [Polars](polars.md)
- [Python Packages](python-packages.md)
- [Python Snippets](python-snippets.md)

## 閱讀提醒

- 如果你常卡在 shape、索引或向量化，先補 [NumPy](numpy/README.md)。
- 如果你常卡在資料清理、彙總與欄位操作，先補 [pandas](pandas/README.md)。
- 寫分析腳本時，`argparse`、`if-name-main`、`assert` 與 `try-except` 會直接影響可維護性。
- 如果你已經能寫 notebook，但常常無法把流程整理成可重跑程式，優先讀「腳本與工程實務」那一組。
