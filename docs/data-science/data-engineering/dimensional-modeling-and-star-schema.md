# Dimensional Modeling and Star Schema

## Why Dimensional Modeling Exists

不是所有分析資料都適合直接用原始交易表來查。當報表與分析需要穩定的彙總、切片與過濾時，團隊通常會把資料整理成比較適合分析的模型。

dimensional modeling 的目標，是把資料整理成：

- 容易理解的 business-facing structure
- 適合彙總與篩選的分析表
- 能穩定支援 BI、semantic model 與 SQL analytics 的資料形狀

## Medallion Architecture and the Gold Layer

很多 lakehouse 流程會先用 medallion architecture 管資料成熟度：

- `Bronze`: 原始資料，盡量保留來源樣貌
- `Silver`: 清理、標準化後的資料
- `Gold`: 適合分析與消費的資料

在 Fabric 這類平台裡，bronze 和 silver 常落在 lakehouse，而 gold 則可能落在 lakehouse 或 warehouse。

一個很實用的理解方式是：

- bronze 重點是保留
- silver 重點是清理
- gold 重點是可分析

而 star schema 常常就是 gold layer 的典型輸出形態。

## What a Star Schema Looks Like

star schema 會把資料分成兩種主要表：

- `fact table`: 記錄事件、交易或可量化活動
- `dimension table`: 提供描述、分類與分析脈絡

這種設計的核心，不是為了看起來整齊，而是讓分析可以自然地回答：

- 什麼時候發生
- 在哪裡發生
- 跟哪個產品、客戶、通路有關
- 數量、金額、次數是多少

## Dimension Tables

dimension table 用來描述 business entities，例如 product、customer、region。

常見欄位包括：

- `surrogate key`: 內部單欄唯一識別碼
- `natural key` / `business key`: 來自來源系統的業務識別碼
- `dimension attributes`: 用來過濾、分組與提供上下文的欄位

surrogate key 很重要，因為分析模型不應過度依賴來源系統的自然鍵直接充當歷史管理與關聯主鍵。

## Fact Tables

fact table 用來描述 business events，例如一次銷售、一筆訂單、一個點擊事件。

常見欄位包括：

- `dimension keys`: 指向相關 dimension 的 surrogate keys
- `attributes`: 與事件有關，但不是維度也不是度量的欄位
- `measures`: 可量化、通常可聚合的數值欄位，例如金額、數量、次數

一個實務提醒是：fact table 的 grain 要先講清楚。若 grain 不清楚，後續所有 aggregation 都可能出現看似合理但其實錯誤的結果。

## Star Schema vs. Snowflake Thinking

star schema 通常偏向把分析常用的描述欄位保留在 dimension 內，讓查詢比較直接。

相對地，snowflake schema 會把 dimension 再進一步正規化，減少重複，但查詢與理解成本通常會提高。

如果目標是分析與報表，star schema 往往比較自然；如果目標是極致去重或高度正規化維護，snowflake 才比較可能有吸引力。

## Slowly Changing Dimensions

dimension 不會永遠不變，所以實務上要先決定歷史如何保留。

最常見的 SCD 類型包括：

- `Type 0`: 不接受變更，保留原始值
- `Type 1`: 直接覆寫，保留最新值
- `Type 2`: 新增新列，保留完整歷史
- `Type 3`: 額外欄位保留有限歷史

課程裡一個很實務的建議是：

- 不需要歷史時，優先考慮 `Type 1`
- 需要歷史時，優先考慮 `Type 2`

其他類型雖然存在，但複雜度通常較高，沒有明確需求時不必急著用。

## Choosing SCD Type in Practice

可以用這個方式快速判斷：

- 如果資料只需要反映最新狀態，例如補充性的聯絡資訊，`Type 1` 常夠用
- 如果分析必須回答「某個時間點當時的狀態」，`Type 2` 更合適
- 如果只想保留極少量前一版本資訊，才考慮 `Type 3`

SCD 決策本質上是在 trade off：

- 歷史保留需求
- 查詢複雜度
- 儲存成本
- 維護成本

## Date and Time Dimensions

date dimension 幾乎是最常見的 conformed dimension，因為大多數 fact table 都會有日期欄位。

常見做法包括：

- natural key 用 date data type
- surrogate key 用 `YYYYMMDD` 整數格式
- 預先提供 year、month、day 等分析欄位

如果分析需要到一天中的時間粒度，則可以另外建立 time dimension。

time dimension 常見做法：

- natural key 用 time data type
- surrogate key 用 `HHMM` 或 `HHMMSS`
- grain 視需求決定是分鐘還是秒

## Conformed Dimensions

conformed dimensions 會被多個 fact table 共用。

最典型的例子是：

- sales fact 和 marketing fact 共用 date dimension
- 多個主題共用 product dimension

它的價值在於讓不同分析主題仍然維持一致的切分方式。若每個主題各自定義日期或產品維度，跨領域比較會很快失真。

## Role-Playing Dimensions

有些 fact table 會多次引用同一張 dimension，但代表不同角色。

例如同一張 date dimension 可能同時扮演：

- order date
- shipping date
- delivery date

這種情況下，不需要複製多份相同維度資料，而是讓同一個 dimension 在模型中扮演不同角色。

## Multivalued Dimensions and Bridge Tables

當 fact 和 dimension 之間不是單純一對一或多對一，而是 many-to-many 時，常需要 bridge table。

bridge table 的用途是：

- 儲存相關 dimension keys 的配對
- 表達 multivalued relationship
- 避免把一對多關係硬塞進單一欄位

這類表有時也會被稱為 factless table，因為它主要保存關係，而不是度量值。

## Practical Design Questions

在建 star schema 前，先問：

- fact table 的 grain 是什麼
- 哪些欄位是描述性維度，哪些才是 measures
- 來源系統的 business key 是否足夠穩定
- 哪些 dimension 需要保留歷史
- 哪些日期或時間角色會重複出現
- 是否存在 many-to-many 需要 bridge table

## Practical Reminders

- star schema 不是為了教科書漂亮，而是為了讓分析更穩定、更好查。
- gold layer 的價值通常不是再做一次清理，而是把資料整理成可被穩定消費的分析模型。
- SCD 選型如果太晚決定，後面補歷史通常很痛。
- date dimension 幾乎永遠值得好好設計，因為它會被大量下游共用。
- 若不同 fact tables 沒有共享 conformed dimensions，跨主題分析很容易失真。

[Back to Data Engineering](README.md)
