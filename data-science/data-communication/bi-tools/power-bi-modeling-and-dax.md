[Data Communication](../README.md) › [BI 工具](README.md) › Power BI 模型與 DAX

# Power BI 模型與 DAX (Power BI Modeling and DAX)

Power BI 把資料準備、資料模型、互動式視覺化與分享串成一條流程：`dataset → model → report → 分享`。本篇先建立整體地圖，再看 semantic model（關係、安全性）與 DAX（context、measure、`CALCULATE()`）。資料前處理見 [Power Query](power-query.md)，報表設計見 [Power BI 報表](power-bi-reports.md)。

> 好的報表是好模型的結果：數字對不對、能不能重用，由模型決定；報表只決定好不好理解與操作。

## 整體地圖

```
1. 載入資料 → 2. Power Query 清理 → 3. 建模型（關係、measure）→ 4. Report view 做報表 → 5. Service 發布分享
```

| View | 看什麼 | 思考層次 |
| --- | --- | --- |
| Table view | 表內容與欄位 | 資料 |
| Model view | 表與關係 | 結構 |
| Report view | 建立與編輯視覺化 | 呈現 |

報表有問題時，先判斷是資料內容、模型結構還是視覺呈現的問題，比較快找到根源。

| 視覺元件 | 適合 |
| --- | --- |
| Table / matrix | 明細與交叉檢視 |
| Card / multi-row card | 單一指標摘要 |
| Gauge / KPI | 與目標的差距 |

| 篩選範圍 | 影響 |
| --- | --- |
| Visual-level filter | 單一視覺 |
| Page-level filter | 同一頁 |
| Report-level filter | 整份報表 |

很多報表混亂不是圖做不好，而是篩選範圍沒設清楚。互動也要設計：用「編輯互動」關掉不該連動的視覺，避免使用者以為所有圖都該互相影響。有天然層級的資料（年 → 季 → 月、地區 → 城市 → 門市、類別 → 子類別 → 產品）用階層與 drill-down，比把所有欄位攤平自然。

## Semantic Model

semantic model 位在原始表與報表之間，把技術性的資料結構轉成業務導向、可建立關係、可重用的分析模型：統一 measure、篩選、階層與權限，避免每份報表各自重做邏輯。在 Fabric 中，建立 lakehouse / warehouse 時就可以自動產生 semantic model，語意層因此更早進入資料平台設計。

### 關係 (Relationships)

| 原則 | 理由 |
| --- | --- |
| 模型形狀接近 star schema：fact 在中間、dimension 圍繞 | 篩選行為可預期；見 [維度模型](../../data-engineering/dimensional-modeling-and-star-schema.md) |
| 關係以 dimension 的唯一 key 對 fact 的 key（一對多） | 多對多關係容易產生意外結果 |
| 單向篩選：dimension → fact | 篩選路徑容易推理 |
| dimension 之間不要互連 | 關係網越複雜，篩選傳播越難預期 |

雙向篩選 (bi-directional) 最常見的用途是「slicer 只顯示與目前情境相關的選項」，但它會讓兩表間出現多條路徑、推理變難、多對多時拖慢效能。預設單向，只有特定互動真的需要時才評估；能用 measure 或明確邏輯（`CROSSFILTER()`）代替就不要把雙向當萬用解。

同兩張表可以有多條關係（訂單日、出貨日、送達日都連到日期表），但同時間只有一條是 active，其他在 measure 中用 `USERELATIONSHIP()` 啟用。這迫使模型先講清楚主要語意。

階層可以是自然的（業務上本來就存在，如國家 → 州 → 城市）或人為的（為了分析方便組出的切法）；自然階層使用者較容易理解。

### 安全性

| 機制 | 控制 | 說明 |
| --- | --- | --- |
| RLS (Row-Level Security) | 使用者能看到哪些列 | 區域、業務單位各看各的；同一模型服務多種角色 |
| OLS (Object-Level Security) | 能否看到某張表或某欄 | 隱藏敏感欄位 |
| Dataset 權限 | Read / Build / Reshare / Write | 看報表、用模型做新內容、再分享、改 metadata 是不同的事 |
| 敏感度標籤 | 內容敏感程度 | 匯出、分享後仍保留保護語意 |

