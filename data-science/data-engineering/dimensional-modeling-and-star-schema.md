# Data Warehousing and Dimensional Modeling

Data warehousing is the practice of collecting, integrating, organizing, and storing data so that it can support large-scale analysis, reporting, and decision-making across an organization.

Key point: A data warehouse is not just a bigger database. It is designed for analytical workloads, integrated business views, and historical reporting rather than day-to-day transaction processing.

## What a Data Warehouse Does

A warehouse gathers data from multiple operational sources and makes it available for analysis in a form that is more consistent and easier to query.

| Warehouse Function | Why It Matters |
| --- | --- |
| Collect data from many systems | Brings fragmented operational data into one analytical environment |
| Integrate and standardize | Makes cross-functional analysis possible |
| Preserve historical context | Supports trend analysis, reporting, and business review |
| Enable BI and analytics | Gives analysts and decision-makers a stable reporting layer |

Tip: Warehouses create value by reducing the effort needed to answer recurring business questions across teams.

## Data Warehouse vs Database vs Data Mart vs Data Lake

These systems solve related but different problems.

| System | Main Purpose | Typical Data Shape |
| --- | --- | --- |
| Transactional database | Run operational applications and store transactions | Structured, row-oriented |
| Data warehouse | Support organization-wide analytics and reporting | Structured, integrated, analytical |
| Data mart | Support analysis for a narrower subject area or department | Structured, focused |
| Data lake | Store large volumes of raw or varied data for flexible future use | Structured and unstructured |

Key point: Warehouses emphasize known analytical use cases and organized structure, while lakes emphasize flexible storage and broader raw-data coverage.

## Why Organizations Use Data Warehouses

Warehouses are especially useful when organizations need analysis without burdening transactional systems.

Common reasons include:

1. support BI and reporting
2. improve organizational decision-making
3. avoid slowing down operational databases with large analytical queries
4. create a stable basis for forecasting, compliance analysis, and growth planning

## Typical Warehouse Layers

Many warehouse architectures can be described with a layered model.

| Layer | Role |
| --- | --- |
| Data source layer | Operational systems, logs, files, spreadsheets, and other inputs |
| Data staging layer | Extraction, transformation, validation, and temporary preparation area |
| Data storage layer | Warehouse tables and sometimes downstream data marts |
| Data presentation layer | BI tools, dashboards, data mining tools, and direct analytical queries |

Tip: The staging layer is where much of the messy integration work happens so that the presentation layer can stay simpler and more reliable.

## Presentation Layer Users and Tools

The presentation layer exists for people, not just systems.

| Tool Group | Typical Use |
| --- | --- |
| Automated reporting and dashboards | Recurring metrics, KPIs, executive and operational reporting |
| BI and analytics tools | Exploratory analysis and pattern discovery |
| Direct queries | Advanced analysis by analysts, data scientists, or engineers |

## Warehouse Life Cycle

A warehouse is typically developed and maintained through a recurring life cycle.

| Life Cycle Area | Typical Activities |
| --- | --- |
| Planning | Clarify business requirements and reporting needs |
| Data modeling | Design fact tables, dimensions, and grain |
| Implementation | Build ETL or ELT pipelines and BI interfaces |
| Maintenance | Modify, test, deploy, and support the system over time |

Key point: Warehouses are not one-time builds. They are long-lived analytical products that require ongoing maintenance and evolution.

## Inmon vs Kimball

Two classic design philosophies appear often in data warehousing.

| Approach | Main Idea | Trade-off |
| --- | --- | --- |
| Inmon, top-down | Build an integrated enterprise warehouse first, then derive marts | More upfront design effort, stronger enterprise consistency |
| Kimball, bottom-up | Start with dimensional data marts and grow from business processes | Faster delivery, lower startup cost, but more coordination needed over time |

### Inmon, Top-Down

This approach prioritizes an enterprise-level integrated design before broad consumption.

| Advantage | Disadvantage |
| --- | --- |
| Strong single source of truth | Lengthy upfront work |
| Easier to align downstream marts later | Higher startup cost |

### Kimball, Bottom-Up

This approach starts from concrete business processes and delivers dimensional models early.

