[Productivity](../README.md) › [試算表](README.md) › Excel 基礎

# Excel 基礎 (Excel Basics)

Excel 以格子 (grid) 為核心：輸入、整理、檢查中小型表格資料，對非工程背景的人也很友善。本篇是試算表系列的入口：基本結構、Table、常用功能與何時該換工具；函數細節見 [進階函數](advanced-excel-functions.md)。

## 核心名詞

| 名詞 | 意義 |
| --- | --- |
| 活頁簿 (workbook) | 一個 Excel 檔，含一或多張工作表 |
| 工作表 (worksheet) | 由列 (row) 與欄 (column) 組成 |
| 儲存格參照 (cell reference) | 欄字母 + 列號，如 `B3` |
| 範圍 (range) | `A1:C10`（起點到終點）、`B:B`（整欄）、`2:2`（整列） |
| 公式 (formula) | 以 `=` 開頭，結合常數、參照與函數 |
| 絕對 / 相對參照 | `$A$1` 複製時不變；`A1` 隨位置平移；`$A1` / `A$1` 只鎖欄或列 |
| 已命名範圍 (named range) | 幫範圍取名（`Sales`），公式比 `A2:A500` 好讀，範圍位移也不易出錯 |

| 規格 | 上限 |
| --- | --- |
| 單張工作表 | 1,048,576 列 × 16,384 欄（`XFD`） |
| 實際能順暢開啟的大小 | 受記憶體限制，通常遠低於上限 |

| 版本 | 適合 |
| --- | --- |
| Excel 網頁版 (Excel for the web) | 共同編輯、分享、基本操作 |
| 桌面版 (Desktop) | 進階功能：Power Pivot、部分 Power Query 來源、VBA、大型活頁簿 |

## 表格 (Excel Table)

把資料區選起來按 `Ctrl + T` 轉成 Table，是寫公式前最值得做的一步：

| 好處 | 說明 |
| --- | --- |
| 自動延伸 | 新增列時公式、格式、樞紐分析來源自動包含 |
| 結構化參照 (structured reference) | 用欄名寫公式：`=AVERAGE(Students[Test Score])` |
| 內建篩選、排序、合計列 (totals row) | 不用自己畫 |
| 下游工具相容 | Power Query、樞紐分析表、[Python](excel-with-python.md) 都能直接讀 Table |

> 一欄只放一種資訊、一列一筆紀錄、不合併儲存格、不在資料區內留空列。這是之後所有分析、樞紐分析與 Power Query 能順利運作的前提。

## 常用功能

| 想做的事 | 功能 | 備註 |
| --- | --- | --- |
| 暫時只看符合條件的列 | 篩選 (Filter) | 也能依儲存格顏色、字型顏色篩 |
| 依欄位值重新排列 | 排序 (Sort) | 先統一型別，否則數字與文字混排 |
| 已排序資料分組小計 | 小計 (Subtotal) | 正式報表用 [樞紐分析表](excel-data-analysis-workflow.md#1-探索樞紐分析表) 更彈性 |
| 限制輸入內容、下拉選單 | 資料驗證 (Data Validation) | 見 [資料驗證](excel-data-validation.md) |
| 依規則自動上色 | 設定格式化的條件 (Conditional Formatting) | 見 [條件式格式](conditional-formatting.md) |
| 重複的匯入與清理 | Power Query | 見 [Power Query](power-query-in-excel.md) |

## 常用公式

函數依用途整理在 [進階函數](advanced-excel-functions.md)；這裡只列最常用的幾個與一個實用技巧。

| 公式 | 用途 |
| --- | --- |
| `=SUM(B2:B11)`、`=AVERAGE(B:B)`、`=COUNT()`、`=MIN()`、`=MAX()` | 基本聚合 |
| `=AVERAGE(Students[Test Score])` | 對 Table 欄位聚合 |
| `=XLOOKUP(A2, Ref[ID], Ref[Name], "N/A")` | 依 ID 帶回名稱 |
| `=TEXTJOIN(",", TRUE, A1:A100)` | 用逗號串接，略過空白 |
| `=IF(A1<>"", LEN(A1) - LEN(SUBSTITUTE(A1, ",", "")) + 1, "empty")` | 計算一格中以逗號分隔的項目數 |

> 最後一式的原理：去掉逗號前後的字元數差 = 逗號數，項目數 = 逗號數 + 1。

## 何時該換工具

| 訊號 | 往哪裡移 |
| --- | --- |
| 每次更新都重做一樣的清理步驟 | [Power Query](power-query-in-excel.md) |
| 多張表要建立關聯、指標要重用 | [Power Pivot](power-pivot-in-excel.md)、[Power BI](../../data-science/data-communication/bi-tools/README.md) |
| 公式跨很多工作表互相引用、難以追蹤 | 重構，或改用 Python / R |
| 資料量讓活頁簿明顯變慢、需要版本控管 | [pandas](../../data-science/python-foundations/pandas/README.md)、[資料庫](../../data-science/databases/README.md) |
| 要自動產出報表或批次處理很多檔 | [Python 處理 Excel](excel-with-python.md) |

> Excel 會自動把 `1-Mar`、`MARCH1`、`SEPT2` 這類字串轉成日期（基因名稱被改壞是生資圈著名的問題），長數字 ID 也可能被轉成科學記號。匯入 CSV 時用 Power Query 或「資料 → 從文字/CSV」並把欄位型別設為文字。