```dax
// 動態 RLS：角色篩選條件，依登入者的 UPN（通常是 email）決定可見範圍
Dim_Region[ManagerEmail] = USERPRINCIPALNAME()
```

| RLS 要注意 | |
| --- | --- |
| 角色在 Desktop 定義，成員在 Service 指派 | 兩邊都做才生效；Desktop 可用「以角色檢視」測試 |
| 額外的列篩選可能拖慢查詢 | — |
| 對 dataset 有寫入權限的人（workspace Admin / Member / Contributor）不受 RLS 限制 | RLS 保護的是報表使用者，不是作者 |
| workspace 角色與 dataset 權限相關但不相同 | 看得到報表不代表能 Build 新報表 |

### 建模前的問題

| 問題 | |
| --- | --- |
| 哪些表直接暴露給報表？ | 工程用欄位（技術 key、載入時間）隱藏 |
| 關係怎麼定義才符合業務邏輯？ | grain、key、方向 |
| 需要依角色篩選列嗎？有敏感欄位要用 OLS 隱藏嗎？ | 安全性 |
| 需要很多例外的篩選路徑嗎？ | 是的話，先回頭檢查 schema 與 dimension 設計 |

## DAX

DAX (Data Analysis Expressions) 是模型層的計算語言（Power BI、Excel Power Pivot、Analysis Services 共用）。它的難點與價值都來自 **context**：同一個 measure 放在不同視覺、不同 slicer 條件下，結果會不同。

| Context | 意義 | 來源 |
| --- | --- | --- |
| Filter context | 計算前已套在資料上的一組篩選 | 視覺的列 / 欄、slicer、篩選窗格、`CALCULATE()` |
| Row context | 逐列計算時「目前這一列」 | 計算欄、`SUMX` 等 iterator |
| Context transition | 在 row context 中呼叫 measure 或 `CALCULATE()`，目前列變成 filter context | 在 iterator 內使用 measure |

> DAX 算錯時，先檢查是在什麼 context 下計算，不要先懷疑函式語法。

### 計算欄 vs Measure

| | 計算欄 (calculated column) | Measure |
| --- | --- | --- |
| 計算方式 | 逐列，在重新整理時算好並存下 | 查詢時依 filter context 聚合 |
| 佔空間 | 是（增加模型大小） | 否 |
| 適合 | 衍生分類、標籤、用來切分或建立關係的欄位 | 總和、比例、KPI、隨 slicer 變化的摘要 |

> 優先寫 explicit measure，不要依賴視覺對欄位的隱式聚合：名稱清楚、可被其他 measure 重用、複雜模型較好維護。能在 Power Query 做的衍生欄位，通常比 DAX 計算欄更好（壓縮較佳）。

### `CALCULATE()`

```dax
CALCULATE(<expression>[, <filter1> [, <filter2> ...]])
```

在修改或明確指定 filter context 後計算 expression（必須回傳單一值）。多個篩選之間是 AND。

```dax
Total Sales      = SUM(Fact_Orders[Sales])
Total Sales EMEA = CALCULATE([Total Sales], Dim_Region[Region] = "EMEA")
Share of Total   = DIVIDE([Total Sales], CALCULATE([Total Sales], ALL(Dim_Region)))   // DIVIDE 處理分母為 0

Sales Growth =
VAR SalesPriorYear = CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Date'[Date]))
RETURN [Total Sales] - SalesPriorYear                    // VAR 命名中間結果、避免重算
```

### 常用函式

