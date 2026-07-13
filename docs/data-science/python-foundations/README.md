# Python Foundations

這個章節整理資料科學工作最常反覆用到的 Python 基礎。重點不是把語法全部背下來，而是建立一套能安全處理資料、撰寫可重用腳本、並理解 NumPy / pandas 行為的工作底層。

## Sections

- [NumPy](numpy/README.md)
- [pandas](pandas/README.md)

## Standalone Topics

- `argparse.md`
- `api-http.md`
- `assert.md`
- `class.md`
- `config-files.md`
- `control-flow.md`
- `core-data-types.md`
- `database-access-sqlalchemy.md`
- `data-type-transformation.md`
- `dask.md`
- `datetime.md`
- `efficient-python.md`
- `file-io.md`
- `function.md`
- `if-name-main.md`
- `importing-data.md`
- `iterator.md`
- `multiprocessing.md`
- `mongodb.md`
- `polars.md`
- `python-packages.md`
- `python-snippets.md`
- `software-engineering.md`
- `regex.md`
- `string-matching.md`
- `subprocess.md`
- `testing.md`
- `try-except.md`
- `web-scraping.md`

## 建議閱讀方式

- 如果你常卡在 shape、索引或向量化，先補 [NumPy](numpy/README.md)。
- 如果你常卡在資料清理、彙總與欄位操作，先補 [pandas](pandas/README.md)。
- 寫分析腳本時，`argparse`、`if-name-main`、`assert` 與 `try-except` 會直接影響可維護性。
