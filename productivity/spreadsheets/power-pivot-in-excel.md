[Productivity](../README.md) › [試算表](README.md) › Power Pivot

# Excel 中的 Power Pivot (Power Pivot in Excel)

Power Pivot 是 Excel 的資料模型 (Data Model) 層：把多張表建立關聯、用 DAX 定義可重用的量值 (measure)，再讓樞紐分析表與 dashboard 共用同一個模型。它和 Power BI 的 semantic model 是同一套引擎，概念可以直接沿用到 [Power BI 模型與 DAX](../../data-science/data-communication/bi-tools/power-bi-modeling-and-dax.md)。

## 什麼時候用

| 適合 | 一般樞紐分析表就夠 |
| --- | --- |
| 多張相關的表（交易、產品、客戶、日期） | 只有一張表 |
| 需要跨表計算、可重用的指標 | 簡單彙總 |
| 資料超過工作表 104 萬列上限 | 資料量小 |
| 多張樞紐表、圖、slicer、KPI 要一致 | 一次性報表 |

啟用：檔案 → 選項 → 增益集 → COM 增益集 → 勾選 Microsoft Power Pivot for Excel（Windows 桌面版）。

## 流程

```text
Power Query 整理資料 ──► 載入資料模型 ──► 建立關聯 ──► 計算欄 / 量值 (DAX)
  ──► 樞紐分析表 / 樞紐分析圖 / slicer / KPI
```

| 工具 | 負責 |
| --- | --- |
| [Power Query](power-query-in-excel.md) | 擷取、轉換、載入 (ETL) |
| Power Pivot | 關聯、DAX、量值、KPI |

## 資料模型

| 概念 | 說明 |
| --- | --- |
| 事實表 (fact table) | 事件與數值：交易、訂單、量測；列數多 |
| 維度表 (dimension table) | 描述欄位：產品、日期、地區、客戶；每個 key 一列 |
| 星狀結構 (star schema) | 事實表在中間，維度表圍繞，以一對多關聯連接 |
| 關聯 (relationship) | 維度表的唯一 key（一）→ 事實表的外鍵（多）；在「圖表檢視」拖拉建立 |
| 日期表 (date table) | 連續日期的維度表，標記為日期表後時間智慧函數才可靠 |

> 先想關聯，再寫 DAX；關聯沒定清楚，量值結果就不穩。比起把所有欄位 merge 成一張超寬表，star schema 更好維護、彙總也更正確。設計原則見 [維度模型](../../data-science/data-engineering/dimensional-modeling-and-star-schema.md)。

## 計算欄 vs 量值

| | 計算欄 (calculated column) | 量值 (measure) |
| --- | --- | --- |
| 計算層級 | 逐列 (row context) | 依目前篩選彙總 (filter context) |
| 何時計算 | 資料重新整理時，結果存在表中 | 查詢時（樞紐表每格各算一次） |
| 佔記憶體 | 是 | 否 |
| 放在樞紐表的 | 列、欄、篩選 | 值 |
| 適合 | 分類標籤、要用來切分或建關聯的欄 | 加總、比率、轉換率、毛利率 |

> 需求是「報表上要顯示的彙總數字」時，先想量值，不要先建一堆計算欄。

```dax
-- 量值：基本聚合
Total Sales := SUM ( Sales[Amount] )

-- 量值：比率（DIVIDE 自動處理分母為 0）
Margin % := DIVIDE ( [Total Profit], [Total Sales] )

-- 量值：改變篩選條件
North Sales := CALCULATE ( [Total Sales], Region[Name] = "North" )

-- 計算欄（在 Sales 表）：從關聯的維度表取值
Category = RELATED ( Product[Category] )
```

Excel Power Pivot 中量值的寫法是 `名稱 := 運算式`（Power BI 用 `=`）。filter context、`CALCULATE` 的完整說明見 [Power BI 模型與 DAX](../../data-science/data-communication/bi-tools/power-bi-modeling-and-dax.md)。

## KPI 與 Dashboard

KPI 把**實際值、目標、狀態**放在同一個指標裡（Power Pivot → KPI → 新增 KPI：選一個量值為基準，設定目標值或目標量值與門檻）。樞紐分析表、樞紐分析圖、slicer 都接在同一個資料模型上時，dashboard 各元件的數字會一致；設計原則見 [Dashboard 設計](../../data-science/data-communication/README.md)。

## 實務守則

| 守則 | 原因 |
| --- | --- |
| 資料先用 Power Query 整理乾淨再載入 | 模型層不適合做清理 |
| 先建關聯，再寫 DAX | 量值依賴關聯傳遞篩選 |
| 量值優先，計算欄節制 | 計算欄佔記憶體、不隨篩選變化 |
| 量值集中放在一張表、取清楚的名稱 | 方便重用與查找 |
| 團隊共用、需要排程更新時 | 模型搬到 Power BI |