| 函式族 | 函式 | 用途 |
| --- | --- | --- |
| 篩選 | `FILTER(table, cond)` | 回傳篩選後的表（給 `CALCULATE` 或 iterator 用） |
| | `ALL()`、`REMOVEFILTERS()`、`ALLEXCEPT()` | 移除篩選：算總體、佔比、全域排名 |
| | `KEEPFILTERS()` | 與既有篩選取交集而非覆蓋 |
| 關係 | `RELATED()` | 從「一」端的表取值（在多端的 row context 中） |
| | `USERELATIONSHIP()` | 啟用非 active 的關係（role-playing 日期） |
| | `CROSSFILTER()` | 在計算中暫時改變篩選方向；進階用法 |
| Iterator | `SUMX()`、`AVERAGEX()`、`COUNTX()`、`RANKX()` | 逐列計算 expression 再聚合 |
| 計數 | `COUNTROWS()`、`DISTINCTCOUNT()` | 列數（事件數、符合條件筆數）、distinct 數 |
| 時間智慧 | `SAMEPERIODLASTYEAR()`、`DATEADD()`、`TOTALYTD()` / `TOTALQTD()` / `TOTALMTD()` | 期間比較（YoY、MoM）、累計 |
| 邏輯 | `IF()`、`SWITCH()` | 分支 |
| 日期與文字 | `DATE()`、`WEEKDAY()`、`LEFT()` / `MID()` / `RIGHT()` | 從零散欄位組日期、取日期成分；日期不乾淨時優先回 Power Query 修 |
| 表 | `SUMMARIZE()`、`ADDCOLUMNS()`、`SUMMARIZECOLUMNS()` | 產生彙總表 |

```dax
// 篩選欄位時直接寫條件，比 FILTER 整張 fact 表有效率
Total Sales Chuck = CALCULATE([Total Sales], Dim_Sales[Salesperson] = "Chuck")
// 等價但較慢：CALCULATE([Total Sales], FILTER(Fact_Orders, RELATED(Dim_Sales[Salesperson]) = "Chuck"))

// Iterator：先逐列算 Sales - Profit 再加總
Total Costs East =
SUMX(FILTER(Fact_Orders, Fact_Orders[Region] = "East"), Fact_Orders[Sales] - Fact_Orders[Profit])

// 排名：ALL 讓排名基於所有 region，而不是目前視覺中被篩選過的部分
Costs Rank = RANKX(ALL(Dim_Sales[Region]), [Total Costs])

// 年初至今：需要標記為日期表、日期連續的 date dimension
Sales YTD = TOTALYTD([Total Sales], 'Date'[Date])

// 多條件分段：SWITCH(TRUE(), ...) 比巢狀 IF 易讀
Performance =
SWITCH(TRUE(),
    [Total Sales] < 25000, "Poor",
    [Total Sales] < 50000, "Below expectations",
    [Total Sales] < 75000, "Above expectations",
    "Exceptional")

// 類別映射；最後一個參數是預設值
Discount = SWITCH([Clothing Type], "Shoes", 0.15, "Pants", 0.20, "Belts", 0.30, "T-shirt", 0.25, 0)

// 彙總表：SUMMARIZE 定義分組，新欄位用 ADDCOLUMNS 加（直接在 SUMMARIZE 內算可能因 context 出錯）
Region Summary =
ADDCOLUMNS(SUMMARIZE(Fact_Orders, Dim_Region[Region]), "Sales", [Total Sales])

// 逐列加欄：欄位要寫完整的 Table[Column]
Orders With Profit = ADDCOLUMNS(Fact_Orders, "Profit", Fact_Orders[Revenue] - Fact_Orders[Costs])
```

| 陷阱 | 說明 |
| --- | --- |
| 時間智慧函式結果怪異 | 沒有連續、標記為日期表的 date dimension；或用了 fact 表的日期欄 |
| 排名只在局部排序 | `RANKX` 沒有用 `ALL()` 擴大排名範圍 |
| 總計列數字不等於各列相加 | measure 在總計列的 filter context 不同，這通常是正確行為；需要相加時用 `SUMX` 包一層 |
| `SUM(Sales)` 報錯 | 聚合函式要指定欄：`SUM(Table[Column])` |

### 學習順序

```
1. 分清楚計算欄與 measure → 2. 理解 context → 3. CALCULATE 調整 filter context
  → 4. FILTER / ALL / SUMX 改變計算範圍與方式 → 5. SWITCH、TOTALYTD、ADDCOLUMNS / SUMMARIZE
```

DAX 不應脫離模型理解：關係影響計算範圍、篩選方向影響結果、模型設計決定 measure 能否重用。Excel 中的同一套概念見 [Power Pivot](../../../productivity/microsoft-office/power-pivot-in-excel.md)。
