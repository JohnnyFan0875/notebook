# Sigma Overview and Workflow

Sigma 是一種比較偏「spreadsheet-style analytics on cloud data warehouses」的 BI 工具。

它的特色不是只會畫 dashboard，而是把資料倉儲連線、表格探索、pivot、chart、互動控制與 workbook 發布流程放進同一個介面。

## Sigma 在解決什麼問題

很多團隊有兩種常見落差：

- 資料在 cloud warehouse 裡，但業務或分析使用者不想直接寫 SQL
- 傳統 dashboard 太靜態，難以支援即時探索與互動式決策

Sigma 的定位，就是讓使用者用比較接近 spreadsheet 的方式，在雲端資料上做分析、整理與互動探索。

## 先用一個心智模型理解 Sigma

可以先把 Sigma 想成：

`cloud data -> workbook -> tables / pivots / charts / controls -> published analytics`

這個流程的重點是，Sigma 不是只負責最後一張圖，而是從資料探索一路延伸到互動式成果交付。

## Workbook 是核心工作單位

Sigma 裡最重要的容器是 `workbook`。

workbook 可以包含：

- tables
- pivot tables
- charts
- filters
- controls
- 多個 pages

這讓它比較像分析工作簿，而不是只有單張 dashboard。

## Sigma 為什麼常被拿來和 spreadsheet 類比

教材裡反覆出現的重點包括：

- row-level formulas
- summaries and grouped tables
- pivots and charts
- interactive controls

這些能力讓 Sigma 很像把 spreadsheet 工作流搬到更正式的雲端資料環境中。

差別在於，它不是把資料複製到本地檔案再分析，而是更貼近 warehouse-native 的工作方式。

## Pivot Tables and Charts

Sigma 很適合處理需要快速回答的分析問題，例如：

- 指標是上升還是下降
- 哪些 merchant 或 segment 風險較高
- 新客與老客的差異在哪裡

這類問題常不需要一開始就建完整 dashboard，而是先透過：

- pivot table
- grouped summary
- quick chart

快速得到方向。

### Child Charts 的意義

教材提到 child charts 會繼承：

- filters
- formatting
- groupings
- calculated results

這個概念很有用，因為它表示視覺化不是獨立存在，而是建立在表格與分析邏輯之上。圖表只是 workbook 分析結果的另一個表現形式。

## Lineage View

Sigma 一個很值得記的功能是 `Lineage view`。

它可以用視覺方式顯示：

- warehouse connections
- data sources
- tables
- charts
- 元件之間的方向與繼承關係

這個功能的重要性在於，它把 workbook 裡的分析邏輯顯性化。當一個 workbook 逐漸變複雜時，lineage 可以幫你看清楚：

- 某張圖是從哪張表來的
- 哪些計算依賴哪些中介結果
- 修改某個上游元素後，哪些下游元件會受影響

## Parameters and Controls

Sigma 的另一個特色，是把互動式分析做得很自然。

### Parameter 是什麼

教材把 parameter 解釋成：

- logic 裡的 placeholder
- 由使用者在互動時填入的值
- 可用於 calculations 或 filters

這是一個很好的心智模型，因為它提醒我們參數不是寫死在公式裡，而是留給使用者決定。

### Parameters in Sigma Are Controls

Sigma 的實作重點是：

- parameters 實際上是 control elements
- 每個 control 都有自己的 control ID
- 可以在 calculation 中引用 user input

這讓 workbook 可以變成動態分析介面，而不只是靜態報表。

常見 control 類型包括：

- dropdowns
- input fields
- switches
- 其他互動元件

### 為什麼這很重要

這種設計可以避免：

- hardcoded thresholds
- 為了不同情境複製很多頁面
- 使用者必須直接改公式才能看不同結果

也就是說，Sigma 的 control 不是裝飾，而是把分析邏輯開放成可調整的決策介面。

## Workbook Lifecycle

Sigma 的 workbook lifecycle 也很值得記。

教材提到：

- new workbook 一開始是 `Exploration`
- exploration 是 temporary、private 的
- Sigma 會 autosave
- changes 先存在 draft mode
- audience 只看到 published version

這個流程代表 Sigma 不是只有單純編輯檔案，而是把探索、協作與發佈分開。

### 為什麼這個 lifecycle 有價值

它可以幫團隊同時滿足兩件事：

- 分析師需要自由探索與快速修改
- 受眾需要穩定、可信的已發布版本

這點和一般 BI 工具的 draft/publish 分界很像，但 Sigma 把它直接放在 workbook 工作流裡。

## Sigma 的典型使用場景

如果一個團隊想要的是：

- 接近 spreadsheet 的易用性
- 接近 BI 工具的互動與視覺化
- 接近 warehouse-native analytics 的資料來源方式

那 Sigma 會是一個很自然的候選工具。

它特別適合：

- 商業分析探索
- 互動式 workbook
- 需要 controls 或 parameterized logic 的分析頁面
- 從探索一路延伸到 stakeholder-facing 成果

## 一個最小心智模型

如果只想先記住最重要的東西，可以抓這五點：

1. Sigma 是建在 cloud data 上的 spreadsheet-style BI 工具
2. workbook 是核心容器，不只是 dashboard 畫布
3. tables、pivots、charts 和 controls 是同一個分析工作流的不同層
4. lineage view 幫助理解邏輯依賴與分析結構
5. draft / publish lifecycle 讓探索與正式交付可以分開

## Related Concepts

- [Dashboard Design](../data-manipulation-and-eda/visualization/dashboard-design.md)
- [Connecting and Combining Data in Tableau](tableau/connecting-and-combining-data.md)
- [Semantic Models and Power BI](../data-engineering/semantic-models-and-power-bi.md)

[Back to Data Communication](README.md)
