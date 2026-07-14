# Foundations

This note covers the platform and workflow view of data engineering: ingestion, storage, pipelines, and architecture. For recommendation-system foundations built around user-item interactions rather than infrastructure, see [Recommendation Foundations](../machine-learning/recommender-systems/foundations.md).

## What Data Engineering Is

Data engineering 的核心工作，是建立與維護資料流動的基礎設施，讓資料能從來源系統穩定進入分析、報表與模型流程。

常見工作包括：

- 擷取與儲存資料
- 設計與維護資料庫
- 建立資料管線
- 確保資料能被下游穩定使用

## Data Engineer vs. Data Scientist

這兩個角色會大量合作，但重心不同。

| 面向 | Data Engineer | Data Scientist |
| --- | --- | --- |
| 主要目標 | 建立可靠的資料基礎設施 | 從資料中產生分析、模型與決策支援 |
| 常見工作 | ingest/store data、set up databases、build pipelines | access databases、use pipeline outputs、train/analyze models |
| 核心能力 | 軟體工程、資料系統、可靠性 | 統計、建模、實驗與解釋 |

一個實用的分界是：

- data engineer 更關心資料能不能穩定流動
- data scientist 更關心資料能不能回答問題

## Data Engineering and Big Data

Big data 不是單純「資料很多」，而是資料的規模、速度或型態已經超過傳統人工流程與單機工具可以輕鬆處理的程度。

當資料量變大後，資料工程的重要性會快速上升，因為團隊需要：

- 自動化資料搬運與更新
- 擴充儲存與計算資源
- 控制資料延遲與成本
- 讓多個下游系統共用一致資料

## Modern vs. Traditional Architecture

現代資料架構和傳統資料架構最大的差別，不只是工具名稱不同，而是整體設計目標不同。

| 面向 | Modern Data Architecture | Traditional Data Architecture |
| --- | --- | --- |
| 資料規模與型態 | 大量資料、多種格式 | 較小、以 structured data 為主 |
| 處理方式 | real-time 或 near real-time 常見 | 以 batch 為主 |
| 擴充方式 | 雲端與彈性擴充 | 較依賴固定硬體 |
| 使用方式 | self-service analytics 較常見 | 對中央 IT 依賴較高 |

## Ingestion to Serving

現代資料架構通常會把整條資料生命週期一起考慮，而不是只看某一段儲存。

常見組件包括：

- data sources
- ingestion
- storage
- processing
- serving

其中 `serving` 的重點是，資料最後要如何被報表、分析、應用程式或模型實際消費。

## Why Pipelines Matter

資料不會只停在一個地方。它通常會經過：

1. 萃取
2. 清理或轉換
3. 儲存
4. 提供給報表、分析或模型

如果沒有 pipeline，這些步驟就會變成手動、零散、難以重現。真正的目標不是「把資料搬一次」，而是建立一條可以自動流動的路。

## Practical Reminders

- 資料工程不是資料科學的前置雜務，而是讓分析與機器學習能持續運作的系統工作。
- 當團隊開始反覆重做同一份資料整理時，通常就代表該把手動流程升級成 pipeline。
- 好的資料工程成果常常不顯眼，但它會直接決定下游分析的速度與可信度。

[Back to Data Engineering](README.md)
