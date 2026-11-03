[Productivity](../README.md) › [試算表](README.md) › 用 Python 處理 Excel

# 用 Python 處理 Excel (Excel with Python)

需要批次處理很多活頁簿、每週自動產出同格式的報表、或把分析結果交給習慣 Excel 的人時，用 Python 讀寫 Excel 比手動操作可靠。讀資料進分析的完整說明見 [匯入資料：Excel](../../data-science/python-foundations/importing-data.md#excel)。

## 選套件

| 套件 | 用途 | 何時用 |
| --- | --- | --- |
| `pandas` | 整張表讀寫成 DataFrame | 資料分析、彙總後輸出 |
| `openpyxl` | 逐儲存格讀寫 `.xlsx`：格式、公式、凍結窗格、條件式格式 | 要控制外觀或修改既有活頁簿 |
| `xlsxwriter` | 只寫不讀，格式與圖表功能完整、速度快 | 從零產出漂亮的報表 |
| `reportlab` | 產生 PDF | Excel 範圍轉 PDF（見下方腳本） |
| `xlwings` | 透過本機 Excel 操作（需安裝 Excel） | 需要 Excel 實際計算公式、執行巨集 |

## 讀寫：pandas

```python
import pandas as pd

df = pd.read_excel("qc.xlsx", sheet_name="qc", skiprows=0, usecols="A:C",
                   dtype={"sample_id": str})            # ID 欄指定字串，保留前導零
sheets = pd.read_excel("qc.xlsx", sheet_name=None)      # 全部工作表 → {name: DataFrame}

# 多張表寫進同一個活頁簿
with pd.ExcelWriter("report.xlsx", engine="openpyxl") as w:
    df.to_excel(w, sheet_name="qc", index=False)
    df.groupby("tissue", as_index=False)["reads_M"].mean().to_excel(w, sheet_name="summary", index=False)
```

## 格式與公式：openpyxl

```python
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill

wb = load_workbook("report.xlsx")
ws = wb["qc"]
for cell in ws[1]:                       # 標題列粗體
    cell.font = Font(bold=True)
ws.freeze_panes = "A2"                   # 凍結標題列
ws.column_dimensions["A"].width = 14
ws["E1"], ws["E2"] = "total", "=SUM(C2:C4)"   # 寫入公式字串
for (cell,) in ws.iter_rows(min_row=2, min_col=3, max_col=3):
    if cell.value < 30:                  # reads 不足標紅
        cell.fill = PatternFill("solid", fgColor="FFC7CE")
wb.save("report.xlsx")
```

| 陷阱 | 說明 |
| --- | --- |
| 公式不會被計算 | openpyxl 只寫公式字串；用 `load_workbook(..., data_only=True)` 讀取時拿到的是**上次 Excel 存檔時快取的值**，Python 寫入、從未在 Excel 開過的檔案會讀到 `None` |
| `load_workbook` 再 `save` 會遺失內容 | 圖表、圖片、樞紐分析表、巨集（`.xlsm` 需 `keep_vba=True`）可能不保留；先在副本上測試 |
| 日期 | pandas 讀成 `datetime64`；文字型日期需 `pd.to_datetime` |
| 大檔案 | `load_workbook(read_only=True)` 串流讀取；大量資料改存 CSV / Parquet |
| 基因名稱被 Excel 轉成日期 | 給別人的檔案若會在 Excel 重新開啟編輯，提醒對方不要從 CSV 直接開 |

> Excel 適合交給人看，不適合當分析中間檔；流程內部用 CSV 或 Parquet，只在最後一步輸出 Excel。

## Excel 範圍轉 PDF

[src/excel2pdf.py](src/excel2pdf.py) 把某張工作表（或指定範圍）輸出成有標題底色與格線的 PDF 表格（`openpyxl` 讀值、`reportlab` 排版，跨頁時重複標題列）。腳本開頭有 [inline script metadata](https://docs.astral.sh/uv/guides/scripts/)，用 `uv` 直接執行即可自動安裝依賴：

```bash
uv run src/excel2pdf.py input.xlsx output.pdf --sheet Sheet1 --range B1:I85
uv run src/excel2pdf.py input.xlsx output.pdf          # 使用中的工作表、整張
```

| 限制 | 說明 |
| --- | --- |
| 只輸出值 | 儲存格格式、合併儲存格、條件式格式不會保留；公式取快取值（同上表） |
| 字型 | 預設 Helvetica 不含中文，中文內容需用 `reportlab.pdfbase.ttfonts` 註冊中文字型 |
| 需要和 Excel 外觀一模一樣 | 改用 Excel 的「另存 PDF」，或在 Windows 用 `xlwings` 呼叫 Excel 匯出 |