| Advantage | Disadvantage |
| --- | --- |
| Faster initial delivery | More ETL coordination over time |
| Lower upfront cost | Greater risk of duplication if domains drift apart |

Tip: Kimball is often attractive when a team needs to prove business impact quickly.

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

## Kimball Modeling Steps

The extracted material follows a common Kimball-style dimensional design sequence.

1. select the organizational process
2. declare the grain
3. identify the dimensions
4. identify the facts

### 1. Select the Organizational Process

Start from a business process such as billing, purchases, marketing, or product monitoring.

### 2. Declare the Grain

Grain defines the lowest level each fact row represents.

Warning: If grain is vague or inconsistent, every downstream metric becomes harder to trust.

### 3. Identify the Dimensions

Choose the descriptive fields users need to analyze the process, such as time, customer, product, location, or payment method.

### 4. Identify the Facts

Choose the numeric measures that are true at the selected grain, such as sales amount, units sold, or time spent before purchase.

## Star Schema vs. Snowflake Thinking

star schema 通常偏向把分析常用的描述欄位保留在 dimension 內，讓查詢比較直接。

相對地，snowflake schema 會把 dimension 再進一步正規化，減少重複，但查詢與理解成本通常會提高。

如果目標是分析與報表，star schema 往往比較自然；如果目標是極致去重或高度正規化維護，snowflake 才比較可能有吸引力。

在 Power BI 這類 BI 工具裡，這個偏好會更明顯：  
Power BI 通常更偏好 star schema，而不是讓 dimension 之間再繼續連很多層。

## Slowly Changing Dimensions

dimension 不會永遠不變，所以實務上要先決定歷史如何保留。

最常見的 SCD 類型包括：

- `Type 0`: 不接受變更，保留原始值
- `Type 1`: 直接覆寫，保留最新值
- `Type 2`: 新增新列，保留完整歷史
- `Type 3`: 額外欄位保留有限歷史
- Snapshot：定期快照整張 dimension，適合較廣泛的歷史報表

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

它的價值不只是把日期拆欄位而已，還包括：

- 提供穩定 calendar
- 降低複雜 date logic 分散在報表層
- 支援 fiscal year 與 calendar year 並存
- 讓 quarter / month / week slicing 更一致

如果分析需要到一天中的時間粒度，則可以另外建立 time dimension。

time dimension 常見做法：

- natural key 用 time data type
- surrogate key 用 `HHMM` 或 `HHMMSS`
- grain 視需求決定是分鐘還是秒

time dimension 通常比 date dimension 少見。  
很多分析只需要日期層級；只有在 call center、IoT、交易時段或其他高頻事件分析時，time dimension 才會變得特別重要。

date dimension 的建立方式也不只一種。常見做法包括：

- 在 database / warehouse 中集中維護
- 以 file 形式提供
- 在 Power BI / DAX 內直接建立

如果多個服務會共用同一份 calendar，集中維護通常比較穩；如果只是單一模型快速建立，DAX 建 date table 也很實用。

## Conformed Dimensions

conformed dimensions 會被多個 fact table 共用。

最典型的例子是：

- sales fact 和 marketing fact 共用 date dimension
- 多個主題共用 product dimension

它的價值在於讓不同分析主題仍然維持一致的切分方式。若每個主題各自定義日期或產品維度，跨領域比較會很快失真。

一個很實務的提醒是：dimension 比較理想的角色，是被多個 facts 重用，而不是彼此之間到處互連。  
如果 dimension 之間關聯越來越複雜，很多 BI 報表的 filter behavior 也會開始變得難以預期。

## Role-Playing Dimensions

有些 fact table 會多次引用同一張 dimension，但代表不同角色。

例如同一張 date dimension 可能同時扮演：

- order date
- shipping date
- delivery date

這種情況下，不需要複製多份相同維度資料，而是讓同一個 dimension 在模型中扮演不同角色。

這也是為什麼 date dimension 常常和 semantic model 裡的 multiple relationships 一起出現。  
資料上仍然是同一張日期維度，但在分析語意上，它會同時代表不同事件時間。

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

## OLAP vs OLTP

Warehouses are commonly associated with `OLAP`, while operational systems are commonly `OLTP`.

