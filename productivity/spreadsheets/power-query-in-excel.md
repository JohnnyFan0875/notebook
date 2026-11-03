[Productivity](../README.md) › [試算表](README.md) › Power Query

# Excel 中的 Power Query (Power Query in Excel)

Power Query 是 Excel 內建的輕量 ETL：把「匯入 → 清理 → 轉換 → 載入」記成可重跑的步驟，資料更新後按「全部重新整理」就重做一次。本篇聚焦 **Excel 介面與工作流**；Applied Steps、M 語言、資料重塑與 M vs DAX 的完整說明以 [Power Query（BI 工具）](../../data-science/data-communication/bi-tools/power-query.md) 為主。

## 什麼時候用

| 適合 | 不必用 |
| --- | --- |
| 每週匯入結構相近的報表、清理步驟每次都一樣 | 一次性的小表修正 |
| 來源欄位很多、只需要一部分 | 純人工輸入的表單 |
| 多個檔案 / 工作表要合併 | 分析很簡單、手動成本很低 |
| 想留下別人看得懂、可審查的清理紀錄 | — |

| 層 | 負責 |
| --- | --- |
| Power Query 編輯器 | 匯入、清理、轉換（準備資料） |
| 工作表 | 檢視、公式分析、報表（消費資料） |
| [Power Pivot](power-pivot-in-excel.md) / 資料模型 | 多表關聯、DAX 量值 |

```
原始來源 ──► Power Query（清理、重塑）──► 工作表 Table 或資料模型 ──► 樞紐分析 / 報表
```

## Excel 操作流程

| 步驟 | 位置 | 說明 |
| --- | --- | --- |
| 1. 取得資料 | 資料 → 取得資料 (Get Data) / 從文字/CSV / 從資料表/範圍 | 來源：活頁簿、CSV、資料夾、網頁、資料庫 |
| 2. 轉換 | 開啟 Power Query 編輯器 | 每個操作記成右側「套用的步驟 (Applied Steps)」 |
| 3. 載入 | 常用 → 關閉並載入至… | 載入成 Table、只建立連線、或加入資料模型 |
| 4. 更新 | 資料 → 全部重新整理 | 來源檔更新後重跑全部步驟 |

| 載入選項 | 何時用 |
| --- | --- |
| 表格 (Table) | 結果要直接在工作表看或寫公式 |
| 只建立連線 (Connection only) | 中間查詢，只給其他查詢合併用 |
| 加入資料模型 (Data Model) | 要在 Power Pivot 建關聯、資料量大（不受工作表列數上限） |

## 常用轉換

| 類別 | 操作 |
| --- | --- |
| 清理與型別 | 改欄名、設定資料類型、移除錯誤 / 空白列、取代值、`Trim` / `Clean`、篩選 |
| 欄位 | 選擇 / 移除欄、分割欄（依分隔符號）、合併欄、自訂欄、條件式欄、索引欄 |
| 重塑 | 取消樞紐 (Unpivot, wide → long)、樞紐 (Pivot)、群組依據 (Group By) |
| 合併 | 附加查詢 (Append)、合併查詢 (Merge) |

> 先改欄名與資料類型，後面的分組、合併、聚合都建立在型別正確之上。

### Append vs Merge

| | Append（附加） | Merge（合併） |
| --- | --- | --- |
| 方向 | 縱向堆疊（加列） | 橫向補欄（依 key） |
| 典型 | 12 個月份的同格式報表合成一張 | 交易表補上產品對照表的類別 |
| 前提 | 欄名、欄數、型別一致，否則多出 null 欄 | 兩邊 key 型別一致、key 品質穩定 |
| 對應 | pandas `concat`、SQL `UNION ALL` | pandas `merge`、SQL `JOIN` |

| Join 類型 | 保留 |
| --- | --- |
| 左方外部 (Left Outer) | 主表全部列 + 對上的資料（最常用） |
| 內部 (Inner) | 只保留兩邊都有的 key |
| 左方反向 (Left Anti) | 主表中**對不上**的列，用來找漏配的 key |
| 完整外部 (Full Outer) | 兩邊全部 |

> Merge 前先想清楚主表是誰、哪些列一定要保留、對不上的 key 怎麼處理；merge 後檢查列數是否暴增（key 不唯一造成一對多）。概念與 [pandas 重塑與合併](../../data-science/python-foundations/pandas/reshape-merge.md) 相同。

### 合併資料夾中的所有檔案

資料 → 取得資料 → 從檔案 → 從資料夾 → 合併並轉換。Power Query 以第一個檔案為範例建立轉換函數，套用到資料夾中每個檔案並 append；之後新檔丟進資料夾、重新整理即可。檔名會成為一欄（`Source.Name`），可保留來源。

## 進階功能

| 功能 | 用途 |
| --- | --- |
| 查詢相依性 (Query Dependencies) | 檢視 → 查詢相依性：看查詢之間的上下游 |
| 進階編輯器 (Advanced Editor) | 查看 / 編輯整段 M 程式碼（`let ... in ...`，區分大小寫） |
| 參數 (Parameters) | 把檔案路徑、日期、門檻抽成參數；換環境或換期間時不必複製查詢 |
| 自訂函數 | 把一段查詢轉成函數，套用到多個來源 |

M 語言範例與自訂欄語法見 [Power Query：M 語言與自訂欄](../../data-science/data-communication/bi-tools/power-query.md#m-語言與自訂欄)。

## 實務守則

| 守則 | 原因 |
| --- | --- |
| 保留原始來源，不在來源檔上手動改 | 重新整理時能完整重跑 |
| 步驟取有意義的名稱（右鍵 → 重新命名） | Applied Steps 本身就是文件 |
| 不把分析邏輯全塞進 Power Query | 準備資料歸 Power Query，量值歸 Power Pivot |
| 檔案路徑用參數 | 換電腦或分享時只改一處 |
| 改了前面的步驟，檢查後面的步驟 | 刪欄、改名會讓後續步驟出錯 |

> 同一套 Power Query 也內建在 Power BI。需要排程更新、多人共用時，見 [BI 工具](../../data-science/data-communication/bi-tools/README.md)；要完整寫程式控制時，改用 [pandas](../../data-science/python-foundations/pandas/README.md)。
