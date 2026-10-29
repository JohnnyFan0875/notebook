[Data Science](../README.md) › [Data Engineering](README.md) › 資料倉儲與維度模型

# 資料倉儲與維度模型 (Data Warehousing and Dimensional Modeling)

資料倉儲 (data warehouse) 收集、整合多個來源的資料，以適合分析的形式長期保存。它不只是更大的資料庫：設計目標是分析查詢、跨部門的整合視角與歷史報表，而不是日常交易。維度模型 (dimensional model) 是倉儲裡最常見的表設計方式。

## 倉儲在做什麼

| 功能 | 價值 |
| --- | --- |
| 從多個系統收集資料 | 把分散的營運資料集中到一個分析環境 |
| 整合與標準化 | 跨單位分析才可行 |
| 保留歷史 | 支援趨勢分析與回顧 |
| 支援 BI 與分析 | 提供穩定的報表層，不拖慢交易系統 |

| 系統 | 主要目的 | 資料形狀 |
| --- | --- | --- |
| 交易資料庫 (OLTP) | 執行應用程式、記錄交易 | 結構化、列式 |
| 資料倉儲 | 組織層級的分析與報表 | 結構化、整合、分析用 |
| 資料市集 (data mart) | 特定主題或部門的分析 | 結構化、聚焦 |
| 資料湖 | 大量原始、多樣資料，保留彈性 | 結構化與非結構化 |

### OLAP vs OLTP

| 特性 | OLAP | OLTP |
| --- | --- | --- |
| 目的 | 分析 | 交易處理 |
| 查詢型態 | 複雜、讀取為主、掃描大量列的少數欄 | 簡單、頻繁、寫入為主、存取整列 |
| 資料組織 | 維度模型、欄式儲存 | 正規化、列式儲存 |
| 角色 | 報表與分析 | 來源系統與應用程式 |

欄式儲存 (column store) 把同一欄的值存在一起，分析查詢只讀需要的欄，壓縮率也高；列式儲存 (row store) 適合一次存取整列的交易。詳見 [NoSQL 基礎](../databases/nosql-foundations.md) 的 row vs column store。

## 倉儲分層

| 層 | 角色 |
| --- | --- |
| 來源層 (source) | 營運系統、log、檔案、試算表 |
| 暫存層 (staging) | 擷取、轉換、驗證；整合的髒活大多在這裡 |
| 儲存層 (storage) | 倉儲表，有時再分出 data mart |
| 展示層 (presentation) | dashboard、BI 工具、分析師直接查詢 |

Lakehouse 常用 medallion architecture 表達同樣的資料成熟度：

| 層 | 重點 | 內容 |
| --- | --- | --- |
| Bronze | 保留 | 原始資料，盡量維持來源樣貌 |
| Silver | 清理 | 標準化、去重、型別修正後的資料 |
| Gold | 可分析 | 給分析與消費的模型，常是 star schema |

倉儲不是一次性建置，而是需要持續維護的分析產品：規劃需求 → 建模（fact、dimension、grain）→ 實作 ETL / ELT 與 BI 介面 → 修改、測試、部署、支援。

## Inmon vs Kimball

| 方法 | 核心想法 | 優點 | 缺點 |
| --- | --- | --- | --- |
| Inmon（由上而下） | 先建整合的企業倉儲（正規化），再衍生 data mart | 單一事實來源、下游一致 | 前期設計久、啟動成本高 |
| Kimball（由下而上） | 從具體業務流程建維度模型 data mart，再逐步擴充 | 交付快、前期成本低，容易先證明價值 | 長期需要協調 ETL；各 mart 定義可能分歧 |

## Star Schema

star schema 把資料分成兩種表：fact table 記錄事件與度量，dimension table 提供描述與分析脈絡。

```
              dim_date
                 │
dim_patient ── fact_measurement ── dim_gene
                 │
              dim_assay (platform, batch)
```

| 表 | 內容 | 欄位 |
| --- | --- | --- |
| Fact table | 業務事件、交易、量測 | 指向各 dimension 的代理鍵、可聚合的度量 (measures)、少量事件屬性 |
| Dimension table | 描述業務實體（產品、客戶、樣本、基因） | 代理鍵、自然鍵 / business key、用來篩選分組的屬性 |

### Kimball 建模四步驟

