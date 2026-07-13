# Data Transformation in Power BI

在 Power BI 裡，data transformation 比單純清理再進一步。  
它關心的不只是把欄位修乾淨，還包含資料 shape、表與表的組合方式、衍生欄位，以及什麼時候要往 `M code` 層看。

如果 [Data Preparation in Power BI](data-preparation-in-power-bi.md) 偏「讓資料變乾淨」，這篇比較偏「讓資料變成更適合分析的形狀」。

## Reshaping Data

很多資料不是內容錯，而是 shape 不適合分析流程。  
課程把這件事先拆成兩種常見結構：

- long format
- wide format

可以先用一個簡化方式理解：

- `long`: 類別值會重複出現在前面欄位，通常比較容易被系統做聚合、分組與視覺化
- `wide`: 一列裡會展開較多數值欄位，通常比較接近人讀表格的習慣

關鍵不是哪一種永遠比較好，而是哪一種更適合你下一步要做的事情。

## Pivot and Unpivot

Power Query 裡最重要的 reshape 操作之一就是：

- `pivot`: long -> wide
- `unpivot`: wide -> long

這兩個操作很常出現在：

- 報表匯出表格太寬
- Excel source 用月份當欄名
- 多個 measure 被分散成多欄，但分析時其實需要 tidy 結構

實務上，很多 Power BI 模型會更偏好能被穩定聚合與切分的 long-ish 結構，而不是過度為人工閱讀優化的寬表。

## Aggregation and Grouping

transformation 不只是在移動欄位，也常包含先做 aggregation。

在 Power Query 的脈絡裡，`Group By` 可以先理解成：

- 先選定 key
- 再把對應列做彙總
- 產生更高層級的分析表

這適合用在：

- 先把明細壓成 customer / product / date 層級
- 先做中間表，再交給模型層
- 降低後續重複計算負擔

## Combining Data

Power Query 裡另一個非常核心的 transformation 類別，是把多個 queries 或 tables 組起來。  
最常見的兩種就是：

- `append`
- `merge`

## Append Queries

`append` 的心智模型是 vertical stacking。

也就是：

- 把多張結構相近的表往下堆
- 增加 rows
- 不改變主要欄位意義

常見使用情境：

- 多個月份的檔案
- 多個門市的同型報表
- 單一檔案放不下的大量同構資料

append 時最需要先檢查的是 schema：

- column names 是否一致
- column count 是否一致
- data types 是否一致

如果欄位對不起來，Power Query 很容易補出 `null`，但那通常不是解法，而是提醒你 schema 還沒對齊。

## Merge Queries

`merge` 的心智模型是 horizontal enrichment。

也就是：

- 根據共同 key 把另一張表的欄位接進來
- 增加 columns
- 用 lookup / relationship-like 的方式補資料

它通常適合：

- 把 lookup table 接回明細表
- 將多張關聯表先整理成較平坦的輸入
- 在模型層之前先補足描述欄位

但 merge 的前提永遠是 key 品質穩定。  
如果 key 型別不同、拼寫不一致、或 cardinality 本來就沒想清楚，後面就會出現缺值、重複列或錯誤匹配。

## Flat Table vs Model Design

課程提到 merge 可以把表組成較 flat 的 structure。  
這在某些前處理情境很有用，但不代表所有表都應該被壓平到只剩一張。

比較穩的做法通常是：

- transformation 階段只做必要整併
- 分清楚哪些欄位適合提前補齊
- 不要因為方便就把模型層應該表達的結構全部抹平

也就是說，Power Query 可以幫你整理 shape，但資料模型該不該維持多表結構，仍然要回到 semantic model 的需求判斷。

## Custom Columns

當內建 transformation 不夠時，Power Query 可以新增 `custom columns`。

這些欄位：

- 用 `M language` 撰寫
- 可以引用多個欄位
- 可以做更進階的 conditional logic
- 能延伸既有 transformation 的能力

它很適合拿來做：

- row-level business rules
- 條件分類
- 依多欄位組合建立新特徵

## Common Operations in Custom Columns

課程整理了幾類常見操作：

- numerical: `+ - * / ^`
- text: `&`
- comparisons: `< > <> <= >= =`
- conditional logic: `if ... then ... else`
- boolean logic: `AND OR NOT`

這些操作看起來簡單，但其實已經足夠應付很多匯入階段的衍生欄位需求。

## Mind the Data Types

custom column 最常見的問題不是語法長，而是 data types 不一致。

常見風險包括：

- 把 text 當 number 算
- 日期還沒轉型就先比較
- null handling 沒想清楚

如果型別沒先穩住，M code 很容易報錯，或更糟的是產出表面合理、實際錯誤的結果。

## Advanced Editor

當 transformation 開始變多，只看 Applied Steps 有時不夠。  
這時 `Advanced Editor` 就很重要。

它讓你：

- 看到 query 的底層程式碼
- 直接編輯 M code
- 理解每個 transformation 如何被表達

一個很重要的觀念是：

- 你在 Power Query 做的每個 transformation，都會被翻成 M code
- 反過來，調整 M code 也會回到 query steps 的邏輯

可以把 `Advanced Editor` 理解成 GUI 與 code 之間的橋。

## M Code vs DAX

Power BI 很容易把 `M` 和 `DAX` 混在一起，但它們負責的層次不同。

| Layer | Main Purpose | Typical Actions |
| ----- | ------------ | --------------- |
| `M language` | load / transform data | rename, filter, pivot, unpivot, group, custom columns |
| `DAX` | analyze on top of model | measures, calculated columns, filter context, summarization |

一個簡化判斷法：

- 如果你要改的是資料本身的 shape 或欄位內容，優先想 `M`
- 如果你要改的是模型上的分析計算，優先想 `DAX`

課程也特別點出：

- `M` 是 case-sensitive
- `DAX` 不區分大小寫

## Applied Steps and M Code

Power Query 很值得保留的一個工程特性，是 step 與 code 的對應關係。

這代表：

- transformation 不是黑箱
- GUI 操作不是一次性手動點擊
- 你可以從 steps 回推 query 邏輯

當 query 出錯時，能不能讀懂 steps 與 M code，常常比會不會背更多按鈕更重要。

## Practical Heuristics

- 先問資料 shape 適不適合分析，再問圖表怎麼畫。
- `append` 是堆 rows，`merge` 是補 columns，不要混用。
- schema 不一致時先修欄名與型別，不要讓 `null` 悄悄吞掉問題。
- custom columns 適合 row-level 邏輯，但不要把整個分析層都塞進 M code。
- 要改資料就想 `M`，要改模型上的計算就想 `DAX`。
- transformation steps 變複雜後，要敢打開 `Advanced Editor` 看底層。

## Relation to Other Notes

- 如果你想看 transformation 之前的資料連線與 refresh 議題，可以接著看 [Data Connections in Power BI](data-connections-in-power-bi.md)。
- 如果你想看欄位型別、text cleaning 與 preview features，可以接著看 [Data Preparation in Power BI](data-preparation-in-power-bi.md)。
- 如果你想看模型層計算，則接著看 [DAX in Power BI](dax-in-power-bi.md)。

## Mental Model

一句話總結：

Power BI 的 data transformation，可以先理解成把 raw tables 轉成 `right shape + right joins + right derived columns` 的 Power Query 重塑層。
