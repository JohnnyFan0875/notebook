[Productivity](../README.md) › 試算表

# 試算表 (Spreadsheets)

以 Excel 為主的試算表筆記：從基本結構、函數、資料準備與驗證，到分析、Power Query / Power Pivot 與用 Python 自動化。Google Sheets 的概念大致相同。

## 建議順序

```text
基礎 → 函數 → 資料準備 → 資料驗證 / 條件式格式 → 資料分析 → Power Query → Power Pivot
                                                              └─ 自動化：Python
```

## 筆記

| 筆記 | 內容 | 回答的問題 |
| --- | --- | --- |
| [Excel 基礎](excel.md) | 參照、Table、常用功能、何時換工具 | 資料該怎麼擺，Excel 能做什麼？ |
| [Excel 函數](advanced-excel-functions.md) | 查找、條件聚合、資料庫函數、邏輯、文字、日期、`OFFSET` | 這件事該用哪個函數？ |
| [資料準備流程](excel-data-preparation-workflow.md) | 匯入、型別、去重、衍生欄位、旗標、查找、樞紐檢查 | 原始資料怎麼變成可分析的表？ |
| [資料驗證](excel-data-validation.md) | 範圍、清單、長度、自訂公式、錯誤訊息、限制 | 怎麼在輸入時就擋掉錯誤？ |
| [條件式格式](conditional-formatting.md) | 規則類型、自訂公式整列上色、設計原則 | 怎麼讓異常值一眼可見？ |
| [資料分析流程](excel-data-analysis-workflow.md) | 樞紐分析、分群、what-if、ETS 預測 | 怎麼從表格回答商業問題？ |
| [Power Query](power-query-in-excel.md) | 匯入與轉換、append / merge、合併資料夾、參數 | 重複的清理流程怎麼一鍵重跑？ |
| [Power Pivot](power-pivot-in-excel.md) | 資料模型、關聯、star schema、計算欄 vs 量值、DAX | 多張表怎麼一起分析？ |
| [貸款攤還表](loan-amortization.md) | `PMT` / `IPMT` / `PPMT`、攤還表公式、情境分析 | 每期付款中利息和本金各多少？ |
| [用 Python 處理 Excel](excel-with-python.md) | pandas、openpyxl、Excel 轉 PDF 腳本 | 怎麼批次讀寫、自動產出報表？ |

Power Query 與 DAX 在 Power BI 的用法見 [BI 工具](../../data-science/data-communication/bi-tools/README.md)。