| Characteristic | OLAP | OLTP |
| --- | --- | --- |
| Main purpose | Analysis | Transaction processing |
| Query style | Complex, read-heavy, multi-dimensional | Simple, frequent, write-heavy |
| Data organization | Often dimensional or analytical | Rows and columns for operations |
| Typical system role | Reporting and analytics | Source systems and applications |

Tip: Moving analytical work into a warehouse helps keep OLTP systems responsive for operational traffic.

## Row Store vs Column Store

Analytical warehouses often benefit from column-oriented storage.

| Storage Style | Best Fit |
| --- | --- |
| Row store | Transactional workloads where full rows are accessed together |
| Column store | Analytical workloads where queries scan a few columns over many rows |

Column stores often improve analytical performance and compression because related column values are stored together.

## ETL vs ELT

Both are ways to move data into an analytical environment, but the order of operations differs.

| Pattern | Sequence |
| --- | --- |
| ETL | Extract -> Transform -> Load |
| ELT | Extract -> Load -> Transform |

### ETL

| ETL Strength | ETL Limitation |
| --- | --- |
| Lower warehouse storage needs | Transformation fixes may require re-pulling data |
| Can help with PII handling before loading | Often needs separate processing infrastructure |

### ELT

| ELT Strength | ELT Limitation |
| --- | --- |
| Transformations can be rerun from loaded raw data | Raw-data storage needs are higher |
| Fits cloud scaling and near real-time needs well | Privacy and compliance controls must be carefully enforced inside the warehouse |

Key point: ELT becomes more attractive when cloud platforms make storage and compute scalable, but ETL can still be useful when early transformation or stricter pre-load control is needed.

## Data Cleaning in Warehouse Pipelines

Warehouse quality depends heavily on data cleaning in the pipeline.

| Cleaning Task | Purpose |
| --- | --- |
| Format normalization | Standardize dates, categories, and capitalization |
| Address parsing | Split and validate address fields into components |
| Validation | Check ranges, types, and business-rule compliance |
| De-duplication | Remove repeated records that distort analysis |

Tip: A warehouse can only be as trustworthy as the rules used to clean and validate the incoming data.

## On-Premise, Cloud, and Hybrid Deployment

Warehouses can be deployed in different infrastructure models.

| Model | Strength | Main Trade-off |
| --- | --- | --- |
| On-premise | High control and custom optimization | High upfront cost and more maintenance burden |
| Cloud | Fast scaling and less infrastructure maintenance | Less low-level control and potentially variable cost |
| Hybrid | Useful for backup, recovery, or mixed constraints | Operational complexity increases |

## Choosing a Practical Approach

Real warehouse design choices depend on business context.

Useful decision questions include:

1. do we need fast visible business impact or a longer enterprise foundation
2. do we expect raw data to be retained for reprocessing
3. is cloud scalability more valuable than infrastructure control
4. which business process should be modeled first
5. which history policy is required for changing dimensions

Warning: There is no single best warehouse design. The right choice depends on workload, team size, governance needs, and time-to-value expectations.

## Minimum Standard for a Usable Warehouse Design

Before calling a warehouse design credible, you should be able to explain:

1. which business processes the warehouse supports
2. which source systems feed it and how the layers interact
3. which dimensional model, grain, facts, and dimensions were chosen
4. whether ETL or ELT is being used and why
5. how the design supports analytical performance, quality, and maintainability

## Practical Reminders

- star schema 不是為了教科書漂亮，而是為了讓分析更穩定、更好查。
- gold layer 的價值通常不是再做一次清理，而是把資料整理成可被穩定消費的分析模型。
- SCD 選型如果太晚決定，後面補歷史通常很痛。
- date dimension 幾乎永遠值得好好設計，因為它會被大量下游共用。
- granularity 要先講成明確的 `by ...` 敘述，例如 `by customer, by product, by day`，不然後面 aggregation 很容易失真。
- 從既有資料去做更細的 grain 通常不現實；往較粗 grain 聚合則常能換到更好的效能與更小的模型。
- 若不同 fact tables 沒有共享 conformed dimensions，跨主題分析很容易失真。
- 如果目標下游是 Power BI 或 semantic model，優先讓 fact / dimension 關係清楚，再考慮是否真的需要 snowflake 化。

[Back to Data Engineering](README.md)
