# Microsoft Fabric Fundamentals

Microsoft Fabric 可以先理解成一個把 data engineering、analytics、BI 與部分 data science 工作流放到同一個平台裡的整合式分析環境。

這份筆記的重點不是背所有 workload 名稱，而是建立一個穩定心智模型：Fabric 想整合什麼、lakehouse 在裡面扮演什麼角色，以及 semantic model 與 Power BI 怎麼接上去。

## Fabric 在解決什麼問題

許多資料團隊的痛點不是單一工具不夠強，而是：

- 資料落在不同平台
- ingestion、storage、modeling、reporting 各自分散
- 權限、部署與協作要跨很多介面處理

Fabric 的核心想法，就是把這些工作盡量收斂到同一個分析平台。

## 先用三層理解 Fabric

入門時可以先把 Fabric 分成三層：

1. 資料進來的方式
2. 資料存放與處理的位置
3. 資料被商業使用者消費的方式

這三層一旦連起來，Fabric 的多數元件就比較不容易看成一堆分散產品。

## Lakehouse 是 Fabric 的核心入口之一

課程一開始就強調 lakehouse，這很合理，因為 Fabric 很多 workflow 都會圍繞它展開。

### Lakehouse 的資料型態

Fabric lakehouse 可以同時承接：

- structured data in Delta tables
- unstructured data in raw files，例如 `.csv`

這個特性很重要，因為它讓平台不需要一開始就強迫所有資料進同一種資料庫抽象。

### Lakehouse 的實務定位

可以先把 Fabric lakehouse 理解成：

- 資料落地與整理的主要場域
- notebook、Spark 與部分 BI workflow 的共用底座
- 比傳統 warehouse 更接近檔案與 table 並存的設計

## Ingestion 不是只有一種方式

Fabric 的 ingestion 流程不是單一路徑，課程裡反覆提到三個常見入口：

- data pipeline
- dataflow
- notebook

### Data Pipeline

比較適合把資料移動、複製、排程與流程串接起來。

### Dataflow

比較適合低程式碼或 analyst-friendly 的資料轉換流程。

### Notebook

比較適合：

- 用 Python 或 Spark SQL 做自訂處理
- 需要更工程化或可重複執行的資料邏輯
- 直接操作 lakehouse 裡的資料

Key point: Fabric 的價值之一，就是讓這三種入口能在同一個平台裡配合，而不是分散在不同服務。

## Lakehouse 與 Warehouse 的差異

課程雖然是入門，但有幾個很值得保留的細節：

- lakehouse 比較能同時容納 raw files 與 Delta tables
- warehouse 比較偏 SQL-first 的分析體驗
- lakehouse 的 SQL 介面與 visual query editor 會有較多限制

這代表一件事：兩者不是誰取代誰，而是對應不同資料工作方式。

### 一個簡單判斷法

- 如果你需要 notebook、Spark、原始檔案與 table 並存，先想到 lakehouse
- 如果你主要想用較完整的 SQL 分析體驗，warehouse 會更自然

## Notebook 不只是分析，也可以做資料操作

課程特別提到：

- Spark SQL notebook cells 可以執行 DML
- PySpark notebook cells 也能處理 lakehouse 資料

這個訊息很實用，因為它提醒我們 notebook 在 Fabric 裡不是只有探索分析用途，也可以成為資料寫入、更新與處理流程的一部分。

## Semantic Model 是 BI 消費層的橋樑

Fabric 後段的重點轉到 semantic model，這很關鍵，因為資料平台真正被業務使用時，不會直接讓每個人自己 join 原始資料表。

### What a Semantic Model Does

semantic model 的核心作用是：

- 定義資料表之間的 relationships
- 把原本彼此獨立的 tables 組成可分析的資料語意層
- 讓報表與商業使用者看到比較友善的分析結構

沒有 semantic model 時，表可能只是分散存在；有了 semantic model，這些表才開始對分析工作產生整體意義。

### Default Semantic Model

課程提到一個很值得記的細節：

- 建立 lakehouse 時，通常會一併產生 default semantic model

這表示 Fabric 不是把資料工程與 BI 完全切開，而是預設你可能很快就要把資料接到分析消費層。

## Power BI 和 Fabric 的關係

Fabric 不是要把 Power BI 排除在外，反而是把它變成整體工作流的一部分。

Power BI 在這裡更像：

- semantic model 與 report 的主要消費介面
- BI developer 的工作場域
- 將資料資產轉成決策資訊的最後一層

所以理解 Fabric 時，不能只看 ingestion 與 storage，也要看到 Power BI 代表的消費端角色。

## BI Developer 的視角

課程提到 BI developer 常需要：

- business acumen
- data skills
- report-building 能力

這提醒我們一件事：Fabric 不是只服務 data engineer。它也在服務需要把資料講成商業故事的人。

## 一個最小 Fabric 心智模型

如果只想先記住最重要的東西，可以抓這五點：

1. Fabric 是把資料處理、分析與 BI 盡量整合在一起的平台
2. lakehouse 是很核心的資料落地與處理入口
3. ingestion 常見三種路線是 data pipeline、dataflow、notebook
4. semantic model 負責把資料表轉成可被商業分析使用的語意層
5. Power BI 是 Fabric 消費層的重要延伸，而不是平台外的附屬品

## Related Concepts

- [Storage and Models](storage-and-models.md)
- [Ingestion](ingestion.md)
- [Microsoft Fabric Environment Design and Deployment](microsoft-fabric-environment-design-and-deployment.md)
- [Semantic Models and Power BI](semantic-models-and-power-bi.md)

[Back to Data Engineering](README.md)
