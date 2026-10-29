[Data Science](../README.md) › [Data Engineering](README.md) › 資料工程基礎

# 資料工程基礎 (Data Engineering Foundations)

資料工程建立並維護讓資料穩定流動的基礎設施：從來源系統擷取、儲存、轉換，最後交付給報表、分析或模型。本篇講平台與流程的整體視角；以使用者–項目互動為主的推薦系統基礎見 [推薦系統基礎](../machine-learning/recommender-systems/foundations.md)。

## 角色分工

| 面向 | Data Engineer | Data Scientist / 生資分析者 |
| --- | --- | --- |
| 主要目標 | 資料能穩定、正確、準時地流到下游 | 用資料回答問題、建模型 |
| 常見工作 | 擷取與儲存、建資料庫、寫 pipeline、監控 | 查資料、使用 pipeline 產出、分析與建模 |
| 核心能力 | 軟體工程、資料系統、可靠性 | 統計、建模、實驗設計、領域知識 |
| 關心的問題 | 明天還能不能自動跑？來源改格式會怎樣？ | 這份資料能不能回答問題？ |

在小型研究團隊裡，兩個角色常是同一個人：同一位生資分析者既要寫 Nextflow / Snakemake 把 FASTQ 變成計數表，也要做下游統計。這時資料工程的觀念（原始資料不可變、流程可重跑、每步有檢查）一樣適用。

## 大資料 (Big Data)

big data 不是「資料很多」而已，而是規模、速度或型態超過單機工具與人工流程能輕鬆處理的程度。

| 面向 | 意義 | 生資例子 |
| --- | --- | --- |
| Volume | 資料量大 | 全基因體定序 cohort、數百萬細胞的 scRNA-seq |
| Velocity | 資料到來速度快 | 定序儀持續產出、醫院 EHR 即時更新 |
| Variety | 來源與格式多 | FASTQ、BAM、VCF、影像、臨床表單、文字病歷 |

規模上去後，需要的不只是更大的機器，而是自動化搬運與更新、可擴充的儲存與運算、可控的延遲與成本，以及讓多個下游共用一致的資料版本。

## 現代 vs 傳統架構

| 面向 | 現代資料架構 | 傳統資料架構 |
| --- | --- | --- |
| 資料規模與型態 | 大量、多種格式 | 較小、以結構化為主 |
| 處理方式 | batch 與 near real-time 並存 | 以 batch 為主 |
| 擴充方式 | 雲端彈性擴充、storage 與 compute 分離 | 固定硬體 |
| 使用方式 | self-service analytics | 依賴中央 IT |

## 資料生命週期

```
資料來源 → 擷取 → 儲存 → 處理 / 轉換 → 交付 (serving)
(sources)  (ingestion) (storage) (processing)  報表、分析、模型、應用程式
```

| 階段 | 重點 | 詳見 |
| --- | --- | --- |
| 擷取 | 來源型態、型別判斷、增量更新 | [資料擷取](ingestion.md) |
| 儲存 | lake / warehouse / lakehouse、檔案格式 | [儲存與資料模型](storage-and-models.md) |
| 處理 | ETL / ELT、batch / stream、排程 | [處理與 Pipeline](processing-and-pipelines.md) |
| 交付 | 下游怎麼取用：SQL 表、API、dashboard、feature table | [維度模型](dimensional-modeling-and-star-schema.md) |
| 貫穿全程 | 品質、治理、版本 | [資料品質](data-quality-checks.md)、[治理](governance.md) |

## 什麼時候該把手動流程升級成 pipeline

| 訊號 | 意義 |
| --- | --- |
| 同一份資料整理每週重做一次 | 手動步驟容易漏、難以重現 |
| 結果要每日更新、餵給 dashboard 或模型 | 已經是產品，不是一次性分析 |
| 別人問「這張表怎麼來的」答不出來 | 缺少 lineage 與文件 |
| 上游一改格式下游就默默算錯 | 缺少 schema 與品質檢查 |

> 好的資料工程成果通常不顯眼，但它決定下游分析的速度與可信度。
