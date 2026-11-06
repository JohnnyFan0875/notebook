[Productivity](../README.md) › [試算表](README.md) › 資料分析流程

# Excel 資料分析流程 (Data Analysis Workflow)

資料準備好之後，Excel 的分析常走這條路：探索 → 分群與彙總 → 假設分析 (what-if) → 初步預測。Excel 擅長把商業問題快速轉成表格邏輯；分析需求長大時，重點是知道何時換工具。

## 流程

```text
1. 樞紐分析表找出值得追的維度與指標
2. IF / IFS / SWITCH 建立分群
3. SUMIFS 等條件聚合算出各群指標
4. Goal Seek / Scenario Manager / Data Table 測試假設
5. 移動平均、趨勢線、FORECAST.ETS 做初步外推
6. 流程變重複、資料變大 → Power Query、BI、SQL、Python
```

## 1. 探索：樞紐分析表

樞紐分析表 (PivotTable) 不只是報表，而是第一個探索工具：哪些維度值得切、哪些群組差異最大、哪些指標要往下追。

| 功能 | 用途 |
| --- | --- |
| 值欄位設定 | 加總、計數、平均、% of total |
| 計算欄位 (Calculated Field) | 補出原始資料沒有的指標（如毛利率） |
| 群組 (Grouping) | 日期 → 月 / 季 / 年；數值 → 區間 |
| 交叉分析篩選器 (Slicer)、時間表 (Timeline) | 互動式篩選，適合 demo 與 review |
| 樞紐分析圖 (PivotChart) | 隨樞紐表一起篩選的圖 |

> 原始表保持乾淨，分析邏輯先在樞紐層驗證；指標與切法穩定後，再決定要不要搬進 [Power Pivot](power-pivot-in-excel.md) 或 BI 工具。

## 2. 分群與條件聚合

很多問題不是「總銷售多少」，而是「哪些客戶值得關注、哪群成長最快」。先用邏輯函數定義群組，再用條件聚合算每群的指標。

| 函數 | 適合 | 例 |
| --- | --- | --- |
| `IF` | 二元：是否達標、是否續約 | `=IF(C2>=Target, "met", "missed")` |
| `IFS` | 多層門檻 | `=IFS(C2>=1000, "A", C2>=500, "B", TRUE, "C")` |
| `SWITCH` | 等值對應 | `=SWITCH(D2, 1, "new", 2, "active", "churned")` |
| `SUMIFS` / `COUNTIFS` / `AVERAGEIFS` | 各群彙總 | `=SUMIFS(Sales[Amount], Sales[Segment], "A")` |

`IFS` 沒有內建 else，全部不成立回傳 `#N/A`，所以最後補 `TRUE, fallback`。語法細節見 [Excel 函數](advanced-excel-functions.md#邏輯與分類)。

## 3. 假設分析 (What-If Analysis)

| 分析 | 問題 | 輸入 |
| --- | --- | --- |
| 情境分析 (scenario analysis) | 幾組離散假設下結果各是多少？ | 保守 / 基準 / 樂觀 |
| 敏感度分析 (sensitivity analysis) | 某輸入在一段範圍內變動，輸出怎麼反應？哪個輸入最敏感？ | 連續範圍 |

模型要分清**自變數**（外部給定的輸入，如收入、扣除額、稅率）與**應變數**（由輸入算出的輸出，如 `應納稅額 = (收入 − 扣除額) × 稅率`）。把輸入集中在一區、輸出公式只參照輸入格，what-if 工具才好用。

| 工具（資料 → 模擬分析） | 用途 | 例 |
| --- | --- | --- |
| 目標搜尋 (Goal Seek) | 已知想要的結果，反推一個輸入 | 毛利率要 20%，售價該設多少？ |
| 分析藍本管理員 (Scenario Manager) | 儲存多組輸入並產生比較摘要 | 最佳 / 基準 / 最差情境 |
| 運算列表 (Data Table) | 一或兩個輸入跑過一段範圍，產生敏感度表 | 折扣 5%–30% × 銷量，對應的利潤 |
| 規劃求解 (Solver，增益集) | 多個輸入、有限制條件的最佳化 | 預算限制下的最大化產量 |

## 4. 初步預測

| 概念 | 意義 |
| --- | --- |
| 預測不是事實 | 依賴歷史資料與方法假設，環境改變就可能失效 |
| 季節性 (seasonality) | 與月份、季節、節日相關的週期規律；有季節性時單純平均會失真 |
| 預測偏誤 (bias) | 系統性偏高或偏低：只跟到舊趨勢、結構改變卻沒更新方法 |
| 預測區間 | 表達不確定性，不要只看單點預測 |

| 方法 | 做法 | 限制 |
| --- | --- | --- |
| 簡單移動平均 | `=AVERAGE(最近 n 期)` | 對突變反應慢、不處理季節性 |
| 加權移動平均 | `=SUMPRODUCT(values, weights) / SUM(weights)` | 權重主觀 |
| 趨勢線 (trendline) | 圖表 → 加入趨勢線，可顯示方程式與 R² | 只看方向，不是完整預測 |
| `FORECAST.LINEAR()` | 線性迴歸外推 | 假設線性、無季節性 |
| `FORECAST.ETS()` / `FORECAST.ETS.CONFINT()` | 指數平滑 (AAA 版本)，自動偵測季節性；後者給預測區間的半寬 | 時間軸需等距；不適合模型比較與回測 |
| 預測工作表 (Data → Forecast Sheet) | 一鍵產生 ETS 預測表與圖 | 同上 |

加權移動平均例：最近三期 2、3、4，權重 0.15、0.35、0.50 → `(2×0.15 + 3×0.35 + 4×0.50) / 1.00 = 3.35`。

> 需要比較模型、做特徵或回測時就離開 Excel：時間序列方法見 [時間序列](../../data-science/statistics/time-series-analysis/README.md)。

## 何時升級工具

| 需求 | 工具 |
| --- | --- |
| 重複的匯入與清理 | [Power Query](power-query-in-excel.md) |
| 多表關聯、可重用指標 | [Power Pivot](power-pivot-in-excel.md)、[Power BI](../../data-science/data-communication/bi-tools/README.md) |
| 統計檢定、迴歸、模型 | Python / R（[統計](../../data-science/statistics/README.md)） |
| Dashboard 設計原則 | [資料溝通](../../data-science/data-communication/README.md) |