| 步驟 | 內容 | 例子 |
| --- | --- | --- |
| 1. 選業務流程 | 從一個具體流程開始 | 檢驗結果、定序產出、銷售 |
| 2. 宣告 grain | 一列 fact 代表什麼，寫成 `by ...` | 「每個樣本 × 每個基因 × 每次 assay 一列」 |
| 3. 找 dimensions | 使用者要用哪些欄位篩選與分組 | 日期、病人、樣本、基因、平台、批次 |
| 4. 找 facts | 在該 grain 下為真的數值 | 計數、TPM、檢驗值 |

> grain 不清楚或不一致，所有下游指標都難以信任。從現有資料往更細的 grain 拆通常不可能；往較粗的 grain 聚合則能換到更好的效能與更小的模型。

### Star vs Snowflake

| | Star schema | Snowflake schema |
| --- | --- | --- |
| Dimension | 反正規化，描述欄位集中在一張表 | 再正規化成多層 |
| 查詢 | 直接、join 少 | join 多、較難理解 |
| 適合 | 分析與 BI（Power BI 等強烈偏好 star） | 維度極大、重複很多時 |

## 緩慢變化維度 (SCD)

dimension 會變（病人轉院、產品改類別），要先決定歷史怎麼保留。

| 類型 | 做法 | 適合 |
| --- | --- | --- |
| Type 0 | 不接受變更，保留原值 | 出生日期等不應變動的屬性 |
| Type 1 | 直接覆寫 | 只需最新狀態（更正錯字、聯絡資訊） |
| Type 2 | 新增一列，加 `valid_from` / `valid_to` / `is_current` | 需要回答「當時的狀態是什麼」 |
| Type 3 | 多一欄保留前一個值 | 只需要有限的前一版本 |
| Snapshot | 定期快照整張 dimension | 大範圍的歷史報表 |

> 不需要歷史就用 Type 1，需要歷史就用 Type 2；其他類型沒有明確需求時不必用。SCD 太晚決定，之後補歷史很痛。dbt 的 [snapshot](dbt-foundations.md#snapshot) 可以實作 Type 2。

## 常見的 dimension 模式

| 模式 | 內容 | 例子 |
| --- | --- | --- |
| Date dimension | 預先建好的日曆表；自然鍵用 date 型別、代理鍵用 `YYYYMMDD` 整數；含年、季、月、週、會計年度 | 幾乎所有 fact 都用到；集中維護比各報表各自算日期穩 |
| Time dimension | 一天內的時間，代理鍵 `HHMM` 或 `HHMMSS` | 只有高頻事件（IoT、call center）才需要 |
| Conformed dimension | 多個 fact table 共用同一張 dimension | sales 與 marketing 共用 date、product；不同 assay 共用 sample |
| Role-playing dimension | 同一張 dimension 在 fact 中扮演多個角色 | date 同時是採檢日、收件日、報告日 |
| Bridge table | 表達多對多；只存 key 配對，也稱 factless table | 一個病人多個診斷、一個樣本多個 run |

> dimension 應該被多個 fact 重用，而不是彼此之間到處互連；dimension 之間的關聯越複雜，BI 報表的篩選行為越難預期。

## 倉儲 pipeline 的清理與部署

| 清理工作 | 目的 |
| --- | --- |
| 格式標準化 | 日期、類別、大小寫一致 |
| 拆解與驗證複合欄位 | 地址、檢體編號拆成組成部分 |
| 驗證 | 範圍、型別、業務規則 |
| 去重 | 重複記錄會扭曲分析 |

| 部署 | 優點 | 代價 |
| --- | --- | --- |
| 地端 (on-premise) | 控制度高、可客製最佳化 | 前期成本與維護負擔高 |
| 雲端 | 擴充快、少維護 | 底層控制少、成本變動 |
| 混合 | 備援、資料不能出境時 | 營運複雜度增加 |

ETL vs ELT 的取捨見 [處理與 Pipeline](processing-and-pipelines.md#etl-與-elt)。

## 設計檢查清單

| 問題 | 為什麼 |
| --- | --- |
| 支援哪些業務流程？由哪些來源餵入？ | 範圍與分層 |
| fact table 的 grain 是什麼？ | 決定所有聚合是否正確 |
| 哪些欄位是 dimension 屬性，哪些是 measure？ | measure 才能聚合 |
| 來源的 business key 夠穩定嗎？ | 決定是否需要代理鍵 |
| 哪些 dimension 要保留歷史？ | SCD 策略 |
| 有沒有重複出現的日期角色、多對多關係？ | role-playing、bridge table |
| 不同 fact 是否共用 conformed dimensions？ | 沒有共用，跨主題分析會失真 |
