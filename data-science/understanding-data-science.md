[Data Science](README.md) › 認識資料科學

# 認識資料科學 (Understanding Data Science)

資料科學把資料轉成可用的理解、預測與決策。它不只是建模：真實的工作流程包含問題定義、資料取得、整理、探索、實驗或建模，以及解讀與溝通，而很多專案在建模之前就已經失敗。

## 工作流程

```
問題定義 → 取得資料 → 整理資料 → 探索 → 實驗 / 建模 → 解讀與溝通 → 行動
   ↑                                                              │
   └──────────────────────── 新問題 ←─────────────────────────────┘
```

| 階段 | 目標 | 產出 | 詳見 |
| --- | --- | --- | --- |
| 問題定義 | 釐清要回答什麼 | 問題、假設、成功指標 | [形成分析問題](data-communication/forming-analytical-questions.md) |
| 取得資料 | 找到相關的內部或外部資料 | 原始表、log、檔案、API 回應 | [Python 匯入資料](python-foundations/importing-data.md)、[Databases](databases/README.md) |
| 整理資料 | 清理與標準化 | 可分析的資料集 | [pandas](python-foundations/pandas/README.md)、[缺失值](data-manipulation-and-eda/missing-data.md) |
| 探索 | 了解結構、模式與風險 | 摘要統計、圖、假設 | [EDA](data-manipulation-and-eda/README.md) |
| 實驗或建模 | 檢驗主張或預測結果 | 統計結果或訓練好的模型 | [Statistics](statistics/README.md)、[Machine Learning](machine-learning/README.md) |
| 解讀與溝通 | 把結果連回決策 | 建議、報告、下一步 | [溝通分析結果](data-communication/communicating-results.md) |

> 很多專案失敗在建模之前：問題模糊、資料品質差、或跳過整理步驟。

## 資料來源

| 類型 | 說明 | 例子 |
| --- | --- | --- |
| 組織內部資料 | 組織運作產生 | 網站事件、客戶資料、交易、物流；醫院 EHR、實驗室 LIMS、定序產出 |
| 公開資料 | 可公開使用與分享 | 政府資料、研究資料集；GEO、SRA / ENA、TCGA、GTEx、UniProt、PDB |
| 受控存取資料 | 需申請與簽署使用協議 | dbGaP、EGA、UK Biobank、All of Us，見 [隱私與法規](responsible-ai/privacy-and-regulation.md) |

| 收集方式 | 例子 | 特性 |
| --- | --- | --- |
| 觀察 / 被動收集 | log、交易、clickstream、營運紀錄、EHR | 量大、反映實際行為；但記錄目的不是研究，可能有選擇偏差與缺漏 |
| 主動徵求 | 問卷、評論、焦點團體、病人自評量表 | 能取得行為紀錄看不到的意見與感受；受題目措辭、抽樣與回應偏差影響 |
| 實驗產生 | A/B 測試、臨床試驗、定序實驗 | 能回答因果問題；需要事先設計 |

知道資料從哪裡來和知道欄位內容一樣重要：來源決定可信度、偏差、新鮮度與使用限制。主動徵求的資料是有自己收集過程的證據，不是中立的事實，見 [調查抽樣](statistics/inferential-statistics/survey-sampling.md)。

## 為什麼資料整理要早做

真實資料很亂。整理不是行政雜務，而是資料科學推理的一部分：它避免明顯錯誤、錯誤的分析結果，以及之後模型或決策中隱藏的偏差。

| 常見工作 | 例子 |
| --- | --- |
| 修正型別 | ID 被讀成數字（`"001"` → 1）、日期被讀成字串 |
| 標準化格式與單位 | mg/dL vs mmol/L、大小寫不一致的類別 |
| 移除真正的重複 | 同一樣本重複匯入（技術重複不是重複資料） |
| 有意識地處理缺值 | 先問為什麼缺，再決定刪除或補值 |
| 檢查類別一致性 | `Male` / `M` / `male`；基因名被 Excel 改成日期 |

## 實驗

```
提出問題 → 形成假設 → 收集資料 → 用合適的統計方法檢驗 → 解讀結果
```

A/B 測試是商業上常見的版本，比較兩個標題、介面、方案或流程；生醫研究中則是對照實驗與臨床試驗。實驗在目標是支持決策（「如果這樣做會怎樣」）而不只是描述發生了什麼時特別有價值，見 [A/B 測試](statistics/experimental-design/ab-testing.md)、[Experimental Design](statistics/experimental-design/README.md)。

## 建模與機器學習

建模是用變數之間的數學關係描述真實世界的過程。

| 概念 | 著重 | 例子 |
| --- | --- | --- |
| 統計建模 | 解釋關係、假設與不確定性 | 迴歸係數與信賴區間、差異表現分析 |
| 機器學習 | 從資料學習模式以提升預測 | 流失預測、推薦系統、影像分類、蛋白質結構預測 |

監督式學習從有標籤的例子學習，再預測新輸入的結果。

| 目標 | 問題 | 取捨 |
| --- | --- | --- |
| 預測 (predictive) | 模型能否準確預測或分類未來案例？ | 預測力強的模型可能難以解釋 |
| 解釋 (explanatory) | 模型能否幫助理解什麼驅動了結果？ | 可能刻意犧牲部分預測準確度換取可解釋性 |

兩者重疊但不相同；先決定要哪一個，因為它影響模型選擇、評估方式與能下的結論（預測模型的重要特徵不代表因果）。見 [解釋性建模（R）](r-foundations/explanatory-modeling-in-r.md)、[Machine Learning](machine-learning/README.md)。

> 模型可以看起來很精密，卻建立在薄弱的假設、品質差的標籤或沒整理好的資料上。

## 接下來讀什麼

| 想做的事 | 章節 |
| --- | --- |
| 整理與探索資料 | [Data Manipulation and EDA](data-manipulation-and-eda/README.md) |
| 定義問題、和利害關係人對齊、報告 | [Data Communication](data-communication/README.md) |
| 估計、檢定、實驗設計 | [Statistics](statistics/README.md) |
| 預測、評估、部署 | [Machine Learning](machine-learning/README.md) |
| 依讀者類型的完整路線 | [Data Science 建議路線](README.md#建議路線) |
