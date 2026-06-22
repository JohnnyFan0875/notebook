# Data Science

這個區塊整理資料科學常見的學習路線，從 Python 基礎、資料整理、統計思維，到機器學習、深度學習與視覺化實作。整體安排以「先理解資料，再建立模型，最後把結果說清楚」為主軸。

## 建議學習順序

1. [Understanding Data Science](understanding-data-science.md): 先建立整體地圖，知道 data science workflow 不只是在選模型。
2. [Python Foundations](python-foundations/README.md): 再補齊資料處理會反覆用到的 Python、NumPy 與 pandas 基礎。
3. [R Foundations](r-foundations/README.md): 如果分析工作也會用 R，這裡補齊日期時間、控制流程、函數與 `apply` 的工作基礎。
4. [Data Manipulation and EDA](data-manipulation-and-eda/README.md): 學會檢查資料品質、探索分布、整理缺失值與建立資料理解。
5. [Visualization](data-manipulation-and-eda/visualization/README.md): 在 EDA 脈絡下練習把探索結果轉成可解讀的圖表。
6. [Data Communication](data-communication/README.md): 學會把模糊需求翻成可分析問題，並讓分析結果能回到決策。
7. [Data Engineering](data-engineering/README.md): 了解資料如何被擷取、儲存、排程、轉換與交付，建立可長期運作的資料供應鏈觀念。
8. [Statistics](statistics/README.md): 建立估計、不確定性、假設檢定、回歸與時間序列的判讀能力。
9. [Operations Research](operations-research/README.md): 當問題變成在成本、容量與邏輯限制下「應該怎麼做」時，進入 optimization 與 prescriptive model 的世界。
10. [Network Analysis](network-analysis/README.md): 當資料的重點在連結結構、路徑與群聚，而不只是單列特徵時，進入 graph thinking。
11. [Machine Learning](machine-learning/README.md): 學會以 workflow 為中心的建模、評估、解釋與部署觀念。
12. [Marketing Analytics](marketing-analytics/README.md): 把價格、促銷、品牌選擇與 customer response 轉成可量化的決策模型。
13. [Deep Learning](deep-learning/README.md): 在理解模型訓練流程後，再進入神經網路與 PyTorch 實作。
14. [LLM Applications and Systems](llm/README.md): 當你開始把模型接到檔案、知識庫、工具與工作流程時，再進入 LLM 應用系統設計。

## 章節地圖

| 章節 | 主要內容 | 你會解決的問題 |
| --- | --- | --- |
| [Understanding Data Science](understanding-data-science.md) | data science workflow、data sources、data preparation、experiments、modeling | 資料科學到底在做什麼？一個完整 workflow 會經過哪些階段？ |
| [Python Foundations](python-foundations/README.md) | Python 語法、函式、檔案、NumPy、pandas | 我該如何有效率地讀取、整理與轉換資料？ |
| [R Foundations](r-foundations/README.md) | 日期時間、控制流程、函數、`apply` 家族 | 我如何在 R 裡安全處理時間欄位、重用邏輯並批次處理資料結構？ |
| [Data Manipulation and EDA](data-manipulation-and-eda/README.md) | 資料剖析、缺失值、探索式分析 | 資料是否可信？哪些欄位有問題？ |
| [Visualization](data-manipulation-and-eda/visualization/README.md) | Matplotlib、Seaborn、圖表設計原則 | 我該用哪種圖？結果要怎麼說才不誤導？ |
| [Data Communication](data-communication/README.md) | 問題定義、需求拆解、stakeholder 對齊、分析敘事起點 | 模糊的商業需求要怎麼翻成可回答的分析問題？ |
| [Data Engineering](data-engineering/README.md) | pipelines、storage、batch/stream、scheduling | 資料如何穩定流進分析與模型流程，而不是每次手動整理？ |
| [Statistics](statistics/README.md) | 描述統計、推論、回歸、時間序列、生存分析 | 這個差異或趨勢是否可靠？ |
| [Operations Research](operations-research/README.md) | optimization、decision variables、constraints、network design、sensitivity analysis | 在需求、成本、容量與商業規則都存在時，最佳決策該怎麼求？ |
| [Network Analysis](network-analysis/README.md) | graphs、centrality、paths、cliques、subgraphs | 當資料的核心是誰和誰相連時，我該如何分析重要節點、最短路徑與群體結構？ |
| [Machine Learning](machine-learning/README.md) | 前處理、模型訓練、評估、解釋、部署 | 我如何建立可泛化、可監控的預測系統？ |
| [Marketing Analytics](marketing-analytics/README.md) | price response、promotion effects、choice models、campaign targeting | 價格、促銷與競品條件改變時，顧客與市場會怎麼反應？ |
| [AI Strategy and Governance](ai-strategy-and-governance/README.md) | AI ethics、治理、風險與策略 | 當 AI 進入真實決策流程時，我如何讓它可控、可解釋、可問責？ |
| [Deep Learning](deep-learning/README.md) | 張量、損失函數、反向傳播、遷移學習 | 我如何用神經網路處理更複雜的資料型態？ |
| [LLM Applications and Systems](llm/README.md) | agents、RAG、tool use、orchestration | 當模型要連接知識、工具與流程時，系統應該怎麼設計？ |
| [Databases](databases/README.md) | MySQL、PostgreSQL | 資料如何在資料庫端先整理、抽取與聚合？ |
| [Finance](finance/README.md) | 金融時間序列概念 | 報酬率與自相關要如何判讀？ |
| [Web Scraping](web-scraping/README.md) | BeautifulSoup、Selenium | 當資料不在 API 或 CSV 時，如何合法抓取？ |

## 一套一致的分析節奏

實務上，很多錯誤不是因為模型不夠複雜，而是前面的資料理解做得不夠。建議每次分析都固定經過下面幾步：

1. 先做資料盤點：欄位型別、缺失值、重複值、異常值、時間範圍。
2. 再做視覺化與描述統計：先看分布、關係與資料收集偏差。
3. 接著才選方法：統計檢定、回歸、分類、分群、時間序列。
4. 最後回到決策：這個結果是否穩定、可解釋、可重現、可部署。

## 閱讀提醒

- 相同概念只在最適合的章節完整說明，其他地方以交叉連結為主，避免重複記憶。
- 程式碼範例優先採用 `seaborn` 內建資料集或可直接建立的小型 DataFrame，方便立即重跑。
- 如果你是初學者，遇到模型章節卡住時，優先回頭補 [EDA](data-manipulation-and-eda/README.md)、[Visualization](data-manipulation-and-eda/visualization/README.md) 與 [Statistics](statistics/README.md)。
